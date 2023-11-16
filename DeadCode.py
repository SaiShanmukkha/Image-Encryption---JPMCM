    # Dual Decryption Loop
    # for idx in range(1):
    #     # Chaotic Mapping - Parameter Generation, Row Deswitching & Column Deswitching
    #     cm_val = key.generate_chaotic_mapping_values(JPDF_values[f"d{idx}"])
    #     print(f"Dcm_val{idx}:\n", cm_val)
    #     # cimage = col_cm.deswitch_columns(cm_val["mu"], cm_val["x"], input_image)
    #     # print(f"DCS{idx}:\n", cimage)
    #     rimage = row_cm.deswitch_rows(cm_val["mu"], cm_val["x"], input_image)
    #     print(f"DRS{idx}:\n", np.array(rimage))
        
    #     # Josephus Parameter Generation, Mapping & De-Scrambling
    #     sc_val = key.generate_scrambling_values(JPDF_values[f"g{idx}"], M, N)
    #     # print(f"Dsc_val{idx}:\n", sc_val)
    #     mapping = JS_Mapping.generate_mapping(M, N, MP=sc_val["MP"], NP=sc_val["NP"], MStep=sc_val["MStep"], NStep=sc_val["NStep"])
    #     scrambled_image = JS_Scramble.descramble_image(mapping, rimage)
    #     # print(f"DSC{idx}:\n", np.array(scrambled_image))
        
    #     input_image = scrambled_image