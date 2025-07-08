# Mind2Web + Agent TARS 自动化测试脚本

这个脚本用于从 Online Mind2Web 数据集加载任务，并使用 Agent TARS 执行这些任务。

## 文件位置

仓库结构：

```
├── scripts/
│   └── run_mind2web_with_agent_tars.py  # 主脚本
├── results/                             # 结果输出目录（自动创建）
│   └── mind2web_agent_tars_results.json # 执行结果
├── images/                              # 截图目录（自动创建）
│   └── *.png                            # Agent TARS 生成的截图
├── .gitignore                           # Git 忽略文件配置
├── README.md                            # 英文说明文档
└── README_CN.md                         # 中文说明文档（本文档）
```

## 功能特性

- 🔄 自动从 HuggingFace 加载 Online Mind2Web 数据集
- 🎯 将数据集中的 `confirmed_task` 和 `website` 格式化为 Agent TARS 输入
- 🐛 支持 debug 模式查看详细执行过程
- 📊 自动保存执行结果到 JSON 文件
- ⏱️ 支持超时控制和任务范围选择
- 🔍 支持 dry-run 模式预览任务
- 🎨 支持示例任务模式（无需数据集即可测试）
- 🎯 支持按长度、难度和网站进行高级任务筛选
- 📝 根据网站名自动生成文件名
- 📸 任务执行过程中自动截图

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

# 执行特定索引的任务并自动生成文件名
python scripts/run_mind2web_with_agent_tars.py --task-length-min 213 --task-length-max 237 --level hard --task-index 0 --auto-filename --timeout 600

# 执行指定范围和难度的特定任务
python scripts/run_mind2web_with_agent_tars.py --task-length-min 237 --task-length-max 253 --level hard --task-index 0 --auto-filename --timeout 600

# 按网站筛选任务并预览
python scripts/run_mind2web_with_agent_tars.py --website-filter booking --dry-run --preview 10
```

### 自定义输出位置

```bash
# 指定结果保存位置
python scripts/run_mind2web_with_agent_tars.py --output my_results/test_run.json
```

### 任务筛选和选择

脚本支持高级任务筛选和选择功能：

```bash
# 按难度级别筛选任务
python scripts/run_mind2web_with_agent_tars.py --level hard --dry-run

# 按长度范围筛选任务
python scripts/run_mind2web_with_agent_tars.py --task-length-min 200 --task-length-max 300 --dry-run

# 按网站筛选任务
python scripts/run_mind2web_with_agent_tars.py --website-filter amazon --dry-run

# 组合筛选条件并执行特定任务
python scripts/run_mind2web_with_agent_tars.py --level hard --task-length-min 237 --task-length-max 253 --task-index 1 --auto-filename

# 执行前预览筛选结果
python scripts/run_mind2web_with_agent_tars.py --level hard --website-filter booking --preview 10 --dry-run
```

### 自动生成文件名

使用 `--auto-filename` 参数配合 `--task-index` 时，脚本会自动生成描述性文件名：

```bash
# 这将生成：./results/mind2web_chase_results.json
python scripts/run_mind2web_with_agent_tars.py --task-index 0 --auto-filename

# 这将生成：./results/mind2web_booking_results.json  
python scripts/run_mind2web_with_agent_tars.py --task-index 1 --auto-filename
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
| `--task-length-min` | - | 任务长度最小值筛选 |
| `--task-length-max` | - | 任务长度最大值筛选 |
| `--level` | - | 任务难度级别筛选（easy/medium/hard） |
| `--website-filter` | - | 按网站筛选任务（部分匹配） |
| `--preview` | `5` | 预览任务数量（默认：5） |
| `--task-index` | - | 执行特定索引的任务（基于筛选结果，从0开始） |
| `--auto-filename` | `False` | 根据网站名自动生成文件名 |

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

## 文件管理和 Git 配置

### 生成的文件

脚本执行过程中会自动创建：
- **`results/` 目录**: 包含带有执行日志的 JSON 结果文件
- **`images/` 目录**: 包含 Agent TARS 在任务执行过程中捕获的 PNG 截图

### Git 忽略配置

仓库包含完整的 `.gitignore` 文件，排除以下内容：
```
# Agent TARS 生成的文件
images/                    # 所有截图（可能很大）
results/                   # 所有结果文件（可能包含敏感数据）
*.log                      # 日志文件

# 标准排除项
node_modules/, __pycache__/, .env 等
```

**重要**: 只有脚本、文档和配置文件会被 Git 跟踪。所有运行时生成的内容（截图、结果、日志）都会自动从版本控制中排除。

## 注意事项

1. **脚本位置**: 主脚本位于 `scripts/` 目录下
2. **执行位置**: 建议在仓库根目录下执行脚本
3. **Agent TARS 配置**: 确保 Agent TARS 已正确配置并可在命令行使用
4. **网络连接**: 某些任务需要访问外部网站
5. **执行时间**: 复杂任务可能需要较长时间，建议设置合适的超时值
6. **资源占用**: 同时执行多个任务会消耗较多系统资源
7. **本地文件**: 截图和结果保存在本地，但不会推送到 GitHub

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

## 实际使用示例

以下是经过测试的实际命令，可以直接使用：

```bash
# 执行长度在213-237范围内的困难任务的第1个
python scripts/run_mind2web_with_agent_tars.py --task-length-min 213 --task-length-max 237 --level hard --task-index 0 --auto-filename --timeout 600

# 执行长度在237-253范围内的困难任务的第1个
python scripts/run_mind2web_with_agent_tars.py --task-length-min 237 --task-length-max 253 --level hard --task-index 0 --auto-filename --timeout 600
```

这些命令会：
- 筛选指定长度范围和难度的任务
- 执行第一个匹配的任务（索引0）
- 自动根据网站名生成结果文件名
- 设置10分钟超时时间
- 正确显示用户选择的任务索引（已修复显示问题）

## 最佳实践

1. **首次使用**: 建议先用 `--use-sample --dry-run` 熟悉脚本功能
2. **批量测试**: 从小批量任务开始，逐步增加任务数量
3. **结果分析**: 定期查看生成的 JSON 结果文件，分析成功率和失败原因
4. **性能优化**: 根据系统性能调整超时时间和并发数量
5. **任务选择**: 使用筛选参数和预览功能选择合适的任务执行
6. **文件管理**: 使用 `--auto-filename` 让结果文件自动按网站分类保存 