from PIL import Image
import numpy as np
from Lib import key
from Lib import JS_Mapping
from Lib import JS_Scramble
from Lib import row_cm
from Lib import col_cm
import time
import os

# Main Encryption Function
def encryption_channel(channel_data, secret_key):
    M, N = channel_data.shape
    JPDF_values = key.generate_JPDF_parameters(secret_key)
    input_data = channel_data
    
    for idx in range(2):
        # Josephus Scrambling
        sc_val = key.generate_scrambling_values(JPDF_values[f"g{idx}"], M, N)
        mapping = JS_Mapping.generate_mapping(M, N, **sc_val)
        scrambled_data = JS_Scramble.scramble_image(mapping, input_data)

        # Chaotic Mapping
        cm_val = key.generate_chaotic_mapping_values(JPDF_values[f"d{idx}"])
        rimage = row_cm.switch_rows(cm_val["mu"], cm_val["x"], np.array(scrambled_data))
        cimage = col_cm.switch_columns(cm_val["mu"], cm_val["x"], rimage)
        input_data = cimage

    return input_data

# Main Decryption Function
def decryption_channel(channel_data, secret_key):
    M, N = channel_data.shape
    JPDF_values = key.generate_JPDF_parameters(secret_key)
    input_data = np.array(channel_data)

    for idx in  range(1, -1, -1):
        # Chaotic Mapping
        cm_val = key.generate_chaotic_mapping_values(JPDF_values[f"d{idx}"])
        cimage = col_cm.deswitch_columns(cm_val["mu"], cm_val["x"], input_data)
        rimage = row_cm.deswitch_rows(cm_val["mu"], cm_val["x"], cimage)

        # Josephus Scrambling
        sc_val = key.generate_scrambling_values(JPDF_values[f"g{idx}"], M, N)
        mapping = JS_Mapping.generate_mapping(M, N, **sc_val)
        scrambled_data = JS_Scramble.descramble_image(mapping, rimage)
        input_data = np.array(scrambled_data)

    return input_data

# RGB Image Handler
def process_color_image(image, secret_key, encryptFlag):   
    image = np.array(image)
    print(image.shape)
    processed_channels = []
    # Measure the start time
    start_time = time.time()
    for idx in range(3):  # process each channel
        channel_data = image[:, :, idx]
        if encryptFlag:
            
            processed_channel = encryption_channel(channel_data, secret_key)
        else:
            processed_channel = decryption_channel(channel_data, secret_key)
        processed_channels.append(processed_channel)
    # Measure the end time
    end_time = time.time()

    # Calculate encryption speed
    elapsed_time = end_time - start_time
    temp1, temp2 = channel_data.shape
    encryption_speed = (temp1*temp2) / (1024 * 1024) / max(1e-6, elapsed_time)  # Avoid division by zero

    print(f"Elapsed Time: {elapsed_time:.6f} seconds")
    print(f"Encryption/Decryption Speed: {encryption_speed:.2f} MB/s")
    
    processed_image = np.stack(processed_channels, axis=-1)
    processed_image = Image.fromarray(processed_image.astype(np.uint8), mode="RGB")

    return processed_image

# Grey Scale Image Handler
def process_grey_scale(image, secret_key, encryptFlag):
    image = np.array(image)
    print(image.shape)
    if encryptFlag:
        # Measure the start time
        start_time = time.time()
        processed_image = encryption_channel(image, secret_key)
        # Measure the end time
        end_time = time.time()

        # Calculate encryption speed
        elapsed_time = end_time - start_time
        temp1, temp2 = image.shape
        encryption_speed = (temp1*temp2) / (1024 * 1024) / max(1e-6, elapsed_time)  # Avoid division by zero

        print(f"Elapsed Time: {elapsed_time:.6f} seconds")
        print(f"Encryption Speed: {encryption_speed:.2f} MB/s")
    else:
        processed_image = decryption_channel(image, secret_key)
    
    processed_image = Image.fromarray(processed_image.astype(np.uint8), mode="L")

    return processed_image

if __name__ == "__main__":
    # #2 Byte or 256 bit Secret Key
    secret_key = "T3RTqXCNwUaIraqIbixsvzYb1W340ZXK"

    # Input for Grey Scale
    # image = Image.open("./Images/Input/GreyScale/test.jpg")

    # Input for RGB Image
    # image = Image.open("./Images/Input/RGB/cmk.jpeg")

    # RGB Images Folder
    path = "./Images/Input/RGB/"

    # Grey Scale Images Folder
    # path = "./Images/Input/GreyScale/"

    for file in os.listdir(path):
        image = Image.open(path + file)
        print(path+file)
        # Grey Scale Image Condition
        if image.mode == "L":
            # Encrypt
            encrypted_image = process_grey_scale(image, secret_key, encryptFlag=True)
            encrypted_image.save(f'./Images/Output/GreyScale/{file}_eimage.png')

            # Decrypt
            decrypted_image = process_grey_scale(encrypted_image, secret_key, encryptFlag=False)
            decrypted_image.save(f'./Images/Output/GreyScale/{file}_dimage.png')
        
        # RGB Image Condition
        elif image.mode == "RGB":
            # Encrypt
            encrypted_image = process_color_image(image, secret_key, encryptFlag=True)
            encrypted_image.save(f'./Images/Output/RGB/{file}_eimage.png')     

            # Decrypt
            decrypted_image = process_color_image(encrypted_image, secret_key, encryptFlag=False)
            decrypted_image.save(f'./Images/Output/RGB/{file}_dimage.png')

        # Exception For Other types of images
        else:
            raise Exception("Unsupported Image Type.")

    

    