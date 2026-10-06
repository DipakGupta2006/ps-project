from django.shortcuts import render
from student_model.models import StudentLog
from house_model.models import HouseLog

def home(request):
    total_student_predictions = StudentLog.objects.count()
    total_house_predictions = HouseLog.objects.count()
    total_predictions = total_student_predictions + total_house_predictions
    
    context = {
        'total_predictions': total_predictions,
        'total_student_predictions': total_student_predictions,
        'total_house_predictions': total_house_predictions,
    }
    return render(request, 'home.html', context)
