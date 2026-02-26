from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .models import Train
from django.utils import timezone
from irctc.mongodb import api_logs
import time

#Create train
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_train(request):
    if request.user.role != 'admin':
        return Response({
            "error": "Only admin can create trains"
        }, status=403)

    data = request.data

    train = Train.objects.create(
        train_number=data['train_number'],
        name=data['name'],
        source=data['source'],
        destination=data['destination'],
        departure_time=data['departure_time'],
        arrival_time=data['arrival_time'],
        total_seats=data['total_seats'],
        available_seats=data['available_seats']
    )

    return Response({
        "message": "Train created successfully"
    })

# Search trains
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_trains(request):
    start_time = time.time()
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    trains = Train.objects.filter(
        source=source,
        destination=destination
    )
    result = []
    for train in trains:
        result.append({
            "train_number": train.train_number,
            "name": train.name,
            "source": train.source,
            "destination": train.destination,
            "departure_time": train.departure_time,
            "arrival_time": train.arrival_time,
            "available_seats": train.available_seats
        })
    execution_time = time.time() - start_time

    # Log to MongoDB
    api_logs.insert_one({
        "endpoint": "/api/trains/search/",
        "source": source,
        "destination": destination,
        "user_id": str(request.user.id),
        "execution_time": execution_time,
        "timestamp": timezone.now()
    })

    return Response(result)