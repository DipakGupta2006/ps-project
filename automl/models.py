from django.db import models

class TrainedModel(models.Model):
    model_name = models.CharField(max_length=255, unique=True)
    pkl_file_path = models.CharField(max_length=500)
    feature_columns = models.JSONField()
    target_column = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.model_name

class PredictionLog(models.Model):
    trained_model = models.ForeignKey(TrainedModel, on_delete=models.CASCADE, related_name='logs')
    input_data = models.JSONField()
    prediction_result = models.CharField(max_length=255)
    response_time_ms = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trained_model.model_name} Prediction at {self.timestamp}"
