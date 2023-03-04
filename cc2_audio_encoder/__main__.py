from sys import argv

from cc2_audio_encoder import bnsf, hca


if argv[1] == "bnsf":
    bnsf_bytes = bnsf.encode_mono(argv[2])
   
    with open(argv[3], "wb") as f:
        f.write(bnsf_bytes)

if argv[1] == "stereo_bnsf":
    bnsf_bytes = bnsf.encode_stereo(argv[2])
    
    with open(argv[3], "wb") as f:
        f.write(bnsf_bytes)

elif argv[1] == "hca":
    if len(argv)>6:
        encryption = { "t": argv[4], "k1": argv[5], "k2": argv[6] }
    else:
        encryption = None
    
    hca_bytes = hca.encode(argv[2], encryption)
    
    with open(argv[3], "wb") as f:
        f.write(hca_bytes)
