import time
from django.shortcuts import render
from django.db.models import Avg
from .models import HouseLog

def predict_price(request):
    context = {}
    if request.method == 'POST':
        start_time = time.time()
        try:
            square_feet = float(request.POST.get('square_feet', 0))
            
            # Dummy Model: Price = Square Feet * 150 + 50000
            predicted_price = square_feet * 150 + 50000
            
            end_time = time.time()
            response_time_ms = (end_time - start_time) * 1000
            
            # Save Log
            HouseLog.objects.create(
                square_feet=square_feet,
                predicted_price=predicted_price,
                response_time_ms=response_time_ms
            )
            
            context = {
                'square_feet': square_feet,
                'predicted_price': round(predicted_price, 2),
                'response_time_ms': round(response_time_ms, 2)
            }
        except ValueError:
            context['error'] = "Invalid input. Please enter a valid number."
            
    return render(request, 'house_predict.html', context)

def dashboard(request):
    import json
    total_predictions = HouseLog.objects.count()
    avg_response_time = HouseLog.objects.aggregate(Avg('response_time_ms'))['response_time_ms__avg'] or 0
    recent_logs = HouseLog.objects.order_by('-created_at')[:5]
    
    # Fake Data Drift Alert
    # e.g., if square_feet is out of range (< 100 or > 10000)
    drift_alert = any(log.square_feet > 10000 or log.square_feet < 100 for log in recent_logs)
    
    # All logs for charts
    all_logs = HouseLog.objects.order_by('created_at')
    
    chart_labels = [log.created_at.strftime("%H:%M:%S") for log in all_logs]
    price_data = [log.predicted_price for log in all_logs]
    response_times = [log.response_time_ms for log in all_logs]
    scatter_data = [{'x': log.square_feet, 'y': log.predicted_price} for log in all_logs]
    
    context = {
        'total_predictions': total_predictions,
        'avg_response_time': round(avg_response_time, 2),
        'recent_logs': recent_logs,
        'drift_alert': drift_alert,
        'chart_labels': json.dumps(chart_labels),
        'price_data': json.dumps(price_data),
        'response_times': json.dumps(response_times),
        'scatter_data': json.dumps(scatter_data),
    }
    return render(request, 'house_dashboard.html', context)
