import random
from typing import List, Optional
from enum import Enum
from tile import Tile, create_all_tiles

class PlayerType(Enum):
    HUMAN = "human"
    CPU = "cpu"

class Player:
    def __init__(self, player_id: int, player_type: PlayerType, name: str):
        self.player_id = player_id
        self.player_type = player_type
        self.name = name
        self.hand = []
        self.discarded = []
    
    def add_tile_to_hand(self, tile: Tile):
        tile.is_in_hand = True
        self.hand.append(tile)
    
    def discard_tile(self, tile_index: int) -> Optional[Tile]:
        if 0 <= tile_index < len(self.hand):
            tile = self.hand.pop(tile_index)
            tile.is_in_hand = False
            tile.is_discarded = True
            self.discarded.append(tile)
            return tile
        return None
    
    def discard_tile_by_object(self, tile: Tile) -> bool:
        if tile in self.hand:
            self.hand.remove(tile)
            tile.is_in_hand = False
            tile.is_discarded = True
            self.discarded.append(tile)
            return True
        return False
    
    def get_hand_count(self) -> int:
        return len(self.hand)
    
    def get_discarded_count(self) -> int:
        return len(self.discarded)
    
    def can_discard(self) -> bool:
        return len(self.hand) > 13

class GameState:
    def __init__(self):
        self.mountain = []
        self.hand = []
        self.discarded = []
        self.reset_game()
    
    def reset_game(self):
        all_tiles = create_all_tiles()
        random.shuffle(all_tiles)
        
        self.mountain = all_tiles
        self.hand = []
        self.discarded = []
        
        for _ in range(13):
            if self.mountain:
                tile = self.mountain.pop()
                tile.is_in_hand = True
                self.hand.append(tile)
    
    def draw_tile(self) -> Optional[Tile]:
        if not self.mountain:
            return None
        
        tile = self.mountain.pop()
        tile.is_in_hand = True
        self.hand.append(tile)
        return tile
    
    def discard_tile(self, tile_index: int) -> bool:
        if 0 <= tile_index < len(self.hand):
            tile = self.hand.pop(tile_index)
            tile.is_in_hand = False
            tile.is_discarded = True
            self.discarded.append(tile)
            return True
        return False
    
    def discard_tile_by_object(self, tile: Tile) -> bool:
        if tile in self.hand:
            self.hand.remove(tile)
            tile.is_in_hand = False
            tile.is_discarded = True
            self.discarded.append(tile)
            return True
        return False
    
    def get_mountain_count(self) -> int:
        return len(self.mountain)
    
    def get_hand_count(self) -> int:
        return len(self.hand)
    
    def get_discarded_count(self) -> int:
        return len(self.discarded)
    
    def can_draw(self) -> bool:
        return len(self.mountain) > 0
    
    def can_discard(self) -> bool:
        return len(self.hand) > 13

class MultiPlayerGameState:
    def __init__(self):
        self.players = [
            Player(0, PlayerType.HUMAN, "あなた"),
            Player(1, PlayerType.CPU, "CPU1"),
            Player(2, PlayerType.CPU, "CPU2"), 
            Player(3, PlayerType.CPU, "CPU3")
        ]
        self.mountain = []
        self.current_player = 0
        self.game_active = False
        self.reset_game()
    
    def reset_game(self):
        all_tiles = create_all_tiles()
        random.shuffle(all_tiles)
        self.mountain = all_tiles
        
        for player in self.players:
            player.hand = []
            player.discarded = []
        
        # 各プレイヤーに13枚配る
        for _ in range(13):
            for player in self.players:
                if self.mountain:
                    tile = self.mountain.pop()
                    player.add_tile_to_hand(tile)
        
        self.current_player = 0
        self.game_active = True
    
    def get_current_player(self) -> Player:
        return self.players[self.current_player]
    
    def get_human_player(self) -> Player:
        return self.players[0]
    
    def draw_tile_for_player(self, player_id: int) -> Optional[Tile]:
        if not self.mountain or player_id < 0 or player_id >= len(self.players):
            return None
        
        tile = self.mountain.pop()
        self.players[player_id].add_tile_to_hand(tile)
        return tile
    
    def draw_tile_current_player(self) -> Optional[Tile]:
        return self.draw_tile_for_player(self.current_player)
    
    def discard_tile_for_player(self, player_id: int, tile_index: int) -> bool:
        if player_id < 0 or player_id >= len(self.players):
            print(f"エラー: 無効なプレイヤーID {player_id}")
            return False
        result = self.players[player_id].discard_tile(tile_index)
        if result is None:
            print(f"エラー: プレイヤー{player_id}の捨て牌失敗 (index: {tile_index})")
            return False
        return True
    
    def discard_tile_by_object_for_player(self, player_id: int, tile: Tile) -> bool:
        if player_id < 0 or player_id >= len(self.players):
            return False
        return self.players[player_id].discard_tile_by_object(tile)
    
    def next_turn(self):
        self.current_player = (self.current_player + 1) % 4
    
    def get_mountain_count(self) -> int:
        return len(self.mountain)
    
    def can_draw(self) -> bool:
        return len(self.mountain) > 0 and self.game_active
    
    def is_game_over(self) -> bool:
        return len(self.mountain) == 0 or not self.game_active
    
    def get_player_info(self, player_id: int) -> dict:
        if player_id < 0 or player_id >= len(self.players):
            return {}
        
        player = self.players[player_id]
        return {
            'name': player.name,
            'hand_count': player.get_hand_count(),
            'discarded_count': player.get_discarded_count(),
            'is_current': player_id == self.current_player,
            'type': player.player_type.value
        }