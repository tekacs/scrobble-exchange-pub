from django.db import models

class Artist(models.Model):
	name = models.CharField(max_length=200)
	fund_score = models.IntegerField('Fundamental Score')
	market_score = models.IntegerField('Market Score')

	def __unicode__(self):
		return self.name

class UserData(models.Model):
	worth = models.IntegerField()

	def __unicode__(self):
		return 'user data'