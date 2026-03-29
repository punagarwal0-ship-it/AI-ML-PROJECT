import pandas as pd
import numpy as np
import os
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments
)
from torch.utils.data import Dataset

FILE="history.csv"
OUTDIR="model"
EPOCHS=4
BATCH=8
MAXLEN=256

def score_to_label(score):
    score=int(score)
    if score>=75: return 2
    if score>=40: return 1
    return 0

LABELS={0:"Sensational",1:"Mixed",2:"Professional"}

class ArticleDataset(Dataset):
    def __init__(self,encodings,labels):
        self.encodings=encodings
        self.labels=labels
    def __len__(self):
        return len(self.labels)
    def __getitem__(self,idx):
        item={k:torch.tensor(v[idx]) for k,v in self.encodings.items()}
        item["labels"]=torch.tensor(self.labels[idx])
        return item

def load_data():
    if not os.path.isfile(FILE):
        print(f"[!] {FILE} not found. Run batch_score.py first.")
        exit(1)
    df=pd.read_csv(FILE)
    if len(df)<50:
        print(f"[!] Only {len(df)} rows in history.csv. Need at least 50. Run batch_score.py to collect more.")
        exit(1)
    df=df.dropna(subset=["writer_intent_summary","neutrality_score"])
    df["label"]=df["neutrality_score"].apply(score_to_label)
    print(f"[+] Loaded {len(df)} records.")
    print(f"    Label distribution: {df['label'].value_counts().to_dict()}")
    return df["writer_intent_summary"].tolist(),df["label"].tolist()

def compute_metrics(pred):
    labels=pred.label_ids
    preds=pred.predictions.argmax(-1)
    report=classification_report(labels,preds,target_names=list(LABELS.values()),output_dict=True)
    return {"accuracy":report["accuracy"]}

def run():
    texts,labels=load_data()
    xtrain,xtest,ytrain,ytest=train_test_split(texts,labels,test_size=0.2,random_state=42,stratify=labels)
    print(f"[+] Train: {len(xtrain)}  Test: {len(xtest)}")
    print("[+] Loading tokenizer...")
    tokenizer=DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
    print("[+] Tokenizing...")
    trainenc=tokenizer(xtrain,truncation=True,padding=True,max_length=MAXLEN)
    testenc=tokenizer(xtest,truncation=True,padding=True,max_length=MAXLEN)
    trainset=ArticleDataset(trainenc,ytrain)
    testset=ArticleDataset(testenc,ytest)
    print("[+] Loading model...")
    model=DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased",num_labels=3)
    args=TrainingArguments(
        output_dir=OUTDIR,
        num_train_epochs=EPOCHS,
        per_device_train_batch_size=BATCH,
        per_device_eval_batch_size=BATCH,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        logging_dir="logs",
        logging_steps=10,
    )
    trainer=Trainer(
        model=model,
        args=args,
        train_dataset=trainset,
        eval_dataset=testset,
        compute_metrics=compute_metrics,
    )
