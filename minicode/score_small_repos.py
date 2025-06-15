import os
import ast
import math
import sys
import argparse

import json
from tqdm import tqdm
from pathlib import Path

from radon.complexity import cc_visit
from radon.raw import analyze
import tiktoken

# TODO calls to LLM are slow and can be parallelized
# from tqdm.asyncio import tqdm
# from tenacity import retry, stop_after_attempt, wait_exponential

# ---- Logprobs ----

# from together import AsyncTogether
# client = AsyncTogether(api_key=os.getenv("TOGETHER_API_KEY"))
# semaphore = asyncio.Semaphore(16)
from together import Together
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

# @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10))
def compute_logprob_together(text, model, enable_logprobs):
    if not enable_logprobs: return [], []
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": text}],
        max_tokens=1,
        echo=True,
        logprobs=1,
    )
    logprobs = response.prompt[0].logprobs.token_logprobs[1:]
    tokens = response.prompt[0].logprobs.tokens[1:]
    return logprobs, tokens

    
# ---- Code Metrics ----

def compute_code_metrics(code: str):
    try:
        raw_metrics = analyze(code)
        complexity_metrics = cc_visit(code)

        return {
            "loc": raw_metrics.loc,     # total lines of code
            "sloc": raw_metrics.sloc,   # source lines of code (non-blank, non-comment)
            "lloc": raw_metrics.lloc,   # logical lines (statements, e.g. `if`, `for`, `return`)
            "comments": raw_metrics.comments,
            "multi": raw_metrics.multi,
            "blank": raw_metrics.blank,
            "cyclomatic": sum(block.complexity for block in complexity_metrics),
        }
    except: 
        return {
            "loc": float('nan'),
            "sloc": float('nan'),
            "lloc":  float('nan'),
            "comments": float('nan'),
            "multi": float('nan'),
            "blank": float('nan'),
            "cyclomatic": float('nan'),
        }

# ---- Repo Metrics ----
# parses the inputs given input file in repo and modules that should not be counted
def parse_imports(file_path):

    excluded_modules = set(sys.stdlib_module_names) | set(sys.builtin_module_names)
    with open(file_path, 'r') as file:
        content = file.read()
    tree = ast.parse(content)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module and not any(node.module.split('.')[0] == excluded for excluded in excluded_modules):
                for alias in node.names:
                    imports.append(f"{node.module}::{alias.name}")
        elif isinstance(node, ast.Import):
            for import_alias in node.names:
                if import_alias.name not in excluded_modules:
                    imports.append(import_alias.name)
    return imports

def get_imported_code(file_path, directory):
    try:
        imports = parse_imports(file_path)
    except Exception as e:
        print(f"[ERROR] Failed to parse {file_path}: {e}")
        return ""

    imported_code_segments = []
    for imported_fn_ref in imports:
        module_name, fn_name = (imported_fn_ref.split("::") + [None])[:2]
        candidate = file_path.parent / Path(module_name.replace(".", "/") + ".py")
        if candidate.exists():
            files = [candidate]
        else:
            # fallback: look for any file matching the module's basename
            basename = module_name.split(".")[-1] + ".py"
            files = list(directory.rglob(basename))

        if not files:
            print(f"[WARN] Cannot find module file for '{module_name}'")
            continue
        # try to find the file matching module_name. make sure to think carefully about if the actually referenced impl is in a deeper subdir or something
        
        src_file = files[0]
        content = src_file.read_text()
        if fn_name:
            try:
                tree = ast.parse(content)
                matches = []
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) \
                       and node.name == fn_name:
                        src = ast.get_source_segment(content, node)
                        if src:
                            matches.append(src)
                if matches:
                    imported_code_segments.append(matches[-1])
                else:
                    print(f"[WARN] No definition '{fn_name}' in {src_file}")
            except Exception as e:
                print(f"[ERROR] Failed to parse {src_file}: {e}")
        else:
            # imported the whole module
            imported_code_segments.append(content)

    return imported_code_segments

def compute_metrics(directory, model, enable_logprobs=False):
    directory = Path(directory)
    
    program_names = []
    codes = {}
    for file in directory.rglob("*.py"):
        if os.path.basename(file).startswith("test_"): continue
        # relative path from repo root
        program_name = str(file.relative_to(directory.parent))
        program_names.append(program_name)

        imported_code_segments = get_imported_code(file, directory)
        codes[program_name] = (imported_code_segments, open(file).read())

    total_logprob = 0.0
    total_tokens = 0
    logprobs_dict = {}
    metrics_dict = {}

    for program_name in program_names:
        imported_code_segments, code = codes[program_name]
        if len(code.strip()) == 0: continue
        # stitch together: imported code (context) + main file
        codebank = ""
        if imported_code_segments:
            codebank = f"""# === IMPORTED LIBRARY CODE START ===
{'\n\n'.join(imported_code_segments)}

# === IMPORTED LIBRARY CODE END ===

# === MAIN SOURCE CODE START ===
"""
            code = f"""{code}
# === MAIN SOURCE CODE END ===
"""
        full_text = codebank + code
        # get logprobs & tokens for the entire text
        logprobs, tokens = compute_logprob_together(full_text, model, enable_logprobs)

        # count how many tokens came from the codebank
        try:
            enc = tiktoken.encoding_for_model(model)
            cb_tokens = enc.encode(codebank) if codebank else []
            num_codebank_tokens = len(cb_tokens)
        except Exception:
            num_codebank_tokens = 0

        # sum only the logprobs for the “new” code
        sum_lp     = sum(logprobs[num_codebank_tokens:])
        new_tokens = len(tokens[num_codebank_tokens:])

        logprobs_dict[program_name] = sum_lp
        total_logprob += sum_lp
        total_tokens  += new_tokens
        print(f"Processed {program_name}: logprob={sum_lp:.2f}, tokens={new_tokens}")

        metrics_dict[program_name] = compute_code_metrics(code) | {"internal_imports": imported_code_segments}

    print("\n=== Summary ===")
    print(f"Full Repo Log Probability: {total_logprob:.2f}")
    print(f"Total Tokens: {total_tokens}")
    total_lloc = sum(m["lloc"] for m in metrics_dict.values() if not math.isnan(m["lloc"]) )
    total_sloc = sum(m["sloc"] for m in metrics_dict.values() if not math.isnan(m["sloc"]) )
    total_cyclomatic = sum(m["cyclomatic"] for m in metrics_dict.values() if not math.isnan(m["cyclomatic"]))
    total_internal_imports = sum(len(m["internal_imports"]) for m in metrics_dict.values())

    print(f"Total Logical LOC (LLOC): {total_lloc}")
    print(f"Total Source LOC (SLOC): {total_sloc}")
    print(f"Total Cyclomatic Complexity: {total_cyclomatic}")
    print(f"Total Internal Imports: {total_internal_imports}")
    
    return logprobs_dict, total_logprob, metrics_dict, total_tokens

def package_all_metrics(logprobs, total_lp, metrics, total_tokens):
    result = {"total_logprobs": total_lp, "total_tokens": total_tokens}
    all_programs = set(logprobs) | set(metrics) 

    total_loc = 0
    total_sloc = 0
    total_lloc = 0
    total_comments = 0
    total_multi = 0
    total_blank = 0
    total_cyclomatic = 0
    total_internal_imports = 0

    for program in all_programs:
        lp = logprobs.get(program, float('nan'))
        program_metrics = metrics.get(program, {})
        result[program] = {
            "logprobs": lp,
            "metrics": program_metrics,
        }
        total_loc += program_metrics["loc"] if not math.isnan(program_metrics["loc"]) else 0
        total_sloc += program_metrics["sloc"] if not math.isnan(program_metrics["sloc"]) else 0
        total_lloc += program_metrics["lloc"] if not math.isnan(program_metrics["lloc"]) else 0
        total_comments += program_metrics["comments"] if not math.isnan(program_metrics["comments"]) else 0
        total_multi += program_metrics["multi"] if not math.isnan(program_metrics["multi"]) else 0
        total_blank += program_metrics["blank"] if not math.isnan(program_metrics["blank"]) else 0
        total_cyclomatic += program_metrics["cyclomatic"] if not math.isnan(program_metrics["cyclomatic"]) else 0
        total_internal_imports += len(program_metrics["internal_imports"]) 
    
    result["total_loc"] = total_loc
    result["total_sloc"] = total_sloc
    result["total_lloc"] = total_lloc
    result["total_comments"] = total_comments
    result["total_multi"] = total_multi
    result["total_blank"] = total_blank
    result["total_cyclomatic"] = total_cyclomatic
    result["total_internal_imports"] = total_internal_imports

    return result

def main(args):
    output_file = os.path.join(args.directory, f"LIBRARYBENCH_metrics{'_nolp' if not args.enable_logprobs else ''}.json")
    if os.path.exists(output_file):
        if input("metrics file already exists... skip? [y/]").strip() == "y": 
            return
    logprobs_dict, total_logprob, metrics_dict, total_tokens = compute_metrics(args.directory, args.model, enable_logprobs=args.enable_logprobs)

    metrics = package_all_metrics(logprobs_dict, total_logprob, metrics_dict, total_tokens)
    with open(output_file, 'w') as wf:
        json.dump(metrics, wf, indent=4)
    
    print(f"Written metrics to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Python files in a folder.")
    parser.add_argument("--directory", type=str, help="Paths to .py files")
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-7B-Instruct-Turbo", help="Name of the model")
    parser.add_argument("--enable_logprobs", action="store_true", default=False, help="turn on logprob computing")
    args = parser.parse_args()
    
    main(args)

# ---- Example usage ----
# python score.py --directory workflow_orchestration/unified --model deepseek-ai/DeepSeek-V3 --enable_logprobs
