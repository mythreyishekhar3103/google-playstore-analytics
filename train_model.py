import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("data/googleplaystore.csv")

df = df.dropna(subset=["Rating"])

df["High_Rated"] = (df["Rating"] >= 4.0).astype(int)

le = LabelEncoder()

df["Category"] = le.fit_transform(
    df["Category"].astype(str)
)

X = df[["Category"]]
y = df["High_Rated"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

pickle.dump(
    model,
    open("model.pkl", "wb")
)

pickle.dump(
    le,
    open("label_encoder.pkl", "wb")
)

print("Model files created successfully")
