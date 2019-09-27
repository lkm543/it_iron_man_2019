import random

def string_to_bytes(input):
    input = bytearray(input, 'utf-8')
    result = ""
    for byte in input:
        for i in range(7, -1, -1):
            result += str((byte >> i) & 1)
    return result

def bytes_to_string(input):
    result = ""
    for idx in range(0, int(len(input)/8)):
        binary = input[8*idx:8*(idx+1)]
        result += chr(int(binary, 2))
    return result

def generate_key(length):
    key = ""
    for i in range(0, length):
        key += str(random.randint(0, 1))
    return key

def xor_operation(text, key):
    if text == key:
        return "0"
    else:
        return "1"

def xor_en_decrypt(text, key):
    result = ""
    len_txt = len(text)
    len_key = len(key)
    for idx in range(0, len_txt):
        if idx >= len_key:
            key_idx = idx % len_key
        else:
            key_idx = idx
        xor_result = xor_operation(text[idx], key[key_idx])
        result += xor_result
    return result


if __name__ == "__main__":
    message = "XOR Cipher!"
    print(f"Origin message: {message}")
    message = string_to_bytes(message)
    print(f"Message in binary: {message}")

    key = generate_key(len(message))
    print(f"Key: {key}")

    encryption = xor_en_decrypt(message, key)
    print(f"Encryption: {encryption}")

    decryption = xor_en_decrypt(encryption, key)
    print(f"Decryption: {decryption}")

    text = bytes_to_string(decryption)
    print(f"Text: {text}")
