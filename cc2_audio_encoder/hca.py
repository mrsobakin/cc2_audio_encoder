from cc2_audio_encoder import utils, exe
from cc2_audio_encoder.paths import HCACC_EXE, HCAENC_EXE


def _encrypt_hca(orig_filename, enc_filename, t, k1, k2):
    exe.run(HCACC_EXE, [orig_filename, enc_filename, "-ot", t, "-o1", k1, "-o2", k2])


def _encode_hca(wav_filename, hca_filename):
    exe.run(HCAENC_EXE, [wav_filename, hca_filename, "-q", "5"])


def encode(wav_filename, encryption=None):
    with utils.temp_file() as filename:
        _encode_hca(wav_filename, filename)
        
        if not encryption:
            with open(filename, "rb") as f:
                return f.read()
        
        with utils.temp_file() as encr_filename:
            _encrypt_hca(filename, encr_filename, encryption["t"], encryption["k1"], encryption["k2"])
            with open(encr_filename, "rb") as f:
                return f.read()
