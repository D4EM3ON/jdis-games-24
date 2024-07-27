from typing import List, Union

from core.action import MoveAction, ShootAction, RotateBladeAction, SwitchWeaponAction, SaveAction
from core.consts import Consts
from core.game_state import GameState, PlayerWeapon, Point
from core.map_state import MapState
from src.treasure_plz import TreasuresCtrl
from src.our_player import AllPlayersCtrl, Player

def flatten_comprehension(matrix):
     return [item for row in matrix for item in row]

class MyBot:
     """
     (fr) Cette classe représente votre bot. Vous pouvez y définir des attributs et des méthodes qui 
          seront conservées entre chaque appel de la méthode `on_tick`.

     (en) This class represents your bot. You can define attributes and methods in it that will be kept 
          between each call of the `on_tick` method.
     """
     __map_state: MapState
     name : str
     
     def __init__(self):
          self.name = "Magellan"
          self.player = Player()
          self.current_goal = None
          self.treasure_ctrl = TreasuresCtrl()
          self.counter = 0
          self.map_save = None
          # self.all_players_ctrl = AllPlayersCtrl()


     def on_tick(self, game_state: GameState) -> List[Union[MoveAction, SwitchWeaponAction, RotateBladeAction, ShootAction, SaveAction]]:
          """
          (fr)    Cette méthode est appelée à chaque tick de jeu. Vous pouvez y définir 
                    le comportement de votre bot. Elle doit retourner une liste d'actions 
                    qui sera exécutée par le serveur.

                    Liste des actions possibles:
                    - MoveAction((x, y))        permet de diriger son bot, il ira a vitesse
                                                constante jusqu'à ce point.

                    - ShootAction((x, y))       Si vous avez le fusil comme arme, cela va tirer
                                                à la coordonnée donnée.

                    - SaveAction([...])         Permet de storer 100 octets dans le serveur. Lors
                                                de votre reconnection, ces données vous seront
                                                redonnées par le serveur.

                    - SwitchWeaponAction(id)    Permet de changer d'arme. Par défaut, votre bot
                                                n'est pas armé, voici vos choix:
                                                       PlayerWeapon.PlayerWeaponNone
                                                       PlayerWeapon.PlayerWeaponCanon
                                                       PlayerWeapon.PlayerWeaponBlade
                                                       
                    - BladeRotateAction(rad)    Si vous avez la lame comme arme, vous pouver mettre votre arme
                                                à la rotation donnée en radian.

          (en)    This method is called at each game tick. You can define your bot's behavior here. It must return a 
                    list of actions that will be executed by the server.

                    Possible actions:
                    - MoveAction((x, y))        Directs your bot to move to the specified point at a constant speed.

                    - ShootAction((x, y))       If you have the gun equipped, it will shoot at the given coordinates.

                    - SaveAction([...])         Allows you to store 100 bytes on the server. When you reconnect, these 
                                                data will be provided to you by the server.

                    - SwitchWeaponAction(id)    Allows you to change your weapon. By default, your bot is unarmed. Here 
                                                are your choices:
                                                  PlayerWeapon.PlayerWeaponNone
                                                  PlayerWeapon.PlayerWeaponCanon
                                                  PlayerWeapon.PlayerWeaponBlade
                    
                    - BladeRotateAction(rad)    if you have the blade as a weapon, you can set your
                                                weapon to the given rotation in radians.

          Arguments:
               game_state (GameState): (fr): L'état de la partie.
                                        (en): The state of the game.   
          """
          # self.load_save(self.__map_state)
          
          print(f"Current tick: {game_state.current_tick}")
          # print(f"Map_save: {self.map_save}")

          SaveAction(bytearray(flatten_comprehension(self.map_save)))
          current_dest = self.player.get_player_info(game_state).dest

          self.player.get_our_player_info(game_state)
          
          points_changed = self.player.have_we_gotten_points(game_state)
          
          if points_changed:
               self.treasure_ctrl.clear_where_we_already_went()
          
          if self.player.ran_into_wall(game_state) and not points_changed:
               # pour nous romain mettre du code ici
               closest_treasure = self.treasure_ctrl.get_closest_treasure(game_state)
               if closest_treasure:
                    current_dest = closest_treasure.pos
               elif self.counter % 4 == 0:
                    current_dest = Point(0, 0)
               elif self.counter % 4 == 1:
                    current_dest = Point(100, 0)
               elif self.counter % 4 == 2:
                    current_dest = Point(0, 100)
               elif self.counter % 4 == 3:
                    current_dest = Point(100, 100)
          
          self.counter += 1
          
          if not current_dest:
               current_dest = Point(50, 50)
          
          # self.all_players_ctrl.next_tick(game_state)
          other_player_pos, other_player = self.player.calculate_next_position_closest_player(game_state, ticker_count=1)
          actions = [
               SwitchWeaponAction(PlayerWeapon.PlayerWeaponCanon) if self.counter == 1 else ShootAction((other_player_pos.x, other_player_pos.y)),
               MoveAction((current_dest.x, current_dest.y)), 
          ]
          for i in range(8):
               actions.append(ShootAction((other_player_pos.x, other_player_pos.y)))
          return actions
    
    
     def on_start(self, map_state: MapState):
          """
          (fr) Cette méthode est appelée une seule fois au début de la partie. Vous pouvez y définir des
               actions à effectuer au début de la partie.

          (en) This method is called once at the beginning of the game. You can define actions to be 
               performed at the beginning of the game.

          Arguments:
               map_state (MapState): (fr) L'état de la carte.
                                   (en) The state of the map.
          """
          self.__map_state = map_state
          self.load_save(map_state)
          pass


     def on_end(self):
          """
          (fr) Cette méthode est appelée une seule fois à la fin de la partie. Vous pouvez y définir des
               actions à effectuer à la fin de la partie.

          (en) This method is called once at the end of the game. You can define actions to be performed 
               at the end of the game.
          """
          pass

     def load_save(self, map_state):
          # set map_state to 0 to force reset
          if not int(map_state.save):
               self.map_save = [
                    [1,1,1,1,1,1,1,1,1,1,1,],
                    [1,0,0,0,0,0,0,0,0,0,1,],
                    [1,0,0,0,0,0,0,0,0,0,1,],
                    [1,0,0,0,0,0,0,0,0,0,1,],
                    [1,0,0,0,0,0,0,0,0,0,1,],
                    [1,0,0,0,0,0,0,0,0,0,1,],
                    [1,0,0,0,0,0,0,0,0,0,1,],
                    [1,0,0,0,0,0,0,0,0,0,1,],
                    [1,0,0,0,0,0,0,0,0,0,1,],
                    [1,0,0,0,0,0,0,0,0,0,1,],
                    [1,1,1,1,1,1,1,1,1,1,1,]
               ]
          else:
               self.map_save = []
               for i in range(0,121,11):
                    self.map_save.append(list(map(int,map_state.save[i:i+11])))

     def save_wall(self, pt):
          self.map_save[round(pt.x/10)][round(pt.y/10)] = 1

          