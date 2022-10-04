import os
import platform
import subprocess
from pathlib import Path

from cc2_audio_encoder import utils


USE_WINE = platform.system() != "Windows"


_BASE_PATH = Path(__file__).parent / "bin"
_DERETORE = _BASE_PATH / "deretore"

IS14_ENCODER_EXE = _BASE_PATH / "encode.exe"

HCACC_EXE = _DERETORE / "hcacc.exe"
HCAENC_EXE = _DERETORE / "hcaenc.exe"


def to4B(n):
    return n.to_bytes(4, byteorder="big")


def generate_bnsf_header(size, samples):
    header = bytearray()
    
    header.extend(b"BNSF")
    header.extend(to4B(size+40))
    header.extend(b"IS14sfmt")
    
    header.extend(to4B(0x14))
    header.extend(to4B(0x01))
    header.extend(to4B(0xBB80))
    header.extend(to4B(samples))

    header.extend(to4B(0x00))
    header.extend(to4B(0x780280))
    header.extend(b"sdat")
    header.extend(to4B(size))
    
    return header


def run_exe(exe, args):
    if USE_WINE:
       return subprocess.run(["wine", exe, *args])
    else:
       return subprocess.run([exe, *args])
        
        
def _encode_is14(file_in, file_out):
    run_exe(IS14_ENCODER_EXE, ["0", file_in, file_out, "48000", "14000"])


def _encrypt_hca(orig_filename, enc_filename, t, k1, k2):
    run_exe(HCACC_EXE, [orig_filename, enc_filename, "-ot", t, "-o1", k1, "-o2", k2])


def _encode_hca(wav_filename, hca_filename):
    run_exe(HCAENC_EXE, [wav_filename, hca_filename, "-q", "5"])


def _encode_pcm(orig_filename, pcm_filename):
    subprocess.run(["ffmpeg", "-i", orig_filename, "-f", "s16le", "-acodec", "pcm_s16le", pcm_filename])


def encode_bnsf(wav_filename):
    with utils.temp_file() as pcm_filename:
        _encode_pcm(wav_filename, pcm_filename)
    
        samples = os.path.getsize(pcm_filename)//2
    
        with utils.temp_file() as is14_filename:
            _encode_is14(pcm_filename, is14_filename)
            
            with open(is14_filename, "rb") as f:
                encodedbytes = f.read()

    bnsf = generate_bnsf_header(len(encodedbytes), samples)
    bnsf.extend(bytearray(encodedbytes))

    return bnsf


def encode_hca(wav_filename, encryption=None):
    with utils.temp_file() as filename:
        _encode_hca(wav_filename, filename)
        
        if not encryption:
            with open(filename, "rb") as f:
                return f.read()
        
        with utils.temp_file() as encr_filename:
            _encrypt_hca(filename, encr_filename, encryption["t"], encryption["k1"], encryption["k2"])
            with open(encr_filename, "rb") as f:
                return f.read()
