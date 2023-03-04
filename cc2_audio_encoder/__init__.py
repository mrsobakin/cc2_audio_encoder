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

def to2B(n):
    return n.to_bytes(2, byteorder="big")


# https://github.com/vgmstream/vgmstream/blob/master/src/meta/bnsf.c
def generate_bnsf_header(data_size, n_samples, n_channels):
    header = bytearray()

    # BNSF magic number + size
    header.extend(b"BNSF")
    header.extend(to4B(data_size+40))
    header.extend(b"IS14")

    # sfmt section
    header.extend(b"sfmt")
    header.extend(to4B(0x14))              # flags
    header.extend(to4B(n_channels))        # n_channels
    header.extend(to4B(0xBB80))            # sample_rate
    header.extend(to4B(n_samples))         # n_samples
    header.extend(to4B(0x00))              # loop_adjust
    header.extend(to2B(120 * n_channels))  # block_size 
    header.extend(to2B(640))               # block_samples

    # sdat section
    header.extend(b"sdat")
    header.extend(to4B(data_size))
    
    return header


def run_exe(exe, args):
    if USE_WINE:
       return subprocess.run(["wine", exe, *args])
    else:
       return subprocess.run([exe, *args])
        

def _encrypt_hca(orig_filename, enc_filename, t, k1, k2):
    run_exe(HCACC_EXE, [orig_filename, enc_filename, "-ot", t, "-o1", k1, "-o2", k2])


def _encode_hca(wav_filename, hca_filename):
    run_exe(HCAENC_EXE, [wav_filename, hca_filename, "-q", "5"])


def _encode_pcm(wav_filename, pcm_filename):
    subprocess.run(["ffmpeg", "-i", wav_filename, "-f", "s16le", "-acodec", "pcm_s16le", pcm_filename])


def _encode_stereo_pcm(wav_filename, left_pcm_filename, right_pcm_filename):
    subprocess.run(["ffmpeg", "-i", wav_filename, "-map_channel", "0.0.0", "-f", "s16le", "-acodec", "pcm_s16le", left_pcm_filename, "-map_channel", "0.0.1", "-f", "s16le", "-acodec", "pcm_s16le", right_pcm_filename])


def encode_is14(pcm_filename):
    with utils.temp_file() as is14_filename:
        run_exe(IS14_ENCODER_EXE, ["0", pcm_filename, is14_filename, "48000", "14000"])

        with open(is14_filename, "rb") as f:
            return f.read()


def encode_mono_bnsf(wav_filename):
    with utils.temp_file() as pcm_filename:
        _encode_pcm(wav_filename, pcm_filename)
    
        n_samples = os.path.getsize(pcm_filename) // 2

        is14bytes = encode_is14(wav_filename)

    bnsf = generate_bnsf_header(len(is14bytes), n_samples, 1)
    bnsf.extend(bytearray(is14bytes))

    return bnsf


def encode_stereo_bnsf(wav_filename):
    with utils.temp_file() as pcm_l_filename, \
         utils.temp_file() as pcm_r_filename:
        
        _encode_stereo_pcm(wav_filename, pcm_l_filename, pcm_r_filename)
        
        n_samples = os.path.getsize(pcm_l_filename) // 2 
        
        is14bytes = bytearray(b''.join(
            utils.interleave(
                utils.chunks(encode_is14(pcm_l_filename), 120),
                utils.chunks(encode_is14(pcm_r_filename), 120),
            )
        ))

    bnsf = generate_bnsf_header(len(is14bytes), n_samples, 2)
    bnsf.extend(is14bytes)

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
