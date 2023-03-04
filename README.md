# CyberConnect2 audio encoding toolbox
A small toolbox for converting `.wav` audio files to CyberConnect2's formats (`.bnsf`, `.hca`, encoded `.hca`)

## How to install
0. If you're using linux, install `wine`
1. Install `ffmpeg`
2. `cd` into the repository folder
3. `pip install .`

## How to use
### As a cli app
#### HCA
`python -m cc2_audio_encoder hca <in_file.wav> <out_file.hca>`

`python -m cc2_audio_encoder hca -t <t> -k1 <k1> -k2 <k2> <in_file.wav> <out_file.hca>`

- t - encryption type
- k1 - encryption key (1)
- k2 - encryption key (2)

For JoJo ASBR, these arguments would be: `-t 56 -k1 012C9A53 -k2 00000000`

#### BNSF

`python -m cc2_audio_encoder bnsf <in_file.wav> <out_file.bnsf>`

To encode a stereo `bnsf`:

`python -m cc2_audio_encoder bnsf --stereo <in_file.wav> <out_file.bnsf>`

To include loop data into `bnsf` (use `-h` for further info):

`python -m cc2_audio_encoder bnsf --loop <in_file.wav> <out_file.bnsf>`

### As a python module
```python
from cc2_audio_encoder import bnsf, hca

bnsf_bytes = bnsf.encode("some_file.wav")
with open("audio.bnsf", "wb") as f:
    f.write(bnsf_bytes)

hca_bytes = hca.encode("some_file.wav", encryption={"t": 56, "k1": "012C9A53", "k2": "00000000"}):
with open("audio.hca", "wb") as f:
    f.write(hca_bytes)
```
Just explore the source code. It's very small.

## Special thanks to:
- [**vgmstream**](https://github.com/vgmstream/vgmstream/blob/master/src/meta/bnsf.c) for reverse engineering the `.bnsf` header
- [**This amazing article**](https://exvsfbce.home.blog/2020/02/04/guide-to-encoding-bnsf-is14-audio-files-converting-wav-back-to-bnsf-is14/) for reverse engineering the `.bnsf` header
- **NSUNS4 Toolbox** for the compiled IS14 encoder (`encode.exe`), which I was too lazy to compile myself
- [**Deretore**](https://github.com/OpenCGSS/DereTore) for the HCA encoder and encrypter (`hcaenc.exe`, `hcacc.exe`)
