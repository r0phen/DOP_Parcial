# applications/auth/models.py

from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Guardaremos password hasheada
    sex = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class FavoriteGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    game_id = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.URLField(blank=True)

    class Meta:
        unique_together = ('user', 'game_id')

    def __str__(self):
        return f"{self.title} - {self.user.username}"
