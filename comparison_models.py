

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression


TARGET_COL = "classification"
POS_LABEL = "outlier"
CSV_PATH = "supervised_dataset.csv"




df = pd.read_csv(CSV_PATH)
df = df.drop(columns=[c for c in ["Unnamed: 0", "_id"] if c in df.columns])

X = df.drop(columns=[TARGET_COL])
y = df[TARGET_COL]


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


numeric_features = X.select_dtypes(include=["int64","float64","int32","float32"]).columns
categorical_features = X.select_dtypes(include=["object","bool","category"]).columns

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("numeric", numeric_transformer, numeric_features),
        ("categorical", categorical_transformer, categorical_features),
    ]
)


def evaluate_model(name, model, is_iso=False):
    print(f"\n================== {name} ==================")

    if is_iso:
        model.fit(X_train)
        raw = model.predict(X_test)
        y_pred = np.where(raw == 1, "normal", "outlier")
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, pos_label=POS_LABEL)
    rec = recall_score(y_test, y_pred, pos_label=POS_LABEL)
    f1 = f1_score(y_test, y_pred, pos_label=POS_LABEL)

    cm = confusion_matrix(y_test, y_pred, labels=["normal", "outlier"])

    print(f"\nAccuracy  : {acc}")
    print(f"Precision : {prec}")
    print(f"Recall    : {rec}")
    print(f"F1-score  : {f1}")

    print("\nConfusion matrix:")
    print(cm)
    print("="*50)



models = [
    ("Random Forest",
     Pipeline([("prep", preprocessor),
               ("model", RandomForestClassifier(n_estimators=200, class_weight="balanced"))]),
     False),

    ("SVM (RBF)",
     Pipeline([("prep", preprocessor),
               ("model", SVC(kernel="rbf", class_weight="balanced"))]),
     False),

    ("Logistic Regression",
     Pipeline([("prep", preprocessor),
               ("model", LogisticRegression(max_iter=1000, class_weight="balanced"))]),
     False),

    ("Isolation Forest",
     Pipeline([("prep", preprocessor),
               ("model", IsolationForest(random_state=42))]),
     True),
]



for name, model, iso in models:
    evaluate_model(name, model, iso)
