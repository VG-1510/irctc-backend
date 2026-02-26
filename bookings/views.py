from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Booking
from trains.models import Train
from django.db import transaction

# Book seats
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking(request):
    train_id = request.data.get('train_id')
    seats = int(request.data.get('seats'))
    try:
        train = Train.objects.get(id=train_id)
    except Train.DoesNotExist:
        return Response({
            "error": "Train not found"
        }, status=404)

    if train.available_seats < seats:
        return Response({
            "error": "Not enough seats available"
        }, status=400)

    # Transaction ensures safe seat deduction
    with transaction.atomic():
        train.available_seats -= seats
        train.save()
        booking = Booking.objects.create(
            user=request.user,
            train=train,
            seats_booked=seats
        )

    return Response({
        "message": "Booking successful",
        "booking_id": booking.id
    })


# Get my bookings
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    result = []
    for booking in bookings:
        result.append({
            "booking_id": booking.id,
            "train_number": booking.train.train_number,
            "train_name": booking.train.name,
            "source": booking.train.source,
            "destination": booking.train.destination,
            "seats_booked": booking.seats_booked,
            "booking_time": booking.booking_time
        })

    return Response(result)