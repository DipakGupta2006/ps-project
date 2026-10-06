import os
import django
import pandas as pd
import joblib
import time
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_project.settings')
django.setup()

from automl.models import TrainedModel, PredictionLog

def main():
    print("Loading test dataset...")
    df = pd.read_csv(r"C:\Users\SURAJ\Downloads\customer_churn_dataset-testing-master.csv")
    
    model_obj = TrainedModel.objects.filter(model_name="Customer_Churn_Model").first()
    if not model_obj:
        print("Model not found in DB.")
        return
        
    model = joblib.load(model_obj.pkl_file_path)
    features = model_obj.feature_columns
    
    # Preprocess testing data
    df = df.dropna()
    target_col = df.columns[-1]
    X_test = df.drop(columns=[target_col, "CustomerID"], errors='ignore')
    X_test = pd.get_dummies(X_test, drop_first=True)
    
    # Align features (add missing cols with 0)
    for f in features:
        if f not in X_test.columns:
            X_test[f] = 0
            
    # Reorder
    X_test = X_test[features]
    
    print("Running predictions to populate monitor log...")
    # Take first 50 rows
    for _, row in X_test.head(50).iterrows():
        start = time.time()
        
        # Convert row to DataFrame for prediction
        row_df = pd.DataFrame([row])
        pred = model.predict(row_df)[0]
        
        end = time.time()
        latency = (end - start) * 1000 + random.uniform(5, 15) # Add some artificial latency for the chart
        
        PredictionLog.objects.create(
            trained_model=model_obj,
            input_data=row.to_dict(),
            prediction_result=str(pred),
            response_time_ms=latency
        )
        
    print("Successfully populated 50 prediction logs!")

if __name__ == "__main__":
    main()
