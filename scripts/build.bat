@echo off
echo ========================================
echo Word Document Space Cleaner - Build Script
echo ========================================
echo.

REM Check if uv is installed
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: uv command not found, please install uv first
    echo Install command: pip install uv
    pause
    exit /b 1
)

REM Switch to project root directory
cd /d "%~dp0.."

echo Current directory: %CD%
echo.

REM Run build script
echo Starting application packaging...
uv run python scripts\build_app.py

echo.
if %errorlevel% equ 0 (
    echo ========================================
    echo Build completed successfully!
    echo ========================================
    echo Output directory: %CD%\dist\Release
    echo Executable file: remove_spaces_tool.exe
    echo ========================================
) else (
    echo ========================================
    echo Build failed!
    echo ========================================
)

echo.
pause