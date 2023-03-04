import subprocess


def encode(wav_filename, pcm_filename):
    subprocess.run(["ffmpeg", "-i", wav_filename, "-f", "s16le", "-acodec", "pcm_s16le", pcm_filename], check=True)


def encode_stereo(wav_filename, left_pcm_filename, right_pcm_filename):
    subprocess.run(["ffmpeg", "-i", wav_filename, "-map_channel", "0.0.0", "-f", "s16le", "-acodec", "pcm_s16le", left_pcm_filename, "-map_channel", "0.0.1", "-f", "s16le", "-acodec", "pcm_s16le", right_pcm_filename], check=True)
