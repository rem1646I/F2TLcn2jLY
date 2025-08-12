# 代码生成时间: 2025-08-12 15:24:16
# folder_organizer.py

import os
import shutil
from bottle import route, run, request, template

# 文件夹结构整理器的配置信息
class FolderOrganizer:
    def __init__(self, source_dir, dest_dir):
        """初始化文件夹结构整理器
        
        Args:
            source_dir (str): 源文件夹路径
            dest_dir (str): 目标文件夹路径
        """
        self.source_dir = source_dir
        self.dest_dir = dest_dir

    def organize(self):
        """整理文件夹结构
        
        Returns:
            bool: 整理成功返回True，否则返回False
        """
        try:
            for item in os.listdir(self.source_dir):
                source_path = os.path.join(self.source_dir, item)
                dest_path = os.path.join(self.dest_dir, item)
                
                # 如果是文件夹，则递归整理
                if os.path.isdir(source_path):
                    if not os.path.exists(dest_path):
                        os.makedirs(dest_path)
                    self.organize_subfolder(source_path, dest_path)
                else:
                    # 如果是文件，则移动到目标文件夹
                    shutil.move(source_path, dest_path)
            return True
        except Exception as e:
            print(f"Error organizing folders: {e}")
            return False

    def organize_subfolder(self, source_subfolder, dest_subfolder):
        "