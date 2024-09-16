# Задание 1
Условие:
Приложение подразумевает ежедневный вход пользователя, начисление баллов за вход. Нужно отследить момент первого входа игрока для аналитики. Также у игрока имеются игровые бонусы в виде нескольких типов бустов. Нужно описать модели игрока и бустов с возможностью начислять игроку бусты за прохождение уровней или вручную. (Можно написать, применяя sqlachemy)
from django.db import models


class Player(models.Model):
    pass
    

class Boost(models.Model):
    pass

# Запуск Django shell
python manage.py shell


from myapp.models import Player

# Создаем нового игрока
new_player = Player.objects.create(username="Player1")

# Начисляем баллы за ежедневный вход
print(new_player.daily_login())

# Начисляем буст игроку
print(new_player.add_boost("speed", 5))

# Выводим информацию о игроке и его бустах
player = Player.objects.get(id=new_player.id)
print(f"Player: {player}")
for boost in player.boosts.all():
    print(f"Boost: {boost}")


Описание кода:
Модель Player:
username: Имя игрока.
first_login: Дата и время первого входа игрока.
points: Количество баллов игрока.
daily_login(): Метод для начисления баллов за ежедневный вход.
add_boost(boost_type, boost_amount): Метод для добавления буста игроку.

Модель Boost:
type: Тип буста (например, "speed", "health").
amount: Количество буста.
player: Внешний ключ, связывающий буст с игроком.

Пример использования в Django shell:
Создается новый игрок.
Начисляются баллы за ежедневный вход с помощью метода daily_login().
Добавляется буст игроку с помощью метода add_boost().
Выводится информация о игроке и его бустах.
Теперь все операции, связанные с начислением баллов и добавлением бустов, выполняются непосредственно через методы модели Player, что делает код более организованным и удобным для использования.



# Задание 2
from django.db import models

class Player(models.Model):
    player_id = models.CharField(max_length=100)
    
    
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
     
     
​
Написать два метода:
Присвоение игроку приза за прохождение уровня.
Выгрузку в csv следующих данных: id игрока, название уровня, пройден ли уровень, полученный приз за уровень. Учесть, что записей может быть 100 000 и более.

# Запуск Django shell
python manage.py shell


from myapp.models import Player, Level, Prize, PlayerLevel, LevelPrize
from django.utils import timezone

# Создаем игрока, уровень и приз
player = Player.objects.create(player_id="Player1")
level = Level.objects.create(title="Level 1", order=1)
prize = Prize.objects.create(title="Gold Medal")

# Создаем запись о прохождении уровня
player_level = PlayerLevel.objects.create(player=player, level=level, completed=timezone.now(), is_completed=True)

# Присваиваем игроку приз за прохождение уровня
print(player_level.assign_prize_for_level(prize))

# Выгружаем данные в CSV
response = PlayerLevel.export_player_levels_to_csv()
with open('player_levels.csv', 'wb') as f:
    f.write(response.content)

Описание кода:
Модель Player:
player_id: Уникальный идентификатор игрока.

Модель Level:
title: Название уровня.
order: Порядковый номер уровня.

Модель Prize:
title: Название приза.

Модель PlayerLevel:
player: Внешний ключ на модель Player.
level: Внешний ключ на модель Level.
completed: Дата прохождения уровня.
is_completed: Флаг, указывающий, пройден ли уровень.
score: Очки, набранные за уровень.
assign_prize_for_level(prize): Метод для присвоения игроку приза за прохождение уровня.
export_player_levels_to_csv(): Статический метод для выгрузки данных в CSV.

Модель LevelPrize:
level: Внешний ключ на модель Level.
prize: Внешний ключ на модель Prize.
received: Дата получения приза.

Пример использования в Django shell:
Создаются игрок, уровень и приз.
Создается запись о прохождении уровня.
Присваивается игроку приз за прохождение уровня.
Выгружаются данные в CSV.
