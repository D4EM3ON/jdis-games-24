from copy import copy, deepcopy
from core.game_state import GameState, PlayerInfo
from core.map_state import Point
import math

class Player:
    def __init__(self, name="' DROP TABLE"):
        self.current_pos = None
        self.previous_pos = None
        self.previous_points = 0
        self.current_points = 0
        self.other_players = []
        self.name = name
        pass

    def get_player_info(self, game_state: GameState) -> PlayerInfo:
        for player in game_state.players:
                if player.name == self.name:
                    return player

    def ran_into_wall(self, game_state: GameState) -> bool:
        self.previous_pos = deepcopy(self.current_pos)
        self.current_pos = self.get_player_info(game_state).pos
        return self.previous_pos == self.current_pos
    
    def have_we_gotten_points(self, game_state: GameState) -> bool:
        self.previous_points = deepcopy(self.current_points)
        self.current_points = self.get_player_info(game_state)
        return self.previous_points == self.current_points
        
    def calculate_next_position_closest_player(self, game_state: GameState, speed: float = 1.15, name=None, ticker_count=1) -> tuple[Point, PlayerInfo]:

        closest_player = sorted(game_state.players, key=lambda player: self.get_player_info(game_state).pos.distance_to(player.dest))
        # print([(player.name, player.)])
        for player in closest_player:
            if player.name != self.name:
                if (name and player.name == name) or not name:
                    closest_player = player
                    break
        print(f"Closest player: {closest_player.name}, distance: {self.get_player_info(game_state).pos.distance_to(closest_player.dest)}")
        direction_x = closest_player.dest.x - closest_player.pos.x
        direction_y = closest_player.dest.y - closest_player.pos.y
        magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if magnitude == 0:
            return Point(closest_player.pos.x, closest_player.pos.y), closest_player
        
        unit_direction_x = direction_x / magnitude
        unit_direction_y = direction_y / magnitude

        displacement_x = unit_direction_x * speed * ticker_count
        displacement_y = unit_direction_y * speed * ticker_count

        next_x = closest_player.pos.x + displacement_x
        next_y = closest_player.pos.y + displacement_y

        print(f"Closest player: {closest_player.name}, next position: {next_x}, {next_y}")
        
        return Point(next_x, next_y), closest_player

        
class AllPlayersCtrl:
    def __init__(self, game_state: GameState):
        self.players = [Player(player.name) for player in game_state.players]
    
    def next_tick(self, game_state: GameState):
        for player in self.players:
            if player.ran_into_wall(game_state):
                # romain on passe ici aussi la position de la meme facon
                pass
    
    