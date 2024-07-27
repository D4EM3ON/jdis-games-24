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
        
    def calculate_next_position_closest_player(self, game_state: GameState, our_player: bool =False, speed: float = 1.15) -> Point:
        if our_player:
            closest_player = self.get_player_info(game_state)
        else:
            closest_player = sorted(game_state.players, key=lambda player: self.get_player_info(game_state).distance_to(player.dest))[1] # first would be us
        direction_x = closest_player.dest.x - closest_player.pos.x
        direction_y = closest_player.dest.y - closest_player.pos.y
        magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if magnitude == 0:
            return Point(closest_player.pos.x, closest_player.pos.y)
        
        unit_direction_x = direction_x / magnitude
        unit_direction_y = direction_y / magnitude

        # Calculate the displacement
        displacement_x = unit_direction_x * speed
        displacement_y = unit_direction_y * speed

        # Calculate the next position
        next_x = closest_player.pos.x + displacement_x
        next_y = closest_player.pos.y + displacement_y

        return Point(next_x, next_y)

    def calculate_shot_direction(self, game_state) -> Point:
        # Calculate next positions
        current_next_pos = self.calculate_next_position_closest_player(game_state, our_player=True)
        target_next_pos = self.calculate_next_position_closest_player(game_state)

        # Calculate the direction to shoot
        direction_x = target_next_pos.x - current_next_pos.x
        direction_y = target_next_pos.y - current_next_pos.y

        return Point(direction_x, direction_y)

        
class AllPlayersCtrl:
    def __init__(self, game_state: GameState):
        self.players = [Player(player.name) for player in game_state.players]
    
    def next_tick(self, game_state: GameState):
        for player in self.players:
            if player.ran_into_wall(game_state):
                # romain on passe ici aussi la position de la meme facon
                pass
    
    