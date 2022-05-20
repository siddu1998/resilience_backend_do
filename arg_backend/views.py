from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from . import  models,serializers
from rest_framework import viewsets
from django.utils import timezone
import json
from datetime import datetime

def index(request):
    return JsonResponse({"message":"Hello Unity! From Django"})


@api_view(http_method_names=['GET'])
def test(request):
    return JsonResponse({"message":"Hello Unity! From Django. You Just called the TEST API"})


# PROJECT APIs Start here


# Django Serializer APIs





# Regular APIs
@api_view(http_method_names=['GET'])
def get_team_details(request):
    team_data = models.Teams.objects.all().values()
    return JsonResponse({"team_data":list(team_data)})

# add points to team
@api_view(http_method_names=['POST'])
def add_points(request,team_username,points):
    try:
        team = models.Teams.objects.get(team_username=team_username)
        team.score +=int(points)
        team.save()
        return JsonResponse({"message":f"[INFO] Awarded {points} to {team_username}"})
    except Exception as e:
        print(e)
        return JsonResponse({"message":f"[ERROR] Failure in Adding Score API! Please check team_username and API format"})

@api_view(http_method_names=['POST'])
def register(request):
    data = request.data
    print(data)
    team = data['team']
    players_data = data['players']
    team_instance = models.Teams(team_username=team,score=0)
    team_instance.save()
    
    
    for player in players_data:
        print(player)
        player_name = players_data[player]['name']
        discord_username = players_data[player]['discord_username']
        player_instance = models.Players(player_name=player_name,
                                         discord_username=discord_username,
                                         team=team_instance)
        player_instance.save()
        
    return JsonResponse({})






@api_view(http_method_names=['GET'])
def get_puzzles(request):
    puzzle_data = models.Puzzle.objects.all().values()
    return JsonResponse({"puzzle_data":list(puzzle_data)})

@api_view(http_method_names=['GET'])
def get_next_puzzle(request,puzzle_id):
    puzzle_queue = models.PuzzleQueue.objects.get(parent_puzzle=puzzle_id)
    return JsonResponse({"next_puzzle":{
        "id":puzzle_queue.child_puzzle.id,

    }})
    

#get_current_puzzle $what is my question -->current question id, text
@api_view(http_method_names=['GET'])
def get_current_puzzle(request):
    data = request.data
    discord_username = data['discord_username']
    player_instance = models.Players.objects.get(discord_username=discord_username)
    team            = player_instance.team
    current_puzzle_id  = team.current_puzzle.id
    return JsonResponse({"current_puzzle":current_puzzle_id})
    

@api_view(http_method_names=['POST'])
def add_points_player(request):
    data =request.data

    discord_username = data['discord_username']
    points           = data['points']

    player_instance = models.Players.objects.get(discord_username=discord_username)
    team            = player_instance.team
    print("[INFO] Discord Awarded Points", points)
    team.score+=points
    team.save()
    
    return JsonResponse({'message':True})




@api_view(http_method_names=['POST'])
def validation(request):
    data =request.data
    
    discord_username = data['discord_username']
    answer = data['answer'].lower()
        
    player_instance = models.Players.objects.get(discord_username=discord_username)
    team            = player_instance.team
    current_puzzle_id  = team.current_puzzle.id
    
    possible_answers = team.current_puzzle.possible_answers
    if answer in [x.lower() for x in possible_answers["answers"]]:
        try:
            if team.current_puzzle.deadline < timezone.now():
                #reduce points and add
                print("DEDUCTING POITNS SINCE YOU Missed the deadline!")
                points_to_add = (team.current_puzzle.points//2)
                print(f"[INFO] ADDING POINTS to {discord_username}",points_to_add)
                team.score+=points_to_add
            else:
                #add points
                print(timezone.now())
                print(team.current_puzzle.deadline)
                print((timezone.now()-team.current_puzzle.deadline).total_seconds())

                time_points=((timezone.now()-team.current_puzzle.deadline).total_seconds())//3600
                print(abs(time_points))
                #time_points+=abs((timezone.now()-team.current_puzzle.deadline).days)*24
                print(f"Adding Time points for solving early!{discord_username}",abs(time_points))
                time_points=abs(time_points)
                team.score+=team.current_puzzle.points+time_points
        except Exception as e:
            print(e)
            print(data)
            team.score+=team.current_puzzle.points

        #find next puzzle
        puzzle_queue = models.PuzzleQueue.objects.get(parent_puzzle=current_puzzle_id)        
        team.current_puzzle = puzzle_queue.child_puzzle
        
        team.current_hint=0
        team.save()
        
        return JsonResponse({
                            "message":True,
                            "current_puzzle_id":current_puzzle_id,
                            "next_puzzle_id":puzzle_queue.child_puzzle.id
                             })
    else:
        #deducted points   
        team.score=team.score-10 #based on a rubric
        print(f"Deducting points for wrong answer {discord_username}")
        team.save()
        return JsonResponse({"message":False})
         
   
@api_view(http_method_names=['POST'])
def get_hint(request):
    data = request.data
    discord_username = data['discord_username']
    
    #get user team
    player_instance = models.Players.objects.get(discord_username=discord_username)
    team            = player_instance.team
    
    hints = team.current_puzzle.hints
    current_hint = team.current_hint
    try:
        hint = hints["hints"][current_hint]
        team.current_hint+=1
        team.score=max(team.score-10,0)
        print(f"deducting points {discord_username} for using hints")
        team.save()
        return JsonResponse({"hint": hint})
    except Exception as e:
        print(e)
        return JsonResponse({"hint":"Sorry! No More hints!"})            
   

@api_view(http_method_names=['GET'])
def get_location_hint(request):
    data = request.data
    discord_username = data['discord_username']
    index            = data['location_hint_index']
        
    #get user team
    player_instance = models.Players.objects.get(discord_username=discord_username)
    team            = player_instance.team
    
    location_hints = team.current_puzzle.location_hints

    try:
        return JsonResponse({"hint":location_hints["hints"][int(index)]})        
    except Exception as e:
        print(e)
        return JsonResponse({"hint":"No Hint"})


@api_view(http_method_names=['POST'])
def get_image_url(request):
    data = request.data
    full_password = data['full_password'].replace(" ","")
    print(full_password,len(full_password))
    try:
        image_mapper_object = models.image_mapper.objects.get(full_password__iexact=full_password)
        if(image_mapper_object.unlock_time<timezone.now()):
            return JsonResponse({
                "image_url":image_mapper_object.url
            })
        else:
            print("time out")
            return JsonResponse({
                "image_url":"https://www.interstellarrift.com/wiki/images/0/0d/Access_Denied.png"
                })
    except Exception as e:
        print(e)
        print(full_password)
        print("Wrong password")
        return JsonResponse({
            "image_url":"https://www.interstellarrift.com/wiki/images/0/0d/Access_Denied.png"
            })

    


@api_view(http_method_names=['POST'])
def authenticate_team(request):
    data = request.data
    authentication_code = data['auth_code']
    try:
        team_instance = models.Teams.objects.get(team_code=authentication_code)
        return JsonResponse({
            "team_username":team_instance.team_username,
        })

    except Exception as e:
        print(e)
        return JsonResponse({})






@api_view(http_method_names=['POST'])
def getSecondHalf(request):
    data =request.data
    code = data['code']
    instance = models.image_mapper.objects.get(code=code)
    if(instance.unlock_time<timezone.now()):
        if instance:
            return JsonResponse({"second_half":instance.half_password})
        else:
            return JsonResponse({"second_half":"Hmmm..This Marker has issues contact the Loyalists"})
    else:
            return JsonResponse({"second_half":"The Marker is Time Gated! The Loyalists are watching and patience is an essential Virtue"})
