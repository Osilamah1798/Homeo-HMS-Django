from django.db import models

class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
        # Add more room types as needed
    ]

    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('not_available', 'Not Available'),
    ]

    image_url = models.URLField(max_length=500)
    type = models.CharField(max_length=20, choices=ROOM_TYPES)
    capacity = models.IntegerField()
    size = models.CharField(max_length=50)  # e.g., "300 sq ft"
    breakfast = models.BooleanField(default=False)
    pets = models.BooleanField(default=False)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')

    # Additional fields you might want to consider
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type} Room - {self.capacity} Person(s)"

    class Meta:
        ordering = ['price_per_day'] 