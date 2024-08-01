from django.db import models
from django.utils import timezone

class Player(models.Model):

    first_login = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(blank=True, null=True)
    daily_points = models.PositiveIntegerField(default=0)
    level_complete = models.BooleanField(default=False)
    def add_boost(self, boost_type):
        Boost.objects.create(player=self.id, type_boost=boost_type)    

class Boost(models.Model):
    BOOST_TYPE_CHOICES = [
        ('speed', 'Speed Boost'),
        ('strength', 'Strength Boost'),
        ('health', 'Health Boost'),
    ]
    
    type_boost = models.CharField(max_length=50, choices=BOOST_TYPE_CHOICES)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='boosts')
    assigned_at = models.DateTimeField(default=timezone.now)

