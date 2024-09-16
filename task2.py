import csv
from django.db import models
from django.utils import timezone
from django.http import HttpResponse


class Player(models.Model):
    player_id = models.CharField(max_length=100)

    def __str__(self):
        return self.player_id


class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Prize(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.player.player_id} - {self.level.title}"

    def assign_prize_for_level(self, prize):
        if self.is_completed:
            LevelPrize.objects.create(
                level=self.level, prize=prize, received=timezone.now())
            return f"Prize {prize.title} assigned for level {self.level.title}"
        else:
            return "Level is not completed yet"

    @staticmethod
    def export_player_levels_to_csv():
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="player_levels.csv"'

        writer = csv.writer(response)
        writer.writerow(['Player ID', 'Level Title',
                        'Is Completed', 'Prize Title'])

        player_levels = PlayerLevel.objects.select_related(
            'player', 'level').all()
        for player_level in player_levels:
            prize_title = LevelPrize.objects.filter(level=player_level.level).first(
            ).prize.title if LevelPrize.objects.filter(level=player_level.level).exists() else ''
            writer.writerow([player_level.player.player_id,
                            player_level.level.title, player_level.is_completed, prize_title])

        return response


class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField()

    def __str__(self):
        return f"{self.prize.title} for {self.level.title}"
