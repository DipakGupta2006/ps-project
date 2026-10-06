import time
from django.shortcuts import render
from django.db.models import Avg
from .models import StudentLog

def predict_marks(request):
    context = {}
    if request.method == 'POST':
        start_time = time.time()
        try:
            study_hours = float(request.POST.get('study_hours', 0))
            
            # Dummy Model: Marks = Study Hours * 9.5 + 5 (Max 100)
            predicted_marks = min(study_hours * 9.5 + 5, 100.0)
            
            end_time = time.time()
            response_time_ms = (end_time - start_time) * 1000
            
            # Save Log
            StudentLog.objects.create(
                study_hours=study_hours,
                predicted_marks=predicted_marks,
                response_time_ms=response_time_ms
            )
            
            context = {
                'study_hours': study_hours,
                'predicted_marks': round(predicted_marks, 2),
                'response_time_ms': round(response_time_ms, 2)
            }
        except ValueError:
            context['error'] = "Invalid input. Please enter a valid number."
            
    return render(request, 'student_predict.html', context)

def dashboard(request):
    import json
    total_predictions = StudentLog.objects.count()
    avg_response_time = StudentLog.objects.aggregate(Avg('response_time_ms'))['response_time_ms__avg'] or 0
    recent_logs = StudentLog.objects.order_by('-created_at')[:5]
    
    # Fake Data Drift Alert
    # Let's say if any of the recent 5 logs has study_hours > 24 or < 0
    drift_alert = any(log.study_hours > 24 or log.study_hours < 0 for log in recent_logs)
    
    # All logs for charts (limit to last 50 for performance if needed, but let's take all for now or say last 20)
    all_logs = StudentLog.objects.order_by('created_at')
    
    chart_labels = [log.created_at.strftime("%H:%M:%S") for log in all_logs]
    marks_data = [log.predicted_marks for log in all_logs]
    response_times = [log.response_time_ms for log in all_logs]
    scatter_data = [{'x': log.study_hours, 'y': log.predicted_marks} for log in all_logs]
    
    context = {
        'total_predictions': total_predictions,
        'avg_response_time': round(avg_response_time, 2),
        'recent_logs': recent_logs,
        'drift_alert': drift_alert,
        'chart_labels': json.dumps(chart_labels),
        'marks_data': json.dumps(marks_data),
        'response_times': json.dumps(response_times),
        'scatter_data': json.dumps(scatter_data),
    }
    return render(request, 'student_dashboard.html', context)
