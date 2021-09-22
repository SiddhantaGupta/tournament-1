## API Endpoints
- #### Get data from the api
1. #### get list of matches and their results
send get request to: "/matches"
2. #### get details and result of a single match
send get request to: "/match/[match id]"
3. #### get list of participants
send get request to: "/participants"
4. #### get team profile
send get request to: "/team/[team id]"
5. #### get player profile
send get request to: "/player/[player id]"

- #### Add data to the API
1. #### add match
send post request to: "/add/match"
with JSON data in body in the format:
{
    "team1": [team id],
    "team2": [team id],
    "year": [year], eg - 2021
    "month": [month], eg - 7
    "day": [day], eg - 22
    "hour": [hour], eg - 14
    "minute": [minute], eg - 55
    "venue": ["venue"],
}
2. #### add player
send post request to: "/add/player"
with JSON data in body in the format:
{
    "name": ["name"],
    "team": [team id]
}
3. #### add team
send post request to: "/add/team"
with JSON data in body in the format:
{
    "name": ["name"]
}
4. #### add result
send post request to: "/add/result"
with JSON data in body in the format:
{
    "winner": [team id],
    "loser": [team id],
    "man_of_the_match": [player id],
    "bowler_of_the_match": [player id],
    "best_fielder": [player id],
    "match": [match id],
}

- #### Update data in the API
1. #### update match
send post request to: "/update/match"
with JSON data in body in the format:
{
    "id": [match id]
    "team1": [team id],
    "team2": [team id],
    "year": [year], eg - 2021
    "month": [month], eg - 7
    "day": [day], eg - 22
    "hour": [hour], eg - 14
    "minute": [minute], eg - 55
    "venue": ["venue"],
}
2. #### update player
send post request to: "/update/player"
with JSON data in body in the format:
{
    "id": [player id]
    "name": ["name"],
    "team": [team id]
}
3. #### update team
send post request to: "/update/team"
with JSON data in body in the format:
{
    "id": [team id]
    "name": ["name"]
}
4. #### update result
send post request to: "/update/result"
with JSON data in body in the format:
{
    "id": [result id]
    "winner": [team id],
    "loser": [team id],
    "man_of_the_match": [player id],
    "bowler_of_the_match": [player id],
    "best_fielder": [player id],
    "match": [match id],
}

- #### delete data in the API
1. #### delete match
send post request to: "/delete/match"
with JSON data in body in the format:
{
    "id": [match id]
}
2. #### delete player
send post request to: "/delete/player"
with JSON data in body in the format:
{
    "id": [player id]
}
3. #### delete team
send post request to: "/delete/team"
with JSON data in body in the format:
{
    "id": [team id]
}
4. #### delete result
send post request to: "/delete/result"
with JSON data in body in the format:
{
    "id": [result id]
}

## Tech stack used
- Django v3.2.5
- python v3.8.10