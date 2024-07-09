from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='gurulearn',
    version='1.0.12',
    description='library for linear_regression and gvgg16 model generation(fixed bugs),audio_classify and audio_classify_predict',
    author='Guru Dharsan T',
    author_email='gurudharsan123@gmail.com',
    packages=find_packages(),
install_requires=[
    'opencv-python==4.5.5.64',
    'scipy==1.8.0',
    'matplotlib==3.5.1',
    'tensorflow==2.9.0',
    'Keras==2.9.0',
    'pandas==1.4.1',
    'numpy==1.22.2',
    'plotly==5.5.0',
    'scikit-learn==1.0.2',
    'librosa==0.8.1',
    'tqdm==4.62.3',
    'resampy==0.3.1'
],
)
