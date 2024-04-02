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

def remove_quantitative_prefix(segment: str) -> tuple[bool, str]:
    for prefix in QUANTITATIVE_PREFIXES:
        if segment.startswith(prefix):
            return segment.removeprefix(prefix)
    
    return segment

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

class MatrixIterator:
    def __init__(self, matrix: Matrix, start_x=0, start_y=0) -> None:
        self.matrix = matrix

        self.current_x = start_x
        self.current_y = start_y

    def move_to_coordinates(self, x, y):
        # diff_x (+) -> right
        # diff_x (-) -> left
        # diff_y (+) -> up
        # diff_y (-) -> down

        diff_x = x - self.current_x
        diff_y = y - self.current_y

        if diff_x > 0:
            for _ in range(abs(diff_x)):
                self.move_right()            
        elif diff_x < 0:
            for _ in range(abs(diff_x)):
                self.move_left()           

        if diff_y > 0:
            for _ in range(abs(diff_y)):
                self.move_up()         
        elif diff_y < 0:
            for _ in range(abs(diff_y)):
                self.move_down()  

    def move_right(self):
        if self.is_x_too_big(self.current_x + 1):
            self.matrix.add_right_column()

        self.current_x += 1

    def move_left(self):
        if self.is_x_too_small(self.current_x - 1):
            self.matrix.add_left_column()
        else:
            self.current_x -= 1

    def move_up(self):
        if self.is_y_too_big(self.current_y + 1):
            self.matrix.add_upper_row()
        
        self.current_y += 1

    def move_down(self):
        if self.is_y_too_small(self.current_y - 1):
            self.matrix.add_lower_row()
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

    def get(self):
        return self.matrix.get(self.current_x, self.current_y)

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

class CoalChainBuilder:
    def __init__(self, hydrogen_amounts_list) -> None:
        self.matrix = Matrix(1, 1, " ")

        self.matrix_iterator = MatrixIterator(self.matrix, 0, 0)

        self.hydrogen_amounts_list = hydrogen_amounts_list
       
        self.coal_x_coordinates = []

    def build(self):
        for index, hydrogen_amount in enumerate(self.hydrogen_amounts_list):
            self.set(COAL)
            self.set_current_coordinates_as_coal_coordinates()
            
            self.build_hydrogen(hydrogen_amount)

            if index != len(self.hydrogen_amounts_list) - 1:
                self.build_bonds()

        return self.matrix, self.coal_x_coordinates, self.matrix_iterator.current_y

    def build_hydrogen(self, hydrogen_amount):
        if hydrogen_amount == 1:
            self.move_right()
            self.set(HYDROGEN)
        elif hydrogen_amount >= 2:
            self.move_right()
            self.set(HYDROGEN)
            self.move_right()

            match(hydrogen_amount):
                case 2:
                    self.set(SUBSCRIPT_2)
                case 3:
                    self.set(SUBSCRIPT_3)        

    def build_bonds(self):
        self.move_right()
        self.move_right()
        self.set(SINGLE_BOND)
        self.move_right()
        self.set(SINGLE_BOND)
        self.move_right()
        self.move_right()        

    def set_current_coordinates_as_coal_coordinates(self):
        self.coal_x_coordinates.append(self.matrix_iterator.current_x)

    def move_right(self):
        self.matrix_iterator.move_right()

    def set(self, item):
        self.matrix_iterator.set(item)

class CoalChainIterator:
    def __init__(self, matrix, coal_x_coordinates, coal_y) -> None:
        self.matrix = matrix
        self.matrix_iterator = MatrixIterator(matrix, coal_x_coordinates[0], coal_y)

        self.coal_y = coal_y
        self.coal_x_coordinates = coal_x_coordinates

        self.current_coal_index = 0

    def reset(self):
        self.current_coal_index = 0
        self.move_to_current_coordinates()

    def move_to_current_coal(self):
        self.move_to_current_coordinates()

    def move_to_next_coal(self):
        self.move_to_coal_index(self.current_coal_index + 1)

    def move_to_coal_index(self, index):
        if self.is_index_valid(index):
            self.current_coal_index = index
            self.move_to_current_coordinates()

    def move_to_current_coordinates(self):
        self.matrix_iterator.move_to_coordinates(self.current_x(), self.current_y())

    def is_index_valid(self, index):
        return 0 < index < len(self.coal_x_coordinates)      

    def current_x(self):
        return self.coal_x_coordinates[self.current_coal_index]

    def current_y(self):
        return self.coal_y

    def set(self, item):
        self.matrix_iterator.set(item)

    def get(self):
        return self.matrix_iterator.get()

    def move_right(self):
        self.matrix_iterator.move_right()

    def move_left(self):
        if self.matrix_iterator.is_x_too_small(self.matrix_iterator.current_x - 1):
            self.increase_x_coordinates()

        self.matrix_iterator.move_left()

    def move_up(self):
        self.matrix_iterator.move_up()

    def move_down(self):
        if self.matrix_iterator.is_y_too_small(self.matrix_iterator.current_y - 1):
            self.coal_y += 1

        self.matrix_iterator.move_down()

    def increase_x_coordinates(self):
        for i in range(len(self.coal_x_coordinates)):
            self.coal_x_coordinates[i] += 1

def add_alkane_group_up(mover: "CoalChainIterator", alkane_group):
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

def add_alkane_group_down(mover: "CoalChainIterator", alkane_group):
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




def add_group_up(mover: "CoalChainIterator", group):
    mover.move_up()
    mover.set("|")
    mover.move_up()

    for char in group:
        mover.set(char)
        mover.move_right()

def add_group_down(mover: "CoalChainIterator", group):
    mover.move_down()
    mover.set("|")
    mover.move_down()

    for char in group:
        mover.set(char)
        mover.move_right()

def add_group_left(mover: "CoalChainIterator", group):
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

def add_group_right(mover: "CoalChainIterator", group):
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



def interprate_compound_name(compound_name):
    splitter = CompoundNameSplitter(compound_name)

    basic_group_items, main_group_items = splitter.split()

    main_group_interpreter = MainGroupInterpreter(main_group_items)

    coal_amount = main_group_interpreter.get_coal_amount()

    coal_indexed_groups = to_coal_indexed_lists_of_groups(basic_group_items, coal_amount)
    
    if main_group_interpreter.has_hydroxyl_group():
        hydroxyl_group_index = main_group_interpreter.get_hydroxyl_group_index()
        coal_indexed_groups[hydroxyl_group_index - 1].append("spc:hydroxyl") # special group hydroxyl group

    hydrogen_amounts = [2 for _ in range(coal_amount)]
    hydrogen_amounts[0] = 3
    hydrogen_amounts[-1] = 3

    for i, groups in enumerate(coal_indexed_groups):
        hydrogen_amounts[i] -= len(groups) 

    matrix, coal_x_coordinates, coal_y = CoalChainBuilder(hydrogen_amounts).build()

    coal_chain_iterator = CoalChainIterator(matrix, coal_x_coordinates, coal_y)

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
                add_element_in_direction(coal_chain_iterator, group, direction)
            elif group.startswith("spc:hydroxyl"):
                add_hydroxyl_group(coal_chain_iterator, direction)
            else:
                add_alkane_group_in_direction(coal_chain_iterator, group, direction)

            coal_chain_iterator.move_to_current_coal()

        coal_chain_iterator.move_to_next_coal()

    bond_index = main_group_interpreter.get_coal_index_of_alkane_bond()
    bond = main_group_interpreter.get_bond_type()

    coal_chain_iterator.move_to_coal_index(bond_index)

    coal_chain_iterator.move_right()

    if coal_chain_iterator.get() == HYDROGEN:
        coal_chain_iterator.move_right()

        if coal_chain_iterator.get() != " ":
            coal_chain_iterator.move_right()

    coal_chain_iterator.move_right()
    coal_chain_iterator.set(bond)
    coal_chain_iterator.move_right()
    coal_chain_iterator.set(bond)

    return matrix

COMPOUNDS = [
    "4-bromo-1,2-dichloro-7-etylo-3,3,7-trimetylo-5,5-dipropylonon-6-yn-6-ol",
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
    compound = "1,2-dichloro-2,3-dibromobutan"
    matrix = interprate_compound_name(compound)
    matrix.print()

def main2():
    compound = input("Enter a name of the compound: ")
    matrix = interprate_compound_name(compound)
    print()
    matrix.print()   

if __name__ == "__main__":
    main1()