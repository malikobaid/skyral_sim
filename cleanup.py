import os
import shutil

for root, dirs, files in os.walk("."):
    for file in files:
        if file.startswith("._") or file == ".DS_Store":
            os.remove(os.path.join(root, file))
    for dir in dirs:
        if dir == "__MACOSX":
            shutil.rmtree(os.path.join(root, dir))