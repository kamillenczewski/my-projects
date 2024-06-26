from random import randint, choices
from os import remove as os_remove_file
from os import system
from shutil import copyfile

STORAGE_FILE = "STORAGE_FILE.txt"

def remove_file(file_name):
    try:
        os_remove_file(file_name)
    except FileNotFoundError:
        print(f"There is no file with name: '{file_name}'.")

def get_possible_chars():
    possible_small_letters = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    possible_big_letters = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    possible_digits = [str(i) for i in range(10)]
    possible_chars = possible_small_letters + possible_big_letters + possible_digits

    return possible_chars

def chars_to_str(chars):
    return "".join(chars)

def generate_random_string(possible_chars):
    random_length = randint(5, 15)
    random_chars = choices(population=possible_chars, k=random_length)
    string = chars_to_str(random_chars)

    return string

def generate_random_strings(possible_chars, amount):
    return [generate_random_string(possible_chars) for _ in range(amount)]

def generate_file_name(possible_chars):
    return generate_random_string(possible_chars) + ".txt"

def generate_file_names(possible_chars, amount):
    return [generate_file_name(possible_chars) for _ in range(amount)]

def write_file(file_name):
    with open(file_name, "w") as file:
        file.write("X" + "D" * 100)

def write_files(file_names):
    for file_name in file_names:
        write_file(file_name)

def add_new_line_char_to_strings(strings):
    return [string + "\n" for string in strings]

def write_storage_file(file_names):
    with open(STORAGE_FILE, "w") as file:
        for file_name in file_names:
            file.write(file_name + "\n")

def remove_files(file_names):
    for file_name in file_names:
        remove_file(file_name)

def get_files_amount(default_amount=3):
    string = input("Enter files amount: ")
    clear_console()
    
    if string.isdigit():
        number = int(string)
        
        if 0 <= number:
            return number 
        
    return default_amount

def clear_console():
    system("cls")

def get_action_index():
    print("1. Generate files")
    print("2. Undo")

    string = input("Enter an index: ")

    clear_console()

    if string.isdigit():
        index = int(string)

        if 1 <= index <= 2:
            return int(index)
    
    return -1

def read_storage_file():
    with open(STORAGE_FILE, "r") as file:
        lines = file.readlines()

    return [line.replace("\n", "") for line in lines]

def execute_action_1():
    amount = get_files_amount()
    possible_chars = get_possible_chars()
    file_names = generate_file_names(possible_chars, amount)
    write_storage_file(file_names)
    write_files(file_names)

def execute_action_2():
    file_names = read_storage_file()
    remove_files(file_names + [STORAGE_FILE])

def clone_file(new_path, source_file_path=__file__):
    copyfile(source_file_path, new_path)

if __name__ == "__main__":
    match(get_action_index()):
        case 1: execute_action_1()
        case 2: execute_action_2()
    clone_file("XDDDD.py")
