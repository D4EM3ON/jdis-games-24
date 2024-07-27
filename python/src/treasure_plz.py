from typing import List
from core.game_state import Coin, GameState
from core.map_state import Point
from src.our_player import Player


class TreasuresCtrl:
    def __init__(self):
        self.where_we_already_went = []
        self.first_blocked = None
        self.player = Player()
        pass
    
    def get_closest_treasure(self, game_state: GameState):
        self.first_blocked = self.first_blocked if self.first_blocked else self.player.get_player_info(game_state).pos
        if self.first_blocked.distance_to(self.player.get_player_info(game_state).pos) > 20:
            self.clear_where_we_already_went()
        treasures = game_state.coins
        current_pos = self.player.get_player_info(game_state).pos
        if treasures:
            treasures = self.filter_treasures_by_distance(treasures, current_pos)
            for treasure in treasures:
                if treasure and treasure.pos not in self.where_we_already_went:
                    self.where_we_already_went.append(treasure.pos)
                    return treasure
            
    def filter_treasures_by_distance(self, treasures: List[Coin], player_pos: Point):
        if not treasures:
            return []
        return sorted(treasures, key=lambda coin: player_pos.distance_to(coin.pos))

    def clear_where_we_already_went(self):
        self.first_blocked = None
        self.where_we_already_went = []