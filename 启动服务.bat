@echo off
chcp 65001 >nul
echo ========================================
echo   健康魔方 - AI饮食记录与建议
echo ========================================
echo.
echo 正在启动后端服务...
echo.
echo 服务地址: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止服务
echo.
echo ========================================
echo.

python app.py
