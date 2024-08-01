from django.db import models
import datetime
import csv

class Player(models.Model):
    player_id = models.CharField(max_length=100)
    
    def give_prize(self, level, prize):
        try:
            player_level = PlayerLevel.objects.get(player=self.player_id, level=level)
            if player_level.is_completed:
                LevelPrize.objects.create(level=level, prize=prize, received=datetime.datetime.now())
                print(f"Приз '{prize.title}' присвоен игроку '{self.player_id}' за прохождение уровня '{level.title}'")
            else:
                print(f"Игрок '{self.player_id}' еще не прошел уровень '{level.title}'")
        except PlayerLevel.DoesNotExist:
            print(f"Игроку '{self.player_id}' не удалось начислить приз'")

    @staticmethod
    def export_csv(filename):
        fieldnames = ['player_id', 'level_title', 'is_completed', 'prize_title']
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for player_level in PlayerLevel.objects.all().iterator():
                level_prizes = LevelPrize.objects.filter(level=player_level.level)
                for level_prize in level_prizes:
                    writer.writerow({
                        'player_id': player_level.player.player_id,
                        'level_title': player_level.level.title,
                        'is_completed': player_level.is_completed,
                        'prize_title': level_prize.prize.title
                    })

class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    
    
    
class Prize(models.Model):
    title = models.CharField()
    
    
class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField()
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)
    
    
class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField()