#!/usr/bin/env python3
"""
OpenCode智能备份系统
检测系统空闲时自动备份，无需固定时间
"""

import os
import shutil
import time
import json
import logging
from datetime import datetime, timedelta
import psutil
import threading
import subprocess

class SmartBackup:
    def __init__(self):
        self.backup_dir = r"C:\Users\Administrator\Desktop\OpenWork\Daily_Backups"
        self.source_dir = r"C:\Users\Administrator\AppData\Roaming\com.differentai.opencode\workspaces\starter"
        self.log_file = os.path.join(self.backup_dir, "smart_backup.log")
        self.state_file = os.path.join(self.backup_dir, "backup_state.json")
        self.last_backup = None
        self.backup_interval = timedelta(hours=12)  # 最小间隔12小时
        
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # 确保备份目录存在
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # 加载上次备份状态
        self.load_state()
    
    def load_state(self):
        """加载备份状态"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    self.last_backup = datetime.fromisoformat(state.get('last_backup', ''))
        except Exception as e:
            self.logger.warning(f"加载状态失败: {e}")
    
    def save_state(self):
        """保存备份状态"""
        try:
            state = {
                'last_backup': self.last_backup.isoformat() if self.last_backup else '',
                'last_check': datetime.now().isoformat()
            }
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"保存状态失败: {e}")
    
    def is_system_idle(self):
        """检测系统是否空闲"""
        try:
            # CPU使用率低于10%
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > 10:
                return False
            
            # 内存使用率低于60%
            memory = psutil.virtual_memory()
            if memory.percent > 60:
                return False
            
            # 检查是否有前台活跃程序
            # 这里可以扩展检查特定程序是否在运行
            active_processes = []
            for proc in psutil.process_iter(['name', 'cpu_percent']):
                try:
                    if proc.info['cpu_percent'] > 5:  # CPU占用超过5%
                        active_processes.append(proc.info['name'])
                except:
                    continue
            
            # 如果有高CPU占用的程序，认为系统忙碌
            if len(active_processes) > 2:  # 允许1-2个活跃进程
                return False
            
            # 网络活动检测（可选）
            network = psutil.net_io_counters()
            if network.bytes_sent > 1024*1024 or network.bytes_recv > 1024*1024:  # 1MB
                return False
            
            return True
            
        except Exception as e:
            self.logger.warning(f"系统状态检测失败: {e}")
            return False
    
    def should_backup(self):
        """判断是否应该备份"""
        now = datetime.now()
        
        # 检查距离上次备份时间
        if self.last_backup and (now - self.last_backup) < self.backup_interval:
            return False
        
        # 检查系统是否空闲
        return self.is_system_idle()
    
    def create_backup(self):
        """创建备份"""
        timestamp = now = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"smart_backup_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            self.logger.info(f"开始创建备份: {backup_name}")
            
            # 创建备份目录
            os.makedirs(backup_path, exist_ok=True)
            
            # 备份工作文件
            file_types = ['*.py', '*.md', '*.jsonc', '*.txt', '*.bat']
            for file_type in file_types:
                for file in os.listdir(self.source_dir):
                    if file.endswith(file_type.replace('*', '')):
                        shutil.copy2(
                            os.path.join(self.source_dir, file),
                            os.path.join(backup_path, file)
                        )
            
            # 备份.opencode目录
            opencode_path = os.path.join(self.source_dir, '.opencode')
            if os.path.exists(opencode_path):
                shutil.copytree(
                    opencode_path,
                    os.path.join(backup_path, '.opencode'),
                    dirs_exist_ok=True
                )
            
            # 生成备份报告
            report_file = os.path.join(backup_path, "backup_report.txt")
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(f"智能备份报告\n")
                f.write(f"{'='*50}\n")
                f.write(f"备份时间: {datetime.now()}\n")
                f.write(f"备份路径: {backup_path}\n")
                f.write(f"备份类型: 智能检测备份\n")
                f.write(f"系统状态: 空闲\n\n")
                
                f.write("备份文件清单:\n")
                for root, dirs, files in os.walk(backup_path):
                    for file in files:
                        f.write(f"{os.path.join(root, file)}\n")
            
            # 更新主备份目录
            main_backup = r"C:\Users\Administrator\Desktop\OpenWork"
            for item in os.listdir(backup_path):
                src = os.path.join(backup_path, item)
                dst = os.path.join(main_backup, item)
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
            
            # 清理过期备份（保留最近5个）
            self.cleanup_old_backups()
            
            # 更新状态
            self.last_backup = datetime.now()
            self.save_state()
            
            self.logger.info(f"备份完成: {backup_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"备份失败: {e}")
            return False
    
    def cleanup_old_backups(self):
        """清理旧备份"""
        try:
            backups = []
            for item in os.listdir(self.backup_dir):
                if item.startswith('smart_backup_') and os.path.isdir(os.path.join(self.backup_dir, item)):
                    backups.append(item)
            
            # 按时间排序，保留最新的5个
            backups.sort(reverse=True)
            for old_backup in backups[5:]:
                old_path = os.path.join(self.backup_dir, old_backup)
                shutil.rmtree(old_path)
                self.logger.info(f"清理旧备份: {old_backup}")
                
        except Exception as e:
            self.logger.warning(f"清理备份失败: {e}")
    
    def run_once(self):
        """运行一次检测"""
        try:
            self.logger.info("执行智能备份检测...")
            
            if self.should_backup():
                self.logger.info("系统空闲，开始备份...")
                success = self.create_backup()
                if success:
                    self.logger.info("智能备份完成")
                else:
                    self.logger.error("智能备份失败")
            else:
                if self.last_backup:
                    hours_since = (datetime.now() - self.last_backup).total_seconds() / 3600
                    self.logger.info(f"系统忙碌或备份间隔未到 (距离上次备份: {hours_since:.1f}小时)")
                else:
                    self.logger.info("系统忙碌，暂不备份")
                    
        except Exception as e:
            self.logger.error(f"智能备份检测异常: {e}")
    
    def start_monitoring(self, check_interval=300):  # 5分钟检测一次
        """启动监控服务"""
        self.logger.info("启动智能备份监控服务...")
        self.logger.info(f"检测间隔: {check_interval}秒")
        self.logger.info(f"备份间隔: {self.backup_interval}")
        
        while True:
            try:
                self.run_once()
                time.sleep(check_interval)
            except KeyboardInterrupt:
                self.logger.info("停止智能备份监控服务")
                break
            except Exception as e:
                self.logger.error(f"监控服务异常: {e}")
                time.sleep(60)  # 出错后等待1分钟再重试

def main():
    """主函数"""
    backup = SmartBackup()
    
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--monitor":
        # 持续监控模式
        backup.start_monitoring()
    else:
        # 单次检测模式
        backup.run_once()

if __name__ == "__main__":
    main()