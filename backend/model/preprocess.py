import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess_data(path):

    df = pd.read_csv(path)

    label_encoders = {}

    # Convert categorical columns
    for col in df.select_dtypes(include="object").columns:

        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])

        label_encoders[col] = le

    return df