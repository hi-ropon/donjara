import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
from typing import List, Optional, Callable
from tile import Tile, TileType
from game_logic import MultiPlayerGameState, PlayerType
from game_controller import GameController
from settings import Settings

class TileWidget:
    def __init__(self, parent, tile: Optional[Tile] = None, click_callback: Optional[Callable] = None, face_down: bool = False):
        self.tile = tile
        self.click_callback = click_callback
        self.face_down = face_down
        self.frame = tk.Frame(parent, relief="raised", borderwidth=1)
        self.label = tk.Label(self.frame, width=3, height=4, bg="lightgray" if face_down else "white")
        self.label.pack()
        
        if click_callback and not face_down:
            self.label.bind("<Button-1>", lambda e: click_callback(tile))
            self.label.config(cursor="hand2")
        
        self.update_image()
    
    def update_image(self):
        if self.face_down or not self.tile:
            self.label.config(text="？", font=("Arial", 10, "bold"), fg="darkblue")
            return
        
        try:
            image_path = self.tile.get_image_path()
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((25, 35), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                self.label.config(image=self.photo)
            else:
                self.label.config(text=str(self.tile), font=("Arial", 6))
        except Exception:
            self.label.config(text=str(self.tile), font=("Arial", 6))

class PlayerAreaWidget:
    def __init__(self, parent, player_id: int, position: str, settings: Settings):
        self.player_id = player_id
        self.position = position  # "bottom", "top", "left", "right"
        self.settings = settings
        
        self.frame = tk.Frame(parent, relief="ridge", borderwidth=2)
        self.hand_widgets = []
        self.discarded_widgets = []
        
        self.create_widgets()
    
    def create_widgets(self):
        # プレイヤー名表示
        self.name_label = tk.Label(self.frame, text="", font=("Arial", 9, "bold"))
        self.name_label.pack(pady=2)
        
        # 手牌エリア
        if self.position == "bottom":
            # 人間プレイヤー: 手牌を詳細表示
            self.hand_frame = tk.Frame(self.frame)
            self.hand_frame.pack(pady=5)
        else:
            # CPU: 手牌数のみ表示
            self.hand_info_frame = tk.Frame(self.frame)
            self.hand_info_frame.pack(pady=5)
            
            self.hand_count_label = tk.Label(self.hand_info_frame, text="手牌: 0枚", font=("Arial", 8))
            self.hand_count_label.pack()
            
            # 裏向き牌の表示
            self.hand_frame = tk.Frame(self.hand_info_frame)
            self.hand_frame.pack(pady=2)
        
        # 捨て牌エリア
        discard_label = tk.Label(self.frame, text="捨て牌", font=("Arial", 8))
        discard_label.pack()
        
        # スクロール可能な捨て牌エリア
        if self.position in ["left", "right"]:
            # 縦配置（CPU左右）
            canvas = tk.Canvas(self.frame, width=80, height=50)
            scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
            self.discarded_frame = tk.Frame(canvas)
        elif self.position == "bottom":
            # 人間プレイヤーエリア（広め）
            canvas = tk.Canvas(self.frame, width=500, height=100)
            scrollbar = ttk.Scrollbar(self.frame, orient="horizontal", command=canvas.xview)
            self.discarded_frame = tk.Frame(canvas)
        else:
            # 上部エリア（CPU上）
            canvas = tk.Canvas(self.frame, width=300, height=30)
            scrollbar = ttk.Scrollbar(self.frame, orient="horizontal", command=canvas.xview)
            self.discarded_frame = tk.Frame(canvas)
        
        self.discarded_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.discarded_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set if self.position in ["left", "right"] else None,
                        xscrollcommand=scrollbar.set if self.position in ["top", "bottom"] else None)
        
        canvas.pack(side="left" if self.position in ["left", "right"] else "top", fill="both", expand=True)
        scrollbar.pack(side="right" if self.position in ["left", "right"] else "bottom", fill="y" if self.position in ["left", "right"] else "x")
    
    def update_display(self, player, is_current: bool, click_callback=None):
        # 名前とターン表示
        name_text = player.name
        if is_current:
            name_text += " ◄"
        self.name_label.config(text=name_text, fg="red" if is_current else "black")
        
        # 手牌更新
        self.update_hand_display(player, click_callback)
        
        # 捨て牌更新
        self.update_discarded_display(player)
    
    def update_hand_display(self, player, click_callback=None):
        # 既存ウィジェット削除
        for widget in self.hand_widgets:
            widget.frame.destroy()
        self.hand_widgets = []
        
        if self.position == "bottom":
            # 人間プレイヤー: 手牌を詳細表示
            for i, tile in enumerate(player.hand):
                custom_path = self.settings.get_custom_image(tile.tile_type, tile.number)
                if custom_path:
                    tile.image_path = custom_path
                
                widget = TileWidget(self.hand_frame, tile, click_callback, face_down=False)
                widget.frame.grid(row=0, column=i, padx=1, pady=1)
                self.hand_widgets.append(widget)
        else:
            # CPU: 手牌数と裏向き表示
            self.hand_count_label.config(text=f"手牌: {player.get_hand_count()}枚")
            
            # 裏向き牌を数枚表示（最大5枚）
            display_count = min(5, player.get_hand_count())
            for i in range(display_count):
                widget = TileWidget(self.hand_frame, None, None, face_down=True)
                if self.position in ["left", "right"]:
                    widget.frame.grid(row=i, column=0, padx=1, pady=1)
                else:
                    widget.frame.grid(row=0, column=i, padx=1, pady=1)
                self.hand_widgets.append(widget)
    
    def update_discarded_display(self, player):
        # 既存ウィジェット削除
        for widget in self.discarded_widgets:
            widget.frame.destroy()
        self.discarded_widgets = []
        
        # 捨て牌表示
        cols = 4 if self.position in ["left", "right"] else 8
        for i, tile in enumerate(player.discarded):
            custom_path = self.settings.get_custom_image(tile.tile_type, tile.number)
            if custom_path:
                tile.image_path = custom_path
            
            widget = TileWidget(self.discarded_frame, tile, face_down=False)
            widget.frame.grid(row=i // cols, column=i % cols, padx=1, pady=1)
            self.discarded_widgets.append(widget)

class MultiPlayerMahjongGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("麻雀風アプリ - Donjara (4人対戦)")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        self.game_state = MultiPlayerGameState()
        self.settings = Settings()
        self.controller = GameController(self.game_state, self.update_display)
        
        self.player_areas = {}
        
        self.create_menu()
        self.create_main_layout()
        self.update_display()
        
        # 自動進行開始
        self.controller.start_auto_play()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ゲーム", menu=game_menu)
        game_menu.add_command(label="新しいゲーム", command=self.new_game)
        game_menu.add_separator()
        game_menu.add_command(label="自動進行 開始/停止", command=self.toggle_auto_play)
        game_menu.add_separator()
        game_menu.add_command(label="終了", command=self.root.quit)
        
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="設定", menu=settings_menu)
        settings_menu.add_command(label="画像設定", command=self.open_image_settings)
        settings_menu.add_command(label="CPU速度設定", command=self.open_speed_settings)
    
    def create_main_layout(self):
        # メイン情報表示
        info_frame = tk.Frame(self.root)
        info_frame.pack(fill="x", padx=10, pady=5)
        
        self.info_label = tk.Label(info_frame, text="", font=("Arial", 10))
        self.info_label.pack(side="left")
        
        self.status_label = tk.Label(info_frame, text="", font=("Arial", 9))
        self.status_label.pack(side="right")
        
        # 4人配置のメインエリア
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=3, pady=3)
        
        # 上部: CPU2
        self.player_areas[2] = PlayerAreaWidget(main_frame, 2, "top", self.settings)
        self.player_areas[2].frame.pack(side="top", fill="x", pady=1)
        
        # 中央部
        center_frame = tk.Frame(main_frame, height=300)
        center_frame.pack(fill="x", expand=False, pady=2)
        center_frame.pack_propagate(False)
        
        # 左: CPU3
        self.player_areas[3] = PlayerAreaWidget(center_frame, 3, "left", self.settings)
        self.player_areas[3].frame.pack(side="left", fill="y", padx=(0, 2))
        
        # 中央: ゲーム情報
        center_info_frame = tk.Frame(center_frame)
        center_info_frame.pack(side="left", fill="both", expand=True, padx=2)
        
        # 山の情報
        mountain_frame = tk.Frame(center_info_frame)
        mountain_frame.pack(expand=True, pady=5)
        
        tk.Label(mountain_frame, text="山", font=("Arial", 14, "bold")).pack()
        self.mountain_label = tk.Label(mountain_frame, text="残り 0枚", font=("Arial", 12))
        self.mountain_label.pack(pady=5)
        
        self.turn_label = tk.Label(mountain_frame, text="", font=("Arial", 11), fg="blue")
        self.turn_label.pack(pady=3)
        
        # 右: CPU1  
        self.player_areas[1] = PlayerAreaWidget(center_frame, 1, "right", self.settings)
        self.player_areas[1].frame.pack(side="right", fill="y", padx=(2, 0))
        
        # 下部: 人間プレイヤー
        self.player_areas[0] = PlayerAreaWidget(main_frame, 0, "bottom", self.settings)
        self.player_areas[0].frame.pack(side="bottom", fill="x", pady=2)
    
    def update_display(self):
        # ゲーム情報更新
        status = self.controller.get_game_status()
        self.info_label.config(text=f"山: {status['mountain_count']}枚")
        
        auto_status = "自動進行中" if status['auto_play_active'] else "一時停止"
        self.status_label.config(text=auto_status)
        
        self.mountain_label.config(text=f"残り {status['mountain_count']}枚")
        self.turn_label.config(text=f"現在: {status['current_player_name']}")
        
        # 各プレイヤーエリア更新
        for i in range(4):
            player = self.game_state.players[i]
            is_current = (i == self.game_state.current_player)
            click_callback = self.on_tile_click if i == 0 else None
            
            self.player_areas[i].update_display(player, is_current, click_callback)
        
        # 人間プレイヤーのターンの場合、自動ツモ実行
        if status['is_human_turn']:
            self.controller.process_human_turn()
    
    def on_tile_click(self, tile: Tile):
        if self.controller.can_human_discard():
            if self.controller.human_discard_tile_by_object(tile):
                pass  # update_display は controller から自動呼び出される
        else:
            if self.controller.is_human_turn():
                messagebox.showwarning("警告", "まずツモを行ってください")
            else:
                messagebox.showwarning("警告", "あなたのターンではありません")
    
    def new_game(self):
        self.controller.stop_auto_play()
        self.game_state.reset_game()
        self.controller = GameController(self.game_state, self.update_display)
        self.update_display()
        self.controller.start_auto_play()
        messagebox.showinfo("情報", "新しいゲームを開始しました")
    
    def toggle_auto_play(self):
        if self.controller.auto_play_active:
            self.controller.stop_auto_play()
        else:
            self.controller.start_auto_play()
    
    def open_image_settings(self):
        from gui import ImageSettingsWindow
        ImageSettingsWindow(self.root, self.settings, self.update_display)
    
    def open_speed_settings(self):
        SpeedSettingsWindow(self.root, self.controller)
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        self.controller.stop_auto_play()
        self.root.destroy()

class SpeedSettingsWindow:
    def __init__(self, parent, controller: GameController):
        self.controller = controller
        
        self.window = tk.Toplevel(parent)
        self.window.title("CPU速度設定")
        self.window.geometry("300x150")
        self.window.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.window, text="CPU思考時間 (秒)", font=("Arial", 12)).pack(pady=10)
        
        self.speed_var = tk.DoubleVar(value=self.controller.turn_delay)
        
        speed_frame = tk.Frame(self.window)
        speed_frame.pack(pady=10)
        
        tk.Label(speed_frame, text="速い").pack(side="left")
        scale = tk.Scale(speed_frame, from_=0.1, to=3.0, resolution=0.1, 
                        orient="horizontal", variable=self.speed_var,
                        length=200, command=self.on_speed_change)
        scale.pack(side="left", padx=10)
        tk.Label(speed_frame, text="遅い").pack(side="left")
        
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="適用", command=self.apply_settings).pack(side="left", padx=5)
        tk.Button(button_frame, text="閉じる", command=self.window.destroy).pack(side="left", padx=5)
    
    def on_speed_change(self, value):
        self.controller.set_turn_delay(float(value))
    
    def apply_settings(self):
        self.controller.set_turn_delay(self.speed_var.get())
        messagebox.showinfo("設定", "CPU速度を設定しました")
        self.window.destroy()