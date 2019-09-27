from random import sample

def txt_shift(txt, shift):
    result = ""
    for idx in range(0, len(txt)):
        char = txt[idx]
        if char.isalpha():
            order = ord(char)
            if char.isupper():
                order -= 65
                order = shift[order]
                order += 65
            elif char.islower():
                order -= 97
                order = shift[order]
                order += 97
            char = chr(order)
        result += char
    return result

def mono_encryption(txt, shift):
    return txt_shift(txt, shift)

def mono_decryption(txt, shift):
    inverse_shift = [0] * 26
    for idx, value in enumerate(shift):
        inverse_shift[value] = idx
    return txt_shift(txt, inverse_shift)

plain_txt = "Hello!"
shift_list = sample(range(0,26), 26)

print(f"原始明文: {plain_txt}")
print(f"Monoalphabet: {shift_list}")
cipher_txt = mono_encryption(plain_txt, shift_list)
print(f"加密密文: {cipher_txt}")
decryption_cipher_txt = mono_decryption(cipher_txt, shift_list)
print(f"解密結果: {decryption_cipher_txt}")
