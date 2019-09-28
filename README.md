# Planet Pieces
Convolutional Neural Network and image segmentation for land classification of high resolution multispectral Planet imagery   

## Collaborators  
[Nga (Nancy) Nguyen](https://github.com/NgaNguyen87)
  
[Claire Miles](https://github.com/clairemiles)  

[Joshua Driscol](https://github.com/Jakidxav)

[Matt Olson](https://github.com/mattols)

[Mike Leech](https://github.com/mikeleech)

[Shashank Bhushan](https://github.com/ShashankBice)

[Michelle Hu](https://github.com/jmichellehu)


### Team Lead:  
Michelle Hu

### Data Science Leads:  
Claire Miles, Joshua Driscol - Tensorflow, Keras  
Shashank Bhushan - Planet data and rasters  
Nga Nguyen, Matt Olson - thresholding and visualization

## Introduction
Background reading:
- [Ensemble CNN for land classification](https://ieeexplore.ieee.org/abstract/document/8334746)
- [RGB-NIR Image Classification](https://ieeexplore.ieee.org/document/8630948)
- [Original U-Net paper](https://arxiv.org/pdf/1505.04597.pdf)
- U-Net architecture borrowed heavily from [this](https://github.com/zizhaozhang/unet-tensorflow-keras/blob/master/model.py) repository.
- [Tensorflow 2.0 Documentation](https://www.tensorflow.org/beta/)

## Files

* `.gitignore`
<br> Globally ignored files by `git` for the project.  
* `environment.yml`
<br> `conda` environment description needed to run this project.  
To preserve the conda environment across sessions, please add this line of code into your `~/.condarc` file, or create that file if it does not exist:
```python
envs_dirs:
 - /home/user/conda-envs/
```

Then run:
```python
conda env create -f environment.yml -n planetpieces
```

And to activate the environment:
```python
conda activate planetpieces
```

* `README.md`
<br> Description of the project and personnel. 

We will be using 3m resolution data from [Planet Labs](https://www.planet.com/) at Mount Rainier in Washington state. The purpose of this repository is to implement novel techniques for analyzing geospatial data sets using neural networks:
- snow vs. land cover segmentation
- techniques for stacking coarse resolution images to train them for upsampling like in [DeepSUM](https://github.com/diegovalsesia/deepsum) 

[Sample](https://geohackweek.github.io/wiki/github_project_management.html#project-guidelines)


## Folders

### `contributors`
Each team member has their own folder under contributors, where they can work on their contributions. Having a dedicated folder for one-self helps to prevent conflicts when merging with master.  

### `notebooks`
Notebooks that are considered delivered results for the project should go in here.  

### `scripts`
Helper utilities that are shared with the team  


### Team Wiki
Further information can be found on our [team wiki page](https://github.com/geohackweek/ghw2019_planetpieces/wiki)

