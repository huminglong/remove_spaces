# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup
```bash
# Install dependencies with uv (recommended)
uv sync

# Traditional setup with pip
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Running the Application
```bash
# Start GUI application
uv run python main.py
# or
python main.py
```

### Testing
```bash
# Run all tests with custom test runner
python tests/run_tests.py

# Run pytest tests
pytest tests/test_processor.py -v

# Run specific test
pytest tests/test_processor.py::TestTextAnalyzer::test_chinese_char_detection -v

# Quick verification of core functionality
python verify_optimization.py
```

### Building and Packaging
```bash
# Build standalone executable
python scripts/build_app.py

# Manual PyInstaller build (alternative)
pyinstaller --clean --noconfirm --onefile --windowed main.py
```

## Architecture Overview

This is a Word document processing tool that removes spaces between Chinese and English text while preserving document formatting. The architecture follows a strict modular design with clear separation of concerns.

### Core Processing Pipeline

The main processing flow follows this sequence:
1. **Document Loading** (`DocumentProcessor`) - Loads .docx files while preserving all formatting
2. **Text Analysis** (`TextAnalyzer`) - Identifies Chinese-English boundaries using Unicode ranges
3. **Space Cleaning** (`SpaceCleaner`) - Removes spaces at language boundaries while preserving intra-language spacing
4. **Document Updating** (`DocumentProcessor`) - Updates text content without modifying formatting
5. **Result Saving** - Saves to new file in `processed_documents/` directory

### Key Architectural Principles

**Format Preservation**: The `DocumentProcessor` operates on the principle that only text content changes, while all Word document formatting (fonts, styles, colors, tables, images) remains completely intact.

**Boundary Detection**: `TextAnalyzer` uses Unicode character ranges (defined in `config/settings.py`) to precisely identify Chinese vs English characters, enabling accurate boundary detection.

**Configuration-Driven**: All magic numbers, paths, and character ranges are centralized in `config/settings.py` with nested configuration classes for different aspects (Window, UI, Paths, TextAnalysis, etc.).

### Module Dependencies

- **src/document_processor.py** - Core document handling, depends on python-docx, exceptions, logging
- **src/text_analyzer.py** - Character analysis, depends only on config/settings
- **src/space_cleaner.py** - Text processing logic, depends on text_analyzer
- **src/exceptions.py** - Custom exception hierarchy for precise error handling
- **src/logger_config.py** - Structured logging configuration
- **gui/main_window.py** - PyQt5-based GUI, orchestrates all modules
- **config/settings.py** - Centralized configuration, no dependencies

### Exception Handling Strategy

The project uses a hierarchical exception structure:
- `DocumentProcessorError` base class with specific subclasses for load/save/update failures
- `TextCleanerError` for text processing issues
- All exceptions are logged with context information for debugging

### Testing Strategy

Tests focus on core functionality verification:
- Text analysis accuracy (character detection, boundary finding)
- Space cleaning logic (basic cases, edge cases, batch processing)
- The custom test runner (`tests/run_tests.py`) provides quick functionality verification
- pytest is used for more granular unit testing

### Build System

The project uses uv for modern Python dependency management but maintains pip compatibility. The build script (`scripts/build_app.py`) handles PyInstaller packaging with automatic cleanup and output directory structure creation.

### Important Implementation Details

- **Unicode Ranges**: Chinese character detection uses ranges from settings, not hardcoded values
- **Context Managers**: `DocumentProcessor` supports `with` statement for resource management
- **Path Handling**: Uses `pathlib.Path` for cross-platform compatibility
- **Logging**: Structured logging with different levels for development vs production
- **GUI Thread Safety**: All document processing happens in background threads to keep UI responsive