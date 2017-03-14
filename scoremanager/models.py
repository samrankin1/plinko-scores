import uuid

from django.db import models
from django.utils import timezone

from . import validators

def identifier_default():
	return uuid.uuid4().hex

class ScoreboardEntry(models.Model):
	identifier		 = models.CharField(max_length = 32, default = identifier_default, editable = False, primary_key = True) # UUIDv4; primary key
	date_created	 = models.DateTimeField(default = timezone.now) # date and time created; automatically set, editable
	score			 = models.PositiveIntegerField() # score (in points), editable
	balls_dropped	 = models.PositiveIntegerField() # balls dropped during the game, editable

	def __str__(self):
		return str(self.score) # a ScoreboardEntry can be represented by its score

	@staticmethod
	def create_new_scoreboard_entry(score, balls_dropped):
		new_scoreboard_entry = ScoreboardEntry(score = score, balls_dropped = balls_dropped)
		new_scoreboard_entry.save()
		return new_scoreboard_entry

	class Meta:
		ordering = ['-score', 'balls_dropped', 'date_created'] # sort by score highest first, then by balls_dropped lowest first, then by date_created newest first
