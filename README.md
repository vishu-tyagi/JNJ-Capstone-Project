# JNJ Capstone Project



<p float="left">
  <img src="notebooks/images/JNJ_logo.png" width='300' />
  <img src="notebooks/images/columbia_dsi_logo.png" width='300'/> 
</p>



### Problem Statement/ Business Need:

The GxP regulatory environment is very complex as different countries have their own regulations, and standardization is very limited. GxP regulations and guidance documents are thousands of pages of text files (pdf or HTML) posted in several internet locations. These regulatory requirements have to be manually parsed, analyzed, and classified to develop the J&J quality requirements. This is a time-consuming process.

### Project Outcome / Solution:

- With fine-tuned GPT-3 model, classify requirements by quality topics and classify quality topics requirements into themes; summarize theme requirements into a J&J Quality requirement that meets all the regulations and guidance documents.
- Build metrics to evaluate the model and benchmark using other available large language models as well as traditional machine learning models.

### Authors:

Vishweshwar Tyagi (captain), Daoxing Zhang, Siqi He, Siwen Xie, Yihao Gao

### Sponsor/Mentor:
Frank Janssens, Majd Mustapha

### Instructor:
Adam Kelleher

### CA:
Xuanyu Li


## Setup Instructions

#### Move into top-level directory
```
cd JNJ-Capstone-Project
```

#### Install environment
```
conda env create -f environment.yml
```

#### Activate environment
```
conda activate capstone
```

#### Install package
```
pip install -e src/capstone
```

Including the optional -e flag will install the package in "editable" mode, meaning that instead of copying the files into your virtual environment, a symlink will be created to the files where they are.

#### Fetch data
```
python -m capstone fetch
```

#### Download NLTK data
```
python -m nltk.downloader all
```

#### Run jupyter server
```
jupyter notebook notebooks/
```

You can now use the jupyter kernel to run notebooks.

## Notebooks

The notebooks may be viewed in the following order:

1. *[eda.ipynb](notebooks/eda.ipynb)* - Exploratory Data Analysis

2. *[naive-model-evaluation.ipynb](notebooks/naive-model-evaluation.ipynb)* - Results from naive model which predicts the most common target (multi-label binarized vector) in the development set

3. *[baseline-evaluation.ipynb](notebooks/baseline-evaluation.ipynb)* - Results from baseline Random Forest trained on TF-IDF features

4. *[bert_evaluation.ipynb](notebooks/bert_evaluation.ipynb)* - Results from fine-tuned BERT

5. *[ada-evaluation.ipynb](notebooks/ada-evaluation.ipynb)* - Results from fine-tuned Ada

6. *[curie-evaluation.ipynb](notebooks/curie-evaluation.ipynb)* - Results from fine-tuned Curie

7. *[davinci-evaluation.ipynb](notebooks/davinci-evaluation.ipynb)* - Results from fine-tuned Davinci

8. *[ensemble-evaluation.ipynb](notebooks/ensemble-evaluation.ipynb)* - Results from ensemble of BERT, Ada, and Curie based on majority vote

9. *[bert_embeddings.ipynb](notebooks/bert_embeddings.ipynb)* - Evaluate embeddings of fine-tuned BERT against vanilla BERT on (unsupervised) clustering task (test dataset)

10. *[gpt3-embeddings-test-set.ipynb](notebooks/gpt3-embeddings-test-set.ipynb)* - Evaluate embeddings of vanilla GPT-3 models (Ada, Curie and Davinci) on (unsupervised) clustering task (test dataset)

11. *[gpt3-embeddings-whole-set.ipynb](notebooks/gpt3-embeddings-whole-set.ipynb)* - Evaluate embeddings of vanilla GPT-3 models (Ada, Curie and Davinci) on (unsupervised) clustering task (whole dataset)

## Reports

1. *[JnJ-Janssens_JnJ-3_Final_Report.pdf](reports/JnJ-Janssens_JnJ-3_Final_Report.pdf)* - Final report

2. *[JnJ-Janssens_JnJ-3_Poster.pdf ](reports/JnJ-Janssens_JnJ-3_Poster.pdf)* - Poster