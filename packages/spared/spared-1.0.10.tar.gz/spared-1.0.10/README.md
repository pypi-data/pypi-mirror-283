# Library_Spared_Spackle

This repository contains all the necessary files to create a PyPI library to the SPARED and SpaCKLE contributions

This is the  README file which will contain the long description of the PiPy library. Most libraries have a README file. Mean while this file will only contain this information and will be soon updated. 

## System Dependencies

Before installing the Python package, ensure the following system dependencies are installed:

```shell
conda create -n spared
conda activate spared
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
conda install lightning -c conda-forge
pip install torch_geometric
conda install -c conda-forge squidpy
pip install wandb
pip install wget
pip install combat
pip install opencv-python
pip install positional-encodings[pytorch]
pip install openpyxl
pip install pyzipper
pip install plotly
pip install sh
pip install sphinx
pip install -U sphinx-copybutton
pip install -U sphinx_rtd_theme
```
