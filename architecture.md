# ドンジャラアプリケーション アーキテクチャ設計図

## プロジェクト概要

ドンジャラ - 144枚の牌を使用した麻雀風ゲーム。Python (tkinter + PIL) で実装された4人対戦モード（人間1人 + CPU3人）のアプリケーション。

## クラス図

```mermaid
classDiagram
    %% Enums
    class TileType {
        <<enumeration>>
        +MANZU : str
        +PINZU : str
        +SOUZU : str
        +JIHAI : str
    }

    class PlayerType {
        <<enumeration>>
        +HUMAN : str
        +CPU : str
    }

    %% 牌（Tile）関連
    class Tile {
        -tile_type : TileType
        -number : int
        -image_path : str
        -is_discarded : bool
        -is_in_hand : bool
        +__init__(tile_type, number, image_path)
        +__str__() : str
        +__eq__(other) : bool
        +get_default_image_path() : str
        +get_image_path() : str
    }

    %% プレイヤー関連
    class Player {
        -player_id : int
        -player_type : PlayerType
        -name : str
        -hand : list[Tile]
        -discarded : list[Tile]
        +__init__(player_id, player_type, name)
        +add_tile_to_hand(tile) : void
        +discard_tile(tile_index) : Tile
        +discard_tile_by_object(tile) : bool
        +get_hand_count() : int
        +get_discarded_count() : int
        +can_discard() : bool
    }

    %% ゲーム状態管理
    class MultiPlayerGameState {
        -players : list[Player]
        -mountain : list[Tile]
        -current_player : int
        -game_active : bool
        +__init__()
        +reset_game() : void
        +get_current_player() : Player
        +get_human_player() : Player
        +draw_tile_for_player(player_id) : Tile
        +draw_tile_current_player() : Tile
        +discard_tile_for_player(player_id, tile_index) : bool
        +discard_tile_by_object_for_player(player_id, tile) : bool
        +next_turn() : void
        +get_mountain_count() : int
        +can_draw() : bool
        +is_game_over() : bool
        +get_player_info(player_id) : dict
    }

    %% AI関連
    class CPUPlayer {
        -difficulty : str
        +__init__(difficulty)
        +choose_discard_tile(hand) : int
        +should_draw(hand, mountain_count) : bool
        -_choose_random_discard(hand) : int
        -_choose_strategic_discard(hand) : int
        -_choose_advanced_discard(hand) : int
        -_find_isolated_tiles(hand) : list[int]
    }

    %% ゲーム制御
    class GameController {
        -game_state : MultiPlayerGameState
        -update_callback : Callable
        -cpu_players : dict[int, CPUPlayer]
        -auto_play_active : bool
        -auto_play_thread : Thread
        -turn_delay : float
        -last_player_id : int
        +__init__(game_state, update_callback)
        +start_auto_play() : void
        +stop_auto_play() : void
        +process_human_turn() : bool
        +human_discard_tile(tile_index) : bool
        +human_discard_tile_by_object(tile) : bool
        +is_human_turn() : bool
        +can_human_discard() : bool
        +set_turn_delay(delay) : void
        +get_game_status() : dict
        -_auto_play_loop() : void
        -_process_cpu_turn(player_id) : void
    }

    %% GUI関連
    class TileWidget {
        -tile : Tile
        -click_callback : Callable
        -face_down : bool
        -frame : tkinter.Frame
        -label : tkinter.Label
        -photo : ImageTk.PhotoImage
        +__init__(parent, tile, click_callback, face_down)
        +update_image() : void
    }

    class PlayerAreaWidget {
        -player_id : int
        -position : str
        -settings : Settings
        -frame : tkinter.Frame
        -hand_widgets : list[TileWidget]
        -discarded_widgets : list[TileWidget]
        +__init__(parent, player_id, position, settings)
        +create_widgets() : void
        +update_display(player, is_current, click_callback) : void
        +update_hand_display(player, click_callback) : void
        +update_discarded_display(player) : void
    }

    class MultiPlayerMahjongGUI {
        -root : tkinter.Tk
        -game_state : MultiPlayerGameState
        -settings : Settings
        -controller : GameController
        -player_areas : dict[int, PlayerAreaWidget]
        -info_label : tkinter.Label
        -status_label : tkinter.Label
        -mountain_label : tkinter.Label
        -turn_label : tkinter.Label
        +__init__()
        +create_menu() : void
        +create_main_layout() : void
        +update_display() : void
        +on_tile_click(tile) : void
        +new_game() : void
        +toggle_auto_play() : void
        +open_image_settings() : void
        +open_speed_settings() : void
        +run() : void
        +on_closing() : void
    }

    class SpeedSettingsWindow {
        -controller : GameController
        -window : tkinter.Toplevel
        -speed_var : tkinter.DoubleVar
        +__init__(parent, controller)
        +create_widgets() : void
        +on_speed_change(value) : void
        +apply_settings() : void
    }

    %% 設定関連
    class Settings {
        -settings_file : str
        -custom_images : dict[str, str]
        +__init__(settings_file)
        +load_settings() : void
        +save_settings() : void
        +set_custom_image(tile_type, number, image_path) : bool
        +get_custom_image(tile_type, number) : str
        +remove_custom_image(tile_type, number) : void
        +clear_all_custom_images() : void
        +get_all_custom_images() : dict[str, str]
        +has_custom_image(tile_type, number) : bool
    }

    %% 関係性
    Tile --* TileType : 使用
    Player --* PlayerType : 使用
    Player "1" *-- "many" Tile : 手牌・捨て牌
    MultiPlayerGameState "1" *-- "4" Player : プレイヤー管理
    MultiPlayerGameState "1" *-- "many" Tile : 山札管理
    GameController "1" --> "1" MultiPlayerGameState : 制御
    GameController "1" --> "many" CPUPlayer : AI制御
    MultiPlayerMahjongGUI "1" --> "1" GameController : UI制御
    MultiPlayerMahjongGUI "1" --> "1" Settings : 設定管理
    MultiPlayerMahjongGUI "1" *-- "4" PlayerAreaWidget : UI表示
    PlayerAreaWidget "1" *-- "many" TileWidget : 牌表示
    TileWidget "1" --> "1" Tile : 表示対象
    SpeedSettingsWindow "1" --> "1" GameController : 設定変更
    Settings --> TileType : 画像設定
```

## シーケンス図

### ゲーム開始フロー

```mermaid
sequenceDiagram
    participant App as app.py
    participant GUI as MultiPlayerMahjongGUI
    participant Controller as GameController  
    participant GameState as MultiPlayerGameState
    participant Player as Player

    App->>GUI: MultiPlayerMahjongGUI()
    GUI->>GameState: MultiPlayerGameState()
    GameState->>GameState: reset_game()
    loop 4プレイヤー
        GameState->>Player: Player(id, type, name)
    end
    loop 各プレイヤーに13枚配布
        GameState->>Player: add_tile_to_hand(tile)
    end
    GUI->>Controller: GameController(game_state, update_callback)
    Controller->>Controller: 各CPUプレイヤーを初期化
    GUI->>Controller: start_auto_play()
    Controller->>Controller: _auto_play_loop() (別スレッド)
    GUI->>GUI: update_display()
```

### 人間プレイヤーのターン処理

```mermaid
sequenceDiagram
    participant GUI as MultiPlayerMahjongGUI
    participant Controller as GameController
    participant GameState as MultiPlayerGameState
    participant Player as Player (人間)

    Note over GUI,Player: 人間プレイヤーのターン開始

    GUI->>Controller: update_display()で自動実行
    Controller->>Controller: is_human_turn()
    alt 手牌が13枚の場合
        Controller->>GameState: draw_tile_for_player(0)
        GameState->>Player: add_tile_to_hand(tile)
        Controller->>GUI: update_display() (コールバック)
    end
    
    Note over GUI,Player: プレイヤーが牌をクリック
    GUI->>GUI: on_tile_click(tile)
    GUI->>Controller: can_human_discard()
    Controller->>Player: can_discard() (手牌>13枚?)
    alt 捨て牌可能
        GUI->>Controller: human_discard_tile_by_object(tile)
        Controller->>GameState: discard_tile_by_object_for_player(0, tile)
        GameState->>Player: discard_tile_by_object(tile)
        Controller->>GameState: next_turn()
        Controller->>GUI: update_display() (コールバック)
    else 捨て牌不可
        GUI->>GUI: messagebox.showwarning()
    end
```

### CPUプレイヤーの自動処理フロー

```mermaid
sequenceDiagram
    participant Controller as GameController
    participant GameState as MultiPlayerGameState
    participant CPUPlayer as CPUPlayer
    participant Player as Player (CPU)
    participant GUI as MultiPlayerMahjongGUI

    Note over Controller,GUI: CPUターンの自動処理

    loop 自動進行ループ
        Controller->>GameState: get_current_player()
        alt CPUプレイヤーのターン
            Controller->>Controller: _process_cpu_turn(player_id)
            
            alt 手牌が13枚の場合（ツモ）
                Controller->>GameState: draw_tile_for_player(player_id)
                GameState->>Player: add_tile_to_hand(tile)
            end
            
            alt 手牌が14枚以上の場合（捨て牌）
                Controller->>CPUPlayer: choose_discard_tile(hand)
                CPUPlayer->>CPUPlayer: 戦略的に捨て牌選択
                Controller->>GameState: discard_tile_for_player(player_id, index)
                GameState->>Player: discard_tile(index)
            end
            
            Controller->>GUI: update_display() (コールバック)
            Controller->>GameState: next_turn()
            Controller->>Controller: time.sleep(turn_delay)
        else 人間プレイヤーのターン
            Controller->>Controller: continue (待機)
        end
    end
```

### GUI更新サイクル

```mermaid
sequenceDiagram
    participant Controller as GameController
    participant GUI as MultiPlayerMahjongGUI
    participant PlayerArea as PlayerAreaWidget
    participant TileWidget as TileWidget
    participant Settings as Settings

    Controller->>GUI: update_display() (コールバック)
    GUI->>Controller: get_game_status()
    GUI->>GUI: ゲーム情報ラベル更新
    
    loop 4プレイヤー
        GUI->>PlayerArea: update_display(player, is_current, click_callback)
        PlayerArea->>PlayerArea: update_hand_display()
        PlayerArea->>PlayerArea: update_discarded_display()
        
        alt 人間プレイヤー（詳細表示）
            loop 手牌の各牌
                PlayerArea->>Settings: get_custom_image()
                PlayerArea->>TileWidget: TileWidget(tile, click_callback)
                TileWidget->>TileWidget: update_image()
            end
        else CPUプレイヤー（裏向き表示）
            PlayerArea->>TileWidget: TileWidget(face_down=True)
        end
        
        loop 捨て牌の各牌
            PlayerArea->>TileWidget: TileWidget(tile)
            TileWidget->>TileWidget: update_image()
        end
    end
```

## アーキテクチャの特徴

### MVCパターンの採用
- **Model**: `MultiPlayerGameState`, `Player`, `Tile` - ゲームのデータと状態管理
- **View**: `MultiPlayerMahjongGUI`, `PlayerAreaWidget`, `TileWidget` - UI表示とユーザー操作
- **Controller**: `GameController` - ゲームフローの制御とModel/View間の調整

### スレッド設計
- メインスレッド: GUI描画とユーザー操作処理
- バックグラウンドスレッド: CPUプレイヤーの自動処理（`_auto_play_loop`）
- 同期機構: コールバック関数によるGUI更新の制御

### 責任分散
- **ゲームロジック**: 牌の管理、プレイヤー状態、ターン制御
- **AI処理**: CPUプレイヤーの戦略的判断
- **UI管理**: 牌の表示、プレイヤーエリア、設定ダイアログ
- **設定管理**: 画像カスタマイズ、ゲーム設定の永続化

### 拡張性
- CPUの難易度レベル調整可能
- 牌画像のカスタマイズ機能
- ゲーム設定の柔軟な変更
- 新しいゲームモードの追加が容易な設計