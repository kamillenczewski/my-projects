from os import listdir as get_files_from_dir
from os import mkdir as create_dir
from random import randint, choice
from os import path as path_lib
from os import system

from files_generator import ( 
    write_file, 
    get_possible_chars,
    generate_random_strings,
    clone_file
)

def join_path(*paths):
    return path_lib.join(*paths)

def is_dir(path):
    return path_lib.isdir(path)

def zero_or_one():
    return randint(0, 1)

def create_file_or_dir(path):
    match(zero_or_one()):
        case 0:
            path += ".txt"
            write_file(path)
        case 1:
            create_dir(path)
        
def fill_dir(possible_chars, path, depth):
    dir_size = randint(2, 7)
    strings = generate_random_strings(possible_chars, dir_size)
    full_paths = [join_path(path, string) for string in strings]

    for full_path in full_paths:
        create_file_or_dir(full_path)

    dir_paths = [full_path for full_path in full_paths if is_dir(full_path)]

    depth -= 1

    if depth == 0: return 

    for dir_path in dir_paths:
        fill_dir(possible_chars, dir_path, depth)

def find_all_dirs(path):
    file_names = get_files_from_dir(path)
    file_names = [join_path(path, file_name) for file_name in file_names]
    
    dir_paths = [file_name for file_name in file_names if is_dir(file_name)]

    new_dir_path = []

    for dir_path in dir_paths:
        new_dir_path.extend(find_all_dirs(dir_path))

    return dir_paths + new_dir_path

def main():
    possible_chars = get_possible_chars()
    fill_dir(possible_chars, "XDD", 2)
    # dir_paths = find_all_dirs("XDD")
    # random_dir_path = choice(dir_paths)
    # clone_file(join_path(random_dir_path, "ELO.py"), __file__)

def main1():
    dir_paths = find_all_dirs("XDD")
    random_dir_path = choice(dir_paths)
    clone_file(join_path(random_dir_path, "ELO.py"), __file__)
    system("catalog_generator.py")

if __name__ == "__main__":
    main1()
