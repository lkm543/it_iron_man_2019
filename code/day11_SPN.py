import random 

def generate_key(key, rounds):
    key += key
    keys = []
    for idx in range(rounds):
        key_this_round = key[4*idx+4:4*idx+20]
        keys.append(key_this_round)
    return keys

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

def substitution(input, s_box):
    output = ""
    for idx in range(4):
        data = input[4*idx:4*(idx+1)]
        number = int(data, 2)
        number_substitution = s_box[number]
        # Convert to binary string
        # ex: 9 -> "1001"
        binary_number = ""
        for i in range(3, -1, -1):
            binary_number += str((number_substitution >> i) & 1)

        output += binary_number
    return output

def permutation(input, p_box):
    output = list("0" * 16)
    for idx, value in enumerate(p_box):
        output[value] = input[idx]
    return "".join(output)

def spn_encrypt(text, rounds, key, s_box, p_box):
    output = text
    for idx in range(rounds):
        output = xor_en_decrypt(output, key[idx])
        output = substitution(output, s_box)
        output = permutation(output, p_box)
    output = xor_en_decrypt(output, key[rounds])
    return output

def spn_decrypt(text, rounds, key, s_box, p_box):
    output = text
    s_box_inverse = [0]*16
    p_box_inverse = [0]*16
    for idx in range(16):
        s_box_inverse[s_box[idx]] = idx
        p_box_inverse[p_box[idx]] = idx
    for idx in range(rounds):
        output = xor_en_decrypt(output, key[rounds-idx])
        output = permutation(output, p_box_inverse)
        output = substitution(output, s_box_inverse)
    output = xor_en_decrypt(output, key[0])
    return output

if __name__ == '__main__':
    rounds = 3
    key = "1011101000111110"
    keys = generate_key(key, rounds + 1)
    print(f"初始金鑰： {key}")
    print(f"產生金鑰： {keys}")

    s_box = random.sample(range(0, 16), 16)
    print(f"s_box： {s_box}")
    p_box = random.sample(range(0, 16), 16)
    print(f"p_box： {p_box}")

    message = "1001001110100101"
    print(f"原始明文： {message}")
    encryption = spn_encrypt(message, rounds, keys, s_box, p_box)
    print(f"加密密文： {encryption}")
    decryption = spn_decrypt(encryption, rounds, keys, s_box, p_box)
    print(f"原始明文： {decryption}")
