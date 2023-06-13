import sys
from pathlib import Path

from normalize import normalize

import shutil

CATEGORIES = {"Audio":['.mp4','.aiff'],
              "Documents":['.doc','.txt','.pdf'],
              "Images": ['.jpg','jpeg']
              }

def move_file(file:Path,root_dir:Path, categorie:str) ->None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        print(f"Make{target_dir}")
        target_dir.mkdir()
    

    file.replace(target_dir.joinpath(f"{normalize(file.stem)}{file.suffix}"))

def get_categories(file:Path)->str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    
    return 'Other'

def sort_folder(path: Path) -> None:
     for item in path.glob("**/*"):
         print(item.is_dir(),item.is_file())
         if item.is_file():
           cat = get_categories(item)
           move_file(item,path,cat)



def delete_empty_folder(path:Path) ->None:
    for item in path.glob('**/*'):
        if item.is_dir() and not any(item.iterdir()):
            item.rmdir() 

            print(f"Empty folder is deleted")
        


def unpack_archive(path:Path) ->None:
    destination_dir = path.parent
    shutil.unpack_archive(path,destination_dir)
    
    



def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"
    
    if not path.exists():
        return f"Folder with path{path} does not exist"
    
    sort_folder(path)
    delete_empty_folder(path)
    unpack_archive(path)
    
    
    return " All ok"
    
if __name__ == '__main__':
    print(main())