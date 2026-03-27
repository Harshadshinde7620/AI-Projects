import os
import shutil

src = r"d:\AI Tester\LinkedIn Post Creator"
dest = r"d:\AI Tester\LinkedIn Post Creator\.ai_temp_repo\LinkedIn Post Creator"

os.makedirs(dest, exist_ok=True)

for item in os.listdir(src):
    if item in [".ai_temp_repo", "copy_script.py", ".git"]:
        continue
    
    s = os.path.join(src, item)
    d = os.path.join(dest, item)
    
    if os.path.isdir(s):
        if os.path.exists(d):
            shutil.rmtree(d)
        shutil.copytree(s, d)
    else:
        shutil.copy2(s, d)

print("Copy completed successfully.")
