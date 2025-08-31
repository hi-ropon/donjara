import time
import threading
from typing import Callable, Optional
from game_logic import MultiPlayerGameState, PlayerType
from cpu_player import CPUPlayer

class GameController:
    def __init__(self, game_state: MultiPlayerGameState, update_callback: Optional[Callable] = None):
        self.game_state = game_state
        self.update_callback = update_callback
        self.cpu_players = {
            1: CPUPlayer("normal"),
            2: CPUPlayer("normal"), 
            3: CPUPlayer("normal")
        }
        self.auto_play_active = False
        self.auto_play_thread = None
        self.turn_delay = 1.5  # CPU思考時間（秒）
        self.last_player_id = -1  # 前回のプレイヤーID（重複ログ防止用）
    
    def start_auto_play(self):
        """自動進行を開始"""
        if not self.auto_play_active:
            self.auto_play_active = True
            self.auto_play_thread = threading.Thread(target=self._auto_play_loop, daemon=True)
            self.auto_play_thread.start()
    
    def stop_auto_play(self):
        """自動進行を停止"""
        self.auto_play_active = False
        if self.auto_play_thread:
            self.auto_play_thread.join(timeout=1.0)
    
    def _auto_play_loop(self):
        """自動進行のメインループ"""
        while self.auto_play_active and not self.game_state.is_game_over():
            try:
                current_player = self.game_state.get_current_player()
                
                # プレイヤーが変わった時のみログ出力
                if self.last_player_id != current_player.player_id:
                    print(f"現在のターン: プレイヤー{current_player.player_id} ({current_player.name})")
                    self.last_player_id = current_player.player_id
                
                # 人間プレイヤーの場合は自動進行しない
                if current_player.player_type == PlayerType.HUMAN:
                    # 初回のみUI更新（13枚の場合のみ）
                    human_player = self.game_state.get_human_player()
                    if len(human_player.hand) == 13:
                        print(f"人間プレイヤー初回処理 - 手牌: {len(human_player.hand)}枚")
                        if self.update_callback:
                            self.update_callback()
                    time.sleep(0.1)
                    continue
                
                # CPUのターン処理
                print(f"CPU{current_player.player_id}のターン開始 - 手牌: {len(current_player.hand)}枚")
                self._process_cpu_turn(current_player.player_id)
                
                # UI更新
                if self.update_callback:
                    self.update_callback()
                
                # 次のターンへ
                self.game_state.next_turn()
                print(f"CPU{current_player.player_id}のターン終了 - 次のプレイヤー: {self.game_state.current_player}")
                
                # 少し待機
                time.sleep(self.turn_delay)
            except Exception as e:
                print(f"自動進行エラー: {e}")
                # エラーが発生しても次のターンへ進む
                self.game_state.next_turn()
                time.sleep(0.5)
    
    def _process_cpu_turn(self, player_id: int):
        """CPUのターン処理"""
        try:
            if player_id not in self.cpu_players:
                print(f"警告: CPU{player_id}が見つかりません")
                return
            
            cpu = self.cpu_players[player_id]
            player = self.game_state.players[player_id]
            
            print(f"  CPU{player_id} 処理前: 手牌{len(player.hand)}枚")
            
            # ツモ
            if len(player.hand) == 13 and self.game_state.can_draw():
                drawn_tile = self.game_state.draw_tile_for_player(player_id)
                if drawn_tile:
                    print(f"  CPU{player_id} ツモ成功: {drawn_tile}")
                else:
                    print(f"  CPU{player_id} ツモ失敗")
            
            # 捨て牌
            if len(player.hand) > 13:
                discard_index = cpu.choose_discard_tile(player.hand)
                print(f"  CPU{player_id} 捨て牌インデックス: {discard_index}")
                if discard_index >= 0 and discard_index < len(player.hand):
                    success = self.game_state.discard_tile_for_player(player_id, discard_index)
                    if success:
                        print(f"  CPU{player_id} 捨て牌成功")
                    else:
                        print(f"  CPU{player_id} 捨て牌失敗")
                else:
                    print(f"  CPU{player_id} 無効な捨て牌インデックス: {discard_index}")
            
            print(f"  CPU{player_id} 処理後: 手牌{len(player.hand)}枚")
        except Exception as e:
            print(f"CPU{player_id}のターン処理エラー: {e}")
            import traceback
            traceback.print_exc()
    
    def process_human_turn(self) -> bool:
        """
        人間プレイヤーのターン処理
        Returns: True if action was successful, False otherwise
        """
        current_player = self.game_state.get_current_player()
        if current_player.player_type != PlayerType.HUMAN:
            print(f"警告: 人間のターンではありません（現在: プレイヤー{current_player.player_id}）")
            return False
        
        human_player = self.game_state.get_human_player()
        
        # 既に14枚以上なら何もしない（重複実行防止）
        if len(human_player.hand) >= 14:
            print(f"人間プレイヤー既に{len(human_player.hand)}枚所持 - ツモ不要")
            return False
        
        # 13枚の場合は自動ツモ
        if len(human_player.hand) == 13 and self.game_state.can_draw():
            print(f"人間プレイヤー自動ツモ実行 - 手牌: {len(human_player.hand)}枚")
            drawn_tile = self.game_state.draw_tile_for_player(0)
            if drawn_tile:
                print(f"人間プレイヤーツモ成功: {drawn_tile} - 手牌: {len(human_player.hand)}枚")
                # update_callbackは呼ばない！（無限ループ防止）
            else:
                print("人間プレイヤーツモ失敗")
            return drawn_tile is not None
        
        return False
    
    def human_discard_tile(self, tile_index: int) -> bool:
        """
        人間プレイヤーが牌を捨てる
        """
        current_player = self.game_state.get_current_player()
        if current_player.player_type != PlayerType.HUMAN:
            return False
        
        success = self.game_state.discard_tile_for_player(0, tile_index)
        if success:
            self.game_state.next_turn()
            if self.update_callback:
                self.update_callback()
        return success
    
    def human_discard_tile_by_object(self, tile) -> bool:
        """
        人間プレイヤーが牌オブジェクトを指定して捨てる
        """
        current_player = self.game_state.get_current_player()
        if current_player.player_type != PlayerType.HUMAN:
            print(f"警告: 人間のターンではありません（現在: プレイヤー{current_player.player_id}）")
            return False
        
        print(f"人間プレイヤー捨て牌: {tile}")
        success = self.game_state.discard_tile_by_object_for_player(0, tile)
        if success:
            print(f"人間プレイヤー捨て牌成功 - 次のターンへ")
            self.game_state.next_turn()
            print(f"ターン移行: プレイヤー0 → プレイヤー{self.game_state.current_player}")
            if self.update_callback:
                self.update_callback()
        else:
            print("人間プレイヤー捨て牌失敗")
        return success
    
    def is_human_turn(self) -> bool:
        """現在が人間プレイヤーのターンかどうか"""
        return self.game_state.get_current_player().player_type == PlayerType.HUMAN
    
    def can_human_discard(self) -> bool:
        """人間プレイヤーが捨て牌できるかどうか"""
        if not self.is_human_turn():
            return False
        return self.game_state.get_human_player().can_discard()
    
    def set_turn_delay(self, delay: float):
        """CPUの思考時間を設定"""
        self.turn_delay = max(0.1, delay)
    
    def get_game_status(self) -> dict:
        """ゲーム状況の取得"""
        return {
            'mountain_count': self.game_state.get_mountain_count(),
            'current_player': self.game_state.current_player,
            'current_player_name': self.game_state.get_current_player().name,
            'is_human_turn': self.is_human_turn(),
            'game_active': self.game_state.game_active,
            'auto_play_active': self.auto_play_active,
            'can_human_discard': self.can_human_discard()
        }