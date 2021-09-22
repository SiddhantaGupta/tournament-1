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
send post request to: "/match/add"
with JSON data in body in the format:
{
    "team1": [team id],
    "team2": [team id],
    "year": [year], eg - 2021
    "month": [month], eg - 7
    "day": [day], eg - 22
    "hour": [hour], eg - 14
    "minute": [minute], eg - 55
    "venue": ["venue"]
}
2. #### add player
send post request to: "/player/add"
with JSON data in body in the format:
{
    "name": ["name"],
    "team": [team id]
}
3. #### add team
send post request to: "/team/add"
with JSON data in body in the format:
{
    "name": ["name"]
}
4. #### add result
send post request to: "/result/add"
with JSON data in body in the format:
{
    "winner": [team id],
    "loser": [team id],
    "man_of_the_match": [player id],
    "bowler_of_the_match": [player id],
    "best_fielder": [player id],
    "match": [match id]
}

- #### Update data in the API
1. #### update match
send post request to: "/match/[match id]"
with JSON data in body in the format:
{
    "team1": [team id],
    "team2": [team id],
    "year": [year], eg - 2021
    "month": [month], eg - 7
    "day": [day], eg - 22
    "hour": [hour], eg - 14
    "minute": [minute], eg - 55
    "venue": ["venue"]
}
2. #### update player
send post request to: "/player/[player id]"
with JSON data in body in the format:
{
    "name": ["name"],
    "team": [team id]
}
3. #### update team
send post request to: "/team/[team id]"
with JSON data in body in the format:
{
    "name": ["name"]
}
4. #### update result
send post request to: "/result/[result id]"
with JSON data in body in the format:
{
    "winner": [team id],
    "loser": [team id],
    "man_of_the_match": [player id],
    "bowler_of_the_match": [player id],
    "best_fielder": [player id],
    "match": [match id],
}

- #### delete data in the API
1. #### delete match
send DELETE request to: "/match/[match id]"

2. #### delete player
send DELETE request to: "/player/[player id]"

3. #### delete team
send DELETE request to: "/team/[team id]"

4. #### delete result
send DELETE request to: "/result/[result id]"

## Tech stack used
- Django v3.2.5
- python v3.8.10
- postgresql