#!/bin/bash
# 环境备份和迁移脚本

# 创建备份目录
BACKUP_DIR="D:/opencode_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "开始备份 OpenCode 环境..."

# 备份当前工作目录
echo "备份工作目录..."
cp -r "C:/Users/Administrator/AppData/Roaming/com.differentai.openwork/workspaces/starter" "$BACKUP_DIR/workspaces"

# 备份重要配置
echo "备份系统配置..."
mkdir -p "$BACKUP_DIR/config"

# 备份Python环境（如果存在）
if command -v python &> /dev/null; then
    echo "备份Python包列表..."
    pip freeze > "$BACKUP_DIR/config/requirements.txt"
fi

# 备份Node.js环境（如果存在）
if command -v node &> /dev/null; then
    echo "备份Node.js包列表..."
    npm list -g --depth=0 > "$BACKUP_DIR/config/npm_global.txt" 2>/dev/null || echo "N/A" > "$BACKUP_DIR/config/npm_global.txt"
fi

# 创建恢复脚本
cat > "$BACKUP_DIR/restore.sh" << 'EOF'
#!/bin/bash
# 环境恢复脚本

echo "开始恢复 OpenCode 环境..."

# 检查备份目录
if [ ! -d "workspaces" ]; then
    echo "错误: 找不到工作目录备份"
    exit 1
fi

# 恢复工作目录
TARGET_DIR="$HOME/AppData/Roaming/com.differentai.openwork/workspaces/starter"
mkdir -p "$(dirname "$TARGET_DIR")"
cp -r workspaces "$TARGET_DIR"

# 恢复Python环境
if [ -f "config/requirements.txt" ] && command -v python &> /dev/null; then
    echo "恢复Python包..."
    pip install -r config/requirements.txt
fi

# 恢复Node.js环境
if [ -f "config/npm_global.txt" ] && command -v npm &> /dev/null; then
    echo "恢复Node.js包..."
    while read -r package; do
        if [ "$package" != "N/A" ] && [ -n "$package" ]; then
            npm install -g "$package"
        fi
    done < config/npm_global.txt
fi

echo "恢复完成！"
EOF

chmod +x "$BACKUP_DIR/restore.sh"

# 创建备份信息文件
cat > "$BACKUP_DIR/backup_info.txt" << EOF
备份时间: $(date)
备份版本: OpenCode $(opencode --version 2>/dev/null || echo "Unknown")
系统信息: $(uname -a)
工作目录: $(pwd)

恢复方法:
1. 将备份文件夹复制到新设备
2. 运行 restore.sh 脚本
3. 重新配置 OpenCode 环境

重要提醒:
- 需要在新设备上重新安装 OpenCode
- 部分配置可能需要手动调整
- 建议同时备份重要文档到云端
EOF

echo "备份完成! 位置: $BACKUP_DIR"
echo "请将此文件夹安全保存，用于设备迁移时恢复环境"

# 可选: 压缩备份
echo "是否压缩备份? (y/n)"
read -r compress
if [ "$compress" = "y" ]; then
    cd "$(dirname "$BACKUP_DIR")"
    tar -czf "$(basename "$BACKUP_DIR").tar.gz" "$(basename "$BACKUP_DIR")"
    echo "压缩完成: $(basename "$BACKUP_DIR").tar.gz"
fi