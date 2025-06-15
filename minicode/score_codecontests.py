import argparse
import json
import math
import os
import sys
from pathlib import Path

import tiktoken
from radon.complexity import cc_visit
from radon.raw import analyze

# Assuming TOGETHER_API_KEY is set in your environment
from together import Together
from tqdm import tqdm

client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

# --- Logprobs (Keep the original function, slightly modified for clarity) ---


def compute_logprob_together(text, model, enable_logprobs):
    """Computes log probabilities for the given text using Together AI."""
    if not enable_logprobs or not text:
        # Return NaNs if logprobs disabled or text is empty
        # Need to return a structure compatible with downstream processing
        return float("nan"), 0, [], []  # logprob_sum, num_tokens, logprobs, tokens

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": text}],
            max_tokens=1,  # Only process the input
            echo=True,  # Return input tokens and logprobs
            logprobs=1,  # Request logprobs for the top token
        )
        # Ensure prompt and logprobs exist before accessing
        if response.prompt and response.prompt[0].logprobs:
            # Skip the first token/logprob (often BOS)
            logprobs = response.prompt[0].logprobs.token_logprobs[1:]
            tokens = response.prompt[0].logprobs.tokens[1:]
            # Handle potential empty logprobs list
            logprob_sum = sum(logprobs) if logprobs else 0.0
            num_tokens = len(tokens)
            return logprob_sum, num_tokens, logprobs, tokens
        else:
            print(f"[WARN] Logprobs not returned for model {model}. Text length: {len(text)}")
            return float("nan"), 0, [], []

    except Exception as e:
        print(f"[ERROR] Failed to compute logprobs for text snippet (len={len(text)}): {e}")
        return float("nan"), 0, [], []


# --- Code Metrics (Keep the original function) ---


def compute_code_metrics(code: str):
    """Computes static code metrics using radon."""
    if not code or not code.strip():
        # Handle empty code string
        return {
            "loc": 0,
            "sloc": 0,
            "lloc": 0,
            "comments": 0,
            "multi": 0,
            "blank": 0,
            "cyclomatic": 0,
        }
    try:
        raw_metrics = analyze(code)
        # Handle potential parsing errors in cc_visit
        try:
            complexity_metrics = cc_visit(code)
            cyclo = sum(block.complexity for block in complexity_metrics)
        except Exception:
            cyclo = float("nan")

        return {
            "loc": raw_metrics.loc,  # total lines of code
            "sloc": raw_metrics.sloc,  # source lines of code (non-blank, non-comment)
            "lloc": raw_metrics.lloc,  # logical lines (statements, e.g. `if`, `for`, `return`)
            "comments": raw_metrics.comments,
            "multi": raw_metrics.multi,
            "blank": raw_metrics.blank,
            "cyclomatic": cyclo,
        }
    except Exception as e:  # Catch broader errors during analysis
        print(f"[WARN] Radon analysis failed: {e}. Code snippet:\n{code[:200]}...")
        return {
            "loc": float("nan"),
            "sloc": float("nan"),
            "lloc": float("nan"),
            "comments": float("nan"),
            "multi": float("nan"),
            "blank": float("nan"),
            "cyclomatic": float("nan"),
        }


def count_tokens(text, model):
    """Counts tokens using tiktoken for the specified model, with fallback."""
    if not text:
        return 0
    try:
        # First, try automatic mapping
        enc = tiktoken.encoding_for_model(model)
        return len(enc.encode(text))
    except KeyError:
        # If automatic mapping fails, try a common fallback
        fallback_encoding = "cl100k_base"
        try:
            print(f"[WARN] Tiktoken encoding_for_model failed for {model}. Trying fallback '{fallback_encoding}'.")
            enc = tiktoken.get_encoding(fallback_encoding)
            return len(enc.encode(text))
        except Exception as e_fallback:
            print(
                f"[ERROR] Tiktoken fallback encoding '{fallback_encoding}' also failed: {e_fallback}. Cannot count tokens accurately."  # noqa: E501
            )
            return float("nan")  # Return NaN if both methods fail
    except Exception as e_general:
        # Catch other potential errors during encoding
        print(
            f"[ERROR] Tiktoken encoding failed unexpectedly for model {model}: {e_general}. Cannot count tokens accurately."  # noqa: E501
        )
        return float("nan")


# --- Core Processing Logic ---


def process_file(file_path: Path, model: str, enable_logprobs: bool, context_code: str = ""):
    """
    Processes a single Python file (main.py or library.py)
    to compute metrics and optionally log probabilities (with context).
    """
    program_name = str(file_path)  # Use full path or relative? Let's keep it simple for now.
    results = {
        "file_path": program_name,
        "metrics": {},
        "logprobs": float("nan"),
        "tokens": 0,
    }

    if not file_path.exists():
        print(f"[WARN] File not found: {file_path}")
        # Assign NaN/0 to all metrics if file doesn't exist
        results["metrics"] = {
            k: float("nan") for k in ["loc", "sloc", "lloc", "comments", "multi", "blank", "cyclomatic"]
        }
        return results

    try:
        code = file_path.read_text()
    except Exception as e:
        print(f"[ERROR] Failed to read file {file_path}: {e}")
        results["metrics"] = {
            k: float("nan") for k in ["loc", "sloc", "lloc", "comments", "multi", "blank", "cyclomatic"]
        }
        return results

    # 1. Compute static code metrics
    results["metrics"] = compute_code_metrics(code)

    # 2. Compute log probabilities (if enabled)
    if enable_logprobs:
        if context_code:
            # Add markers for clarity when context is present
            context_marker_start = "# === CONTEXT CODE START ===\n"
            context_marker_end = "\n# === CONTEXT CODE END ===\n\n"
            main_marker_start = "# === MAIN CODE START ===\n"
            main_marker_end = "\n# === MAIN CODE END ==="
            full_text = (
                context_marker_start + context_code + context_marker_end + main_marker_start + code + main_marker_end
            )
            # Need token count of the context *including markers* for correct offset
            context_with_markers = context_marker_start + context_code + context_marker_end + main_marker_start
            num_context_tokens = count_tokens(context_with_markers, model)

        else:
            full_text = code
            num_context_tokens = 0

        if math.isnan(num_context_tokens):
            print(
                f"[WARN] Could not calculate context tokens for {file_path}. Logprobs for this file might be inaccurate."  # noqa: E501
            )
            # Decide how to handle this - skip logprobs or proceed with potentially wrong offset?
            # Let's skip logprob calculation for this file if context token count failed.
            results["logprobs"] = float("nan")
            results["tokens"] = count_tokens(code, model)  # Count tokens for the main code only
        elif full_text.strip():
            _, _, all_logprobs, all_tokens = compute_logprob_together(full_text, model, enable_logprobs)

            # Extract logprobs and tokens *only* for the main code part
            main_logprobs = all_logprobs[num_context_tokens:]
            main_tokens = all_tokens[num_context_tokens:]  # For counting

            results["logprobs"] = sum(main_logprobs) if main_logprobs else 0.0
            results["tokens"] = len(main_tokens)
        else:
            # Handle case where the code file itself is empty
            results["logprobs"] = 0.0
            results["tokens"] = 0
    else:
        # If logprobs disabled, still count tokens for the main code
        results["tokens"] = count_tokens(code, model)

    # Handle NaN token counts
    if math.isnan(results["tokens"]):
        print(f"[WARN] Token count failed for {file_path}. Setting tokens to NaN.")

    return results


def aggregate_metrics(program_results: list):
    """Aggregates metrics from a list of program processing results."""
    total_metrics = {
        "logprobs": 0.0,
        "tokens": 0,
        "loc": 0,
        "sloc": 0,
        "lloc": 0,
        "comments": 0,
        "multi": 0,
        "blank": 0,
        "cyclomatic": 0,
    }
    valid_logprobs = 0
    valid_tokens = 0
    valid_loc = 0
    valid_sloc = 0
    valid_lloc = 0
    valid_comments = 0
    valid_multi = 0
    valid_blank = 0
    valid_cyclo = 0

    for result in program_results:
        # Sum logprobs only if they are valid numbers
        if not math.isnan(result.get("logprobs", float("nan"))):
            total_metrics["logprobs"] += result["logprobs"]
            valid_logprobs += 1
        # Sum tokens only if they are valid numbers
        if not math.isnan(result.get("tokens", float("nan"))):
            total_metrics["tokens"] += result["tokens"]
            valid_tokens += 1

        # Sum static metrics only if they are valid numbers
        metrics = result.get("metrics", {})
        if not math.isnan(metrics.get("loc", float("nan"))):
            total_metrics["loc"] += metrics["loc"]
            valid_loc += 1
        if not math.isnan(metrics.get("sloc", float("nan"))):
            total_metrics["sloc"] += metrics["sloc"]
            valid_sloc += 1
        if not math.isnan(metrics.get("lloc", float("nan"))):
            total_metrics["lloc"] += metrics["lloc"]
            valid_lloc += 1
        if not math.isnan(metrics.get("comments", float("nan"))):
            total_metrics["comments"] += metrics["comments"]
            valid_comments += 1
        if not math.isnan(metrics.get("multi", float("nan"))):
            total_metrics["multi"] += metrics["multi"]
            valid_multi += 1
        if not math.isnan(metrics.get("blank", float("nan"))):
            total_metrics["blank"] += metrics["blank"]
            valid_blank += 1
        if not math.isnan(metrics.get("cyclomatic", float("nan"))):
            total_metrics["cyclomatic"] += metrics["cyclomatic"]
            valid_cyclo += 1

    # Check if any valid metrics were found before finalizing
    if valid_logprobs == 0:
        total_metrics["logprobs"] = float("nan")
    if valid_tokens == 0:
        total_metrics["tokens"] = float("nan")
    if valid_loc == 0:
        total_metrics["loc"] = float("nan")
    if valid_sloc == 0:
        total_metrics["sloc"] = float("nan")
    if valid_lloc == 0:
        total_metrics["lloc"] = float("nan")
    if valid_comments == 0:
        total_metrics["comments"] = float("nan")
    if valid_multi == 0:
        total_metrics["multi"] = float("nan")
    if valid_blank == 0:
        total_metrics["blank"] = float("nan")
    if valid_cyclo == 0:
        total_metrics["cyclomatic"] = float("nan")

    return total_metrics


# --- Main Function ---


def main(args):
    cluster_name = args.cluster_name
    base_refactored_dir = Path("codecontests")
    base_original_dir = Path("codecontests_original")
    model = args.model
    enable_logprobs = args.enable_logprobs

    refactored_cluster_dir = base_refactored_dir / cluster_name
    original_cluster_dir = base_original_dir / cluster_name

    if not refactored_cluster_dir.is_dir():
        print(f"[ERROR] Refactored cluster directory not found: {refactored_cluster_dir}")
        sys.exit(1)
    if not original_cluster_dir.is_dir():
        print(f"[ERROR] Original cluster directory not found: {original_cluster_dir}")
        sys.exit(1)

    output_file = Path(f"{cluster_name}_comparison_metrics.json")
    print(f"Processing cluster: {cluster_name}")
    print(f"Refactored code path: {refactored_cluster_dir}")
    print(f"Original code path:   {original_cluster_dir}")
    print(f"LLM Model: {model}")
    print(f"Logprobs Enabled: {enable_logprobs}")
    print(f"Output file: {output_file}")

    # --- Process Refactored Cluster ---
    print("\n--- Processing Refactored Files ---")
    refactored_library_path = refactored_cluster_dir / "library.py"
    library_content = ""
    library_results = {}

    if refactored_library_path.exists():
        print(f"Processing library file: {refactored_library_path}")
        try:
            library_content = refactored_library_path.read_text()
            # Process library: No context needed for the library itself
            library_results = process_file(refactored_library_path, model, enable_logprobs, context_code="")
        except Exception as e:
            print(f"[ERROR] Failed to read or process library file {refactored_library_path}: {e}")
            # Create placeholder results if library processing fails
            library_results = {
                "file_path": str(refactored_library_path),
                "metrics": {
                    k: float("nan") for k in ["loc", "sloc", "lloc", "comments", "multi", "blank", "cyclomatic"]
                },
                "logprobs": float("nan"),
                "tokens": 0,
            }
    else:
        print("[WARN] library.py not found in refactored cluster.")
        # Create placeholder results if library doesn't exist
        library_results = {
            "file_path": str(refactored_library_path),
            "metrics": {
                k: 0 for k in ["loc", "sloc", "lloc", "comments", "multi", "blank", "cyclomatic"]
            },  # Metrics are 0 if no file
            "logprobs": 0.0,
            "tokens": 0,  # Logprobs/Tokens are 0 if no file
        }

    refactored_program_results = []
    problem_dirs_refactored = [d for d in refactored_cluster_dir.iterdir() if d.is_dir()]

    for problem_dir in tqdm(problem_dirs_refactored, desc="Refactored Problems"):
        main_py_path = problem_dir / "main.py"
        if main_py_path.exists():
            # Process main.py with library content as context
            result = process_file(main_py_path, model, enable_logprobs, context_code=library_content)
            # Add problem name for easier identification
            result["problem_name"] = problem_dir.name
            refactored_program_results.append(result)
        else:
            print(f"[WARN] main.py not found in {problem_dir}")

    # Aggregate metrics for refactored programs (main.py files only)
    aggregated_refactored_mains = aggregate_metrics(refactored_program_results)

    # Combine library metrics with main program metrics for overall refactored aggregate
    # Important: Need to handle potential NaN values during addition
    def safe_add(*args):
        total = 0
        valid_count = 0
        for x in args:
            if not math.isnan(x):
                total += x
                valid_count += 1
        return total if valid_count > 0 else float("nan")

    aggregated_refactored_total = {
        "logprobs": safe_add(aggregated_refactored_mains["logprobs"], library_results.get("logprobs", float("nan"))),
        "tokens": safe_add(aggregated_refactored_mains["tokens"], library_results.get("tokens", float("nan"))),
        "loc": safe_add(
            aggregated_refactored_mains["loc"], library_results.get("metrics", {}).get("loc", float("nan"))
        ),
        "sloc": safe_add(
            aggregated_refactored_mains["sloc"], library_results.get("metrics", {}).get("sloc", float("nan"))
        ),
        "lloc": safe_add(
            aggregated_refactored_mains["lloc"], library_results.get("metrics", {}).get("lloc", float("nan"))
        ),
        "comments": safe_add(
            aggregated_refactored_mains["comments"], library_results.get("metrics", {}).get("comments", float("nan"))
        ),
        "multi": safe_add(
            aggregated_refactored_mains["multi"], library_results.get("metrics", {}).get("multi", float("nan"))
        ),
        "blank": safe_add(
            aggregated_refactored_mains["blank"], library_results.get("metrics", {}).get("blank", float("nan"))
        ),
        "cyclomatic": safe_add(
            aggregated_refactored_mains["cyclomatic"],
            library_results.get("metrics", {}).get("cyclomatic", float("nan")),
        ),
    }

    # --- Process Original Cluster ---
    print("\n--- Processing Original Files ---")
    original_program_results = []
    problem_dirs_original = [d for d in original_cluster_dir.iterdir() if d.is_dir()]

    for problem_dir in tqdm(problem_dirs_original, desc="Original Problems"):
        main_py_path = problem_dir / "main.py"
        if main_py_path.exists():
            # Process original main.py without any context
            result = process_file(main_py_path, model, enable_logprobs, context_code="")
            # Add problem name
            result["problem_name"] = problem_dir.name
            original_program_results.append(result)
        else:
            print(f"[WARN] main.py not found in {problem_dir}")

    # Aggregate metrics for original programs
    aggregated_original_total = aggregate_metrics(original_program_results)

    # --- Calculate Ratios ---
    print("\n--- Calculating Ratios ---")
    ratios = {}
    try:
        # Ensure denominators are not zero or NaN
        orig_tokens = aggregated_original_total.get("tokens", float("nan"))
        ref_tokens = aggregated_refactored_total.get("tokens", float("nan"))
        if not math.isnan(orig_tokens) and not math.isnan(ref_tokens) and orig_tokens != 0:
            ratios["tokens_refactored_div_original"] = ref_tokens / orig_tokens
        else:
            ratios["tokens_refactored_div_original"] = float("nan")

        orig_logprobs = aggregated_original_total.get("logprobs", float("nan"))
        ref_logprobs = aggregated_refactored_total.get("logprobs", float("nan"))
        # Avoid division by zero or NaN. Also, logprobs can be negative.
        if not math.isnan(orig_logprobs) and not math.isnan(ref_logprobs) and orig_logprobs != 0:
            # Be careful with signs if comparing directly. Ratio might be less intuitive.
            # Maybe compare average logprob per token?
            ratios["logprobs_refactored_div_original"] = ref_logprobs / orig_logprobs
            # Add average logprob per token comparison
            avg_lp_orig = orig_logprobs / orig_tokens if orig_tokens else float("nan")
            avg_lp_ref = ref_logprobs / ref_tokens if ref_tokens else float("nan")
            ratios["avg_logprob_per_token_original"] = avg_lp_orig
            ratios["avg_logprob_per_token_refactored"] = avg_lp_ref
        else:
            ratios["logprobs_refactored_div_original"] = float("nan")
            ratios["avg_logprob_per_token_original"] = float("nan")
            ratios["avg_logprob_per_token_refactored"] = float("nan")

    except ZeroDivisionError:
        print("[WARN] Division by zero encountered while calculating ratios.")
    except Exception as e:
        print(f"[ERROR] Error calculating ratios: {e}")

    # --- Package Results ---
    print("\n--- Packaging Results ---")
    final_results = {
        "cluster_name": cluster_name,
        "model": model,
        "logprobs_enabled": enable_logprobs,
        "refactored_library": library_results,
        "refactored_programs": {res["problem_name"]: res for res in refactored_program_results},
        "original_programs": {res["problem_name"]: res for res in original_program_results},
        "aggregated_metrics_refactored": aggregated_refactored_total,
        "aggregated_metrics_original": aggregated_original_total,
        "comparison_ratios": ratios,
    }

    # --- Write Output ---
    try:
        with open(output_file, "w") as wf:
            # Use a custom encoder to handle Path objects and NaN values if necessary
            class CustomEncoder(json.JSONEncoder):
                def default(self, obj):
                    if isinstance(obj, Path):
                        return str(obj)
                    if isinstance(obj, float) and math.isnan(obj):
                        return "NaN"  # Represent NaN as a string
                    return super(CustomEncoder, self).default(obj)

            json.dump(final_results, wf, indent=4, cls=CustomEncoder)
        print(f"\nResults successfully written to {output_file}")
    except Exception as e:
        print(f"[ERROR] Failed to write output JSON file: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze and compare refactored vs original code in a cluster.")
    parser.add_argument("--cluster_name", type=str, required=True, help="Name of the cluster folder (e.g., cluster0)")
    parser.add_argument(
        "--model",
        type=str,
        default="Qwen/Qwen2.5-7B-Instruct-Turbo",
        help="Name of the model hosted on Together AI (or compatible)",
    )  # Changed default model as V3 might not exist
    parser.add_argument(
        "--enable_logprobs", action="store_true", default=False, help="Turn on logprob computing via Together AI"
    )
    args = parser.parse_args()

    main(args)

# ---- Example usage ----
# python your_script_name.py --cluster_name cluster0 --enable_logprobs --model deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct # noqa: E501
