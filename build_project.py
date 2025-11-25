#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
24时计时法教学系统 - 跨平台打包工具

打包说明：
- 在 Windows 上运行此脚本会：
  1. 生成 Windows 版本（可直接使用）
  2. 准备 macOS 打包工具包（需在 macOS 系统上打包）
  
注意：由于 PyInstaller 不支持交叉编译，macOS 版本必须在 macOS 系统上打包
      但前端文件已经在 Windows 上构建完成，macOS 打包时无需重新构建前端
"""

import os
import shutil
import subprocess
import sys
import platform

# 检测操作系统
IS_WINDOWS = platform.system() == 'Windows'
IS_MAC = platform.system() == 'Darwin'
IS_LINUX = platform.system() == 'Linux'

def get_executable_name():
    """根据操作系统返回可执行文件名"""
    if IS_WINDOWS:
        return 'TimeTeachingSystem.exe'
    elif IS_MAC or IS_LINUX:
        return 'TimeTeachingSystem'
    else:
        return 'TimeTeachingSystem'

def get_platform_name():
    """返回平台名称"""
    if IS_WINDOWS:
        return 'Windows'
    elif IS_MAC:
        return 'macOS'
    elif IS_LINUX:
        return 'Linux'
    else:
        return platform.system()

def run_command(command, cwd=None, check=True):
    """执行命令并处理错误"""
    print(f"\n执行命令: {command}")
    if cwd:
        print(f"工作目录: {cwd}")
    result = subprocess.run(command, shell=True, cwd=cwd)
    if check and result.returncode != 0:
        print(f"❌ 命令执行失败: {command}")
        print(f"返回码: {result.returncode}")
        sys.exit(1)
    return result

def check_requirements():
    """检查必要的工具是否安装"""
    print("\n=== 检查环境 ===")
    print(f"当前操作系统: {get_platform_name()} ({platform.machine()})")
    
    if IS_WINDOWS:
        print("\n📌 打包策略:")
        print("   1. 生成 Windows 版本（可直接使用）")
        print("   2. 准备 macOS 打包工具包（需在 macOS 系统上打包）")
        print("   注意: 由于 PyInstaller 不支持交叉编译，macOS 版本需要在 macOS 系统上打包")
        print("         但前端文件已构建完成，macOS 打包只需运行 Python 打包即可\n")
    
    # 检查 Node.js
    try:
        result = subprocess.run('node --version', shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Node.js 已安装: {result.stdout.strip()}")
        else:
            print("❌ Node.js 未安装，请先安装 Node.js")
            print("   下载地址: https://nodejs.org/")
            sys.exit(1)
    except:
        print("❌ 无法检查 Node.js，请确保已安装")
        sys.exit(1)
    
    # 检查 npm
    try:
        result = subprocess.run('npm --version', shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ npm 已安装: {result.stdout.strip()}")
        else:
            print("❌ npm 未安装")
            sys.exit(1)
    except:
        print("❌ 无法检查 npm")
        sys.exit(1)
    
    # 检查 Python
    print(f"✓ Python 版本: {sys.version.split()[0]}")
    
    # 检查 PyInstaller
    try:
        result = subprocess.run('pyinstaller --version', shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ PyInstaller 已安装: {result.stdout.strip()}")
        else:
            print("⚠ PyInstaller 未安装，将在后续步骤中自动安装")
    except:
        print("⚠ PyInstaller 未安装，将在后续步骤中自动安装")

def build():
    """主构建函数"""
    print("\n" + "="*60)
    print("24时计时法教学系统 - 跨平台打包工具")
    print("="*60)
    
    # 获取路径（使用跨平台路径处理）
    root_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.join(root_dir, 'frontend')
    backend_dir = os.path.join(root_dir, 'backend')
    dist_dir = os.path.join(frontend_dir, 'dist')
    backend_web_dir = os.path.join(backend_dir, 'web')
    build_output_dir = os.path.join(root_dir, 'release')
    
    # 检查环境
    check_requirements()
    
    print("\n=== 1. 构建前端 (Vue) ===")
    # 检查 node_modules
    if not os.path.exists(os.path.join(frontend_dir, 'node_modules')):
        print("正在安装前端依赖...")
        run_command('npm install', cwd=frontend_dir)
    else:
        print("前端依赖已存在，跳过安装")
    
    print("正在编译前端静态文件...")
    run_command('npm run build', cwd=frontend_dir)
    
    # 检查构建结果
    if not os.path.exists(dist_dir) or not os.listdir(dist_dir):
        print("❌ 前端构建失败，dist 目录为空")
        sys.exit(1)
    print("✓ 前端构建成功")
    
    print("\n=== 2. 准备后端资源 ===")
    # 复制构建好的前端文件到后端目录
    if os.path.exists(backend_web_dir):
        print(f"清理旧的 web 目录: {backend_web_dir}")
        shutil.rmtree(backend_web_dir)
    
    print(f"正在复制前端文件: {dist_dir} -> {backend_web_dir}")
    shutil.copytree(dist_dir, backend_web_dir)
    print("✓ 前端文件已复制到后端目录")
    
    print("\n=== 3. 安装后端依赖 ===")
    print("正在检查/安装后端依赖...")
    run_command('pip install -r requirements.txt', cwd=backend_dir)
    print("✓ 后端依赖安装完成")
    
    # 根据当前平台打包
    if IS_WINDOWS:
        print("\n=== 4. 打包 Windows 版本 ===")
        build_windows_version(root_dir, backend_dir, build_output_dir)
        
        print("\n=== 5. 准备 macOS 版本（无需打包环境） ===")
        prepare_macos_python_version(root_dir, backend_dir, build_output_dir)
        
        print("\n=== 6. 准备 macOS 打包工具包（可选） ===")
        prepare_macos_build_package(root_dir, backend_dir, build_output_dir)
        
    else:
        # 非 Windows 平台，直接打包当前平台版本
        print(f"\n=== 4. 打包 {get_platform_name()} 版本 ===")
        build_current_platform(root_dir, backend_dir, build_output_dir)
    
    # 打印最终总结
    print("\n" + "="*60)
    print("✓ 打包完成！")
    print("="*60)
    
    if IS_WINDOWS:
        windows_dir = os.path.join(build_output_dir, 'Windows')
        macos_python_dir = os.path.join(build_output_dir, 'macOS_Python版本')
        macos_package_dir = os.path.join(build_output_dir, 'macOS_打包工具包')
        print(f"\n📦 Windows 版本:")
        print(f"   位置: {windows_dir}")
        print(f"   说明: 可以直接分发给 Windows 用户使用")
        print(f"\n📦 macOS Python 版本（推荐，无需打包环境）:")
        print(f"   位置: {macos_python_dir}")
        print(f"   说明: 可以直接分发给 macOS 用户使用，只需安装 Python 3")
        print(f"   优点: 无需打包环境，体积小，启动快")
        print(f"\n📦 macOS 打包工具包（可选）:")
        print(f"   位置: {macos_package_dir}")
        print(f"   说明: 如需生成独立的可执行文件，可使用此工具包打包")
        print(f"\n💡 提示:")
        print(f"   - Windows 版本已经可以立即使用")
        print(f"   - macOS Python 版本推荐使用（最简单，只需 Python 3）")
        print(f"   - macOS 打包工具包用于生成独立可执行文件（需要打包环境）")
    else:
        platform_dir = os.path.join(build_output_dir, get_platform_name())
        print(f"\n📦 {get_platform_name()} 版本:")
        print(f"   位置: {platform_dir}")
        print(f"   说明: 可以直接分发给用户使用")
    
    print("="*60)

def build_windows_version(root_dir, backend_dir, build_output_dir):
    """打包 Windows 版本"""
    print("开始打包 Windows 版本...")
    
    # 清理旧的构建文件
    build_dir = os.path.join(backend_dir, 'build')
    spec_file = os.path.join(backend_dir, 'TimeTeachingSystem.spec')
    old_dist = os.path.join(backend_dir, 'dist')
    
    if os.path.exists(build_dir):
        print("清理旧的 build 目录...")
        shutil.rmtree(build_dir)
    
    if os.path.exists(old_dist):
        print("清理旧的 dist 目录...")
        shutil.rmtree(old_dist)
    
    # 使用 spec 文件打包（如果存在）
    if os.path.exists(spec_file):
        print("使用 spec 文件打包...")
        cmd = f'pyinstaller --noconfirm --clean {spec_file}'
    else:
        # PyInstaller 命令
        add_data = 'web;web'  # Windows 使用分号
        cmd = f'pyinstaller --noconfirm --clean --onefile --console --name="TimeTeachingSystem" --add-data="{add_data}" --hidden-import=flask --hidden-import=flask_cors --hidden-import=sqlalchemy app.py'
    
    print("开始打包（这可能需要几分钟，请耐心等待）...")
    print("提示：打包过程会显示很多信息，这是正常的...")
    run_command(cmd, cwd=backend_dir)
    
    # 创建 Windows 发布目录
    windows_output_dir = os.path.join(build_output_dir, 'Windows')
    if os.path.exists(windows_output_dir):
        shutil.rmtree(windows_output_dir)
    os.makedirs(windows_output_dir, exist_ok=True)
    
    # 复制可执行文件
    exe_name = 'TimeTeachingSystem.exe'
    exe_path = os.path.join(backend_dir, 'dist', exe_name)
    
    if not os.path.exists(exe_path):
        print(f"❌ 打包失败，未找到可执行文件: {exe_path}")
        sys.exit(1)
    
    print(f"复制可执行文件到发布目录...")
    shutil.copy2(exe_path, windows_output_dir)
    
    # 创建启动脚本
    create_windows_start_script(windows_output_dir)
    
    # 创建使用说明
    create_windows_readme(windows_output_dir)
    
    # 检查文件大小
    exe_size = os.path.getsize(os.path.join(windows_output_dir, exe_name))
    exe_size_mb = exe_size / (1024 * 1024)
    
    print(f"\n✓ Windows 版本打包完成！")
    print(f"  发布位置: {windows_output_dir}")
    print(f"  文件大小: {exe_size_mb:.2f} MB")

def prepare_macos_python_version(root_dir, backend_dir, build_output_dir):
    """准备 macOS Python 脚本版本（无需打包环境，直接运行）"""
    print("正在准备 macOS Python 脚本版本（无需打包环境）...")
    
    macos_python_dir = os.path.join(build_output_dir, 'macOS_Python版本')
    if os.path.exists(macos_python_dir):
        shutil.rmtree(macos_python_dir)
    os.makedirs(macos_python_dir, exist_ok=True)
    
    # 复制后端目录（包含构建好的前端文件）
    print("复制后端代码和资源...")
    backend_copy = os.path.join(macos_python_dir, 'backend')
    if os.path.exists(backend_copy):
        shutil.rmtree(backend_copy)
    shutil.copytree(backend_dir, backend_copy, ignore=shutil.ignore_patterns(
        'build', 'dist', '__pycache__', '*.pyc', '*.spec', 'instance', 'time24_teaching.db'
    ))
    
    # 创建启动脚本
    create_macos_python_start_script(macos_python_dir)
    
    # 创建初始化数据库脚本
    create_macos_init_script(macos_python_dir)
    
    # 创建使用说明
    create_macos_python_readme(macos_python_dir)
    
    print(f"\n✓ macOS Python 脚本版本准备完成！")
    print(f"  版本位置: {macos_python_dir}")
    print(f"  说明: macOS 用户可以直接使用，只需安装 Python 3 和依赖")

def prepare_macos_build_package(root_dir, backend_dir, build_output_dir):
    """准备 macOS 打包工具包"""
    print("正在准备 macOS 打包工具包...")
    
    macos_build_package_dir = os.path.join(build_output_dir, 'macOS_打包工具包')
    if os.path.exists(macos_build_package_dir):
        shutil.rmtree(macos_build_package_dir)
    os.makedirs(macos_build_package_dir, exist_ok=True)
    
    # 复制后端目录（包含构建好的前端文件）
    print("复制后端代码和资源...")
    backend_copy = os.path.join(macos_build_package_dir, 'backend')
    if os.path.exists(backend_copy):
        shutil.rmtree(backend_copy)
    shutil.copytree(backend_dir, backend_copy, ignore=shutil.ignore_patterns(
        'build', 'dist', '__pycache__', '*.pyc', '*.spec', 'instance'
    ))
    
    # 创建 macOS 打包脚本
    create_macos_build_script(macos_build_package_dir, root_dir)
    
    # 创建 macOS 打包说明
    create_macos_build_readme(macos_build_package_dir)
    
    print(f"\n✓ macOS 打包工具包准备完成！")
    print(f"  工具包位置: {macos_build_package_dir}")
    print(f"  说明: 请将此文件夹复制到 macOS 系统上，运行其中的 '在macOS上打包.sh' 脚本")

def build_current_platform(root_dir, backend_dir, build_output_dir):
    """打包当前平台版本（非 Windows）"""
    # 清理旧的构建文件
    build_dir = os.path.join(backend_dir, 'build')
    spec_file = os.path.join(backend_dir, 'TimeTeachingSystem.spec')
    old_dist = os.path.join(backend_dir, 'dist')
    
    if os.path.exists(build_dir):
        print("清理旧的 build 目录...")
        shutil.rmtree(build_dir)
    
    if os.path.exists(old_dist):
        print("清理旧的 dist 目录...")
        shutil.rmtree(old_dist)
    
    # 使用 spec 文件打包（如果存在）
    if os.path.exists(spec_file):
        print("使用 spec 文件打包...")
        cmd = f'pyinstaller --noconfirm --clean {spec_file}'
    else:
        # PyInstaller 命令
        add_data = 'web:web'  # macOS/Linux 使用冒号
        exe_name = get_executable_name()
        cmd = f'pyinstaller --noconfirm --clean --onefile --console --name="TimeTeachingSystem" --add-data="{add_data}" --hidden-import=flask --hidden-import=flask_cors --hidden-import=sqlalchemy app.py'
    
    print("开始打包（这可能需要几分钟，请耐心等待）...")
    print("提示：打包过程会显示很多信息，这是正常的...")
    run_command(cmd, cwd=backend_dir)
    
    # 创建发布目录
    platform_output_dir = os.path.join(build_output_dir, get_platform_name())
    if os.path.exists(platform_output_dir):
        shutil.rmtree(platform_output_dir)
    os.makedirs(platform_output_dir, exist_ok=True)
    
    # 复制可执行文件
    exe_name = get_executable_name()
    exe_path = os.path.join(backend_dir, 'dist', exe_name)
    
    if not os.path.exists(exe_path):
        print(f"❌ 打包失败，未找到可执行文件: {exe_path}")
        sys.exit(1)
    
    print(f"复制可执行文件到发布目录...")
    shutil.copy2(exe_path, platform_output_dir)
    
    # 添加执行权限
    if IS_MAC or IS_LINUX:
        os.chmod(os.path.join(platform_output_dir, exe_name), 0o755)
        print("✓ 已添加可执行权限")
    
    # 创建启动脚本
    create_unix_start_script(platform_output_dir)
    
    # 创建使用说明
    create_unix_readme(platform_output_dir)
    
    # 检查文件大小
    exe_size = os.path.getsize(os.path.join(platform_output_dir, exe_name))
    exe_size_mb = exe_size / (1024 * 1024)
    
    print(f"\n✓ {get_platform_name()} 版本打包完成！")
    print(f"  发布位置: {platform_output_dir}")
    print(f"  文件大小: {exe_size_mb:.2f} MB")

def create_windows_start_script(output_dir):
    """创建 Windows 启动脚本"""
    start_script = os.path.join(output_dir, '启动系统.bat')
    with open(start_script, 'w', encoding='utf-8') as f:
        f.write('''@echo off
chcp 65001 >nul
title 24时计时法教学系统
color 0A
echo ========================================
echo   24时计时法教学系统
echo ========================================
echo.
echo 正在启动系统，请稍候...
echo.
echo 系统启动后，将自动在浏览器中打开
echo 如果未自动打开，请手动访问: http://localhost:5000
echo.
echo 按 Ctrl+C 可以停止服务
echo ========================================
echo.

REM 延迟3秒后自动打开浏览器
start "" cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:5000"

REM 启动主程序
TimeTeachingSystem.exe

pause
''')
    print("✓ 已创建 Windows 启动脚本")

def create_unix_start_script(output_dir):
    """创建 macOS/Linux 启动脚本"""
    start_script = os.path.join(output_dir, '启动系统.sh')
    with open(start_script, 'w', encoding='utf-8') as f:
        f.write('''#!/bin/bash

# 设置颜色输出
GREEN='\\033[0;32m'
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   24时计时法教学系统${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "正在启动系统，请稍候..."
echo ""
echo "系统启动后，将自动在浏览器中打开"
echo "如果未自动打开，请手动访问: http://localhost:5000"
echo ""
echo "按 Ctrl+C 可以停止服务"
echo "========================================"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 延迟3秒后自动打开浏览器
(sleep 3 && open http://localhost:5000 2>/dev/null || xdg-open http://localhost:5000 2>/dev/null || echo "请手动打开浏览器访问 http://localhost:5000") &

# 启动主程序
cd "$SCRIPT_DIR"
./TimeTeachingSystem

echo ""
echo "系统已停止运行"
read -p "按回车键退出..."
''')
    # 添加执行权限
    os.chmod(start_script, 0o755)
    print("✓ 已创建 macOS/Linux 启动脚本")

def create_macos_build_script(package_dir, root_dir):
    """创建 macOS 打包脚本"""
    build_script = os.path.join(package_dir, '在macOS上打包.sh')
    with open(build_script, 'w', encoding='utf-8') as f:
        f.write('''#!/bin/bash

# 设置颜色输出
GREEN='\\033[0;32m'
BLUE='\\033[0;34m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   24时计时法教学系统 - macOS 打包工具${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查 Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}❌ Python 3 未安装${NC}"
    echo "请先安装 Python 3: brew install python3"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 已安装${NC}"
python3 --version

# 检查 pip3
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}❌ pip3 未安装${NC}"
    exit 1
fi

echo -e "${GREEN}✓ pip3 已安装${NC}"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$SCRIPT_DIR/backend"

echo "=== 1. 安装后端依赖 ==="
cd "$BACKEND_DIR"
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}❌ 依赖安装失败${NC}"
    exit 1
fi

echo ""
echo "=== 2. 使用 PyInstaller 打包 ==="

# 清理旧的构建文件
if [ -d "$BACKEND_DIR/build" ]; then
    rm -rf "$BACKEND_DIR/build"
fi

if [ -d "$BACKEND_DIR/dist" ]; then
    rm -rf "$BACKEND_DIR/dist"
fi

# 使用 spec 文件打包（如果存在）
if [ -f "$BACKEND_DIR/TimeTeachingSystem.spec" ]; then
    echo "使用 spec 文件打包..."
    cd "$BACKEND_DIR"
    pyinstaller --noconfirm --clean TimeTeachingSystem.spec
else
    # PyInstaller 命令
    echo "使用命令行打包..."
    cd "$BACKEND_DIR"
    pyinstaller --noconfirm --clean --onefile --console \\
        --name="TimeTeachingSystem" \\
        --add-data="web:web" \\
        --hidden-import=flask \\
        --hidden-import=flask_cors \\
        --hidden-import=sqlalchemy \\
        app.py
fi

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}❌ 打包失败${NC}"
    exit 1
fi

echo ""
echo "=== 3. 准备发布包 ==="

EXE_PATH="$BACKEND_DIR/dist/TimeTeachingSystem"
OUTPUT_DIR="$SCRIPT_DIR/macOS"

if [ ! -f "$EXE_PATH" ]; then
    echo -e "${YELLOW}❌ 未找到可执行文件${NC}"
    exit 1
fi

# 创建发布目录
if [ -d "$OUTPUT_DIR" ]; then
    rm -rf "$OUTPUT_DIR"
fi
mkdir -p "$OUTPUT_DIR"

# 复制可执行文件
cp "$EXE_PATH" "$OUTPUT_DIR/"
chmod +x "$OUTPUT_DIR/TimeTeachingSystem"

# 创建启动脚本
cat > "$OUTPUT_DIR/启动系统.sh" << 'EOFSCRIPT'
#!/bin/bash

GREEN='\\033[0;32m'
NC='\\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   24时计时法教学系统${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "正在启动系统，请稍候..."
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
(sleep 3 && open http://localhost:5000 2>/dev/null || echo "请手动打开浏览器访问 http://localhost:5000") &

cd "$SCRIPT_DIR"
./TimeTeachingSystem

echo ""
echo "系统已停止运行"
read -p "按回车键退出..."
EOFSCRIPT

chmod +x "$OUTPUT_DIR/启动系统.sh"

# 创建使用说明
cat > "$OUTPUT_DIR/使用说明.txt" << 'EOFREADME'
═══════════════════════════════════════════════════
    24时计时法教学系统 - 使用说明 (macOS)
═══════════════════════════════════════════════════

【快速开始】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 双击 "启动系统.sh" 文件
   （或在终端中运行: ./启动系统.sh）
2. 如果提示权限不足，请在终端运行: chmod +x 启动系统.sh
3. 等待系统启动（会显示终端窗口）
4. 系统会自动在浏览器中打开，如果没有自动打开，
   请手动访问: http://localhost:5000

【停止系统】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
在终端窗口中按 Ctrl+C，然后关闭窗口

【默认账号】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
教师后台登录：
  - 用户名: teacher
  - 密码: teacher123

⚠️ 注意：生产环境建议修改默认密码！

【数据存储】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 首次运行会自动创建数据库文件 time24_teaching.db
- 数据库文件会保存在程序同目录下
- 删除数据库文件会清空所有数据

【系统要求】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 操作系统: macOS 10.12 或更高版本
- 浏览器: Safari、Chrome、Firefox 等现代浏览器
- 网络: 无需联网（本地运行）

【常见问题】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. macOS 安全提示
   问题：提示"无法打开，因为来自身份不明的开发者"
   解决：
   - 右键点击可执行文件，选择"打开" → 点击"打开"确认
   - 或在终端运行: xattr -d com.apple.quarantine TimeTeachingSystem

2. 端口被占用
   解决：关闭占用 5000 端口的其他程序后重试

═══════════════════════════════════════════════════
EOFREADME

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ macOS 版本打包完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "发布位置: $OUTPUT_DIR"
echo ""
echo "打包好的程序在 macOS 文件夹中，可以直接分发给用户使用。"
echo ""
''')
    # 添加执行权限
    os.chmod(build_script, 0o755)
    print("✓ 已创建 macOS 打包脚本")

def create_macos_build_readme(package_dir):
    """创建 macOS 打包工具包说明"""
    readme_path = os.path.join(package_dir, 'README_macOS打包说明.txt')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write('''═══════════════════════════════════════════════════
    macOS 打包工具包使用说明
═══════════════════════════════════════════════════

这个工具包包含了在 macOS 上打包所需的所有文件。

【使用方法】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 将此文件夹复制到 macOS 系统上
2. 打开终端（Terminal）
3. 进入此文件夹目录
4. 运行打包脚本：
   ./在macOS上打包.sh
   
   如果提示权限不足，请先运行：
   chmod +x 在macOS上打包.sh

【前置要求】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- macOS 10.12 或更高版本
- Python 3.6 或更高版本（推荐使用 Python 3.8+）
  - 如果没有安装，可以通过 Homebrew 安装：
    brew install python3
- pip3（通常随 Python 3 一起安装）

【打包过程】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
打包脚本会自动执行以下步骤：
1. 检查 Python 3 和 pip3 是否安装
2. 安装后端 Python 依赖
3. 使用 PyInstaller 打包程序
4. 生成 macOS 可执行文件和启动脚本
5. 创建使用说明文档

打包完成后，会在当前目录生成 "macOS" 文件夹，
其中包含打包好的程序，可以直接分发给用户使用。

【注意事项】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 首次运行打包好的程序时，macOS 可能会提示"无法打开"
  这是正常的安全提示，请右键选择"打开"即可
- 打包过程可能需要几分钟，请耐心等待
- 如果遇到错误，请查看终端中的错误信息

═══════════════════════════════════════════════════
''')
    print("✓ 已创建 macOS 打包说明")

def create_macos_python_start_script(package_dir):
    """创建 macOS Python 版本启动脚本"""
    start_script = os.path.join(package_dir, '启动系统.sh')
    with open(start_script, 'w', encoding='utf-8') as f:
        f.write('''#!/bin/bash

# 设置颜色输出
GREEN='\\033[0;32m'
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   24时计时法教学系统${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$SCRIPT_DIR/backend"

# 设置颜色
RED='\\033[0;31m'

# 检查 Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 未安装${NC}"
    echo ""
    echo "请先安装 Python 3："
    echo "  方法1: 访问 https://www.python.org/downloads/ 下载安装"
    echo "  方法2: 使用 Homebrew 安装: brew install python3"
    echo ""
    read -p "按回车键退出..."
    exit 1
fi

echo -e "${GREEN}✓ Python 3 已安装${NC}"
python3 --version
echo ""

# 检查依赖是否已安装
if ! python3 -c "import flask" 2>/dev/null; then
    echo "检测到缺少 Python 依赖，正在安装..."
    echo "（首次运行需要安装依赖，可能需要几分钟）"
    echo ""
    cd "$BACKEND_DIR"
    python3 -m pip install --user -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo ""
        echo -e "${RED}❌ 依赖安装失败${NC}"
        echo "请手动运行: cd backend && pip3 install -r requirements.txt"
        echo ""
        read -p "按回车键退出..."
        exit 1
    fi
    echo ""
    echo -e "${GREEN}✓ 依赖安装完成${NC}"
    echo ""
fi

# 初始化数据库（如果不存在）
if [ ! -f "$BACKEND_DIR/instance/time24_teaching.db" ]; then
    echo "首次运行，正在初始化数据库..."
    cd "$BACKEND_DIR"
    python3 init_data.py
    echo -e "${GREEN}✓ 数据库初始化完成${NC}"
    echo ""
fi

echo "正在启动系统，请稍候..."
echo ""
echo "系统启动后，将自动在浏览器中打开"
echo "如果未自动打开，请手动访问: http://localhost:5000"
echo ""
echo "按 Ctrl+C 可以停止服务"
echo "========================================"
echo ""

# 延迟3秒后自动打开浏览器
(sleep 3 && open http://localhost:5000 2>/dev/null || echo "请手动打开浏览器访问 http://localhost:5000") &

# 启动主程序
cd "$BACKEND_DIR"
python3 app.py

echo ""
echo "系统已停止运行"
read -p "按回车键退出..."
''')
    # 添加执行权限
    os.chmod(start_script, 0o755)
    print("✓ 已创建 macOS Python 启动脚本")

def create_macos_init_script(package_dir):
    """创建 macOS 初始化数据库脚本"""
    init_script = os.path.join(package_dir, '初始化数据库.sh')
    with open(init_script, 'w', encoding='utf-8') as f:
        f.write('''#!/bin/bash

echo "正在初始化数据库..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/backend"

if [ ! -f "instance/time24_teaching.db" ]; then
    python3 init_data.py
    echo "✓ 数据库初始化完成"
else
    echo "数据库已存在，跳过初始化"
    read -p "是否重新初始化数据库？这将清空所有数据！(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -f instance/time24_teaching.db
        python3 init_data.py
        echo "✓ 数据库已重新初始化"
    fi
fi
''')
    os.chmod(init_script, 0o755)
    print("✓ 已创建初始化数据库脚本")

def create_macos_python_readme(package_dir):
    """创建 macOS Python 版本使用说明"""
    readme_path = os.path.join(package_dir, '使用说明.txt')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write('''═══════════════════════════════════════════════════
    24时计时法教学系统 - 使用说明 (macOS Python 版本)
═══════════════════════════════════════════════════

【系统要求】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- macOS 10.12 或更高版本
- Python 3.6 或更高版本（macOS 通常已预装）
  - 如果没有，请访问: https://www.python.org/downloads/
- 浏览器: Safari、Chrome、Firefox 等现代浏览器

【快速开始】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 双击 "启动系统.sh" 文件
   （或在终端中运行: ./启动系统.sh）
   
2. 如果提示权限不足，请在终端运行:
   chmod +x 启动系统.sh
   
3. 首次运行会自动：
   - 检查并安装 Python 依赖（如果需要）
   - 初始化数据库
   - 启动系统
   
4. 系统会自动在浏览器中打开
   如果没有自动打开，请手动访问: http://localhost:5000

【停止系统】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
在终端窗口中按 Ctrl+C，然后关闭窗口

【默认账号】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
教师后台登录：
  - 用户名: teacher
  - 密码: teacher123

⚠️ 注意：生产环境建议修改默认密码！

【数据存储】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 数据库文件位置: backend/instance/time24_teaching.db
- 首次运行会自动创建数据库
- 删除数据库文件会清空所有数据（包括学生记录、答题记录等）
- 可以使用 "初始化数据库.sh" 重新初始化数据库

【常见问题】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Python 3 未安装
   问题：提示 "Python 3 未安装"
   解决：
   - 访问 https://www.python.org/downloads/ 下载安装
   - 或使用 Homebrew: brew install python3
   - 安装后重启终端

2. 依赖安装失败
   问题：首次运行时依赖安装失败
   解决：
   - 手动运行: cd backend && pip3 install -r requirements.txt
   - 如果提示权限错误，使用: pip3 install --user -r requirements.txt

3. 端口被占用
   问题：启动时提示端口 5000 已被占用
   解决：关闭占用 5000 端口的其他程序后重试

4. 无法访问页面
   问题：浏览器显示无法连接
   解决：
   - 检查终端窗口是否显示错误信息
   - 确认程序已正常启动（终端应显示 Flask 启动信息）
   - 尝试手动访问: http://localhost:5000

5. 权限错误
   问题：双击 .sh 文件提示权限不足
   解决：
   - 在终端中运行: chmod +x 启动系统.sh
   - 或在终端中运行: ./启动系统.sh

【优势】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ 无需打包环境，只需 Python 3
✓ 体积小，启动快
✓ 易于更新和维护
✓ 支持热更新（修改代码后重启即可）

【技术支持】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
如有问题，请检查：
1. 终端窗口中的错误信息
2. 浏览器控制台的错误信息（按 F12 打开）
3. Python 版本: python3 --version
4. 联系开发人员获取支持

═══════════════════════════════════════════════════
版本: 2.0.0
平台: macOS (Python 脚本版本)
最后更新: 2024年
═══════════════════════════════════════════════════
''')
    print("✓ 已创建 macOS Python 版本使用说明")

def create_windows_readme(output_dir):
    """创建 Windows 使用说明"""
    readme_path = os.path.join(output_dir, '使用说明.txt')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write('''═══════════════════════════════════════════════════
    24时计时法教学系统 - 使用说明 (Windows)
═══════════════════════════════════════════════════

【快速开始】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 双击 "启动系统.bat" 文件
2. 等待系统启动（会显示一个命令行窗口）
3. 系统会自动在浏览器中打开，如果没有自动打开，
   请手动访问: http://localhost:5000

【停止系统】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
在命令行窗口中按 Ctrl+C，然后关闭窗口

【默认账号】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
教师后台登录：
  - 用户名: teacher
  - 密码: teacher123

⚠️ 注意：生产环境建议修改默认密码！

【数据存储】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 首次运行会自动创建数据库文件 time24_teaching.db
- 数据库文件会保存在程序同目录下
- 删除数据库文件会清空所有数据（包括学生记录、答题记录等）

【系统要求】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 操作系统: Windows 7 或更高版本（Windows 10/11 推荐）
- 浏览器: Chrome、Edge、Firefox 等现代浏览器
- 网络: 无需联网（本地运行）
- 其他: 无需安装 Python、Node.js 等开发环境

【常见问题】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 端口被占用
   问题：启动时提示端口 5000 已被占用
   解决：关闭占用 5000 端口的其他程序后重试

2. 无法访问页面
   问题：浏览器显示无法连接
   解决：检查命令行窗口是否显示错误信息，确认程序已正常启动

3. 程序无法运行
   问题：双击 exe 文件没有反应
   解决：
   - 检查是否被杀毒软件拦截（添加信任）
   - 尝试右键"以管理员身份运行"
   - 查看是否有错误提示信息

【技术支持】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
如有问题，请检查：
1. 命令行窗口中的错误信息
2. 浏览器控制台的错误信息（按 F12 打开）
3. 联系开发人员获取支持

═══════════════════════════════════════════════════
版本: 1.0.0
目标平台: Windows
最后更新: 2024年
═══════════════════════════════════════════════════
''')
    print("✓ 已创建 Windows 使用说明")

def create_unix_readme(output_dir):
    """创建 macOS/Linux 使用说明"""
    readme_path = os.path.join(output_dir, '使用说明.txt')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(f'''═══════════════════════════════════════════════════
    24时计时法教学系统 - 使用说明 ({get_platform_name()})
═══════════════════════════════════════════════════

【快速开始】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 双击 "启动系统.sh" 文件
   （或在终端中运行: ./启动系统.sh）
2. 如果提示权限不足，请在终端运行: chmod +x 启动系统.sh
3. 等待系统启动（会显示终端窗口）
4. 系统会自动在浏览器中打开，如果没有自动打开，
   请手动访问: http://localhost:5000

【停止系统】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
在终端窗口中按 Ctrl+C，然后关闭窗口

【默认账号】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
教师后台登录：
  - 用户名: teacher
  - 密码: teacher123

⚠️ 注意：生产环境建议修改默认密码！

【数据存储】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 首次运行会自动创建数据库文件 time24_teaching.db
- 数据库文件会保存在程序同目录下
- 删除数据库文件会清空所有数据（包括学生记录、答题记录等）

【系统要求】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 操作系统: {get_platform_name()} 10.12 或更高版本（macOS）
- 浏览器: Safari、Chrome、Firefox 等现代浏览器
- 网络: 无需联网（本地运行）
- 其他: 无需安装 Python、Node.js 等开发环境

【常见问题】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. macOS 安全提示
   问题：macOS 提示"无法打开，因为来自身份不明的开发者"
   解决：
   - 右键点击可执行文件，选择"打开" → 点击"打开"确认
   - 或在"系统偏好设置" > "安全性与隐私"中允许运行
   - 或在终端运行: xattr -d com.apple.quarantine TimeTeachingSystem

2. 端口被占用
   问题：启动时提示端口 5000 已被占用
   解决：关闭占用 5000 端口的其他程序后重试

3. 无法访问页面
   问题：浏览器显示无法连接
   解决：检查终端窗口是否显示错误信息，确认程序已正常启动

【技术支持】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
如有问题，请检查：
1. 终端窗口中的错误信息
2. 浏览器控制台的错误信息（按 F12 打开）
3. 联系开发人员获取支持

═══════════════════════════════════════════════════
版本: 1.0.0
目标平台: {get_platform_name()}
最后更新: 2024年
═══════════════════════════════════════════════════
''')
    print("✓ 已创建使用说明文件")

if __name__ == '__main__':
    try:
        build()
    except KeyboardInterrupt:
        print("\n\n打包已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 打包过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
