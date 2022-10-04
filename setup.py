from setuptools import setup

setup(
    name = 'cc2_audio_encoder',
    version = '0.0.1',    
    description = 'Small toolbox for encoding CyberConnect2\'s audio',
    packages = [
        "cc2_audio_encoder",
        "cc2_audio_encoder.bin",
        "cc2_audio_encoder.bin.deretore"
    ],
    package_data = {
        "": ["*.dll", "*.exe"]
    },
    include_package_data=True
)
