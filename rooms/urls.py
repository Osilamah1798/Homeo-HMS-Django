
from django.urls import path
from .views import get_rooms, add_room, update_room, delete_room, RoomDetailView

urlpatterns = [
    path('getrooms/', get_rooms, name='get-rooms'),
    path('addrooms/', add_room, name='add-room'),
    path('updaterooms/<int:id>/', update_room, name='update-room'),
    path('deleterooms/<int:id>/', delete_room, name='delete-room'),
    path('rooms/<int:id>/', RoomDetailView.as_view(), name='room-detail'),
]
