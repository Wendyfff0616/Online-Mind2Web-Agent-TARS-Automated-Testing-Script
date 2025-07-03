# Online Mind2Web + Agent TARS Automated Testing Script

**Languages:** [English](#english-version) | [中文](#中文版本)

---

## English Version

This script loads tasks from the Online Mind2Web dataset and executes them using Agent TARS.

## File Structure

The repository structure:

```
├── scripts/
│   └── run_mind2web_with_agent_tars.py  # Main script
├── results/                             # Output directory (auto-created)
│   └── mind2web_agent_tars_results.json # Execution results
└── README.md                            # This documentation
```

## Features

- 🔄 Automatically loads Online Mind2Web dataset from HuggingFace
- 🎯 Formats `confirmed_task` and `website` from dataset as Agent TARS input
- 🐛 Supports debug mode for detailed execution process
- 📊 Automatically saves execution results to JSON file
- ⏱️ Supports timeout control and task range selection
- 🔍 Supports dry-run mode to preview tasks
- 🎨 Supports sample task mode (test without dataset)

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
```

### Custom Output Location

```bash
# Specify result save location
python scripts/run_mind2web_with_agent_tars.py --output my_results/test_run.json
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

## Important Notes

1. **Script Location**: Main script is located in `scripts/` directory
2. **Execution Location**: Run commands from the repository root directory
3. **Agent TARS Configuration**: Ensure Agent TARS is properly configured and available in command line
4. **Network Connection**: Some tasks require access to external websites
5. **Execution Time**: Complex tasks may take considerable time, set appropriate timeout values
6. **Resource Usage**: Executing multiple tasks simultaneously consumes significant system resources

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

## Best Practices

1. **First Use**: Recommend starting with `--use-sample --dry-run` to familiarize with script functionality
2. **Batch Testing**: Start with small batches, gradually increase task numbers
3. **Result Analysis**: Regularly review generated JSON result files to analyze success rates and failure causes
4. **Performance Optimization**: Adjust timeout and concurrency based on system performance

---

## 中文版本

# Mind2Web + Agent TARS 自动化测试脚本

这个脚本用于从 Online Mind2Web 数据集加载任务，并使用 Agent TARS 执行这些任务。

## 文件位置

仓库结构：

```
├── scripts/
│   └── run_mind2web_with_agent_tars.py  # 主脚本
├── results/                             # 结果输出目录（自动创建）
│   └── mind2web_agent_tars_results.json # 执行结果
└── README.md                            # 本说明文档
```

## 功能特性

- 🔄 自动从 HuggingFace 加载 Online Mind2Web 数据集
- 🎯 将数据集中的 `confirmed_task` 和 `website` 格式化为 Agent TARS 输入
- 🐛 支持 debug 模式查看详细执行过程
- 📊 自动保存执行结果到 JSON 文件
- ⏱️ 支持超时控制和任务范围选择
- 🔍 支持 dry-run 模式预览任务
- 🎨 支持示例任务模式（无需数据集即可测试）

## 安装依赖

### 1. 基础环境要求

- **Agent TARS**: 确保已安装并配置了 Agent TARS CLI
  - 测试版本: `agent-tars/0.2.8 darwin-arm64 node-v22.17.0`
- **Python 3.7+**: 脚本需要 Python 环境

### 2. 安装 Python 依赖

```bash
# 安装 HuggingFace datasets 库（可选，仅在使用真实数据集时需要）
pip install datasets

# 登录 HuggingFace 以访问数据集（可选）
huggingface-cli login
```

## 使用方法

### 快速开始（推荐）

```bash
# 克隆并进入仓库
git clone <your-repo-url>
cd <repo-name>

# 使用示例任务进行测试（无需安装 datasets）
python scripts/run_mind2web_with_agent_tars.py --use-sample --dry-run

# 执行一个示例任务
python scripts/run_mind2web_with_agent_tars.py --use-sample --max-tasks 1
```

### 基础用法

```bash
# 执行前 2 个测试任务（默认）
python scripts/run_mind2web_with_agent_tars.py

# 执行前 10 个任务
python scripts/run_mind2web_with_agent_tars.py --max-tasks 10
```

### 高级用法

```bash
# 执行指定范围的任务
python scripts/run_mind2web_with_agent_tars.py --start 10 --end 20

# 使用不同的数据集分割
python scripts/run_mind2web_with_agent_tars.py --split train

# 设置超时时间（秒）
python scripts/run_mind2web_with_agent_tars.py --timeout 600

# 禁用 debug 模式（更快但信息较少）
python scripts/run_mind2web_with_agent_tars.py --no-debug

# 预览任务而不执行（dry-run）
python scripts/run_mind2web_with_agent_tars.py --dry-run --max-tasks 3
```

### 自定义输出位置

```bash
# 指定结果保存位置
python scripts/run_mind2web_with_agent_tars.py --output my_results/test_run.json
```

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--split` | `test` | 数据集分割（train/test/validation） |
| `--start` | `0` | 起始任务索引 |
| `--end` | - | 结束任务索引（不指定则使用 max-tasks） |
| `--max-tasks` | `5` | 最大执行任务数 |
| `--timeout` | `300` | 每个任务的超时时间（秒） |
| `--output` | `results/mind2web_agent_tars_results.json` | 结果输出文件 |
| `--no-debug` | `False` | 禁用 debug 模式 |
| `--dry-run` | `False` | 仅预览任务，不执行 |
| `--use-sample` | `False` | 使用示例任务而非数据集 |

## 输出格式

脚本会生成一个 JSON 文件，包含每个任务的详细执行结果：

```json
[
  {
    "index": 0,
    "task_input": "在网站 https://www.amazon.com 上执行以下任务: Search for wireless headphones under $50",
    "confirmed_task": "Search for wireless headphones under $50",
    "website": "https://www.amazon.com",
    "timestamp": "2025-01-02 10:30:45",
    "success": true,
    "stdout": "详细的 Agent TARS 执行日志...",
    "stderr": "",
    "returncode": 0
  }
]
```

## 示例执行

### 1. 预览示例任务

```bash
python scripts/run_mind2web_with_agent_tars.py --use-sample --dry-run
```

输出示例：
```
Using sample tasks for demonstration...

总任务数: 3
将执行任务范围: 0 到 2 (共 3 个任务)

=== DRY RUN 模式 - 仅显示任务，不执行 ===

任务 0:
  网站: https://www.amazon.com
  任务: Search for wireless headphones under $50
  格式化输入: 在网站 https://www.amazon.com 上执行以下任务: Search for wireless headphones under $50

任务 1:
  网站: https://www.cnet.com
  任务: Find the latest iPhone reviews
  格式化输入: 在网站 https://www.cnet.com 上执行以下任务: Find the latest iPhone reviews

任务 2:
  网站: https://weather.com
  任务: Look up weather forecast for New York
  格式化输入: 在网站 https://weather.com 上执行以下任务: Look up weather forecast for New York
```

### 2. 执行示例任务

```bash
python scripts/run_mind2web_with_agent_tars.py --use-sample --max-tasks 1
```

输出示例：
```
================================================================================
执行 Agent TARS 任务:
输入: 在网站 https://www.amazon.com 上执行以下任务: Search for wireless headphones under $50
命令: agent-tars run --input 在网站 https://www.amazon.com 上执行以下任务: Search for wireless headphones under $50 --debug
================================================================================

[详细的 Agent TARS 执行日志...]

任务 1 执行结果: ✅ 成功

结果已保存到: results/mind2web_agent_tars_results.json

================================================================================
执行总结:
总任务数: 1
成功任务: 1
失败任务: 0
成功率: 100.0%
================================================================================
```

## 注意事项

1. **脚本位置**: 主脚本位于 `scripts/` 目录下
2. **执行位置**: 建议在仓库根目录下执行脚本
3. **Agent TARS 配置**: 确保 Agent TARS 已正确配置并可在命令行使用
4. **网络连接**: 某些任务需要访问外部网站
5. **执行时间**: 复杂任务可能需要较长时间，建议设置合适的超时值
6. **资源占用**: 同时执行多个任务会消耗较多系统资源

## 故障排除

### 数据集加载失败
```bash
# 重新登录 HuggingFace
huggingface-cli login

# 或者使用示例任务模式
python scripts/run_mind2web_with_agent_tars.py --use-sample
```

### Agent TARS 命令不存在
```bash
# 检查 Agent TARS 是否已安装
agent-tars --version

# 如果未安装，参考 Agent TARS 文档进行安装
```

### 任务执行超时
```bash
# 增加超时时间
python scripts/run_mind2web_with_agent_tars.py --timeout 600
```

### 权限问题
```bash
# 确保脚本有执行权限
chmod +x scripts/run_mind2web_with_agent_tars.py
```

## 最佳实践

1. **首次使用**: 建议先用 `--use-sample --dry-run` 熟悉脚本功能
2. **批量测试**: 从小批量任务开始，逐步增加任务数量
3. **结果分析**: 定期查看生成的 JSON 结果文件，分析成功率和失败原因
4. **性能优化**: 根据系统性能调整超时时间和并发数量 