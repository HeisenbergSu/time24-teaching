@echo off
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
