from sys import argv


if argv[1] == "bnsf":
    from cc2_audio_encoder import encode_bnsf
    
    bnsf_bytes = encode_bnsf(argv[2])
    
    with open(argv[3], "wb") as f:
        f.write(bnsf_bytes)

elif argv[1] == "hca":
    from cc2_audio_encoder import encode_hca
    
    if len(argv)>6:
        encryption = { "t": argv[4], "k1": argv[5], "k2": argv[6] }
    else:
        encryption = None
    
    hca_bytes = encode_hca(argv[2], encryption)
    
    with open(argv[3], "wb") as f:
        f.write(hca_bytes)
