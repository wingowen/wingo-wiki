import os
import shutil

# 源目录和目标目录
source_dir = "/workspace/wingo-wiki/wiki/concepts"
target_dir = "/workspace/content/concepts"

# 确保目标目录存在
os.makedirs(target_dir, exist_ok=True)

# 遍历源目录中的所有子目录和文件
def migrate_content(source, target):
    for root, dirs, files in os.walk(source):
        for file in files:
            if file.endswith(".md"):
                # 构建源文件路径
                source_file = os.path.join(root, file)
                
                # 构建目标文件路径
                # 计算相对路径，去掉 source 前缀
                relative_path = os.path.relpath(source_file, source)
                # 将路径中的子目录转换为文件名的一部分
                target_file_name = relative_path.replace(os.path.sep, "-")
                target_file = os.path.join(target, target_file_name)
                
                # 复制文件
                print(f"迁移: {source_file} -> {target_file}")
                shutil.copy2(source_file, target_file)

# 执行迁移
migrate_content(source_dir, target_dir)

print("迁移完成！")