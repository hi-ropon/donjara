import random
from typing import Optional
from tile import Tile

class CPUPlayer:
    def __init__(self, difficulty: str = "normal"):
        self.difficulty = difficulty
    
    def choose_discard_tile(self, hand: list[Tile]) -> int:
        """
        CPUが捨てる牌を選択する
        現在はランダム選択だが、後で戦略的なロジックに拡張可能
        """
        if not hand:
            return -1
        
        if self.difficulty == "easy":
            return self._choose_random_discard(hand)
        elif self.difficulty == "normal":
            return self._choose_strategic_discard(hand)
        elif self.difficulty == "hard":
            return self._choose_advanced_discard(hand)
        else:
            return self._choose_random_discard(hand)
    
    def _choose_random_discard(self, hand: list[Tile]) -> int:
        """完全ランダムで捨て牌を選択"""
        return random.randint(0, len(hand) - 1)
    
    def _choose_strategic_discard(self, hand: list[Tile]) -> int:
        """基本的な戦略で捨て牌を選択"""
        # 字牌を優先的に捨てる
        for i, tile in enumerate(hand):
            if tile.tile_type.value == "jihai":
                return i
        
        # 孤立牌（周りに連続する数がない牌）を捨てる
        isolated_tiles = self._find_isolated_tiles(hand)
        if isolated_tiles:
            return random.choice(isolated_tiles)
        
        # それでもない場合はランダム
        return self._choose_random_discard(hand)
    
    def _choose_advanced_discard(self, hand: list[Tile]) -> int:
        """高度な戦略で捨て牌を選択"""
        # より複雑なロジックを実装可能（将来の拡張用）
        return self._choose_strategic_discard(hand)
    
    def _find_isolated_tiles(self, hand: list[Tile]) -> list[int]:
        """孤立している牌のインデックスを見つける"""
        isolated = []
        
        # 各牌について、同種の隣接する数字があるかチェック
        for i, tile in enumerate(hand):
            if tile.tile_type.value == "jihai":
                continue
                
            has_neighbor = False
            tile_number = tile.number
            tile_type = tile.tile_type
            
            # 隣接する数字があるかチェック
            for other_tile in hand:
                if (other_tile.tile_type == tile_type and 
                    abs(other_tile.number - tile_number) == 1):
                    has_neighbor = True
                    break
            
            if not has_neighbor:
                isolated.append(i)
        
        return isolated
    
    def should_draw(self, hand: list[Tile], mountain_count: int) -> bool:
        """
        CPUがツモするかどうかを判断
        現在の実装では常にツモする（山に牌がある限り）
        """
        return mountain_count > 0 and len(hand) == 13