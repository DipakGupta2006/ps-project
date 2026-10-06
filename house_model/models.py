from django.db import models

class HouseLog(models.Model):
    square_feet = models.FloatField()
    predicted_price = models.FloatField()
    response_time_ms = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"HouseLog - {self.square_feet} sqft -> ${self.predicted_price}"
