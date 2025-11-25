#!/bin/bash

# 设置颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

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
    pyinstaller --noconfirm --clean --onefile --console \
        --name="TimeTeachingSystem" \
        --add-data="web:web" \
        --hidden-import=flask \
        --hidden-import=flask_cors \
        --hidden-import=sqlalchemy \
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

GREEN='\033[0;32m'
NC='\033[0m'

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
