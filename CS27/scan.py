import os
import ast
import sys
import pkgutil

PROJECT_DIR = "."  # 项目根目录，可改为绝对路径

# 内置模块集合（可选过滤）
builtin_modules = set(sys.builtin_module_names)
builtin_modules.update(pkgutil.iter_modules([os.path.dirname(sys.executable)]))

found_modules = set()

def extract_imports_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except Exception:
            return  # 忽略无法解析的文件
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    found_modules.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    found_modules.add(node.module.split('.')[0])

for root, _, files in os.walk(PROJECT_DIR):
    for file in files:
        if file.endswith(".py"):
            extract_imports_from_file(os.path.join(root, file))

# 去掉内置模块（可选）
filtered_modules = sorted(m for m in found_modules if m not in builtin_modules)

# 输出结果
print("🧪 Imported packages found in project:")
for mod in filtered_modules:
    print(mod)
