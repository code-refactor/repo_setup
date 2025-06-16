#!/usr/bin/env python3
"""
Parser for codecontests results to extract metrics for original and refactored code.
Extracts: total tests passed, total tests, total log prob, total tokens, total cyclomatic complexity
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple

def parse_compression_json(file_path: str) -> Dict:
    """Parse a compression JSON file to extract aggregated metrics."""
    metrics = {}
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Extract refactored metrics
    if 'aggregated_metrics_refactored' in data:
        refactored = data['aggregated_metrics_refactored']
        metrics['refactored'] = {
            'log_prob': refactored.get('logprobs', 0),
            'total_tokens': refactored.get('tokens', 0),
            'cyclomatic_complexity': refactored.get('cyclomatic', 0)
        }
    
    # Extract original metrics
    if 'aggregated_metrics_original' in data:
        original = data['aggregated_metrics_original']
        metrics['original'] = {
            'log_prob': original.get('logprobs', 0),
            'total_tokens': original.get('tokens', 0),
            'cyclomatic_complexity': original.get('cyclomatic', 0)
        }
    
    return metrics

def parse_test_results_file(file_path: str) -> Dict:
    """Parse a test results file to extract test metrics."""
    metrics = {}
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Look for final results summary
    final_results_match = re.search(r'Final Results: (\d+)/(\d+) problems passed all tests', content)
    if final_results_match:
        passed_problems = int(final_results_match.group(1))
        total_problems = int(final_results_match.group(2))
        
        # Count individual test results
        total_tests_passed = 0
        total_tests = 0
        
        # Find all test result lines
        test_results = re.findall(r'Results: (\d+)/(\d+) tests passed', content)
        for passed, total in test_results:
            total_tests_passed += int(passed)
            total_tests += int(total)
        
        metrics['tests_passed'] = total_tests_passed
        metrics['total_tests'] = total_tests
        metrics['problems_passed'] = passed_problems
        metrics['total_problems'] = total_problems
    
    return metrics

def parse_cluster_results(cluster_name: str, results_dir: Path) -> Dict:
    """Parse all result files for a single cluster."""
    results = {
        'original': {},
        'refactored': {}
    }
    
    # Parse compression JSON file for metrics
    compression_json = results_dir / f'{cluster_name}_compression.json'
    if compression_json.exists():
        compression_data = parse_compression_json(str(compression_json))
        if 'original' in compression_data:
            results['original'].update(compression_data['original'])
        if 'refactored' in compression_data:
            results['refactored'].update(compression_data['refactored'])
    
    # Parse test results for refactored code
    test_refactored = results_dir / f'{cluster_name}_tests.txt'
    if test_refactored.exists():
        test_data = parse_test_results_file(str(test_refactored))
        results['refactored'].update(test_data)
    
    # Parse test results for original code
    test_original = results_dir / f'{cluster_name}_tests_original.txt'
    if test_original.exists():
        test_data = parse_test_results_file(str(test_original))
        results['original'].update(test_data)
    
    return results

def main():
    """Main function to parse all codecontests results."""
    results_dir = Path('results/codecontests')
    all_results = {}
    
    # Get all cluster files
    cluster_files = [f for f in results_dir.glob('cluster*_compression.json')]
    cluster_names = sorted(set([f.stem.replace('_compression', '') for f in cluster_files]))
    
    for cluster_name in cluster_names:
        print(f"Parsing {cluster_name}...")
        
        try:
            cluster_results = parse_cluster_results(cluster_name, results_dir)
            all_results[cluster_name] = cluster_results
        except Exception as e:
            print(f"Error parsing {cluster_name}: {e}")
    
    # Print summary table
    print("\n" + "="*140)
    print(f"{'Cluster':<15} {'Type':<12} {'Tests Passed':<12} {'Total Tests':<12} {'Log Prob':<15} {'Tokens':<10} {'Complexity':<10} {'LogP Ratio':<10} {'Token Ratio':<12}")
    print("="*140)
    
    for cluster_name in sorted(all_results.keys()):
        cluster_data = all_results[cluster_name]
        
        for repo_type in ['original', 'refactored']:
            data = cluster_data[repo_type]
            
            tests_passed = data.get('tests_passed', 'N/A')
            total_tests = data.get('total_tests', 'N/A')
            log_prob = f"{data.get('log_prob', 'N/A'):.2f}" if data.get('log_prob') is not None else 'N/A'
            tokens = data.get('total_tokens', 'N/A')
            complexity = data.get('cyclomatic_complexity', 'N/A')
            
            # Calculate ratios for refactored rows
            logp_ratio = ""
            token_ratio = ""
            if repo_type == 'refactored':
                orig_data = cluster_data['original']
                if (data.get('log_prob') is not None and orig_data.get('log_prob') is not None and 
                    orig_data.get('log_prob') != 0):
                    logp_ratio = f"{data['log_prob'] / orig_data['log_prob']:.3f}"
                if (data.get('total_tokens') is not None and orig_data.get('total_tokens') is not None and 
                    orig_data.get('total_tokens') != 0):
                    token_ratio = f"{data['total_tokens'] / orig_data['total_tokens']:.3f}"
            
            print(f"{cluster_name:<15} {repo_type:<12} {tests_passed:<12} {total_tests:<12} {log_prob:<15} {tokens:<10} {complexity:<10} {logp_ratio:<10} {token_ratio:<12}")
    
    # Calculate totals
    print("\n" + "="*140)
    print("TOTALS:")
    print("="*140)
    
    for repo_type in ['original', 'refactored']:
        total_tests_passed = 0
        total_tests_all = 0
        total_log_prob = 0.0
        total_tokens_all = 0
        total_complexity_all = 0
        valid_clusters = 0
        
        for cluster_data in all_results.values():
            data = cluster_data[repo_type]
            if data.get('tests_passed') is not None:
                total_tests_passed += data['tests_passed']
            if data.get('total_tests') is not None:
                total_tests_all += data['total_tests']
            if data.get('log_prob') is not None:
                total_log_prob += data['log_prob']
            if data.get('total_tokens') is not None:
                total_tokens_all += data['total_tokens']
            if data.get('cyclomatic_complexity') is not None:
                total_complexity_all += data['cyclomatic_complexity']
                valid_clusters += 1
        
        # Calculate overall ratios for totals
        total_logp_ratio = ""
        total_token_ratio = ""
        if repo_type == 'refactored':
            # Calculate totals for original to get ratios
            orig_total_log_prob = 0.0
            orig_total_tokens = 0
            for cluster_data in all_results.values():
                orig_data = cluster_data['original']
                if orig_data.get('log_prob') is not None:
                    orig_total_log_prob += orig_data['log_prob']
                if orig_data.get('total_tokens') is not None:
                    orig_total_tokens += orig_data['total_tokens']
            
            if orig_total_log_prob != 0:
                total_logp_ratio = f"{total_log_prob / orig_total_log_prob:.3f}"
            if orig_total_tokens != 0:
                total_token_ratio = f"{total_tokens_all / orig_total_tokens:.3f}"
        
        print(f"{'TOTAL ' + repo_type.upper():<15} {'':<12} {total_tests_passed:<12} {total_tests_all:<12} {total_log_prob:<15.2f} {total_tokens_all:<10} {total_complexity_all:<10} {total_logp_ratio:<10} {total_token_ratio:<12}")
    
    # Save detailed results to JSON
    output_file = 'codecontests_parsed_results.json'
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\nDetailed results saved to {output_file}")

if __name__ == "__main__":
    main()
