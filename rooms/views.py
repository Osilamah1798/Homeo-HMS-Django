import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Room
from django.views import View
# from rest_framework.generics import RetrieveAPIView
from .serializers import RoomSerializer

@csrf_exempt
def get_rooms(request):
    if request.method == 'GET':
        # Extract query parameters
        room_type = request.GET.get('type')
        room_capacity = request.GET.get('capacity')

        # Fetch all rooms
        rooms = Room.objects.all()

        # Apply filters based on query parameters
        if room_type:
            rooms = rooms.filter(type__icontains=room_type)
        
        if room_capacity:
            try:
                capacity = int(room_capacity)
                rooms = rooms.filter(capacity=capacity)
            except ValueError:
                return JsonResponse({"error": "Invalid capacity value"}, status=400)

        # Convert queryset to list of dicts
        room_list = list(rooms.values())

        return JsonResponse({"data": room_list}, status=200)
    else:
        return JsonResponse({"error": "GET method required"}, status=400)

@csrf_exempt
def add_room(request):
    if request.method == 'POST':
        try:
            json_data = request.body.decode('utf-8')
            data_dict = json.loads(json_data)

            # Check if a room with the same type and capacity already exists
            existing_room = Room.objects.filter(type=data_dict.get("type"), capacity=data_dict.get("capacity")).first()
            if existing_room:
                return JsonResponse({"message": "Room with this type and capacity already exists"}, status=409)

            # Create a new room
            Room.objects.create(**data_dict)
            return JsonResponse({"message": "Room added successfully"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "POST method required"}, status=400)


@csrf_exempt
def update_room(request, id):
    if request.method == 'PUT':
        try:
            json_data = request.body.decode('utf-8')
            data_dict = json.loads(json_data)
            
            # Fetch the room by ID
            try:
                room = Room.objects.get(id=id)
            except Room.DoesNotExist:
                return JsonResponse({"error": "Room not found"}, status=404)

            # Update the room fields
            for field in ['image_url', 'type', 'capacity', 'size', 'breakfast', 'pets', 'price_per_day', 'description', 'availability']:
                if field in data_dict:
                    setattr(room, field, data_dict[field])
            room.save()

            return JsonResponse({"message": "Room updated successfully"}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "PUT method required"}, status=400)

@csrf_exempt
def delete_room(request, id):
    if request.method == 'DELETE':
        try:
            # Fetch the room by ID
            try:
                room = Room.objects.get(id=id)
            except Room.DoesNotExist:
                return JsonResponse({"error": "Room not found"}, status=404)

            # Delete the room
            room.delete()
            return JsonResponse({"message": "Room deleted successfully"}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "DELETE method required"}, status=400)

class RoomDetailView(View):
    def get(self, request, id, *args, **kwargs):
        try:
            room = Room.objects.get(id=id)
            serializer = RoomSerializer(room)
            return JsonResponse(serializer.data)
        except Room.DoesNotExist:
            return JsonResponse({'error': 'Room not found'}, status=404)