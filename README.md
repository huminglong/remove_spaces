# Word文档中英文空格处理工具

## 项目简介

这是一个用于检测并去除Word文档中英文与中文文本之间多余空格的工具。该工具能够精准识别文档中中文与英文之间的空格，并仅移除这些特定位置的空格，同时严格保留英文单词之间的正常空格。

## 功能特点

- ✅ 精准识别中英文边界
- ✅ 仅去除中英文之间的多余空格
- ✅ 保留英文单词间的正常空格
- ✅ **严格保持文档格式不变** - 字体、字号、颜色、样式等所有格式信息完全保留
- ✅ **保持文档结构完整** - 段落、表格、图片等非文字元素保持不变
- ✅ 用户友好的图形界面
- ✅ 实时文本对比显示
- ✅ 详细的处理统计信息
- ✅ **现代化项目管理** - 使用uv进行依赖管理和环境配置

## 技术栈

- **Python 3.12** (项目当前版本)
- **uv** - 现代Python包管理器，比pip快10-100倍
- python-docx: Word文档解析和处理
- PyQt5: 图形用户界面
- pytest: 单元测试框架
- PyInstaller: 应用打包工具

## 安装

### 方法一：使用uv（推荐）

```bash
# 安装uv（如果尚未安装）
pip install uv

# 克隆项目
git clone <repository-url>
cd remove_spaces

# 初始化uv项目并安装依赖
uv init --name remove_spaces
uv add -r requirements.txt

# 运行程序
uv run python main.py
```

### 方法二：传统方式

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行程序
python main.py
```

## 使用方法

1. **启动程序**：`python main.py`
2. **选择文档**：点击"打开Word文档"按钮选择要处理的Word文档
3. **查看原始内容**：系统自动显示文档的原始文本内容
4. **处理文档**：点击"处理文档"开始清理空格，系统会显示处理进度
5. **查看结果**：处理完成后，右侧会显示处理后的文本对比
6. **保存结果**：点击"保存结果"将处理后的文档保存到新文件

### 使用示例

**处理前**：`这是一个 test 文档 包含 machine learning 机器学习 内容`
**处理后**：`这是一个test文档包含machine learning机器学习内容`

- ✅ 移除了中英文之间的空格：`test → 文档`
- ✅ 移除了中英文之间的空格：`learning → 机器学习`  
- ✅ 保留了英文单词间的空格：`machine learning`

## 项目结构

```text
remove_spaces/
├── main.py                    # 主程序入口
├── requirements.txt           # 依赖包列表
├── .gitignore                # Git忽略文件
├── src/                       # 核心源码目录
│   ├── __init__.py
│   ├── document_processor.py  # 文档处理核心模块（保持格式不变）
│   ├── text_analyzer.py       # 文本分析和边界检测模块
│   └── space_cleaner.py       # 空格清理和处理模块
├── gui/                       # 图形界面目录
│   ├── __init__.py
│   └── main_window.py         # 主窗口界面和交互逻辑
├── tests/                     # 测试目录
│   ├── __init__.py
│   ├── run_tests.py          # 测试运行脚本
│   └── test_processor.py     # 单元测试
├── README.md                  # 项目说明文档
└── 实施文档.md               # 详细技术实施文档
```

## 核心模块详细说明

## 打包成 Windows 可执行文件 (.exe)

如果你想把本项目打包成独立的 Windows 可执行文件（exe），可以使用 PyInstaller。仓库里已经包含一个方便的 PowerShell 打包脚本 `./scripts/build_exe.ps1`，脚本会自动激活存放在项目根目录的虚拟环境 `.venv`，并用 PyInstaller 进行打包。

推荐步骤（在 Windows PowerShell 中）：

```powershell
# 进入项目根目录
cd \path\to\remove_spaces

# 创建并激活虚拟环境（如果尚未创建）
python -m venv .venv
. .venv\Scripts\Activate.ps1

# 安装项目运行时依赖
pip install -r requirements.txt

# 安装开发 / 打包工具（包含 pyinstaller）
pip install -r requirements-dev.txt

# 使用脚本打包为单文件 GUI exe（默认不显示控制台）
./scripts/build_exe.ps1 -OneFile -NoConsole -Name RemoveSpaces

# 打包完成后生成文件位于 dist\RemoveSpaces 或 dist\RemoveSpaces.exe（单文件）
```

常用参数：

- `-OneFile`：生成单个 exe 文件（--onefile）
- `-NoConsole`：GUI 程序通常不需要控制台（--noconsole）
- `-Entry`：指定入口文件，默认 `main.py`
- `-Name`：输出文件名，默认 `RemoveSpaces`

注意事项：

- PyInstaller 会将运行时依赖打包进 exe，生成的文件可能比较大。
- 确保 `.venv` 中安装的依赖与 `requirements.txt` 保持一致，打包时使用相同的 Python 版本（推荐 Python 3.11）。
- 如果使用 PyQt5 GUI，PyInstaller 会自动收集大多数 Qt 运行时文件；如遇到资源缺失请查看 PyInstaller 的日志并根据提示添加 `--add-data` 或编写 hooks。

### 📁 src/ 核心模块

#### `document_processor.py` - 文档处理器

**功能职责**：

- 加载和解析Word文档(.docx格式)
- 提取文档结构信息（段落、表格、文本片段）
- 保持文档格式完整性（字体、颜色、样式等）
- 更新处理后的文本内容到文档中
- 保存处理结果到新文件

**关键方法**：

- `load_document()`: 加载Word文档
- `get_all_text()`: 提取所有可处理文本
- `update_text_content()`: 更新文档文本内容
- `save_document()`: 保存文档到指定路径

#### `text_analyzer.py` - 文本分析器

**功能职责**：

- 识别中文和英文字符
- 检测中英文边界位置
- 分析文本语言类型分布
- 分割文本为语言片段

**关键方法**：

- `is_chinese_char()`: 判断字符是否为中文
- `is_english_char()`: 判断字符是否为英文
- `find_chinese_english_boundaries()`: 检测中英文边界
- `analyze_text()`: 分析文本统计信息

#### `space_cleaner.py` - 空格清理器

**功能职责**：

- 执行智能空格清理逻辑
- 移除中英文边界处的多余空格
- 保留英文单词间的正常空格
- 提供处理统计信息

**关键方法**：

- `clean_text()`: 清理单个文本的空格
- `clean_multiple_texts()`: 批量处理多个文本
- `get_processing_statistics()`: 获取处理统计数据

### 🖥️ gui/ 界面模块

#### `main_window.py` - 主窗口界面

**功能职责**：

- 提供用户友好的图形界面
- 处理用户交互（文件选择、处理控制）
- 显示处理进度和结果对比
- 展示详细的处理统计信息

### 🧪 tests/ 测试模块

#### `test_processor.py` - 单元测试

**测试覆盖**：

- 文本分析功能测试
- 空格清理逻辑测试
- 文档处理流程测试
- 边界情况处理测试

## 详细使用示例

### 基本使用流程

```python
from src.document_processor import DocumentProcessor
from src.space_cleaner import SpaceCleaner

# 1. 初始化处理器
processor = DocumentProcessor()
cleaner = SpaceCleaner()

# 2. 加载文档
if processor.load_document('example.docx'):
    # 3. 获取所有文本内容
    texts = processor.get_all_text()

    # 4. 处理文本
    cleaned_texts = []
    for text in texts:
        result = cleaner.clean_text(text)
        cleaned_texts.append(result['cleaned_text'])

    # 5. 更新文档内容
    processor.update_text_content(cleaned_texts)

    # 6. 保存结果
    processor.save_document('cleaned_example.docx')
```

### 命令行使用

```bash
# 启动图形界面
python main.py

# 运行测试
python tests/run_tests.py
```

### API使用示例

#### 文本分析

```python
from src.text_analyzer import TextAnalyzer

analyzer = TextAnalyzer()

# 分析文本
text = "这是一个test文本，包含machine learning内容"
result = analyzer.analyze_text(text)

print(f"中文字符数: {result['chinese_chars']}")
print(f"英文字符数: {result['english_chars']}")
print(f"空格数: {result['spaces']}")

# 检测边界
boundaries = analyzer.find_chinese_english_boundaries(text)
print(f"检测到 {len(boundaries)} 个中英文边界")
```

#### 空格清理

```python
from src.space_cleaner import SpaceCleaner

cleaner = SpaceCleaner()

# 清理单个文本
text = "你好 hello world 世界"
result = cleaner.clean_text(text)

print(f"原始文本: {result['original_text']}")
print(f"清理后: {result['cleaned_text']}")
print(f"移除空格数: {result['spaces_removed']}")

# 批量处理
texts = ["你好 hello", "world 世界", "machine learning"]
results = cleaner.clean_multiple_texts(texts)

# 获取统计信息
stats = cleaner.get_processing_statistics(results)
print(f"处理文本总数: {stats['total_texts']}")
print(f"变更率: {stats['change_rate']}%")
```

### 架构图

```mermaid
graph TD
    GUI[用户界面层<br/>GUI Layer] --> Logic[业务逻辑层<br/>Business Logic Layer]
    Logic --> Data[数据层<br/>Data Layer]

    GUI --> MainWindow[主窗口<br/>Main Window]
    GUI --> ProgressBar[进度显示<br/>Progress Bar]
    GUI --> DetailsTable[详细信息表格<br/>Details Table]

    Logic --> DocProcessor[文档处理器<br/>Document Processor]
    Logic --> TextAnalyzer[文本分析器<br/>Text Analyzer]
    Logic --> SpaceCleaner[空格清理器<br/>Space Cleaner]

    DocProcessor --> SharedUtils[共享工具类<br/>Shared Utilities]
    TextAnalyzer --> SharedUtils
    SpaceCleaner --> SharedUtils

    Data --> WordDoc[Word文档<br/>.docx Files]
    Data --> ProcessedDoc[处理结果<br/>Processed Documents]
    Data --> TempFiles[临时文件<br/>Temporary Files]

    classDef layerClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef componentClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef dataClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px

    class GUI,Logic,Data layerClass
    class MainWindow,ProgressBar,DetailsTable,DocProcessor,TextAnalyzer,SpaceCleaner,SharedUtils componentClass
    class WordDoc,ProcessedDoc,TempFiles dataClass
```

## 核心特性详解

### 🎯 精准的中英文边界识别

- 使用正则表达式和字符编码检测
- 准确识别中文、英文、数字、标点符号
- 智能判断真正的中英文边界位置

### 🔄 格式保持机制

- **零格式丢失**：所有字体、字号、颜色、粗体、斜体、下划线等格式完全保留
- **结构完整性**：段落、表格、页眉页脚等文档结构保持不变
- **非文字元素**：图片、图表、形状等非文字内容完全不受影响

### 📊 详细的处理统计

- 总文本段落数量
- 发生变更的文本数量
- 移除的空格总数
- 变更率百分比
- 每个变更的详细说明

## 测试

```bash
# 运行所有测试
python tests/run_tests.py

# 运行pytest测试
pytest tests/test_processor.py -v

# 运行特定测试
pytest tests/test_processor.py::TestTextAnalyzer::test_chinese_char_detection -v
```

## 故障排除

### 常见问题

1. **依赖安装失败**

   ```bash
   # 升级pip
   python -m pip install --upgrade pip
   
   # 重新安装依赖
   pip install -r requirements.txt --force-reinstall
   ```

2. **程序无法启动**
   - 检查Python版本是否为3.11（实际测试版本）
   - 确认已安装PyQt5：`pip install PyQt5`
   - 在Windows上可能需要安装Microsoft Visual C++ 运行库

3. **文档处理失败**
   - 确认文档是`.docx`格式（不支持`.doc`）
   - 检查文档是否损坏
   - 确认文档没有被其他程序占用

## 开发环境

- **Python版本**: 3.11 (实际测试版本)
- **操作系统**: Windows/Linux/MacOS
- **IDE支持**: PyPy、VS Code等

## 贡献指南

1. Fork项目
2. 创建特性分支：`git checkout -b feature-name`
3. 提交修改：`git commit -am 'Add some feature'`
4. 推送到分支：`git push origin feature-name`
5. 提交Pull Request

## 注意事项

- 仅支持 `.docx` 格式的Word文档
- 处理过程中原文档不会被修改，结果保存到新文件
- 建议在处理重要文档前先进行备份
- 程序会自动在项目目录下创建`processed_documents`文件夹保存处理结果

## 更新日志

- **v1.0**: 基础功能实现，支持中英文边界空格清理
- **v2.0**: 重构文档处理器，实现严格的格式保持机制
- **v2.1**: 优化用户界面，添加处理进度显示和详细信息表格
