import os
import sys

sys.path.append(os.getcwd())
os.chdir("..")

import pandas as pd
import torch
from src import surname_classification
from src import utils
from src.label_encoder import LabelEncoder
from torch.utils.data import DataLoader
import pickle
from transformers import BertForSequenceClassification, get_linear_schedule_with_warmup, BertTokenizer
from itertools import islice
from sklearn.model_selection import train_test_split


df = pd.read_parquet("data/preprocessed/final_dataset.parquet")

label_encoder = LabelEncoder(columns_to_encode=["country"])
df = label_encoder.fit_transform(df)

valid_size = 0.2
test_size = 0.5
random_state = 1
df_train, df_valid = train_test_split(df, test_size=valid_size, stratify=df["country"], random_state=random_state)
df_valid, df_test = train_test_split(df_valid, test_size=test_size, stratify=df_valid["country"], random_state=random_state)


# Tokenize each dataset
train_encodings = surname_classification.tokenize_data(df_train, surname_col="surname")
val_encodings = surname_classification.tokenize_data(df_val, surname_col="surname")
test_encodings = surname_classification.tokenize_data(df_test, surname_col="surname")

utils.dill_dump(file_loc="data/encodings/train_encodings.dill", content=train_encodings)
utils.dill_dump(file_loc="data/encodings/val_encodings.dill", content=val_encodings)
utils.dill_dump(file_loc="data/encodings/test_encodings.dill", content=test_encodings)