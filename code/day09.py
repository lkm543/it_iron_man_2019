def hash(input):
    hash_number = 512
    for char in input:
        hash_number *= ord(char)
        hash_number += 3
        hash_number %= 1024
    hash_number *= len(input)
    hash_number %= 1024
    return hash_number

if __name__ == "__main__":
    print(hash("Hello World!"))
    print(hash("Bill Gates"))
    print(hash("100000000"))
