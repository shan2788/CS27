"""
This is a little python script to delete all of the Django migration files.

It was becoming a reccuring theme.
"""

# Imports
import os


# Functions
def empty_target_dirs(start, target):
    paths = []
    for root, dirs, files in os.walk(start):
        # print(f"{root = }, {dirs = }, {files = }")
        if root.endswith(target): paths.append(root)

    print(f"The following {'{'}{target}{'}'} directories have been found:")
    for path in paths:
        print(f"- {path}")
    if input("Are you sure you want to empty these directories? (y/n)\n> ").lower() != "y": return

    for path in paths:
        empty_dir(path)


def empty_dir(dir):
    for root, dirs, files in os.walk(dir):
        for name in files:
            if (name != "__init__.py"):
                os.remove(f"{root}\\{name}")


# Main
if __name__ == "__main__":
    empty_target_dirs(".\\AgDeskDjango", "migrations")
