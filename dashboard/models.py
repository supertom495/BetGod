from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(
        User,
        null=True,
        on_delete=models.CASCADE

    )
    mobile = models.CharField(max_length=20)


class Post(models.Model):
    author = models.ForeignKey(
        Author,
        null=True,
        on_delete=models.CASCADE,
        related_name="post_author"
    )
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=1000)


class Card(models.Model):
    card_type = models.CharField(max_length=50)
    card_number = models.BigIntegerField(primary_key=True)
    card_expiration_date = models.DateField()
    card_CVV = models.IntegerField()


class Wallet(models.Model):
    wallet_id = models.AutoField(primary_key=True)
    wallet_points = models.PositiveIntegerField()
    wallet_card = models.ForeignKey(Card, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_description = models.CharField(max_length=500)
    user_security_question = models.CharField(max_length=200)
    user_security_answer = models.CharField(max_length=200)
    user_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)


class LeaderBoard(models.Model):
    rank = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Team(models.Model):
    team_name = models.CharField(max_length=200)
    team_description = models.CharField(max_length=500)


class Admin(models.Model):
    admin_email = models.EmailField()
    admin_nickname = models.CharField(max_length=20)
    admin_password = models.CharField(max_length=200)
    admin_privilege = models.IntegerField()


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=200)
    event_result = models.CharField(max_length=200)
    event_create_date = models.DateField()
    event_odds_a = models.FloatField()
    event_odds_b = models.FloatField()
    event_team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='+')
    event_team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='+')
    event_admin = models.ForeignKey(Admin, on_delete=models.CASCADE)


class Bet(models.Model):
    bet_id = models.AutoField(primary_key=True)
    bet_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    bet_user = models.ForeignKey(User, on_delete=models.CASCADE)
    bet_odds = models.FloatField()
    bet_amount = models.FloatField()
    bet_date = models.DateField()
    bet_result_released = models.BooleanField()
    bet_result = models.BooleanField()
