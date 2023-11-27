from PIL import Image
import numpy as np
from Lib import key
from Lib import JS_Mapping
from Lib import JS_Scramble
from Lib import row_cm
from Lib import col_cm


def gen_rgb():
    a = [[ 1,  2,  3,  4],
        [ 5,  6,  7,  8],
        [ 9, 10, 11, 12],
        [13, 14, 15, 16]]
    
    a = np.array(a)

    lst = [a,a,a]

    rb = np.stack(lst, axis=-1)

    print(rb)
    return rb

# Assuming other functions and modules (key, JS_Mapping, JS_Scramble, row_cm, col_cm) are already defined as per your provided code

def encrypt_decrypt_channel(channel_data, secret_key, encrypt=True):
    M, N = channel_data.shape
    JPDF_values = key.generate_JPDF_parameters(secret_key)
    # print(JPDF_values)
    input_data = channel_data
    
    range_func = range(2)  # for encryption

    for idx in range_func:
        # Josephus Scrambling
        sc_val = key.generate_scrambling_values(JPDF_values[f"g{idx}"], M, N)
        mapping = JS_Mapping.generate_mapping(M, N, **sc_val)
        scrambled_data = JS_Scramble.scramble_image(mapping, input_data)

        # Chaotic Mapping
        cm_val = { 
        "x" : 0.19870228,
        "mu": 3.99999999
        }

        rimage = row_cm.switch_rows(cm_val["mu"], cm_val["x"], np.array(scrambled_data))
        cimage = col_cm.switch_columns(cm_val["mu"], cm_val["x"], rimage)
        input_data = cimage

    return input_data

def edec_channel(channel_data, secret_key, encrypt=True):
    M, N = channel_data.shape
    JPDF_values = key.generate_JPDF_parameters(secret_key)
    # print(JPDF_values)
    input_data = np.array(channel_data)
    print(input_data.shape)
    range_func = range(1, -1, -1)  # for decryption
    # Chaotic Mapping
    cm_val = { 
    "x" : 0.19870228,
    "mu": 3.99999999
    }
    for idx in range_func:
        cimage = col_cm.deswitch_columns(cm_val["mu"], cm_val["x"], input_data)
        rimage = row_cm.deswitch_rows(cm_val["mu"], cm_val["x"], cimage)

        # Josephus Scrambling
        sc_val = key.generate_scrambling_values(JPDF_values[f"g{idx}"], M, N)
        mapping = JS_Mapping.generate_mapping(M, N, **sc_val)
        scrambled_data = JS_Scramble.descramble_image(mapping, rimage)
        input_data = np.array(scrambled_data)

    return input_data

def process_image(image, secret_key, encrypt=True):
    # im = Image.open(image_path)
    
    # print(image.shape)
    # if im.mode != "RGB":
    #     raise ValueError("Only RGB images are supported.")
    
    image = np.array(image)
    processed_channels = []

    for idx in range(3):  # process each channel
        channel_data = image[:, :, idx]
        if encrypt:
            processed_channel = encrypt_decrypt_channel(channel_data, secret_key, encrypt)
        else:
            processed_channel = edec_channel(channel_data, secret_key, encrypt)
        processed_channels.append(processed_channel)
    if(encrypt):
        print("Encryption\n:")
    else:
        print("Decryption\n")
    for ch in processed_channels:
        print(ch)
    processed_image = np.stack(processed_channels, axis=-1)
    processed_image = Image.fromarray(processed_image.astype(np.uint8), mode="RGB")

    return processed_image

# Example Usage
secret_key = "T3RTqXCNwUaIraqIbixsvzYb1W340ZXK"
image = Image.open("./Images/cmk.jpeg")
# Encrypt
encrypted_image = process_image(image, secret_key, encrypt=True)
encrypted_image.save('./Images/eimage.png')
print(encrypted_image)
# Decrypt
decrypted_image = process_image(encrypted_image, secret_key, encrypt=False)
decrypted_image.save('./Images/dimage.png')
print(decrypted_image)