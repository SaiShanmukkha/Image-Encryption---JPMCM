from PIL import Image
import numpy as np
from Lib import key
from Lib import JS_Mapping
from Lib import JS_Scramble
from Lib import row_cm
from Lib import col_cm

def encryption_channel(channel_data, secret_key):
    M, N = channel_data.shape
    JPDF_values = key.generate_JPDF_parameters(secret_key)
    input_data = channel_data
    cm_val = { 
        "x" : 0.19870228,
        "mu": 3.99999999
        }

    for idx in range(2):
        # Josephus Scrambling
        sc_val = key.generate_scrambling_values(JPDF_values[f"g{idx}"], M, N)
        mapping = JS_Mapping.generate_mapping(M, N, **sc_val)
        scrambled_data = JS_Scramble.scramble_image(mapping, input_data)

        # Chaotic Mapping
        rimage = row_cm.switch_rows(cm_val["mu"], cm_val["x"], np.array(scrambled_data))
        cimage = col_cm.switch_columns(cm_val["mu"], cm_val["x"], rimage)
        input_data = cimage

    return input_data

def decryption_channel(channel_data, secret_key):
    M, N = channel_data.shape
    JPDF_values = key.generate_JPDF_parameters(secret_key)
    input_data = np.array(channel_data)

    cm_val = { 
    "x" : 0.19870228,
    "mu": 3.99999999
    }

    for idx in  range(1, -1, -1):
        # Chaotic Mapping
        cimage = col_cm.deswitch_columns(cm_val["mu"], cm_val["x"], input_data)
        rimage = row_cm.deswitch_rows(cm_val["mu"], cm_val["x"], cimage)

        # Josephus Scrambling
        sc_val = key.generate_scrambling_values(JPDF_values[f"g{idx}"], M, N)
        mapping = JS_Mapping.generate_mapping(M, N, **sc_val)
        scrambled_data = JS_Scramble.descramble_image(mapping, rimage)
        input_data = np.array(scrambled_data)

    return input_data

def process_color_image(image, secret_key, encryptFlag):   
    image = np.array(image)
    processed_channels = []

    for idx in range(3):  # process each channel
        channel_data = image[:, :, idx]
        if encryptFlag:
            processed_channel = encryption_channel(channel_data, secret_key)
        else:
            processed_channel = decryption_channel(channel_data, secret_key)
        processed_channels.append(processed_channel)
    
    processed_image = np.stack(processed_channels, axis=-1)
    processed_image = Image.fromarray(processed_image.astype(np.uint8), mode="RGB")

    return processed_image

def process_grey_scale(image, secret_key, encryptFlag):
    image = np.array(image)

    if encryptFlag:
        processed_image = encryption_channel(image, secret_key)
    else:
        processed_image = decryption_channel(image, secret_key)
    
    processed_image = Image.fromarray(processed_image.astype(np.uint8), mode="L")

    return processed_image

if __name__ == "__main__":
    secret_key = "T3RTqXCNwUaIraqIbixsvzYb1W340ZXK"
    image = Image.open("./Images/cmk.jpeg")

    if image.mode == "L":
        # Encrypt
        encrypted_image = process_grey_scale(image, secret_key, encryptFlag=True)
        encrypted_image.save('./Images/eimage.png')

        # Decrypt
        decrypted_image = process_grey_scale(encrypted_image, secret_key, encryptFlag=False)
        decrypted_image.save('./Images/dimage.png')
        
    elif image.mode == "RGB":
        # Encrypt
        encrypted_image = process_color_image(image, secret_key, encryptFlag=True)
        encrypted_image.save('./Images/eimage.png')     

        # Decrypt
        decrypted_image = process_color_image(encrypted_image, secret_key, encryptFlag=False)
        decrypted_image.save('./Images/dimage.png')

    

    