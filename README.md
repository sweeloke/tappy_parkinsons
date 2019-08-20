# Diagnosis from the keyboard

## Prerequisites
This project was written on top of [Google Colab](https://colab.research.google.com) and Google Drive, so the easiest way to run or play with it, is using these tools instead of trying to setup locally on your computer.

Inside the notebooks we always start with this cell to configure the locations and basic setup.
Please, don't forget to adjust your `HOME_DIR` to follow your Google Drive location for the project (if you want something different than `My Drive/tappy_parkinsons`).
```python
# First we must mount google drive 
from google.colab import drive
GDRIVE_BASE_PATH = '/content/gdrive'
drive.mount(GDRIVE_BASE_PATH)

# Loading all updates from GitHub and our project setup
HOME_DIR = f'{GDRIVE_BASE_PATH}/My Drive/tappy_parkinsons'
% cd '$HOME_DIR'
! git fetch origin && git reset --hard origin/master
from util.project_setup import ProjectSetup
```

The other small change is in the `util/project_setup.py` ensuring you have the correct `home_dir` configured:
```python
class ProjectSetup:
  home_dir = '/content/gdrive/My Drive/tappy_parkinsons'
```

## File and folder structure

### Folder: `colab_notebooks`
All the Colab Notebooks are in this folder. They were named prefixed by the order that we should run then. Here's a brief description of what you should see in each notebook:

#### `01_downloading.ipynb`
To automatically download the whole dataset from Kaggle to your local drive and unzip all files. When you finish running this notebook, you should have all raw data available.

#### `02_loading_and_exploring.ipynb`
To get familiar with the data. In this notebook we load the raw data into pandas and start understanding its structure, nuances etc. This is our inial exploration step.

#### `03_feature_engineering.ipynb`
To generate the desired features that will be consumed by our ML models. Here we aggregate raw data from the tappy and users datasets, resulting in a close-to-final dataset that the ML algoriths will use to generate predictions.

#### `04_pipeline_and_models.ipynb`
To train models and produce predictions. Here we have the final ML steps. We split the dataset, create a pipeline to do some preprocessing and training different models. Last but not least, we evaluate the different models and define our final model architecture.

### Folder: `util`
We created some utility library classes to simplify some colab notebooks. All the parsing logic to read the raw data from the files is written in these classes. By doing that, the notebooks can focus on exploration instead of coding, so the complexity is encapsulated inside the libraries.

## Presentation: 
This is the presentation as part of the project submission: 

Presentation doc: tappy_presentation.pdf

The youtube link is: https://youtu.be/DbAyfjLckXA
