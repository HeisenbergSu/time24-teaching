@echo off
chcp 65001 >nul
title 24时计时法教学系统 - 打包工具
echo ========================================
echo   24时计时法教学系统 - 打包工具
echo   目标平台: Windows
echo ========================================
echo.
echo 正在启动打包程序...
echo.

python build_project.py

echo.
echo ========================================
pause
