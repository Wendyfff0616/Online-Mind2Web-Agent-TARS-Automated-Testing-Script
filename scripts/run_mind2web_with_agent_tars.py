#!/usr/bin/env python3
"""
Script to run Mind2Web tasks with Agent TARS
Loads tasks from the Online Mind2Web dataset and executes them using Agent TARS CLI.
"""

import subprocess
import sys
import json
import argparse
import time
from typing import Dict, List, Optional
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        from datasets import load_dataset
        return True
    except ImportError:
        return False

def load_mind2web_dataset():
    """Load the Online Mind2Web dataset"""
    try:
        from datasets import load_dataset
        print("Loading Online Mind2Web dataset...")
        # Login using `huggingface-cli login` to access this dataset
        ds = load_dataset("osunlp/Online-Mind2Web")
        print(f"Dataset loaded successfully. Available splits: {list(ds.keys())}")
        return ds
    except Exception as e:
        print(f"Error loading dataset: {e}")
        print("Make sure you have logged in with: huggingface-cli login")
        sys.exit(1)

def format_task_input(task_data: Dict) -> str:
    """Format the task data into an input string for Agent TARS"""
    confirmed_task = task_data.get('confirmed_task', '')
    website = task_data.get('website', '')
    
    if website:
        # Include website URL in the task instruction
        return f"在网站 {website} 上执行以下任务: {confirmed_task}"
    else:
        return confirmed_task

def run_agent_tars(task_input: str, debug: bool = True, timeout: int = 300) -> Dict:
    """Run Agent TARS with the given task input"""
    
    # Prepare the command
    cmd = ["agent-tars", "run", "--input", task_input]
    if debug:
        cmd.append("--debug")
    
    print(f"\n{'='*80}")
    print(f"执行 Agent TARS 任务:")
    print(f"输入: {task_input}")
    print(f"命令: {' '.join(cmd)}")
    print(f"{'='*80}\n")
    
    try:
        # Run the command with timeout
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
        
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'stdout': '',
            'stderr': f'Task timed out after {timeout} seconds',
            'returncode': -1
        }
    except Exception as e:
        return {
            'success': False,
            'stdout': '',
            'stderr': f'Error executing command: {str(e)}',
            'returncode': -1
        }

def run_agent_tars_realtime(task_input: str, debug: bool = True, timeout: int = 300) -> Dict:
    """Run Agent TARS with real-time output display"""
    
    # Prepare the command
    cmd = ["agent-tars", "run", "--input", task_input]
    if debug:
        cmd.append("--debug")
    
    print(f"\n{'='*80}")
    print(f"执行 Agent TARS 任务:")
    print(f"输入: {task_input}")
    print(f"命令: {' '.join(cmd)}")
    print(f"{'='*80}\n")
    
    try:
        # Use Popen for real-time output
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Merge stderr into stdout
            text=True,
            bufsize=1,  # Line buffered for real-time output
            universal_newlines=True
        )
        
        output_lines = []
        
        # Read output line by line and display in real-time
        try:
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    # Print to terminal in real-time
                    print(line.rstrip())
                    # Store for later
                    output_lines.append(line)
        except KeyboardInterrupt:
            print("\n⚠️  任务被用户中断 (Ctrl+C)")
            process.terminate()
            process.wait()
            return {
                'success': False,
                'stdout': ''.join(output_lines),
                'stderr': 'Task interrupted by user (Ctrl+C)',
                'returncode': -2
            }
        
        # Wait for process to complete
        process.wait()
        
        # Join all output lines
        full_output = ''.join(output_lines)
        
        return {
            'success': process.returncode == 0,
            'stdout': full_output,
            'stderr': '',  # We merged stderr into stdout
            'returncode': process.returncode
        }
        
    except Exception as e:
        return {
            'success': False,
            'stdout': '',
            'stderr': f'Error executing command: {str(e)}',
            'returncode': -1
        }

def save_results(results: List[Dict], output_file: str):
    """Save the execution results to a JSON file"""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n结果已保存到: {output_path}")

def create_sample_tasks():
    """Create sample tasks for demonstration when dataset is not available"""
    return [
        {
            'confirmed_task': 'Search for wireless headphones under $50',
            'website': 'https://www.amazon.com'
        },
        {
            'confirmed_task': 'Find the latest iPhone reviews',
            'website': 'https://www.cnet.com'
        },
        {
            'confirmed_task': 'Look up weather forecast for New York',
            'website': 'https://weather.com'
        }
    ]

def main():
    parser = argparse.ArgumentParser(description="Run Mind2Web tasks with Agent TARS")
    parser.add_argument("--split", default="test", help="Dataset split to use (default: test)")
    parser.add_argument("--start", type=int, default=0, help="Start index (default: 0)")
    parser.add_argument("--end", type=int, help="End index (if not specified, runs all from start)")
    parser.add_argument("--max-tasks", type=int, default=2, help="Maximum number of tasks to run (default: 2)")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout per task in seconds (default: 300)")
    parser.add_argument("--output", default="results/mind2web_agent_tars_results.json", 
                       help="Output file for results (default: results/mind2web_agent_tars_results.json)")
    parser.add_argument("--no-debug", action="store_true", help="Disable debug mode")
    parser.add_argument("--dry-run", action="store_true", help="Show tasks without executing them")
    parser.add_argument("--use-sample", action="store_true", help="Use sample tasks instead of loading dataset")
    
    args = parser.parse_args()
    
    # Check dependencies unless using sample data
    if not args.use_sample and not check_dependencies():
        print("Error: 'datasets' library not found. Please install it with:")
        print("pip install datasets")
        print("\nAlternatively, use --use-sample to run with sample tasks:")
        print("python scripts/run_mind2web_with_agent_tars.py --use-sample --dry-run")
        sys.exit(1)
    
    # Load data
    if args.use_sample:
        print("Using sample tasks for demonstration...")
        split_data = create_sample_tasks()
        total_tasks = len(split_data)
    else:
        # Load dataset
        dataset = load_mind2web_dataset()
        split_data = dataset[args.split]
        total_tasks = len(split_data)
    
    # Determine task range
    start_idx = args.start
    end_idx = args.end if args.end is not None else min(start_idx + args.max_tasks, total_tasks)
    end_idx = min(end_idx, total_tasks)
    
    print(f"\n总任务数: {total_tasks}")
    print(f"将执行任务范围: {start_idx} 到 {end_idx-1} (共 {end_idx - start_idx} 个任务)")
    
    if args.dry_run:
        print("\n=== DRY RUN 模式 - 仅显示任务，不执行 ===")
    
    results = []
    
    for i in range(start_idx, end_idx):
        if args.use_sample:
            task_data = split_data[i]
        else:
            task_data = split_data[i]
            
        task_input = format_task_input(task_data)
        
        task_info = {
            'index': i,
            'task_input': task_input,
            'confirmed_task': task_data.get('confirmed_task', ''),
            'website': task_data.get('website', ''),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if args.dry_run:
            print(f"\n任务 {i}:")
            print(f"  网站: {task_data.get('website', 'N/A')}")
            print(f"  任务: {task_data.get('confirmed_task', 'N/A')}")
            print(f"  格式化输入: {task_input}")
            continue
        
        # Execute the task
        execution_result = run_agent_tars_realtime(
            task_input, 
            debug=not args.no_debug, 
            timeout=args.timeout
        )
        
        # Combine task info with execution result
        task_result = {**task_info, **execution_result}
        results.append(task_result)
        
        # Print execution summary
        status = "✅ 成功" if execution_result['success'] else "❌ 失败"
        print(f"\n任务 {i} 执行结果: {status}")
        if not execution_result['success']:
            print(f"错误信息: {execution_result['stderr']}")
        
        # Small delay between tasks
        if i < end_idx - 1:
            print("等待 2 秒后执行下一个任务...")
            time.sleep(2)
    
    if not args.dry_run and results:
        # Save results
        save_results(results, args.output)
        
        # Print summary
        successful_tasks = sum(1 for r in results if r['success'])
        print(f"\n{'='*80}")
        print(f"执行总结:")
        print(f"总任务数: {len(results)}")
        print(f"成功任务: {successful_tasks}")
        print(f"失败任务: {len(results) - successful_tasks}")
        print(f"成功率: {successful_tasks/len(results)*100:.1f}%")
        print(f"{'='*80}")

if __name__ == "__main__":
    main() 