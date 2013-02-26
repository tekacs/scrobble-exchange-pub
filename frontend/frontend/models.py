from django.db import models
from django.contrib.auth.models import User

from se_api import ttypes

class Artist(models.Model):
	mbid = models.CharField(max_length=36)
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

class Profile(models.Model):
	user = models.OneToOneField(User)
	authuser = ttypes.AuthUser


#class ArtistHistory(models.Model):
	#TODO: histvalue
	#TODO: daterange

# class ArtistSE(models.Model):
# 	artist = models.ForeignKey('Artist')
# 	price = models.IntegerField()
# 	num_remaining = models.IntegerField()
# 	ownedby = models.BooleanField()






# 	fund_score = models.IntegerField('Fundamental Score')
# 	market_score = models.IntegerField('Market Score')

# 	def __unicode__(self):	

class UserData(models.Model):
	worth = models.IntegerField()

	def __unicode__(self):
		return 'user data'