def alpha_to_number(letter):
    return ord(letter) - 64

def convert_letter(letter):
    number = alpha_to_number(letter)
    right = number % 5
    left = (number - right) // 5
    return "|" * left + "." * right

def convert_word(word):
    return "   ".join([convert_letter(char) for char in word])

def convert_sentence(sentence: str):
    words = sentence.split()
    return "-" + "/".join([convert_word(word) for word in words]) + "-"

print(convert_sentence("ALA MA KOTA"))
