import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.


def public_id_fun():
    length = 16
    while True:
        code = ''.join(random.choices(string.ascii_letters, k=length))
        if Profile.objects.filter(public_id=code).count() == 0:
            break
    return code


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    first_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    mobile_number = models.CharField(max_length=25, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    dp = models.ImageField(default='Mikasa.jpg',
                           upload_to='dp', blank=True, null=True)
    public_id = models.CharField(
        max_length=25, default=public_id_fun, unique=True)
    wallet = models.IntegerField(blank=True, null=True, default=100)
    payment_password = models.CharField(
        max_length=255, default='hello', blank=True, null=True)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.user)


class Post(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=CASCADE)

    text_area = models.TextField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    cash_required = models.CharField(max_length=255, blank=True, null=True)
    cash_received = models.IntegerField(default=0, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    documents = models.FileField(upload_to='doc', blank=True, null=True)
    category = models.IntegerField(default=0, blank=True, null=True)
    completed = models.BooleanField(default=False)
    sort_factor = models.FloatField(blank=True,null=True)

    def __str__(self):
        return str(self.id)


class Payment(models.Model):
    sender_profile = models.ForeignKey(
        Profile, related_name='sender_profile', on_delete=CASCADE)
    receiver_profile = models.ForeignKey(
        Profile, related_name='receiver_profile', on_delete=CASCADE)
    post = models.ForeignKey(Post, related_name='post_map', on_delete=CASCADE)
    cash = models.CharField(max_length=25, blank=True, null=True)
    date_created = models.CharField(max_length=255, blank=True, null=True)


class Block(models.Model):
    payment_header = models.ForeignKey(Payment, on_delete=CASCADE)
    current_hash = models.CharField(max_length=255, blank=True, null=True)
    previous_hash = models.CharField(max_length=225, blank=True)
    nonce = models.CharField(max_length=10, blank=True, null=True)
    sender = models.CharField(max_length=255, blank=True, null=True)
    receiver = models.CharField(max_length=255, blank=True, null=True)
    cash = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.CharField(max_length=255, blank=True, null=True)
