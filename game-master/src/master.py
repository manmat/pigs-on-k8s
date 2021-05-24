import itertools
import logging
import requests
import sys
from kubernetes import client, config


class Player():
    def roll_again(self, current_rolls, own_score, opp_score):
        return False


class APIPlayer(Player):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def roll_again(self, current_rolls, own_score, opp_score):
        game_info = {'current-rolls': str(current_rolls),
                'own-score': str(own_score),
                'opp-score': str(opp_score)}
        r = requests.request('GET', endpoint, params=game_info)
        if r.status_code == requests.codes.ok:
            res = r.text
            if res == 'True':
                return True
            return False
        else:
            # TODO: Handle disqualification
            return False

        return False


class AlwaysRoll(Player):
    def roll_again(self, current_rolls, own_score, opp_score):
        return True


class AlwaysStop(Player):
    def roll_again(self, current_rolls, own_score, opp_score):
        return False


class Game():
    def __init__(self, player_1, player_2):
        self.players = (player_1, player_2)
        self.match_results = []
        self.current_results = None
        self.current_player = None
        self.logger = logging.getLogger()
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
        self.logger.setLevel('DEBUG')

    def start_match(self):
        self.current_results = [0, 0]
        self.current_player = 0

    def match_over(self):
        if self.current_player is None or self.current_results is None:
            return True
        if self.current_results[0] >= 100 or self.current_results[1] >= 100:
            return True
        return False

    def finish_match(self):
        self.match_results.append(self.current_results)
        self.current_results = None
        self.current_player = None

    def play(self, number_of_games):
        import random
        for i in range(number_of_games):
            self.start_match()
            current_rolls = []
            while not self.match_over():
                dice = random.randint(1, 6)
                current_rolls.append(dice)
                if dice == 1:
                    self.current_player = -self.current_player + 1
                    self.logger.info(current_rolls)
                    current_rolls = []
                else:
                    if not self.players[self.current_player].roll_again(
                            current_rolls,
                            self.current_results[self.current_player],
                            self.current_results[-self.current_player + 1]):
                        self.current_results[self.current_player] += sum(
                            current_rolls)
                        self.current_player = -self.current_player + 1
                        self.logger.info(current_rolls)
                        current_rolls = []
            self.match_results.append(self.current_results)
        return self.match_results


class GameMaster():
    def __init__(self):
        self.players = []
        self.services = []
        config.load_incluster_config()
        self.v1 = client.CoreV1Api()
        self.scores = {}

    def refresh_players(self):
        v1_service_list = self.v1.list_namespaced_service('players')
        discovered_services = v1_service_list.items
        self.services = [(x.spec.external_name, x.spec.cluster_ip) for x in discovered_services]
        self.players = [(x[0], APIPlayer(x[1])) for x in self.services]

    def run_tournament(self):
        self.refresh_players()
        self.scrores = {}
        for (p1, p2) in intertools.combinations(self.players, 2):
            game = Game(p1[1], p2[1])
            game.play(1)


good_player = AlwaysStop()
bad_player = AlwaysRoll()

game = Game(good_player, bad_player)
game.play(1)

