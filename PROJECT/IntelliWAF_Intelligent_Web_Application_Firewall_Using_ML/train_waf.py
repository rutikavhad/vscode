import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib


df=pd.read_csv("vul_dataset.csv")
print(df.head())
X=df['text_input']
y=df['label']


#train a machin via this code
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


#convert text to number

vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)


