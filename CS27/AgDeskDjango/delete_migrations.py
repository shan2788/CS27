import os
import shutil

# Path to the directory where this script is located (assumed to be the web folder)
dir_path = os.path.dirname(os.path.realpath(__file__))

# Walk through the directory structure
for subdir, dirs, files in os.walk(dir_path, followlinks=False, topdown=False):
    # Check if the current directory is a 'migrations' directory
    if subdir.endswith('migrations'):
        # Delete files except '__init__.py'
        for file in files:
            if file != '__init__.py':
                filepath = os.path.join(subdir, file)
                print(f"Deleting: {filepath}")
                os.remove(filepath)
                
        # Ensure '__init__.py' exists
        init_path = os.path.join(subdir, '__init__.py')
        if not os.path.exists(init_path):
            print(f"Creating: {init_path}")
            open(init_path, 'a').close()  # 'a' mode creates the file if it doesn't exist

    # Additionally, check for and delete '__pycache__' directories
    for dir in dirs:
        if dir == '__pycache__':
            pycache_path = os.path.join(subdir, dir)
            print(f"Removing directory: {pycache_path}")
            shutil.rmtree(pycache_path)

