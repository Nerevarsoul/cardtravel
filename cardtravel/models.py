import datetime

from django.db import models
from django.contrib.auth.models import User


def encode_url(raw_url):
    return raw_url.replace(' ', '_')


# Create your models here.
class Card(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    series = models.CharField(max_length=50)
    catalog_codes = models.CharField(max_length=50)
    issued_on = models.IntegerField()
    description = models.TextField(blank=True)
    face_picture = models.ImageField(upload_to='card_images', blank=True)
    reverse_picture = models.ImageField(upload_to='card_images', blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/cards/%i/" % self.id


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile")

    picture = models.ImageField(upload_to='profile_images', blank=True)
    address = models.TextField(blank=True)
    wishlist = models.ManyToManyField(Card, related_name="wishlist", blank=True, null=True)
    collection = models.ManyToManyField(Card, related_name="collection", blank=True, null=True)

    def __unicode__(self):
        return self.user.username


class Trade(models.Model):

    CONDITION = (
        ('mint', ('mint')), 
        ('mint+', ('mint+')), 
        ('mint--', ('mint--')), 
        ('mint-', ('mint-')),
    )

    user = models.ForeignKey(User)
    card = models.ForeignKey(Card)
    condition = models.CharField(choices=CONDITION, max_length=20)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='active')
    face_picture = models.ImageField(upload_to='trade_images')
    reverse_picture = models.ImageField(upload_to='trade_images', blank=True, default=None)
    addiction_picture1 = models.ImageField(upload_to='trade_images', blank=True, default=None)
    addiction_picture2 = models.ImageField(upload_to='trade_images', blank=True, default=None)
    addiction_picture3 = models.ImageField(upload_to='trade_images', blank=True, default=None)
    date = models.DateTimeField(auto_now=True, default = datetime.datetime.now())

    def __unicode__(self):
        return "{} {}".format(self.card.name, self.condition)

    def get_absolute_url(self):
        return "/trades/%i/" % self.id


class Comment(models.Model):
    user = models.ForeignKey(User)
    trade = models.ForeignKey(Trade)
    text = models.TextField()
    created = models.DateTimeField(auto_now=True, default = datetime.datetime.now())

    def __unicode__(self):
        return "{} {}".format(self.user.name, self.time)