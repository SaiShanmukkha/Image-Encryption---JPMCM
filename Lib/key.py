def generate_prime_key_one(k1, k2, k3):
    t = int(k3, 2)
    t_prime = t%120
    k_2 = k2[120-t_prime:] + k2[:120-t_prime]
    key = int(k1, 2) ^ int(k_2, 2) ^ int(k3, 2)
    return bin(key)[2:].zfill(120)

def generate_prime_key_two(k1, k2, k3):
    t = int(k3, 2)
    t_prime = t%120
    k_1 = k1[120-t_prime:] + k1[:120-t_prime]
    key = int(k_1, 2) ^ int(k2, 2) ^ int(k3, 2)
    return bin(key)[2:].zfill(120)

def generate_values_from_key(SECRET_KEY):
    val_gen = ""
    for char in SECRET_KEY:
        val_gen += bin(ord(char))[2:].zfill(8)
    k1 = val_gen[:120]
    k2 = val_gen[120:240]
    k3 = val_gen[240:]
    k1_prime = generate_prime_key_one(k1, k2, k3)
    k2_prime = generate_prime_key_two(k1, k2, k3)
    return [k1_prime, k2_prime]

def generate_JPDF_parameters(subkey):
    val_list = generate_values_from_key(subkey)
    res = dict()
    for idx, key in enumerate(val_list):
        res[f"g{idx}"] = key[:24]
        res[f"d{idx}"] = key[24:]
    return res

def generate_scrambling_values(bin_data, M, N):
    sc_val = dict()
    sc_val["MP"] = (int(bin_data[:8], 2)%M)+1
    sc_val["NP"] = (int(bin_data[8:16], 2)%N)+1
    sc_val["MStep"] = int(bin_data[16:20], 2)
    sc_val["NStep"] = int(bin_data[20:], 2)
    return sc_val
    
def generate_chaotic_mapping_values(bin_data):
    fh = bin_data[:48]
    lh = bin_data[48:]
    x = int(fh,2)/(2**48)
    mu = 3.96+(int(lh,2)%0.04)
    return { 
        "x" : 0.19870228,
        "mu": 3.99999999
    }
    

# if __name__ == "__main__":
#     SECRET_KEY = "T3RTqXCNwUaIraqIbixsvzYb1W340ZXK"
#     res_dict = generate_JPDF_parameters(SECRET_KEY)
#     print(res_dict)