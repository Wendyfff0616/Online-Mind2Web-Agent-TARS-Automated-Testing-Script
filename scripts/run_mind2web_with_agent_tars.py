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

def filter_tasks(dataset, task_length_min=None, task_length_max=None, 
                level=None, website_filter=None, max_tasks=None):
    """Filter tasks based on various criteria"""
    filtered_tasks = []
    total_checked = 0
    
    print("\n🔍 正在筛选任务...")
    print(f"筛选条件:")
    if task_length_min or task_length_max:
        print(f"  - confirmed_task长度: {task_length_min or '无限制'} - {task_length_max or '无限制'}")
    if level:
        print(f"  - 难度级别: {level}")
    if website_filter:
        print(f"  - 网站包含: {website_filter}")
    if max_tasks:
        print(f"  - 最大任务数: {max_tasks}")
    
    for i, task in enumerate(dataset):
        total_checked += 1
        
        # 检查confirmed_task长度
        confirmed_task = task.get('confirmed_task', '')
        task_length = len(confirmed_task)
        
        if task_length_min and task_length < task_length_min:
            continue
        if task_length_max and task_length > task_length_max:
            continue
        
        # 检查难度级别
        if level and task.get('level') != level:
            continue
        
        # 检查网站筛选
        website = task.get('website', '')
        if website_filter and website_filter.lower() not in website.lower():
            continue
        
        # 添加原始索引信息
        task_with_index = {
            'original_index': i,
            'task_length': task_length,
            **task
        }
        filtered_tasks.append(task_with_index)
        
        # 达到最大任务数就停止
        if max_tasks and len(filtered_tasks) >= max_tasks:
            break
    
    print(f"✅ 筛选完成: 从 {total_checked} 个任务中筛选出 {len(filtered_tasks)} 个符合条件的任务")
    
    # 显示筛选结果统计
    if filtered_tasks:
        lengths = [t['task_length'] for t in filtered_tasks]
        print(f"   任务长度范围: {min(lengths)} - {max(lengths)}")
        
        levels = [t.get('level', 'unknown') for t in filtered_tasks]
        level_counts = {}
        for level in levels:
            level_counts[level] = level_counts.get(level, 0) + 1
        print(f"   难度分布: {level_counts}")
        
        websites = list(set([t.get('website', '') for t in filtered_tasks]))
        print(f"   涉及网站数: {len(websites)}")
    
    return filtered_tasks

def display_task_preview(filtered_tasks, preview_count=5):
    """Display a preview of filtered tasks"""
    print(f"\n📋 任务预览 (前 {min(preview_count, len(filtered_tasks))} 个):")
    print("-" * 100)
    
    for i, task in enumerate(filtered_tasks[:preview_count]):
        confirmed_task = task.get('confirmed_task', '')
        website = task.get('website', '')
        level = task.get('level', 'unknown')
        length = task.get('task_length', 0)
        
        print(f"任务 {i+1} (原索引: {task['original_index']}):")
        print(f"  网站: {website}")
        print(f"  难度: {level} | 长度: {length}")
        print(f"  任务: {confirmed_task[:100]}{'...' if len(confirmed_task) > 100 else ''}")
        print("-" * 100)

def format_task_input(task_data: Dict) -> str:
    """Format the task data into an input string for Agent TARS"""
    confirmed_task = task_data.get('confirmed_task', '')
    website = task_data.get('website', '')
    
    if website:
        # Include website URL in the task instruction
        return f"""在网站 {website} 上执行以下任务: {confirmed_task}

执行要求:
1. 逐步完成任务的每个步骤
2. 在关键操作点使用 browser_screenshot 工具记录进度
3. 确保真正完成任务目标，而不仅仅是截图
4. 每次截图后继续执行下一步操作

注意：GUI Agent会自动截图用于决策，你需要额外调用browser_screenshot工具来保存重要进度截图到本地。"""
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
    
    # Prepare the command - 使用--input参数
    cmd = ["agent-tars", "run", "--input", task_input]
    if debug:
        cmd.append("--debug")
    
    print(f"\n{'='*80}")
    print(f"执行 Agent TARS 任务:")
    print(f"输入: {task_input[:100]}{'...' if len(task_input) > 100 else ''}")
    print(f"命令: agent-tars run --input \"{task_input[:80]}{'...' if len(task_input) > 80 else ''}\" {'--debug' if debug else ''}")
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

def generate_website_filename(website: str) -> str:
    """Generate filename based on website domain"""
    if not website:
        return "unknown"
    
    # Extract domain name from URL
    from urllib.parse import urlparse
    try:
        parsed = urlparse(website)
        domain = parsed.netloc or parsed.path
        # Remove 'www.' prefix if present
        if domain.startswith('www.'):
            domain = domain[4:]
        # Remove .com/.org etc. suffix and take first part
        domain_name = domain.split('.')[0]
        return domain_name.lower()
    except:
        # Fallback: clean the website string
        clean_name = website.replace('https://', '').replace('http://', '').replace('www.', '')
        clean_name = clean_name.split('.')[0].split('/')[0]
        return clean_name.lower()

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
    parser.add_argument("--max-tasks", type=int, default=10, help="Maximum number of tasks to run (default: 10)")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout per task in seconds (default: 300)")
    parser.add_argument("--output", default="./results/mind2web_agent_tars_results.json", 
                       help="Output file for results (default: ./results/mind2web_agent_tars_results.json)")
    parser.add_argument("--no-debug", action="store_true", help="Disable debug mode")
    parser.add_argument("--dry-run", action="store_true", help="Show tasks without executing them")
    parser.add_argument("--use-sample", action="store_true", help="Use sample tasks instead of loading dataset")
    
    # 新增筛选参数
    parser.add_argument("--task-length-min", type=int, help="Minimum confirmed_task length")
    parser.add_argument("--task-length-max", type=int, help="Maximum confirmed_task length") 
    parser.add_argument("--level", choices=["easy", "medium", "hard"], help="Task difficulty level")
    parser.add_argument("--website-filter", help="Filter tasks by website (partial match)")
    parser.add_argument("--preview", type=int, default=5, help="Number of tasks to preview (default: 5)")
    parser.add_argument("--task-index", type=int, help="Run specific task by index (0-based, from filtered results)")
    parser.add_argument("--auto-filename", action="store_true", help="Auto-generate filename based on website name")
    
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
        # 添加task_length字段到示例数据
        for task in split_data:
            task['task_length'] = len(task.get('confirmed_task', ''))
            task['original_index'] = split_data.index(task)
        filtered_tasks = split_data
        total_tasks = len(split_data)
    else:
        # Load dataset
        dataset = load_mind2web_dataset()
        split_data = dataset[args.split]
        total_tasks = len(split_data)
        
        # Apply filters
        filtered_tasks = filter_tasks(
            split_data,
            task_length_min=args.task_length_min,
            task_length_max=args.task_length_max,
            level=args.level,
            website_filter=args.website_filter,
            max_tasks=args.max_tasks
        )
    
    # Show preview
    if filtered_tasks:
        display_task_preview(filtered_tasks, args.preview)
    else:
        print("❌ 没有找到符合筛选条件的任务")
        return
    
    # Determine task range from filtered results
    if args.task_index is not None:
        # Run specific task by index
        if 0 <= args.task_index < len(filtered_tasks):
            tasks_to_run = [filtered_tasks[args.task_index]]
            print(f"\n🎯 选择运行任务索引 {args.task_index}")
        else:
            print(f"❌ 任务索引 {args.task_index} 超出范围 (0-{len(filtered_tasks)-1})")
            return
    elif not args.use_sample:
        # 重新计算范围，基于筛选后的结果
        start_idx = args.start
        end_idx = args.end if args.end is not None else len(filtered_tasks)
        end_idx = min(end_idx, len(filtered_tasks))
        tasks_to_run = filtered_tasks[start_idx:end_idx]
    else:
        tasks_to_run = filtered_tasks
    
    print(f"\n总筛选结果: {len(filtered_tasks)} 个任务")
    print(f"将执行任务数: {len(tasks_to_run)} 个任务")
    
    if args.dry_run:
        print("\n=== DRY RUN 模式 - 仅显示任务，不执行 ===")
        for i, task_data in enumerate(tasks_to_run):
            task_input = format_task_input(task_data)
            # 当使用 --task-index 时，显示用户选择的索引
            if args.task_index is not None:
                display_index = args.task_index
            else:
                display_index = i
            print(f"\n任务 {display_index} (原索引: {task_data.get('original_index', display_index)}):")
            print(f"  网站: {task_data.get('website', 'N/A')}")
            print(f"  任务长度: {task_data.get('task_length', 'N/A')}")
            print(f"  难度: {task_data.get('level', 'N/A')}")
            print(f"  任务: {task_data.get('confirmed_task', 'N/A')}")
            print(f"  格式化输入: {task_input[:100]}{'...' if len(task_input) > 100 else ''}")
        return
    
    results = []
    
    for i, task_data in enumerate(tasks_to_run):
        task_input = format_task_input(task_data)
        
        # 当使用 --task-index 时，记录用户选择的索引
        if args.task_index is not None:
            task_index = args.task_index
        else:
            task_index = i
            
        task_info = {
            'index': task_index,
            'original_index': task_data.get('original_index', task_index),
            'task_input': task_input,
            'confirmed_task': task_data.get('confirmed_task', ''),
            'website': task_data.get('website', ''),
            'task_length': task_data.get('task_length', 0),
            'level': task_data.get('level', 'unknown'),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
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
        # 当使用 --task-index 时，显示用户选择的索引
        if args.task_index is not None:
            display_index = args.task_index
        else:
            display_index = i
        print(f"\n任务 {display_index} (原索引: {task_data.get('original_index', display_index)}) 执行结果: {status}")
        if not execution_result['success']:
            print(f"错误信息: {execution_result['stderr']}")
        
        # Small delay between tasks
        if i < len(tasks_to_run) - 1:
            print("等待 2 秒后执行下一个任务...")
            time.sleep(2)
    
    if results:
        # Generate output filename
        output_file = args.output
        if args.auto_filename and len(results) == 1:
            # Auto-generate filename for single task based on website
            website = results[0].get('website', '')
            website_name = generate_website_filename(website)
            output_file = f"./results/mind2web_{website_name}_results.json"
            print(f"📝 自动生成文件名: {output_file}")
        
        # Save results
        save_results(results, output_file)
        
        # Print summary
        successful_tasks = sum(1 for r in results if r['success'])
        print(f"\n{'='*80}")
        print(f"执行总结:")
        print(f"总任务数: {len(results)}")
        print(f"成功任务: {successful_tasks}")
        print(f"失败任务: {len(results) - successful_tasks}")
        print(f"成功率: {successful_tasks/len(results)*100:.1f}%")
        
        # 按难度统计
        level_stats = {}
        for result in results:
            level = result.get('level', 'unknown')
            if level not in level_stats:
                level_stats[level] = {'total': 0, 'success': 0}
            level_stats[level]['total'] += 1
            if result['success']:
                level_stats[level]['success'] += 1
        
        print(f"\n按难度级别统计:")
        for level, stats in level_stats.items():
            success_rate = stats['success'] / stats['total'] * 100 if stats['total'] > 0 else 0
            print(f"  {level}: {stats['success']}/{stats['total']} ({success_rate:.1f}%)")
        
        print(f"{'='*80}")

if __name__ == "__main__":
    main() 