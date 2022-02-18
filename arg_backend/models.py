from django.db import models
import uuid
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.urls import reverse

import json



class Puzzle(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(null=True,blank=True,max_length=100)
    puzzle_text = models.CharField(null=False,blank=False,unique=True,max_length=2000)
    completion_text = models.CharField(null=True,blank=True,max_length=1000)
    possible_answers = models.JSONField(null=True,blank=True)
    hints = models.JSONField(null=True,blank=True)
    location_hints = models.JSONField(null=True,blank=True)    
    points = models.IntegerField(null=True,blank=True)
    deadline = models.DateTimeField(auto_now_add=False,null=True,blank=False)
    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return str(self.title)

# Create your models here.
class Teams(models.Model):
    id             = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    team_username           = models.CharField(null=False,blank=False,unique=True,max_length=100)
    score          = models.IntegerField(null=True,blank=False)
    
    current_puzzle =  models.ForeignKey(Puzzle,on_delete=models.SET_NULL,null=True,blank=True)
    current_hint   = models.IntegerField(null=True,blank=False,default=0)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at", null=True)

    class Meta:
        ordering = ['-score']
    
    def __str__(self):
        return str(self.team_username)




class PuzzleQueue(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    parent_puzzle = models.ForeignKey(Puzzle,on_delete=models.SET_NULL,null=True,blank=True,related_name="parent_puzzle")
    child_puzzle = models.ForeignKey(Puzzle,on_delete=models.SET_NULL,null=True,blank=True,related_name="child_puzzle")

    class Meta:
        ordering = ['parent_puzzle']

    def __str__(self):
        return str(self.parent_puzzle)


class Players(models.Model):
    id             = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    player_name           = models.CharField(null=False,blank=False,max_length=100)
    discord_username           = models.CharField(null=False,blank=False,unique=True,max_length=100)
    team                    = models.ForeignKey(Teams,on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at", null=True)
    
    class Meta:
        ordering = ['created_at']
    def __str__(self):
        return str(self.player_name)



class image_mapper(models.Model):
    id             =  models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    puzzle         =  models.ForeignKey(Puzzle,on_delete=models.SET_NULL,null=True,blank=True)  
    half_password  =  models.CharField(null=True,blank=True,max_length=100,unique=True)
    full_password  =  models.CharField(null=True,blank=True,max_length=100,unique=True)
    code           =  models.CharField(null=False,blank=False,max_length=100,unique=True)
    url            =  models.CharField(null=False,blank=False,max_length=600)
    unlock_time = models.DateTimeField(auto_now_add=False,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at", null=True)
    
    class Meta:
        ordering = ['code']
    
    def __str__(self):
        return str(self.code)