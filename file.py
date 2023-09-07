def remove_bigger_than(sortedList, biggerThan):
    for item in sortedList:
        if item <= biggerThan:
            yield item
        else:
            break

def remove_smaller_than(sortedList, smallerThan):
    return [x for x in sortedList if x >= smallerThan]

def not_equal_to(number, items):
    for item in items:
        if number == item:
            return False
    
    return True

def is_prime(previousPrimes, number):
    if not_equal_to(number % 10, [1,3,7,9]):
        return False

    divisors = remove_bigger_than(previousPrimes, int(number**0.5))

    for divisor in divisors:
        if number % divisor == 0:
            return False

    return True 

def get_primes(index):
    numbers = [2,3,5,7]

    for i in range(11, index):
        if is_prime(numbers, i):
            numbers.append(i)

    return numbers
