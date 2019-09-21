This folder contain the algorithms for feature grounding, as well as the target CUB image dataset

Feature grounding is a neural-network based technique that highlights the image region of target
attributes (e.g., blue chest, red belly of birds, in our case). For more information about this 
technique, please refer to the paper: "Guo, Pei & Anderson, Connor & Pearson, Kolten & Farrell, 
Ryan. (2018). Neural Network Interpretation via Fine Grained Textual Summarization. "

The main algorithms in this folder are:

- "finetune.py": finetunes a pre-trained Resnet 50 model on the CUB dataset

- "VAG.ipynb": that apply the finetuned Resnet model to generate a Bayesian Inference framework, whcih
implements feature extraction. Please note that this programme is in Jupyter Notebook format.

The other python codes in this folder are sub-funtions of the above main algorithms, and

- "data_split.py" and "train_test_split": split the CUB image dataset into training and testing sets.

- "utils.py": stores some utility functions and they are not necessary for this experiment.

The other text and image files belong to the original CUB dataset.







