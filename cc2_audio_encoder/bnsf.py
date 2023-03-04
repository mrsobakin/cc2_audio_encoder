import os

from cc2_audio_encoder import utils, exe, pcm
from cc2_audio_encoder.utils import to2B, to4B
from cc2_audio_encoder.paths import IS14_ENCODER_EXE


# https://github.com/vgmstream/vgmstream/blob/master/src/meta/bnsf.c
def generate_header(data_size, n_samples, n_channels):
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


def _encode_is14(pcm_filename):
    with utils.temp_file() as is14_filename:
        exe.run(IS14_ENCODER_EXE, ["0", pcm_filename, is14_filename, "48000", "14000"])

        with open(is14_filename, "rb") as f:
            return f.read()


def encode_mono(wav_filename):
    with utils.temp_file() as pcm_filename:
        pcm.encode(wav_filename, pcm_filename)
    
        n_samples = os.path.getsize(pcm_filename) // 2

        is14bytes = _encode_is14(wav_filename)

    bnsf = generate_header(len(is14bytes), n_samples, n_channels=1)
    bnsf.extend(bytearray(is14bytes))

    return bnsf


def encode_stereo(wav_filename):
    with utils.temp_file() as pcm_l_filename, \
         utils.temp_file() as pcm_r_filename:
        
        pcm.encode_stereo(wav_filename, pcm_l_filename, pcm_r_filename)
        
        n_samples = os.path.getsize(pcm_l_filename) // 2 
        
        is14bytes = bytearray(b''.join(
            utils.interleave(
                utils.chunks(_encode_is14(pcm_l_filename), 120),
                utils.chunks(_encode_is14(pcm_r_filename), 120),
            )
        ))

    bnsf = generate_header(len(is14bytes), n_samples, n_channels=2)
    bnsf.extend(is14bytes)

    return bnsf
