@echo off
REM OpenCode自动备份脚本 - Windows版本
REM 每日备份任务

set BACKUP_DIR=C:\Users\Administrator\Desktop\OpenWork\Daily_Backups
set SOURCE_DIR=C:\Users\Administrator\AppData\Roaming\com.differentai.openwork\workspaces\starter
set TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%
set BACKUP_NAME=backup_%TIMESTAMP%

echo ================================
echo OpenCode自动备份 - %date% %time%
echo ================================

REM 创建备份目录
if not exist "%BACKUP_DIR%" (
    mkdir "%BACKUP_DIR%"
)

REM 创建当日备份目录
set TODAY_BACKUP=%BACKUP_DIR%\%BACKUP_NAME%
mkdir "%TODAY_BACKUP%"

REM 备份工作文件
echo [1/6] 备份工作文件...
xcopy "%SOURCE_DIR%\*.py" "%TODAY_BACKUP%\" /Y /Q >nul 2>&1
xcopy "%SOURCE_DIR%\*.md" "%TODAY_BACKUP%\" /Y /Q >nul 2>&1
xcopy "%SOURCE_DIR%\*.jsonc" "%TODAY_BACKUP%\" /Y /Q >nul 2>&1
xcopy "%SOURCE_DIR%\*.txt" "%TODAY_BACKUP%\" /Y /Q >nul 2>&1

REM 备份.opencode配置
echo [2/6] 备份OpenCode配置...
xcopy "%SOURCE_DIR%\.opencode" "%TODAY_BACKUP%\.opencode\" /E /I /Y /Q >nul 2>&1

REM 备份requirements.txt（如果存在）
if exist "%SOURCE_DIR%\requirements.txt" (
    copy "%SOURCE_DIR%\requirements.txt" "%TODAY_BACKUP%\" /Y >nul
)

REM 生成备份报告
echo [3/6] 生成备份报告...
set REPORT_FILE=%TODAY_BACKUP%\backup_report.txt
echo OpenCode自动备份报告 > "%REPORT_FILE%"
echo ======================== >> "%REPORT_FILE%"
echo 备份时间: %date% %time% >> "%REPORT_FILE%"
echo 备份路径: %TODAY_BACKUP% >> "%REPORT_FILE%"
echo 备份类型: 完整备份 >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

echo 备份文件清单: >> "%REPORT_FILE%"
dir "%TODAY_BACKUP%" /B /S >> "%REPORT_FILE%"

REM 清理过期备份（保留最近7天）
echo [4/6] 清理过期备份...
for /f "skip=7 delims=" %%F in ('dir "%BACKUP_DIR%" /B /O-D /AD 2^>nul') do (
    echo 删除过期备份: %%F
    rd /s /q "%BACKUP_DIR%\%%F" 2>nul
)

REM 验证备份完整性
echo [5/6] 验证备份完整性...
set BACKUP_SIZE=0
for /f "tokens=3" %%A in ('dir "%TODAY_BACKUP%" /s /-c ^| findstr 个文件') do set BACKUP_SIZE=%%A

if %BACKUP_SIZE% GTR 0 (
    echo [6/6] ✅ 备份完成! 文件数: %BACKUP_SIZE%
    echo 备份状态: 成功 >> "%REPORT_FILE%"
    echo 文件数量: %BACKUP_SIZE% >> "%REPORT_FILE%"
) else (
    echo [6/6] ❌ 备份失败! 文件为空
    echo 备份状态: 失败 >> "%REPORT_FILE%"
    echo 问题: 备份文件为空 >> "%REPORT_FILE%"
)

REM 更新主备份目录
echo [6/6] 更新主备份目录...
xcopy "%TODAY_BACKUP%\*" "C:\Users\Administrator\Desktop\OpenWork\" /Y /Q >nul 2>&1

echo ================================
echo 备份完成 - %date% %time%
echo ================================
echo 位置: %TODAY_BACKUP%
echo. >> "%REPORT_FILE%"
echo 脚本执行完成时间: %date% %time% >> "%REPORT_FILE%"

REM 记录到日志文件
echo %date% %time% - 自动备份完成 >> "%BACKUP_DIR%\backup.log"

pause