from typing import Any


QUANTITATIVE_PREFIXES = ["di", "tri", "tetra"]
ALKANE_PREFIXES = ["met", "et", "prop", "but", "pent", "heks", "hept", "okt", "non", "dek"]

GROUPS_AND_SYMBOLS = {"bromo":"Br", "chloro":"Cl", "enylo":"En"}
DASH = '-'

SINGLE_BOND = "-"
DOUBLE_BOND = "="
TRIPLE_BOND = "\u2261"

SUBSCRIPT_2 = "\u2082"
SUBSCRIPT_3 = "\u2083"

COAL = "C"
HYDROGEN = "H"

ALKANE_GROUPS_AND_COAL_AMOUNTS = {"metylo":1, "etylo":2, "propylo":3, "butylo":4}

ALKANE_SUFFIXES_AND_BONDS = {"an":SINGLE_BOND, "en":DOUBLE_BOND, "yn":TRIPLE_BOND}

def get_symbol(group):
    return GROUPS_AND_SYMBOLS[group]

def alkane_group_to_coal_amount(alkane_group):
    return ALKANE_GROUPS_AND_COAL_AMOUNTS[alkane_group]

def is_element(string):
    return string in GROUPS_AND_SYMBOLS

def alkane_prefix_to_coal_amount(alkane_prefix):
    return ALKANE_PREFIXES.index(alkane_prefix) + 1

def get_bond(alkane_suffix):
    return ALKANE_SUFFIXES_AND_BONDS[alkane_suffix]

class CompoundNameSplitter:
    def __init__(self, compound_name) -> None:
        self.compound_name = compound_name
        self.items = []
        self.basic_group_items = []
        self.main_group_items = []

    def split(self):
        self.remove_space()
        self.items = self.split_by_dash()
        index, prefix = self.get_start_index_and_prefix_with_main_group()

        if index == -1:
            self.error_compound_not_contains_main_alkane()

        self.basic_group_items = self.items[:index]
        self.main_group_items = self.items[(index + 1):]

        main_alkane_group = self.items[index]

        self.add_last_basic_group_and_first_main_group(main_alkane_group, prefix)

        return self.basic_group_items, self.main_group_items

    def error_compound_not_contains_main_alkane(self):
        raise ValueError("The compound doesn't contain main alkane!")

    def add_last_basic_group_and_first_main_group(self, main_alkane_group: str, prefix):
        last_basic_group = main_alkane_group.removesuffix("an").removesuffix(prefix)
        self.basic_group_items.append(last_basic_group)

        # adding first main group   

        if main_alkane_group.endswith("an"):
            self.main_group_items.insert(0, "an")
            self.main_group_items.insert(0, "1")

        self.main_group_items.insert(0, prefix)

    def remove_space(self):
        self.compound_name.replace(" ", "")

    def split_by_dash(self):
        return self.compound_name.split(DASH)

    def get_start_index_and_prefix_with_main_group(self):
        for i in range(len(self.items) - 1, -1, -1):
            item_with_alkane_suffix = self.items[i]
            item_without_suffix_an = self.items[i].removesuffix("an")

            for prefix in ALKANE_PREFIXES:
                if item_with_alkane_suffix.endswith(prefix) or item_without_suffix_an.endswith(prefix):
                    return i, prefix
                
        return -1, None

def remove_quantitative_prefix(segment: str) -> tuple[bool, str]:
    for prefix in QUANTITATIVE_PREFIXES:
        if segment.startswith(prefix):
            return segment.removeprefix(prefix)
    
    return segment

class Matrix:
    def __init__(self, height, length, default_item):
        self.height = height
        self.length = length
        self.default_item = default_item
        self.items = self.create_items()

    def get_row(self, y):
        return self.items[y]

    def create_items(self):
        return [self.create_row() for _ in range(self.height)]

    def create_row(self):
        return [self.default_item for _ in range(self.length)]

    def set(self, x, y, item):
        self.items[y][x] = item

    def get(self, x, y):
        return self.items[y][x]
    
    def remove_empty_sequence(self, x):
        coordinates_to_remove = []

        for y, row in enumerate(self.items):
            x_to_remove = -1

            if row[x] == self.default_item:
                x_to_remove = x
            elif row[x + 1] == self.default_item:
                x_to_remove = x + 1
            elif row[x - 1] == self.default_item:
                x_to_remove = x - 1
            else:
                return

            coordinates_to_remove.append((x_to_remove, y))

        for x1, y1 in coordinates_to_remove:
            self.items[y1].pop(x1)

        self.length -= 1

    def remove_empty_column(self, x):
        if self.is_empty_column(x):
            self.remove_column(x)

    def is_empty_column(self, x):
        for row in self.items:
            if row[x] != self.default_item:
                return False
        
        return True

    def remove_column(self, x):
        for row in self.items:
            row.pop(x)

    def add_right_column(self):
        for row in self.items:
            row.append(self.default_item)
        
        self.length += 1

    def add_left_column(self):
        for row in self.items:
            row.insert(0, self.default_item)

        self.length += 1

    def add_upper_row(self):
        self.items.append(self.create_row())
        self.height += 1

    def add_lower_row(self):
        self.items.insert(0, self.create_row())
        self.height += 1

    def print(self):
        for row in self.items:
            string = "".join(row)
            print(string)
    
class MatrixMover:
    def __init__(self, matrix: Matrix, coal_x, coal_y, max_coal_index=1) -> None:
        self.matrix = matrix

        self.coal_x = coal_x
        self.coal_y = coal_y

        self.current_x = self.coal_x
        self.current_y = self.coal_y

        self.current_coal_index = 1
        self.max_coal_index = max_coal_index

    def move_to_coal_index(self, index):
        if not self.is_coal_index_valid(index):
            return

        if index - self.current_coal_index < 0:
            for i in range(self.current_coal_index - index):
                self.move_to_previous_coal()
        else:
            for i in range(index - self.current_coal_index):
                self.move_to_next_coal()            

    def is_coal_index_valid(self, index):
        return  1 <= index <= self.max_coal_index

    def move_right(self):
        if self.is_x_too_big(self.current_x + 1):
            self.matrix.add_right_column()

        self.current_x += 1

    def move_left(self):
        if self.is_x_too_small(self.current_x - 1):
            self.matrix.add_left_column()
            self.coal_x += 1
        else:
            self.current_x -= 1

    def move_up(self):
        if self.is_y_too_big(self.current_y + 1):
            self.matrix.add_upper_row()
        
        self.current_y += 1

    def move_down(self):
        if self.is_y_too_small(self.current_y - 1):
            self.matrix.add_lower_row()
            self.coal_y += 1
        else:
            self.current_y -= 1

    def is_x_too_big(self, x):
        return x >= self.matrix.length
    
    def is_x_too_small(self, x):
        return x < 0
    
    def is_y_too_big(self, y):
        return y >= self.matrix.height
    
    def is_y_too_small(self, y):
        return y < 0

    def set(self, item):
        self.matrix.set(self.current_x, self.current_y, item)

    def move_to_previous_coal(self):
        self.set_previous_coal_coordinates()
        self.move_to_current_coal()        

    def set_previous_coal_coordinates(self):
        self.coal_x -= 7

    def move_to_next_coal(self):
        self.set_next_coal_coordinates()
        self.move_to_current_coal()

    def move_to_current_coal(self):
        self.current_x = self.coal_x
        self.current_y = self.coal_y

    def set_next_coal_coordinates(self):
        self.coal_x += 7

def add_alkane_group_up(mover: MatrixMover, alkane_group):
    coal_amount = alkane_group_to_coal_amount(alkane_group)
    
    for _ in range(coal_amount - 1):
        mover.move_up()
        mover.set("|")
        mover.move_up()

        mover.set("C")
        mover.move_right()
        mover.set("H")
        mover.move_right()
        mover.set(SUBSCRIPT_2)
        mover.move_left()
        mover.move_left()

    mover.move_up()
    mover.set("|")
    mover.move_up()

    mover.set("C")
    mover.move_right()
    mover.set("H")
    mover.move_right()
    mover.set(SUBSCRIPT_3)

def add_alkane_group_down(mover: MatrixMover, alkane_group):
    coal_amount = alkane_group_to_coal_amount(alkane_group)
    
    for _ in range(coal_amount - 1):
        mover.move_down()
        mover.set("|")
        mover.move_down()

        mover.set("C")
        mover.move_right()
        mover.set("H")
        mover.move_right()
        mover.set(SUBSCRIPT_2)
        mover.move_left()
        mover.move_left()

    mover.move_down()
    mover.set("|")
    mover.move_down()

    mover.set("C")
    mover.move_right()
    mover.set("H")
    mover.move_right()
    mover.set(SUBSCRIPT_3)




def add_group_up(mover: MatrixMover, group):
    mover.move_up()
    mover.set("|")
    mover.move_up()

    for char in group:
        mover.set(char)
        mover.move_right()

def add_group_down(mover: MatrixMover, group):
    mover.move_down()
    mover.set("|")
    mover.move_down()

    for char in group:
        mover.set(char)
        mover.move_right()

def add_group_left(mover: MatrixMover, group):
    mover.move_left()
    mover.move_left()
    mover.set("-")
    mover.move_left()
    mover.set("-")
    mover.move_left()
    mover.move_left()

    for char in group[::-1]:
        mover.set(char)
        mover.move_left()

def add_group_right(mover: MatrixMover, group):
    mover.move_right()
    mover.move_right()
    mover.move_right()
    mover.move_right()
    mover.set("-")
    mover.move_right()
    mover.set("-")
    mover.move_right()
    mover.move_right()

    for char in group:
        mover.set(char)
        mover.move_right()

def create_matrix_and_mover(coal_amount):
    height = 5
    length = coal_amount * 3 + (coal_amount - 1) * 4

    coal_x = 0
    coal_y = 2

    matrix = Matrix(height, length, " ")
    mover = MatrixMover(matrix, coal_x, coal_y, coal_amount)

    items = matrix.items

    items[2][0::7] = ["C" for _ in range(len(items[2][0::7]))]
    items[2][1::7] = ["H" for _ in range(len(items[2][1::7]))]
    items[2][2::7] = ["0" for _ in range(len(items[2][2::7]))]
    items[2][4::7] = ["-" for _ in range(len(items[2][4::7]))]
    items[2][5::7] = ["-" for _ in range(len(items[2][5::7]))] 

    return matrix, mover

def add_element_in_direction(mover, group, direction):
    symbol = get_symbol(group)

    match(direction):
        case "up":
            add_group_up(mover, symbol)
        case "down":
            add_group_down(mover, symbol)
        case "right":
            add_group_right(mover, symbol)
        case "left":
            add_group_left(mover, symbol)

def add_alkane_group_in_direction(mover, group, direction):
    match(direction):
        case "up":
            add_alkane_group_up(mover, group)
        case "down":
            add_alkane_group_down(mover, group)

def add_hydroxyl_group(mover, direction):
    match(direction):
        case "up":
            add_group_up(mover, "OH")
        case "down":
            add_group_down(mover, "OH")
        case "right":
            add_group_right(mover, "OH")
        case "left":
            add_group_left(mover, "OH")

def to_coal_indexed_lists_of_groups(basic_group_items, coal_amount):
    numbers_lists = basic_group_items[::2]
    group_names = basic_group_items[1::2]

    numbers_lists = [[int(char) for char in numbers.split(',')] for numbers in numbers_lists]

    coal_indexed_groups = [[] for _ in range(coal_amount)]

    for numbers, group in zip(numbers_lists, group_names):
        group = remove_quantitative_prefix(group)

        for number in numbers:
            coal_indexed_groups[number - 1].append(group)

    return coal_indexed_groups

class MainGroupInterpreter:
    def __init__(self, main_group_items) -> None:
        self.main_group_items = main_group_items

    def get_coal_amount(self):
        return alkane_prefix_to_coal_amount(self.get_main_alkane())
    
    def get_main_alkane(self):
        return self.main_group_items[0]

    def get_alkane_suffix(self):
        return self.main_group_items[2]
    
    def get_coal_index_of_alkane_bond(self):
        return int(self.main_group_items[1])

    def get_bond_type(self):
        return get_bond(self.get_alkane_suffix())
    
    def get_hydroxyl_group_index(self):
        return int(self.main_group_items[3])

    def has_hydroxyl_group(self):
        return len(self.main_group_items) == 5 and self.main_group_items[4] == "ol"

def interprate_compound_name(compound_name):
    splitter = CompoundNameSplitter(compound_name)

    basic_group_items, main_group_items = splitter.split()

    main_group_interpreter = MainGroupInterpreter(main_group_items)

    coal_amount = main_group_interpreter.get_coal_amount()

    coal_indexed_groups = to_coal_indexed_lists_of_groups(basic_group_items, coal_amount)
    
    hydroxyl_group_index = main_group_interpreter.get_hydroxyl_group_index()
    if main_group_interpreter.has_hydroxyl_group():
        coal_indexed_groups[hydroxyl_group_index - 1].append("spc:hydroxyl") # special group hydroxyl group


    matrix, mover = create_matrix_and_mover(coal_amount)


    for coal_index, groups in enumerate(coal_indexed_groups):
        directions = ["up", "down"]

        if coal_index == 0:
            directions.append("left")
        elif coal_index == len(coal_indexed_groups) - 1:
            directions.append("right")

        for group in groups:
            direction = directions[0]
            directions.pop(0)

            if is_element(group):
                add_element_in_direction(mover, group, direction)
            elif group.startswith("spc:hydroxyl"):
                add_hydroxyl_group(mover, direction)
            else:
                add_alkane_group_in_direction(mover, group, direction)

            mover.move_to_current_coal()

        mover.move_to_next_coal()

    hydrogen_amounts = [2 for _ in range(coal_amount)]
    hydrogen_amounts[0] = 3
    hydrogen_amounts[-1] = 3

    for i, groups in enumerate(coal_indexed_groups):
        hydrogen_amounts[i] -= len(groups) 

    columns_to_remove = []

    for hydrogen_amount in hydrogen_amounts[::-1]:
        mover.move_to_previous_coal()
        mover.move_right()
        mover.move_right()

        match(hydrogen_amount):
            case 0:
                columns_to_remove.append(mover.current_x)
                columns_to_remove.append(mover.current_x)
                mover.set(" ")
                mover.move_left()
                mover.set(" ")
            case 1:
                columns_to_remove.append(mover.current_x)
                mover.set(" ")
            case 2:
                mover.set(SUBSCRIPT_2)
            case 3:
                mover.set(SUBSCRIPT_3)

    # Setting bond

    bond_index = main_group_interpreter.get_coal_index_of_alkane_bond()
    bond = main_group_interpreter.get_bond_type()

    mover.move_to_coal_index(bond_index)
    mover.move_right() # H
    mover.move_right() # 2
    mover.move_right() # 
    mover.move_right() # -
    mover.set(bond)
    mover.move_right()
    mover.set(bond)

    for x in columns_to_remove:
        matrix.remove_empty_sequence(x)

    return matrix

COMPOUNDS = [
    "4-bromo-1,2-dichloro-7-etylo-3,3,7-trimetylonon-5-en-4-ol",
    "4-bromo-1,2-dichloro-7-etylo-3,3,7-trimetylononan",
    "1,2-dichloro-2,3-dibromobutan",
    "2,3,4-tribromo-2,3,4,5-tetrachloro-5-etylodekan",
    "4,4-dibromo-5-chloro-3,3,6,6-tetrametylooktan",
    "1,2-dienylo-4,4-dibromo-5-chloro-3,3,6,6-tetrametylooktan",
    
]

def main():
    for compound in COMPOUNDS:
        matrix = interprate_compound_name(compound)
        matrix.print()
        print()


def main1():
    compound = "4-bromo-1,2-dichloro-7-etylo-3,3,7-trimetylo-5,5-dipropylonon-5-yn-6-ol" 
    matrix = interprate_compound_name(compound)
    matrix.print()

def main2():
    compound = input("Enter a name of the compound: ")
    matrix = interprate_compound_name(compound)
    print()
    matrix.print()   

if __name__ == "__main__":
    main1()