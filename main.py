from PIL import Image
import numpy as np
from Lib import key
from Lib import JS_Mapping
from Lib import JS_Scramble
from Lib import row_cm
from Lib import col_cm
import time

def encrypt_image(image, secret_key):
    # Measure the start time
    start_time = time.time()
    # Handle Key - Generate Parameters
    JPDF_values = key.generate_JPDF_parameters(secret_key)
    M = len(image)
    N = len(image[0])
    
    input_image = image
    # Dual Encrytion Loop
    for idx in range(2):
        # Josephus Parameter Generation, Mapping & Scrambling
        sc_val = key.generate_scrambling_values(JPDF_values[f"g{idx}"], M, N)
        # print(f"sc_val{idx}:\n", sc_val)
        mapping = JS_Mapping.generate_mapping(M, N, MP=sc_val["MP"], NP=sc_val["NP"], MStep=sc_val["MStep"], NStep=sc_val["NStep"])
        scrambled_image = JS_Scramble.scramble_image(mapping, input_image)
        # print(f"SC{idx}:\n", np.array(scrambled_image))
        # scimage = Image.fromarray(np.array(scrambled_image).astype(np.uint8))
        # scimage.save('./Images/scimage.png')
        
        # Chaotic Mapping - Parameter Generation, Row Switching & Column Switching
        cm_val = key.generate_chaotic_mapping_values(JPDF_values[f"d{idx}"])
        # print(f"cm_val{idx}:\n", cm_val)
        rimage = row_cm.switch_rows(cm_val["mu"], cm_val["x"], np.array(scrambled_image))
        # print(f"RS{idx}:\n", np.array(rimage))
        cimage = col_cm.switch_columns(cm_val["mu"], cm_val["x"], rimage)
        # print(f"CS{idx}:\n", cimage)
        
        input_image = cimage
    
    # Measure the end time
    end_time = time.time()

    # Calculate encryption speed
    elapsed_time = end_time - start_time
    encryption_speed = (M*N) / (1024 * 1024) / max(1e-6, elapsed_time)  # Avoid division by zero

    print(f"Elapsed Time: {elapsed_time:.6f} seconds")
    print(f"Encryption Speed: {encryption_speed:.2f} MB/s")

    return input_image

def decrypt_image(eimage:np.ndarray, secret_key):
   
    # Handle Key - Generate Parameters
    JPDF_values = key.generate_JPDF_parameters(secret_key)
    M = len(image)
    N = len(image[0])
    
    # Dual Decryption Loop
    input_image = eimage.copy()
    for idx in range(1, -1, -1):
        # Chaotic Mapping - Parameter Generation, Row Deswitching & Column Deswitching
        # x= 0.19870228
        # mu=3.99999999
        # res = row_cm.deswitch_rows(mu, x, eimage)
        # Chaotic Mapping - Parameter Generation, Row Deswitching & Column Deswitching
        cm_val = key.generate_chaotic_mapping_values(JPDF_values[f"d{idx}"])
        # print(f"Dcm_val{idx}:\n", cm_val)
        cimage = col_cm.deswitch_columns(cm_val["mu"], cm_val["x"], input_image)
        # print(f"DCS{idx}:\n", cimage)
        res = row_cm.deswitch_rows(cm_val["mu"], cm_val["x"], cimage)
        # print(f"DRS{idx}:\n", np.array(rimage))
        
        
        sc_val = key.generate_scrambling_values(JPDF_values[f"g{idx}"], M, N)
        mapping = JS_Mapping.generate_mapping(M, N, MP=sc_val["MP"], NP=sc_val["NP"], MStep=sc_val["MStep"], NStep=sc_val["NStep"])
        scrambled_image = JS_Scramble.descramble_image(mapping, res)
        input_image = np.array(scrambled_image)
        
    return input_image
    
    
if __name__ == "__main__":
    secret_key = "T3RTqXCNwUaIraqIbixsvzYb1W340ZXK"
    im = Image.open("./Images/test.jpg")
    im_mode = im.mode
    image = np.array(im)
    # im_mode = "L"
    # image = np.array([[91,160,117,112], [135,124,175,126], [239, 234, 249, 224], [ 21,  28,  27,  22], [91,160,117,112], [135,124,175,126]])
    
    print("\n########################\n")
    print("Original IMage:\n", image)
    print("\n########################\n")
    
    
    if im_mode == "L":
        enc_image = encrypt_image(image, secret_key)
        enc_image = np.array(enc_image)
        eimage = Image.fromarray(enc_image.astype(np.uint8))
        eimage.save('./Images/eimage.png')
    elif im_mode == "RGB":
        pass
    else:
        raise Exception("Unsupported Image Type. Currently supported Only Grayscale or RGB.")
    
    
    print("\n########################\n")
    print("Encrypted Image:\n", enc_image)
    print("\n########################\n")
    
    secret_key = "T3RTqXCNwUaIraqIbixsvzYb1W340ZXK"
    eim = Image.open("./Images/eimage.png")
    eim_mode = eim.mode
    eim_mat = np.array(eim)
    # eim_mode = "L"
    # eim_mat = np.array(enc_image)
    if eim_mode == "L":
        dec_image = decrypt_image(eim_mat, secret_key)
        dec_image = np.array(dec_image)
        deimage = Image.fromarray(dec_image.astype(np.uint8))
        deimage.save('./Images/dimage.png')
    elif eim_mode == "RGB":
        pass
    else:
        raise Exception("Unsupported Image Type. Currently supported Only Grayscale or RGB.")
        
    print("\n########################\n")
    print("Decrypted Image:\n", dec_image)
    print("\n########################\n")