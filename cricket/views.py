from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import JsonResponse
from .models import Team, Match, Player, Result
import json
import datetime
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return JsonResponse({
        "get list of matches and their results": "send get request to: /matches",
        "get details and result of a single match": "send get request to: /match/<match id>",
        "get list of participants": "send get request to: /participants",
        "get team profile": "send get request to: /team/<team id>",
        "get player profile": "send get request to: /player/<player id>",
        "delete match": "send post request to: /delete/match",
        "delete player": "send post request to: /delete/player",
        "delete team": "send post request to: /delete/team",
        "delete result": "send post request to: /delete/result",
        "add match": "send post request to: /add/match",
        "add player": "send post request to: /add/player",
        "add team": "send post request to: /add/team",
        "add result": "send post request to: /add/result",
        "update match": "send post request to: /update/match",
        "update player": "send post request to: /update/player",
        "update team": "send post request to: /update/team",
        "update result": "send post request to: /update/result"
    })

# gives detail of matches and their results
def matches(request):
    matches = Match.objects.all()
    return JsonResponse([match.serialize() for match in matches], safe=False)

def match(request, id):
    try:
        match = Match.objects.get(pk=id)
    except Match.DoesNotExist:
        return JsonResponse({
            "error": "Match does not exist"
        }, status=400)
    return JsonResponse(match.serialize())

# gives list of participants of the tournament
def participants(request):
    participants = Team.objects.all()
    return JsonResponse([participant.serialize() for participant in participants], safe=False)

# complete detail of a single team
def team(request, id):
    try:
        team = Team.objects.get(pk=id)
    except Team.DoesNotExist:
        return JsonResponse({
            "error": "Team does not exist"
        }, status=400)
    matches_obj = Match.objects.filter(Q(team1=team) | Q(team2=team))
    matches = [match.serialize() for match in matches_obj]
    data = {**team.serialize(), "matches": [match.serialize() for match in matches_obj]}
    return JsonResponse(data)

# complete detail of a single player
def player(request, id):
    try:
        player = Player.objects.get(pk=id)
    except Player.DoesNotExist:
        return JsonResponse({
            "error": "Player does not exist"
        }, status=400)
    return JsonResponse(player.serialize())

# methods to Add, Delete, and Update
@csrf_exempt
def crud_match(request, crud):
    if request.method != "POST":
        return JsonResponse({"error": "Post request required"}, status=400)
    
    crud = crud.lower()
    data = json.loads(request.body)

    if crud == "delete":
        required = ["id"]
        missing = check_keys(required, data)
        if missing:
            return JsonResponse({
                "error": f"Missing keys {missing}"
            }, status=400)
        try:
            match = Match.objects.get(pk=int(data["id"]))
            match.delete()
        except Match.DoesNotExist:
            return JsonResponse({
                "error": "Match does not exist"
            }, status=400)
        except:
            return JsonResponse({
                "error": "Please check the values for your keys"
            }, status=400)

    elif crud == "add":
        required = ["team1", "team2", "year", "month", "day", "hour", "minute", "venue"]
        missing = check_keys(required, data)
        if missing:
            return JsonResponse({
                "error": f"Missing keys {missing}"
            }, status=400)
        try:
            team1 = Team.objects.get(pk=int(data["team1"]))
            team2 = Team.objects.get(pk=int(data["team2"]))
            year = int(data["year"])
            month = int(data["month"])
            day = int(data["day"])
            hour = int(data["hour"])
            minute = int(data["minute"])
            timestamp = datetime.datetime(year, month, day, hour, minute)
            venue = data["venue"]
            match = Match.objects.create(team1=team1, team2=team2, date=timestamp, venue=venue, match_stage=0)
            match.save()
        except Team.DoesNotExist:
            return JsonResponse({
                "error": "one or both of the teams do not exist"
            }, status=400)
        except:
            return JsonResponse({
                "error": "Please check the values for your keys"
            }, status=400)

    elif crud == "update":
        required = ["id", "team1", "team2", "year", "month", "day", "hour", "minute", "venue"]
        missing = check_keys(required, data)
        if missing:
            return JsonResponse({
                "error": f"Missing keys {missing}"
            }, status=400)
        try:
            obj = Match.objects.get(pk=int(data["id"]))
            obj.team1 = Team.objects.get(pk=int(data["team1"]))
            obj.team2 = Team.objects.get(pk=int(data["team2"]))
            year = int(data["year"])
            month = int(data["month"])
            day = int(data["day"])
            hour = int(data["hour"])
            minute = int(data["minute"])
            obj.date = datetime.datetime(year, month, day, hour, minute)
            obj.venue = data["venue"]
            obj.save()
        except Match.DoesNotExist:
            return JsonResponse({
                "error": "Match does not exist"
            }, status=400)
        except Team.DoesNotExist:
            return JsonResponse({
                "error": "one or both of the teams do not exist"
            }, status=400)
        except:
            return JsonResponse({
                "error": "Please check the values for your keys"
            }, status=400)

    else:
        return JsonResponse({"error": "invalid operation through URL"}, status=400)

    return JsonResponse({
        "success": f"operation {crud} match"
    })


@csrf_exempt
def crud_player(request, crud):
    if request.method != "POST":
        return JsonResponse({"error": "Post request required"}, status=400)

    crud = crud.lower()
    data = json.loads(request.body)

    if crud == "delete":
        required = ["id"]
        missing = check_keys(required, data)
        if missing:
            return JsonResponse({
                "error": f"Missing keys {missing}"
            }, status=400)
        try:
            player = Player.objects.get(pk=int(data["id"]))
            player.delete()
        except Player.DoesNotExist:
            return JsonResponse({
                "error": "Player does not exist"
            }, status=400)
        except:
            return JsonResponse({
                "error": "Please check the values for your keys"
            }, status=400)

    elif crud == "add":
        required = ["name", "team"]
        missing = check_keys(required, data)
        if missing:
            return JsonResponse({
                "error": f"Missing keys {missing}"
            }, status=400)
        try:
            name = data["name"]
            team = Team.objects.get(pk=int(data["team"]))
            player = Player.objects.create(name=name, team=team)
            player.save()
        except Team.DoesNotExist:
            return JsonResponse({
                "error": "Team does not exist"
            }, status=400)
        except:
            return JsonResponse({
                "error": "Please check the values for your keys"
            }, status=400)

    elif crud == "update":
        required = ["id", "name", "team"]
        missing = check_keys(required, data)
        if missing:
            return JsonResponse({
                "error": f"Missing keys {missing}"
            }, status=400)
        try:
            player = Player.objects.get(pk=int(data["id"]))
            team = Team.objects.get(pk=int(data["team"]))
            player.name = data["name"]
            player.team = team
            player.save()
        except Player.DoesNotExist:
            return JsonResponse({
                "error": "Player does not exist"
            }, status=400)
        except Team.DoesNotExist:
            return JsonResponse({
                "error": "Team does not exist"
            }, status=400)
        except:
            return JsonResponse({
                "error": "Please check the values for your keys"
            }, status=400)

    else:
        return JsonResponse({"error": "invalid operation through URL"}, status=400)

    return JsonResponse({
        "success": f"operation {crud} player"
    })


@csrf_exempt
def crud_team(request, crud):
    if request.method != "POST":
        return JsonResponse({"error": "Post request required"}, status=400)
    
    crud = crud.lower()
    data = json.loads(request.body)

    if crud == "delete":
        required = ["id"]
        missing = check_keys(required, data)
        if missing:
            return JsonResponse({
                "error": f"Missing keys {missing}"
            }, status=400)
        try:
            team = Team.objects.get(pk=int(data["id"]))
            team.delete()
        except Team.DoesNotExist:
            return JsonResponse({
                "error": "Team does not exist"
            }, status=400)
        except:
            return JsonResponse({
                "error": "Please check the values for your keys"
            }, status=400)

    elif crud == "add":
        required = ["name"]
        missing = check_keys(required, data)
        if missing:
            return JsonResponse({
                "error": f"Missing keys {missing}"
            }, status=400)
        try:
            country = data["name"]
            team = Team.objects.create(country=country)
            team.save()
        except Team.DoesNotExist:
            return JsonResponse({
                "error": "Team does not exist"
            }, status=400)
        except:
            return JsonResponse({
                "error": "Please check the values for your keys"
            }, status=400)

    elif crud == "update":
        required = ["id", "name"]
        missing = check_keys(required, data)
        if missing:
            return JsonResponse({
                "error": f"Missing keys {missing}"
            }, status=400)
        try:
            team = Team.objects.get(pk=int(data["id"]))
            team.country = data["name"]
            team.save()
        except Team.DoesNotExist:
            return JsonResponse({
                "error": "Team does not exist"
            }, status=400)
        except:
            return JsonResponse({
                "error": "Please check the values for your keys"
            }, status=400)

    else:
        return JsonResponse({"error": "invalid operation through URL"}, status=400)

    return JsonResponse({
        "success": f"operation {crud} team"
    })


@csrf_exempt
def crud_result(request, crud):
    if request.method != "POST":
        return JsonResponse({"error": "Post request required"}, status=400)
    
    crud = crud.lower()
    data = json.loads(request.body)

    if crud == "delete":
        required = ["id"]
        missing = check_keys(required, data)
        if missing:
            return JsonResponse({
                "error": f"Missing keys {missing}"
            }, status=400)
        try:
            result = Result.objects.get(pk=int(data["id"]))
            result.delete()
        except Result.DoesNotExist:
            return JsonResponse({
                "error": "Result does not exist"
            }, status=400)
        except:
            return JsonResponse({
                "error": "Please check the values for your keys"
            }, status=400)

    elif crud == "add":
        required = ["winner", "loser", "man_of_the_match", "bowler_of_the_match", "best_fielder", "match"]
        missing = check_keys(required, data)
        if missing:
            return JsonResponse({
                "error": f"Missing keys {missing}"
            }, status=400)
        try:
            winner = Team.objects.get(pk=int(data["winner"]))
            loser = Team.objects.get(pk=int(data["loser"]))
            man_of_the_match = Player.objects.get(pk=int(data["man_of_the_match"]))
            bowler_of_the_match = Player.objects.get(pk=int(data["bowler_of_the_match"]))
            best_fielder = Player.objects.get(pk=int(data["best_fielder"]))
            match = Match.objects.get(pk=int(data["match"]))
            result = Result.objects.create(winner=winner, loser=loser, man_of_the_match=man_of_the_match, bowler_of_the_match=bowler_of_the_match,best_fielder=best_fielder, match=match)
            result.save()
        except (Team.DoesNotExist, Player.DoesNotExist, Match.DoesNotExist):
            return JsonResponse({
                "error": "One or more values do not exist"
            }, status=400)
        except:
            return JsonResponse({
                "error": "Please check the values for your keys"
            }, status=400)

    elif crud == "update":
        required = ["id", "winner", "loser", "man_of_the_match", "bowler_of_the_match", "best_fielder", "match"]
        missing = check_keys(required, data)
        if missing:
            return JsonResponse({
                "error": f"Missing keys {missing}"
            }, status=400)
        try:
            result = Result.objects.get(pk=int(data["id"]))
            result.winner = Team.objects.get(pk=int(data["winner"]))
            result.loser = Team.objects.get(pk=int(data["loser"]))
            result.man_of_the_match = Player.objects.get(pk=int(data["man_of_the_match"]))
            result.bowler_of_the_match = Player.objects.get(pk=int(data["bowler_of_the_match"]))
            result.best_fielder = Player.objects.get(pk=int(data["best_fielder"]))
            result.match = Match.objects.get(pk=int(data["match"]))
            result.save()
        except Result.DoesNotExist:
            return JsonResponse({
                "error": "One or more values do not exist"
            }, status=400)
        except Team.DoesNotExist:
            return JsonResponse({
                "error": "one or both the teams do not exist"
            }, status=400)
        except Player.DoesNotExist:
            return JsonResponse({
                "error": "one or more players do not exist"
            }, status=400)
        except Match.DoesNotExist:
            return JsonResponse({
                "error": "Match does not exist"
            }, status=400)
        except:
            return JsonResponse({
                "error": "Please check the values for your keys"
            }, status=400)

    else:
        return JsonResponse({"error": "invalid operation through URL"}, status=400)

    return JsonResponse({
        "success": f"operation {crud} resutl"
    })

def check_keys(required, data):
    missing = []
    for key in required:
        if key not in data:
            missing.append(key)

    return missing