def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return(fib(n-1) + fib(n-2))

def reverse(word:str):
    if len(word) < 2:
        return word
    return reverse(word[1:]) + word[0]

def sum_nested(list1:list):
    i = 0
    final = 0
    while i < len(list1):
        if isinstance(list1[i], list):
            final += sum_nested(list1[i])
        else:
            final += list1[i]
        i += 1
    return final

def flatten(list1:list):
    i = 0
    final = []
    while i < len(list1):
        if isinstance(list1[i], list):
            final = final + flatten(list1[i])
        else:
            final.append(list1[i])
        i += 1
    return final

def binary_search(list1:list,number:int):
    if len(list1) == 0:
        return False
    if list1[0] == number:
        return True
    j = binary_search(list1[1:],number)
    if j == True:
        return True
    elif j == False:
        return False

def power(n:int,exponent:int):
    if exponent == 0:
        return 1
    if exponent == 1:
        return n
    final = n * power(n,exponent-1)
    return final

def is_palindrome(word:list):
    revered = reverse(word)
    if revered == word:
        return True
    else:
        return False



print("\n=== Palindrome ===")
print(is_palindrome("racecar"))    # True
print(is_palindrome("hello"))      # False
print(is_palindrome("a"))          # True
print(is_palindrome("abba"))       # True
print(is_palindrome("abcba"))      # True
print(is_palindrome("ab"))         # False