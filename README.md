# Machine Learning Repo Template

## Installation
```
conda create -n <env_name> python=3.9
conda activate <env_name>

# https://pytorch.org/get-started/locally/
conda install pytorch torchvision pytorch-cuda=11.8 -c pytorch -c nvidia

# This will install src. 
# -e means, if src is edited after running the following command, 
# there's no need to rerun the following pip install again.
pip install -e .
```