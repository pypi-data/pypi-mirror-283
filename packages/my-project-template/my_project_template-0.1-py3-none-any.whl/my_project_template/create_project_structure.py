import os
import shutil

def create_structure():
    src = os.path.join(os.path.dirname(__file__), 'template')
    dst = os.getcwd()

    if os.path.exists(src):
        try:
            shutil.copytree(src, dst, dirs_exist_ok=True)
            print("Project structure created successfully.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Template directory not found.")
