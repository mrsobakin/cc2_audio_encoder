# CyberConnect2 audio encoding toolbox
A small toolbox for converting `.wav` audio files to CyberConnect2's formats (`.bnsf`, `.hca`, encoded `.hca`)

## How to install
0. If you're using linux, install `wine`
1. Install `ffmpeg`
2. `cd` into the repository folder
3. `pip install .`

## How to use
### As a cli app
`python -m cc2-audio-encoding hca <in_file.wav> <out_file.hca>`

`python -m cc2-audio-encoding hca <in_file.wav> <out_file.hca> <t> <k1> <k2>`

- t - encryption type
- k1 - encryption key (1)
- k2 - encryption key (2)

For JoJo ASBR these parameters would be `56 012C9A53 00000000`

`python -m cc2-audio-encoding bnsf <in_file.wav> <out_file.bnsf>`

### As a python module
```python
from cc2_audio_encoding import encode_bnsf, encode_hca

bnsf_bytes = encode_bnsf("some_file.wav")
with open("audio.bnsf", "wb") as f:
    f.write(bnsf_bytes)

hca_bytes = encode_hca("some_file.wav", encryption={"t": 56, "k1": "012C9A53", "k2": "00000000"}):
with open("audio.hca", "wb") as f:
    f.write(hca_bytes)
```
Just explore the source code. It's very small.

## Special thanks to:
- [**This amazing article**](https://exvsfbce.home.blog/2020/02/04/guide-to-encoding-bnsf-is14-audio-files-converting-wav-back-to-bnsf-is14/) for reverse engineering the `.bnsf` header
- **NSUNS4 Toolbox** for the compiled IS14 encoder (`encode.exe`), which I was too lazy to compile myself
- [**Deretore**](https://github.com/OpenCGSS/DereTore) for the HCA encoder and encrypter (`hcaenc.exe`, `hcacc.exe`)
