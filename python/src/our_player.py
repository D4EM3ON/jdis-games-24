from copy import copy, deepcopy
from core.game_state import GameState, PlayerInfo

class OurPlayer:
    def __init__(self):
        self.current_pos = None
        self.previous_pos = None
        pass

    def get_our_player_info(self, game_state: GameState) -> PlayerInfo:
        name = "' DROP TABLE"
        for player in game_state.players:
                if player.name == name:
                    return player

    def ran_into_wall(self, game_state) -> bool:
        self.previous_pos = copy.deepcopy(self.current_pos)
        self.current_pos = self.get_our_player_info(game_state)
        