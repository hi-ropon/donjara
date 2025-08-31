from enum import Enum
from typing import Optional
import os

class TileType(Enum):
    MANZU = "manzu"      # 萬子
    PINZU = "pinzu"      # 筒子  
    SOUZU = "souzu"      # 索子
    JIHAI = "jihai"      # 字牌

class Tile:
    def __init__(self, tile_type: TileType, number: int, image_path: Optional[str] = None):
        self.tile_type = tile_type
        self.number = number
        self.image_path = image_path
        self.is_discarded = False
        self.is_in_hand = False
        
    def __str__(self):
        type_names = {
            TileType.MANZU: "萬",
            TileType.PINZU: "筒", 
            TileType.SOUZU: "索",
            TileType.JIHAI: "字"
        }
        return f"{self.number}{type_names[self.tile_type]}"
    
    def __eq__(self, other):
        if not isinstance(other, Tile):
            return False
        return self.tile_type == other.tile_type and self.number == other.number
    
    def get_default_image_path(self):
        type_folders = {
            TileType.MANZU: "wan",
            TileType.PINZU: "pin",
            TileType.SOUZU: "sou", 
            TileType.JIHAI: "honor"
        }
        folder = type_folders[self.tile_type]
        return os.path.join("assets", folder, f"{self.number}.png")
    
    def get_image_path(self):
        if self.image_path and os.path.exists(self.image_path):
            return self.image_path
        return self.get_default_image_path()

def create_all_tiles():
    tiles = []
    
    # 萬子 1-9 × 4枚
    for number in range(1, 10):
        for _ in range(4):
            tiles.append(Tile(TileType.MANZU, number))
    
    # 筒子 1-9 × 4枚  
    for number in range(1, 10):
        for _ in range(4):
            tiles.append(Tile(TileType.PINZU, number))
    
    # 索子 1-9 × 4枚
    for number in range(1, 10):
        for _ in range(4):
            tiles.append(Tile(TileType.SOUZU, number))
    
    # 字牌 1-7 × 4枚 (東南西北白發中)
    for number in range(1, 8):
        for _ in range(4):
            tiles.append(Tile(TileType.JIHAI, number))
    
    return tiles