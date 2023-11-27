from PIL import Image
import numpy as np
from Lib import key
from Lib import JS_Mapping
from Lib import JS_Scramble
from Lib import row_cm
from Lib import col_cm

def encrypt_image(image, secret_key):
    
    # Handle Key - Generate Parameters
    JPDF_values = key.generate_JPDF_parameters(secret_key)
    M = len(image)
    N = len(image[0])
    
    input_image = image
    # Dual Encrytion Loop
    for idx in range(2):
        # Josephus Parameter Generation, Mapping & Scrambling
        sc_val = key.generate_scrambling_values(JPDF_values[f"g{idx}"], M, N)
        mapping = JS_Mapping.generate_mapping(M, N, MP=sc_val["MP"], NP=sc_val["NP"], MStep=sc_val["MStep"], NStep=sc_val["NStep"])
        scrambled_image = JS_Scramble.scramble_image(mapping, input_image)
        
        # Chaotic Mapping - Parameter Generation, Row Switching & Column Switching
        cm_val = key.generate_chaotic_mapping_values(JPDF_values[f"d{idx}"])
        rimage = row_cm.switch_rows(cm_val["mu"], cm_val["x"], np.array(scrambled_image))
        cimage = col_cm.switch_columns(cm_val["mu"], cm_val["x"], rimage)
        
        input_image = cimage
    
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
        cm_val = key.generate_chaotic_mapping_values(JPDF_values[f"d{idx}"])
        cimage = col_cm.deswitch_columns(cm_val["mu"], cm_val["x"], input_image)
        res = row_cm.deswitch_rows(cm_val["mu"], cm_val["x"], cimage)
        
        # Josephus Parameter Generation, Mapping & De-Scrambling
        sc_val = key.generate_scrambling_values(JPDF_values[f"g{idx}"], M, N)
        mapping = JS_Mapping.generate_mapping(M, N, MP=sc_val["MP"], NP=sc_val["NP"], MStep=sc_val["MStep"], NStep=sc_val["NStep"])
        scrambled_image = JS_Scramble.descramble_image(mapping, res)
        input_image = np.array(scrambled_image)
        
    return input_image
    
    
if __name__ == "__main__":
    secret_key = "T3RTqXCNwUaIraqIbixsvzYb1W340ZXK"
    # im = Image.open("./Images/color.jpg")
    im = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12],[13,14,15,16]])
    im_mode = "L"
    # im_mode = im.mode
    # im = im.convert("L")
    image = np.array(im)
    print("IMage Mode =", im_mode)
    print("IMage Shape = ", image.shape)
    print("\n########################\n")
    print("Original IMage:\n", image)
    print("\n########################\n")
    
    
    if im_mode in ["L", "P"]:
        enc_image = encrypt_image(image, secret_key)
        enc_image = np.array(enc_image)
        # eimage = Image.fromarray(enc_image.astype(np.uint8), mode=im_mode)
    elif im_mode == "RGB":
        enc_image_array = []
        for idx in range(3):
            unc_img = image[:, :, idx]
            print(unc_img)
            print("Shape = ", unc_img.shape)
            enc_image_mat = encrypt_image(unc_img, secret_key)
            enc_image_array.append(enc_image_mat)
        enc_image = np.stack(enc_image_array, axis=-1)
        eimage = Image.fromarray(enc_image.astype(np.uint8), mode="RGB")
    else:
        raise Exception(f"${im_mode} Unsupported Image Type. Currently supported Only Grayscale or RGB.")
    
    
    # eimage.save('./Images/eimage.png')
    
    print("\n########################\n")
    print("Encrypted Image:\n", enc_image)
    print("\n########################\n")
    
    secret_key = "T3RTqXCNwUaIraqIbixsvzYb1W340ZXK"
    # eim = Image.open("./Images/eimage.png")
    eim = enc_image
    # eim_mode = eim.mode
    eim_mode = "L"
    eim_mat = np.array(eim)
    
    
    if eim_mode in ["L", "P"]:
        dec_image = decrypt_image(eim_mat, secret_key)
        dec_image = np.array(dec_image)
        # deimage = Image.fromarray(dec_image.astype(np.uint8), mode=im_mode)
    elif eim_mode == "RGB":
        dec_image_array = []
        for idx in range(3):
            dec_imgs = eim_mat[:, :, idx]
            print("D Image:\n", dec_imgs)
            print("Shape = ",dec_imgs.shape)
            dec_image_mat = decrypt_image(dec_imgs, secret_key)
            dec_image_array.append(enc_image_mat)
        dec_image = np.stack(dec_image_array, axis=-1)
        print(dec_image.shape)
        deimage = Image.fromarray(dec_image.astype(np.uint8), mode="RGB")
    else:
        raise Exception(f"{eim_mode} Unsupported Image Type. Currently supported Only Grayscale or RGB.")
    
    # deimage.save('./Images/dimage.png')

    print("\n########################\n")
    print("Decrypted Image:\n", dec_image)
    print("\n########################\n")
    print(np.array_equal(image, dec_image))