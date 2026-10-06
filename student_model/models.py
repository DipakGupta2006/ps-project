from django.db import models

class StudentLog(models.Model):
    study_hours = models.FloatField()
    predicted_marks = models.FloatField()
    response_time_ms = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"StudentLog - {self.study_hours} hrs -> {self.predicted_marks} marks"
