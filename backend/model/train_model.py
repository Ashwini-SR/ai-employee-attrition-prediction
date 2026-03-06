import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from preprocess import preprocess_data

# Load dataset
df = preprocess_data("../dataset/employee_attrition.csv")

# Features and target
X = df.drop("Attrition", axis=1)
y = df["Attrition"]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Evaluate
pred = model.predict(X_test)

accuracy = accuracy_score(y_test, pred)

print("Model Accuracy:", accuracy)

# Save trained model
joblib.dump(model, "attrition_model.pkl")

print("Model Saved Successfully")