from django.db import models

class Team(models.Model):
    country = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.country}"

    def serialize(self):
        players_obj = Player.objects.filter(team=self)
        players = [player.serialize() for player in players_obj]
        wins = Result.objects.filter(winner=self).count()
        losses = Result.objects.filter(loser=self).count()
        return {
            "id": self.id,
            "name": self.country,
            "wins": wins,
            "losses": losses,
            "players": players,
        }


class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='competitor_1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="competitor_2")
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    venue = models.CharField(max_length=128)
    # match_stage field will store an integer representing the particular matches tournament stage (Finals, Semi-finals, Quarter-finals etc)
    match_stage = models.IntegerField()

    def __str__(self):
        return f"{self.team1} vs. {self.team2} stage: {self.match_stage}"

    def serialize(self):
        try:
            result_obj = Result.objects.get(match=self)
            result = result_obj.serialize()
        except Result.DoesNotExist:
            result = []
        return {
            "match_no": self.id,
            "team1": self.team1.country,
            "team2": self.team2.country,
            "timestamp": self.date,
            "venue": self.venue,
            "result": result
        }


class Player(models.Model):
    name = models.CharField(max_length=64)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players")

    def __str__(self):
        return f"{self.name}"

    def serialize(self):
        man_of_the_match = Result.objects.filter(man_of_the_match=self).count()
        bowler_of_the_match = Result.objects.filter(bowler_of_the_match=self).count()
        best_fielder = Result.objects.filter(best_fielder=self).count()
        return {
            "id": self.id,
            "name": self.name,
            "team": self.team.country,
            "man of the match": man_of_the_match,
            "bowler of the match": bowler_of_the_match,
            "best fielder": best_fielder
        }


class Result(models.Model):
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="win")
    loser = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="loss")
    man_of_the_match = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="man")
    bowler_of_the_match = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="bowler")
    best_fielder = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="fielder")
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="result")

    def __str__(self):
        return f"Result for {self.match}"

    def serialize(self):
        return {
            "match_no": self.match.id,
            "winner": self.winner.country,
            "loser": self.loser.country,
            "man_of_the_match": self.man_of_the_match.name,
            "bowler_of_the_match": self.bowler_of_the_match.name,
            "best_fielder": self.best_fielder.name
        }