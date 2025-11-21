#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件名: scripts/build_app.py
功能描述: 项目打包脚本，使用PyInstaller将应用打包成独立的可执行文件
主要函数:
  - clean_build(): 清理之前的构建文件
  - build_executable(): 执行打包过程
  - main(): 主函数
主要类: 无
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def get_project_root():
    """获取项目根目录"""
    return Path(__file__).parent.parent

def clean_build(project_root):
    """
    清理之前的构建文件
    
    Args:
        project_root: 项目根目录路径
    """
    print("正在清理之前的构建文件...")
    
    # 要清理的目录列表
    dirs_to_clean = [
        project_root / 'build',
        project_root / 'dist',
        project_root / '__pycache__',
    ]
    
    # 递归清理所有__pycache__目录
    for root, dirs, files in os.walk(project_root):
        if '__pycache__' in dirs:
            dirs_to_clean.append(Path(root) / '__pycache__')
    
    # 清理目录
    for dir_path in dirs_to_clean:
        if dir_path.exists():
            print(f"删除目录: {dir_path}")
            shutil.rmtree(dir_path, ignore_errors=True)
    
    # 清理.spec文件（除了我们的配置文件）
    for spec_file in project_root.glob('*.spec'):
        if spec_file.name != 'build_config.spec':
            print(f"删除spec文件: {spec_file}")
            spec_file.unlink()
    
    print("清理完成!")

def create_output_directories(project_root):
    """
    创建输出目录结构
    
    Args:
        project_root: 项目根目录路径
    """
    print("正在创建输出目录...")
    
    # 创建输出目录
    output_dir = project_root / 'dist' / 'Release'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"输出目录已创建: {output_dir}")
    return output_dir

def build_executable(project_root, output_dir):
    """
    执行打包过程
    
    Args:
        project_root: 项目根目录路径
        output_dir: 输出目录路径
        
    Returns:
        bool: 打包是否成功
    """
    print("开始打包应用程序...")
    
    # 切换到项目根目录
    original_cwd = os.getcwd()
    os.chdir(project_root)
    
    try:
        # 使用uv运行PyInstaller
        cmd = [
            'uv', 'run', 'pyinstaller',
            '--clean',
            '--noconfirm',
            'build_config.spec'
        ]
        
        print(f"执行命令: {' '.join(cmd)}")
        
        # 执行打包命令
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode != 0:
            print(f"打包失败! 错误信息:")
            print(result.stderr)
            return False
        
        print("打包成功!")
        print(result.stdout)
        
        # 移动可执行文件到输出目录
        exe_name = 'remove_spaces_tool.exe'
        source_exe = project_root / 'dist' / exe_name
        target_exe = output_dir / exe_name
        
        if source_exe.exists():
            shutil.move(str(source_exe), str(target_exe))
            print(f"可执行文件已移动到: {target_exe}")
        else:
            print(f"警告: 找不到生成的可执行文件 {source_exe}")
            return False
        
        # 创建必要的文件夹结构
        processed_docs_dir = output_dir / 'processed_documents'
        processed_docs_dir.mkdir(exist_ok=True)
        print(f"已创建文档输出目录: {processed_docs_dir}")
        
        return True
        
    except Exception as e:
        print(f"打包过程中发生错误: {e}")
        return False
    
    finally:
        # 恢复原始工作目录
        os.chdir(original_cwd)

def verify_build(output_dir):
    """
    验证构建结果
    
    Args:
        output_dir: 输出目录路径
        
    Returns:
        bool: 验证是否通过
    """
    print("正在验证构建结果...")
    
    exe_file = output_dir / 'remove_spaces_tool.exe'
    if not exe_file.exists():
        print("错误: 可执行文件不存在!")
        return False
    
    # 检查文件大小
    file_size = exe_file.stat().st_size / (1024 * 1024)  # MB
    print(f"可执行文件大小: {file_size:.2f} MB")
    
    # 检查必要目录
    processed_docs_dir = output_dir / 'processed_documents'
    if not processed_docs_dir.exists():
        print("警告: processed_documents目录不存在")
        processed_docs_dir.mkdir(exist_ok=True)
    
    print("构建验证通过!")
    return True

def cleanup_build_files(project_root):
    """
    清理所有过程文件，只保留exe可执行文件
    
    Args:
        project_root: 项目根目录路径
    """
    print("正在清理过程文件...")
    
    # 要清理的文件和目录
    items_to_clean = [
        project_root / 'build',           # PyInstaller构建目录
        project_root / 'build_config.spec',  # 配置文件
        project_root / 'version_info.txt',   # 版本信息文件
        project_root / '__pycache__',     # Python缓存目录
    ]
    
    # 递归清理所有__pycache__目录
    for root, dirs, files in os.walk(project_root):
        if '__pycache__' in dirs:
            items_to_clean.append(Path(root) / '__pycache__')
    
    # 清理项目中的其他缓存文件
    for pattern in ['*.pyc', '*.pyo']:
        for file_path in project_root.rglob(pattern):
            items_to_clean.append(file_path)
    
    # 执行清理
    for item in items_to_clean:
        try:
            if item.exists():
                if item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                    print(f"已删除目录: {item}")
                else:
                    item.unlink()
                    print(f"已删除文件: {item}")
        except Exception as e:
            print(f"删除 {item} 时出错: {e}")
    
    print("过程文件清理完成!")

def create_readme(output_dir):
    """
    创建使用说明文件
    
    Args:
        output_dir: 输出目录路径
    """
    readme_content = """# Word文档中英文空格清理工具

## 使用说明

1. 双击运行 `remove_spaces_tool.exe` 启动应用程序
2. 点击"打开Word文档"按钮选择要处理的.docx文件
3. 点击"处理文档"按钮开始清理中英文边界空格
4. 查看处理结果和统计信息
5. 点击"保存处理结果"将清理后的文档保存到processed_documents文件夹

## 功能特点

- 自动清理中英文边界的不必要空格
- 保持原文档格式不变
- 提供详细的处理统计信息
- 支持批量文本处理
- 直观的图形用户界面

## 注意事项

- 仅支持.docx格式的Word文档
- 处理后的文档会自动保存到processed_documents文件夹
- 建议在处理重要文档前先备份

## 技术支持

如有问题请联系技术支持。
"""
    
    readme_file = output_dir / 'README.md'
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"使用说明已创建: {readme_file}")

def main():
    """主函数"""
    print("=" * 50)
    print("Word文档中英文空格清理工具 - 打包脚本")
    print("=" * 50)
    
    # 获取项目根目录
    project_root = get_project_root()
    print(f"项目根目录: {project_root}")
    
    # 检查必要文件
    main_file = project_root / 'main.py'
    config_file = project_root / 'build_config.spec'
    
    if not main_file.exists():
        print(f"错误: 找不到主程序文件 {main_file}")
        return False
    
    if not config_file.exists():
        print(f"错误: 找不到配置文件 {config_file}")
        return False
    
    try:
        # 1. 清理之前的构建文件
        clean_build(project_root)
        
        # 2. 创建输出目录
        output_dir = create_output_directories(project_root)
        
        # 3. 执行打包
        if not build_executable(project_root, output_dir):
            print("打包失败!")
            return False
        
        # 4. 验证构建结果
        if not verify_build(output_dir):
            print("构建验证失败!")
            return False
        
        # 5. 创建使用说明
        create_readme(output_dir)
        
        # 6. 清理所有过程文件，只保留exe文件
        cleanup_build_files(project_root)
        
        print("=" * 50)
        print("打包完成!")
        print(f"输出目录: {output_dir}")
        print("可执行文件: remove_spaces_tool.exe")
        print("所有过程文件已清理，只保留最终可执行文件!")
        print("=" * 50)
        
        return True
        
    except KeyboardInterrupt:
        print("\n打包被用户中断")
        return False
    except Exception as e:
        print(f"打包过程中发生未预期的错误: {e}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)