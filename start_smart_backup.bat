@echo off
REM 启动智能备份监控系统
REM 后台运行，检测系统空闲时自动备份

echo 🚀 启动OpenCode智能备份监控...
echo 📋 备份策略: 系统空闲时自动备份 (间隔12小时)
echo ⚡ 检测间隔: 5分钟
echo 📁 备份位置: C:\Users\Administrator\Desktop\OpenWork\Daily_Backups\
echo.
echo 按 Ctrl+C 停止监控
echo ================================

cd /d "C:\Users\Administrator\AppData\Roaming\com.differentai.openwork\workspaces\starter"

python smart_backup.py --monitor

pause