import os
import django
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_project.settings')
django.setup()

from automl.models import TrainedModel

def main():
    print("Loading dataset...")
    # Load the training data
    df = pd.read_csv(r"C:\Users\SURAJ\Downloads\customer_churn_dataset-training-master.csv")
    
    # Preprocess
    print("Preprocessing data...")
    # Drop rows with missing target
    target_col = df.columns[-1]
    df = df.dropna(subset=[target_col])
    
    # Fill missing values
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].mean())
            
    # Force target to string/category if it's not
    df[target_col] = df[target_col].astype(str)
    
    y = df[target_col]
    X = df.drop(columns=[target_col, "CustomerID"], errors='ignore')
    
    # Handle categorical variables
    X = pd.get_dummies(X, drop_first=True)
    
    # Train model
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Save model
    print("Saving model...")
    model_name = "Customer_Churn_Model"
    save_dir = os.path.join(os.getcwd(), 'saved_models')
    os.makedirs(save_dir, exist_ok=True)
    pkl_path = os.path.join(save_dir, f"{model_name}.pkl")
    
    joblib.dump(model, pkl_path)
    
    # Save to database
    TrainedModel.objects.create(
        model_name=model_name,
        pkl_file_path=pkl_path,
        feature_columns=list(X.columns),
        target_column=target_col
    )
    
    print(f"Successfully trained and saved model: {model_name}")

if __name__ == "__main__":
    main()
