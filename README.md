# Online Mind2Web + Agent TARS Automated Testing Script

**Languages:** [English](README.md) | [中文](README_CN.md)

---

This script loads tasks from the Online Mind2Web dataset and executes them using Agent TARS.

## File Structure

The repository structure:

```
├── scripts/
│   └── run_mind2web_with_agent_tars.py  # Main script
├── results/                             # Output directory (auto-created)
│   └── mind2web_agent_tars_results.json # Execution results
├── images/                              # Screenshots directory (auto-created)
│   └── *.png                            # Agent TARS generated screenshots
├── .gitignore                           # Git ignore configuration
├── README.md                            # English documentation
└── README_CN.md                         # Chinese documentation
```

## Features

- 🔄 Automatically loads Online Mind2Web dataset from HuggingFace
- 🎯 Formats `confirmed_task` and `website` from dataset as Agent TARS input
- 🐛 Supports debug mode for detailed execution process
- 📊 Automatically saves execution results to JSON file
- ⏱️ Supports timeout control and task range selection
- 🔍 Supports dry-run mode to preview tasks
- 🎨 Supports sample task mode (test without dataset)
- 🎯 Advanced task filtering by length, difficulty, and website
- 📝 Auto-generated filenames based on website names
- 📸 Automatic screenshot capture during task execution

## Installation

### 1. Basic Requirements

- **Agent TARS**: Ensure Agent TARS CLI is installed and configured
  - Tested with: `agent-tars/0.2.8 darwin-arm64 node-v22.17.0`
- **Python 3.7+**: Script requires Python environment

### 2. Install Python Dependencies

```bash
# Install HuggingFace datasets library (optional, only needed for real dataset)
pip install datasets

# Login to HuggingFace to access datasets (optional)
huggingface-cli login
```

## Usage

### Quick Start (Recommended)

```bash
# Clone and enter the repository
git clone <your-repo-url>
cd <repo-name>

# Test with sample tasks (no datasets installation needed)
python scripts/run_mind2web_with_agent_tars.py --use-sample --dry-run

# Execute one sample task
python scripts/run_mind2web_with_agent_tars.py --use-sample --max-tasks 1
```

### Basic Usage

```bash
# Execute first 2 test tasks (default)
python scripts/run_mind2web_with_agent_tars.py

# Execute first 10 tasks
python scripts/run_mind2web_with_agent_tars.py --max-tasks 10
```

### Advanced Usage

```bash
# Execute tasks in specified range
python scripts/run_mind2web_with_agent_tars.py --start 10 --end 20

# Use different dataset split
python scripts/run_mind2web_with_agent_tars.py --split train

# Set timeout (seconds)
python scripts/run_mind2web_with_agent_tars.py --timeout 600

# Disable debug mode (faster but less information)
python scripts/run_mind2web_with_agent_tars.py --no-debug

# Preview tasks without execution (dry-run)
python scripts/run_mind2web_with_agent_tars.py --dry-run --max-tasks 3

# Execute specific task by index with auto-generated filename
python scripts/run_mind2web_with_agent_tars.py --task-length-min 213 --task-length-max 237 --level hard --task-index 0 --auto-filename --timeout 600

# Execute specific task with filters and custom index
python scripts/run_mind2web_with_agent_tars.py --task-length-min 237 --task-length-max 253 --level hard --task-index 0 --auto-filename --timeout 600

# Filter tasks by website and show preview
python scripts/run_mind2web_with_agent_tars.py --website-filter booking --dry-run --preview 10
```

### Custom Output Location

```bash
# Specify result save location
python scripts/run_mind2web_with_agent_tars.py --output my_results/test_run.json
```

### Task Filtering and Selection

The script supports advanced task filtering and selection capabilities:

```bash
# Filter tasks by difficulty level
python scripts/run_mind2web_with_agent_tars.py --level hard --dry-run

# Filter tasks by length range
python scripts/run_mind2web_with_agent_tars.py --task-length-min 200 --task-length-max 300 --dry-run

# Filter tasks by website
python scripts/run_mind2web_with_agent_tars.py --website-filter amazon --dry-run

# Combine filters and execute specific task
python scripts/run_mind2web_with_agent_tars.py --level hard --task-length-min 237 --task-length-max 253 --task-index 1 --auto-filename

# Preview filtered results before execution
python scripts/run_mind2web_with_agent_tars.py --level hard --website-filter booking --preview 10 --dry-run
```

### Auto-Generated Filenames

When using `--auto-filename` flag with `--task-index`, the script automatically generates descriptive filenames:

```bash
# This will generate: ./results/mind2web_chase_results.json
python scripts/run_mind2web_with_agent_tars.py --task-index 0 --auto-filename

# This will generate: ./results/mind2web_booking_results.json  
python scripts/run_mind2web_with_agent_tars.py --task-index 1 --auto-filename
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--split` | `test` | Dataset split (train/test/validation) |
| `--start` | `0` | Starting task index |
| `--end` | - | Ending task index (uses max-tasks if not specified) |
| `--max-tasks` | `5` | Maximum number of tasks to execute |
| `--timeout` | `300` | Timeout for each task (seconds) |
| `--output` | `results/mind2web_agent_tars_results.json` | Result output file |
| `--no-debug` | `False` | Disable debug mode |
| `--dry-run` | `False` | Preview tasks only, don't execute |
| `--use-sample` | `False` | Use sample tasks instead of dataset |
| `--task-length-min` | - | Minimum task length filter |
| `--task-length-max` | - | Maximum task length filter |
| `--level` | - | Task difficulty level filter (easy/medium/hard) |
| `--website-filter` | - | Filter tasks by website (partial match) |
| `--preview` | `5` | Number of tasks to preview (default: 5) |
| `--task-index` | - | Run specific task by index (0-based, from filtered results) |
| `--auto-filename` | `False` | Auto-generate filename based on website name |

## Output Format

The script generates a JSON file containing detailed execution results for each task:

```json
[
  {
    "index": 0,
    "task_input": "Execute the following task on website https://www.amazon.com: Search for wireless headphones under $50",
    "confirmed_task": "Search for wireless headphones under $50",
    "website": "https://www.amazon.com",
    "timestamp": "2025-01-02 10:30:45",
    "success": true,
    "stdout": "Detailed Agent TARS execution log...",
    "stderr": "",
    "returncode": 0
  }
]
```

## Example Execution

### 1. Preview Sample Tasks

```bash
python scripts/run_mind2web_with_agent_tars.py --use-sample --dry-run
```

Example output:
```
Using sample tasks for demonstration...

Total tasks: 3
Will execute task range: 0 to 2 (3 tasks total)

=== DRY RUN MODE - Only showing tasks, not executing ===

Task 0:
  Website: https://www.amazon.com
  Task: Search for wireless headphones under $50
  Formatted input: Execute the following task on website https://www.amazon.com: Search for wireless headphones under $50

Task 1:
  Website: https://www.cnet.com
  Task: Find the latest iPhone reviews
  Formatted input: Execute the following task on website https://www.cnet.com: Find the latest iPhone reviews

Task 2:
  Website: https://weather.com
  Task: Look up weather forecast for New York
  Formatted input: Execute the following task on website https://weather.com: Look up weather forecast for New York
```

### 2. Execute Sample Task

```bash
python scripts/run_mind2web_with_agent_tars.py --use-sample --max-tasks 1
```

Example output:
```
================================================================================
Executing Agent TARS task:
Input: Execute the following task on website https://www.amazon.com: Search for wireless headphones under $50
Command: agent-tars run --input Execute the following task on website https://www.amazon.com: Search for wireless headphones under $50 --debug
================================================================================

[Detailed Agent TARS execution log...]

Task 1 execution result: ✅ Success

Results saved to: results/mind2web_agent_tars_results.json

================================================================================
Execution Summary:
Total tasks: 1
Successful tasks: 1
Failed tasks: 0
Success rate: 100.0%
================================================================================
```

## File Management and Git Configuration

### Generated Files

During execution, the script automatically creates:
- **`results/` directory**: Contains JSON result files with execution logs
- **`images/` directory**: Contains PNG screenshots captured by Agent TARS during task execution

### Git Ignore Configuration

The repository includes a comprehensive `.gitignore` file that excludes:
```
# Agent TARS generated files
images/                    # All screenshots (can be large)
results/                   # All result files (may contain sensitive data)
*.log                      # Log files

# Standard exclusions
node_modules/, __pycache__/, .env, etc.
```

**Important**: Only scripts, documentation, and configuration files are tracked in Git. All runtime-generated content (screenshots, results, logs) is automatically excluded from version control.

## Important Notes

1. **Script Location**: Main script is located in `scripts/` directory
2. **Execution Location**: Run commands from the repository root directory
3. **Agent TARS Configuration**: Ensure Agent TARS is properly configured and available in command line
4. **Network Connection**: Some tasks require access to external websites
5. **Execution Time**: Complex tasks may take considerable time, set appropriate timeout values
6. **Resource Usage**: Executing multiple tasks simultaneously consumes significant system resources
7. **Local Files**: Screenshots and results are saved locally but not pushed to GitHub

## Troubleshooting

### Dataset Loading Failed
```bash
# Re-login to HuggingFace
huggingface-cli login

# Or use sample task mode
python scripts/run_mind2web_with_agent_tars.py --use-sample
```

### Agent TARS Command Not Found
```bash
# Check if Agent TARS is installed
agent-tars --version

# If not installed, refer to Agent TARS documentation for installation
```

### Task Execution Timeout
```bash
# Increase timeout duration
python scripts/run_mind2web_with_agent_tars.py --timeout 600
```

### Permission Issues
```bash
# Ensure script has execution permissions
chmod +x scripts/run_mind2web_with_agent_tars.py
```

## Real-World Usage Examples

The following are tested commands that can be used directly:

```bash
# Execute the first task in 213-237 length range with hard difficulty
python scripts/run_mind2web_with_agent_tars.py --task-length-min 213 --task-length-max 237 --level hard --task-index 0 --auto-filename --timeout 600

# Execute the first task in 237-253 length range with hard difficulty  
python scripts/run_mind2web_with_agent_tars.py --task-length-min 237 --task-length-max 253 --level hard --task-index 0 --auto-filename --timeout 600
```

These commands will:
- Filter tasks by specified length range and difficulty
- Execute the first matching task (index 0)
- Auto-generate result filename based on website name
- Set 10-minute timeout
- Correctly display the user-selected task index (display issue fixed)

## Best Practices

1. **First Use**: Recommend starting with `--use-sample --dry-run` to familiarize with script functionality
2. **Batch Testing**: Start with small batches, gradually increase task numbers
3. **Result Analysis**: Regularly review generated JSON result files to analyze success rates and failure causes
4. **Performance Optimization**: Adjust timeout and concurrency based on system performance
5. **Task Selection**: Use filtering parameters and preview features to select appropriate tasks for execution
6. **File Management**: Use `--auto-filename` to automatically categorize result files by website

