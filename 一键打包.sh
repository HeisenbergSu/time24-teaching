#!/bin/bash

# 设置颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   24时计时法教学系统 - 打包工具${NC}"
echo -e "${GREEN}   目标平台: macOS${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "正在启动打包程序..."
echo ""

python3 build_project.py

echo ""
echo "========================================"
read -p "按回车键退出..."

