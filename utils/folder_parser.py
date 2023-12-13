import os

def run_fast_scandir(dir, ext) -> list:    # dir: str, ext: list
    subfolders, files = [], []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                files.append(f.path)


    for dir in list(subfolders):
        sf, f = run_fast_scandir(dir, ext)
        subfolders.extend(sf)
        files.extend(f)
    return subfolders, files


def scan_sub_dirs(dir) -> list:
    subfolders = []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append({"path":f.path,"name":f.name})
    
    return subfolders

def scan_videofiles(dir,ext) -> list:
    files = []

    for f in os.scandir(dir):
        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                files.append({"path":f.path,"name":f.name})
    
    return files

