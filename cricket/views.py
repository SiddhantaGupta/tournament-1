from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import JsonResponse
from .models import Team, Match, Player, Result
import json
import datetime
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    return JsonResponse({
    "get all matches and their results": "send GET request to: /matches",
    "get all participating teams": "send GET request to: /participants",
    "get team info": "send GET request to: /team/<team id>",
    "update team info": "send POST request with data to: /team/<team id>",
    "delete team": "send DELETE request to: /team/<team id>",
    "add team": "send POST request with data to: /team/add",
    "get player info": "send GET request to: /player/<player id>",
    "update player info": "send POST request with data to: /player/<player id>",
    "delete player info": "send DELETE request to: /player/<player id>",
    "add player": "send POST request with data to: /player/add",
    "get match info": "send GET request to: /match/<match id>",
    "update match info": "send POST request with data to: /match/<match id>",
    "delete match info": "send DELETE request to: /match/<match id>",
    "add match": "send POST request with data to: /match/add",
    "get result info": "send GET request to: /result/<result id>",
    "update result info": "send POST request with data to: /result/<result id>",
    "delete result info": "send DELETE request to: /result/<result id>",
    "add result": "send POST request with data to: /result/add"
    })

# gives detail of matches and their results
@csrf_exempt
def matches(request):
    matches = Match.objects.all()
    return JsonResponse([match.serialize() for match in matches], safe=False)

# Read, Update, Delete match by id
@csrf_exempt
def match(request, id):
    if request.method == "GET":
        try:
            match = Match.objects.get(pk=id)
        except Match.DoesNotExist:
            return JsonResponse({
                "error": "Match does not exist"
            }, status=400)
        return JsonResponse(match.serialize())
    
    elif request.method == "POST":
        data = json.loads(request.body)
        required = ["team1", "team2", "year", "month", "day", "hour", "minute", "venue"]
        missing = check_keys(required, data)
        if missing:
            return JsonResponse({
                "error": f"Missing keys {missing}"
            }, status=400)
        try:
            obj = Match.objects.get(pk=id)
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
            return JsonResponse({
        "success": f"operation update match",
        "data": f"{data}"
    })
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

    elif request.method == "DELETE":
        try:
            match = Match.objects.get(pk=id)
            try:
                result = Result.objects.get(match=match)
                result.delete()
            except Result.DoesNotExist:
                pass
            match.delete()
            return JsonResponse({
        "success": f"operation delete match"
    })
        except Match.DoesNotExist:
            return JsonResponse({
                "error": "Match does not exist"
            }, status=400)
        except:
            return JsonResponse({
                "error": "Please check the values for your keys"
            }, status=400)

    else:
        return JsonResponse({
                "error": "invalid HTTP request method"
            }, status=400)

# gives list of participants of the tournament
@csrf_exempt
def participants(request):
    participants = Team.objects.all()
    return JsonResponse([participant.serialize() for participant in participants], safe=False)

# Read, Update, Delete result by id
@csrf_exempt
def result(request, id):
    if request.method == "GET":
        try:
            result = Result.objects.get(pk=id)
        except Result.DoesNotExist:
            return JsonResponse({
                "error": "Result does not exist"
            }, status=400)
        return JsonResponse(result.serialize())

    elif request.method == "POST":
        data = json.loads(request.body)
        required = ["winner", "loser", "man_of_the_match", "bowler_of_the_match", "best_fielder", "match"]
        missing = check_keys(required, data)
        if missing:
            return JsonResponse({
                "error": f"Missing keys {missing}"
            }, status=400)
        try:
            result = Result.objects.get(pk=id)
            result.winner = Team.objects.get(pk=int(data["winner"]))
            result.loser = Team.objects.get(pk=int(data["loser"]))
            result.man_of_the_match = Player.objects.get(pk=int(data["man_of_the_match"]))
            result.bowler_of_the_match = Player.objects.get(pk=int(data["bowler_of_the_match"]))
            result.best_fielder = Player.objects.get(pk=int(data["best_fielder"]))
            result.match = Match.objects.get(pk=int(data["match"]))
            result.save()
            return JsonResponse({
        "success": f"operation update result",
        "data": f"{data}"
    })
        except Result.DoesNotExist:
            return JsonResponse({
                "error": "Result does not exist"
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

    elif request.method == "DELETE":
        try:
            result = Result.objects.get(pk=id)
            result.delete()
            return JsonResponse({
        "success": f"operation delete result"
    })
        except Result.DoesNotExist:
            return JsonResponse({
                "error": "Result does not exist"
            }, status=400)
        except:
            return JsonResponse({
                "error": "Please check the values for your keys"
            }, status=400)

    else:
        return JsonResponse({
                "error": "invalid HTTP request method"
            }, status=400)


# # Read, Update, Delete team by id
@csrf_exempt
def team(request, id):
    if request.method == "GET":
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

    elif request.method == "POST":
        data = json.loads(request.body)
        required = ["name"]
        missing = check_keys(required, data)
        if missing:
            return JsonResponse({
                "error": f"Missing keys {missing}"
            }, status=400)
        try:
            team = Team.objects.get(pk=id)
            team.country = data["name"]
            team.save()
            return JsonResponse({
        "success": f"operation update team",
        "data": f"{data}"
    })
        except Team.DoesNotExist:
            return JsonResponse({
                "error": "Team does not exist"
            }, status=400)
        except:
            return JsonResponse({
                "error": "Please check the values for your keys"
            }, status=400)

    elif request.method == "DELETE":
        try:
            team = Team.objects.get(pk=id)
            team.delete()
            return JsonResponse({
        "success": f"operation delete team"
    })
        except Team.DoesNotExist:
            return JsonResponse({
                "error": "Team does not exist"
            }, status=400)
        except:
            return JsonResponse({
                "error": "Please check the values for your keys"
            }, status=400)

    else:
        return JsonResponse({
                "error": "invalid HTTP request method"
            }, status=400)

# Read, Update, Delete player by id
@csrf_exempt
def player(request, id):
    if request.method == "GET":
        try:
            player = Player.objects.get(pk=id)
        except Player.DoesNotExist:
            return JsonResponse({
                "error": "Player does not exist"
            }, status=400)
        return JsonResponse(player.serialize())
    
    elif request.method == "POST":
        data = json.loads(request.body)
        required = ["name", "team"]
        missing = check_keys(required, data)
        if missing:
            return JsonResponse({
                "error": f"Missing keys {missing}"
            }, status=400)
        try:
            player = Player.objects.get(pk=id)
            team = Team.objects.get(pk=int(data["team"]))
            player.name = data["name"]
            player.team = team
            player.save()
            return JsonResponse({
        "success": f"operation update player",
        "data": f"{data}"
    })
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

    elif request.method == "DELETE":
        try:
            player = Player.objects.get(pk=id)
            player.delete()
            return JsonResponse({
        "success": f"operation delete player"
    })
        except Player.DoesNotExist:
            return JsonResponse({
                "error": "Player does not exist"
            }, status=400)
        except:
            return JsonResponse({
                "error": "Please check the values for your keys"
            }, status=400)

    else:
        return JsonResponse({
                "error": "invalid HTTP request method"
            }, status=400)

# this methods adds new data
@csrf_exempt
def add(request, field):
    if request.method != "POST":
        return JsonResponse({"error": "Post request required"}, status=400)

    field = field.lower()
    data = json.loads(request.body)

    if field == "player":
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

    elif field == "team":
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

    elif field == "match":
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

    elif field == "result":
        required = ["winner", "loser", "man_of_the_match", "bowler_of_the_match", "best_fielder", "match"]
        missing = check_keys(required, data)
        if missing:
            return JsonResponse({
                "error": f"Missing keys {missing}"
            }, status=400)
        try:
            match_test = Match.objects.get(pk=int(data["match"]))
            result_test = Result.objects.get(match=match_test)
            return JsonResponse({
                "error": "A result for this match already exists"
            }, status=400)
        except Match.DoesNotExist:
            return JsonResponse({
                "error": "match does not exist"
            }, status=400)
        except Result.DoesNotExist:
            pass
        try:
            winner = Team.objects.get(pk=int(data["winner"]))
            loser = Team.objects.get(pk=int(data["loser"]))
            man_of_the_match = Player.objects.get(pk=int(data["man_of_the_match"]))
            bowler_of_the_match = Player.objects.get(pk=int(data["bowler_of_the_match"]))
            best_fielder = Player.objects.get(pk=int(data["best_fielder"]))
            match = Match.objects.get(pk=int(data["match"]))
            result = Result.objects.create(winner=winner, loser=loser, man_of_the_match=man_of_the_match, bowler_of_the_match=bowler_of_the_match,best_fielder=best_fielder, match=match)
            result.save()
        except Team.DoesNotExist:
            return JsonResponse({
                "error": "One or more teams do not exist"
            }, status=400)
        except Player.DoesNotExist:
            return JsonResponse({
                "error": "One or more players do not exist"
            }, status=400)
        except Match.DoesNotExist:
            return JsonResponse({
                "error": "match does not exist"
            }, status=400)
        except:
            return JsonResponse({
                "error": "Please check the values for your keys"
            }, status=400)

    return JsonResponse({
        "success": f"operation add {field}",
        "data": f"{data}"
    })

def check_keys(required, data):
    missing = []
    for key in required:
        if key not in data:
            missing.append(key)

    return missing