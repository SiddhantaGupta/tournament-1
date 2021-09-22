## API Endpoints
1. #### Get data from the api
- #### get list of matches and their results
send get request to: "/matches"
- #### get details and result of a single match
send get request to: "/match/[match id]"
- #### get list of participants
send get request to: "/participants"
- #### get team profile
send get request to: "/team/[team id]"
- #### get player profile
send get request to: "/player/[player id]"

2. #### Add data to the API
- #### add match
send post request to: "/match/add"
```
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
```
- #### add player
send post request to: "/player/add"
```
with JSON data in body in the format:
{
    "name": ["name"],
    "team": [team id]
}
```
- #### add team
send post request to: "/team/add"
```
with JSON data in body in the format:
{
    "name": ["name"]
}
```
- #### add result
send post request to: "/result/add"
```
with JSON data in body in the format:
{
    "winner": [team id],
    "loser": [team id],
    "man_of_the_match": [player id],
    "bowler_of_the_match": [player id],
    "best_fielder": [player id],
    "match": [match id]
}
```

3. #### Update data in the API
- #### update match
send post request to: "/match/[match id]"
```
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
```
- #### update player
send post request to: "/player/[player id]"
```
with JSON data in body in the format:
{
    "name": ["name"],
    "team": [team id]
}
```
- #### update team
send post request to: "/team/[team id]"
```
with JSON data in body in the format:
{
    "name": ["name"]
}
```
- #### update result
send post request to: "/result/[result id]"
```
with JSON data in body in the format:
{
    "winner": [team id],
    "loser": [team id],
    "man_of_the_match": [player id],
    "bowler_of_the_match": [player id],
    "best_fielder": [player id],
    "match": [match id],
}
```

4. #### delete data in the API
- #### delete match
send DELETE request to: "/match/[match id]"

- #### delete player
send DELETE request to: "/player/[player id]"

- #### delete team
send DELETE request to: "/team/[team id]"

- #### delete result
send DELETE request to: "/result/[result id]"

## Tech stack used
- Django v3.2.5
- python v3.8.10
- postgresql