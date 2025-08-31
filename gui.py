import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
from typing import List, Optional, Callable
from tile import Tile, TileType
from game_logic import GameState
from settings import Settings

class TileWidget:
    def __init__(self, parent, tile: Tile, click_callback: Optional[Callable] = None):
        self.tile = tile
        self.click_callback = click_callback
        self.frame = tk.Frame(parent, relief="raised", borderwidth=1)
        self.label = tk.Label(self.frame, width=4, height=6, bg="white")
        self.label.pack()
        
        if click_callback:
            self.label.bind("<Button-1>", lambda e: click_callback(tile))
            self.label.config(cursor="hand2")
        
        self.update_image()
    
    def update_image(self):
        try:
            image_path = self.tile.get_image_path()
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((40, 60), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                self.label.config(image=self.photo)
            else:
                self.label.config(text=str(self.tile), font=("Arial", 8))
        except Exception:
            self.label.config(text=str(self.tile), font=("Arial", 8))

class MahjongGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("麻雀風アプリ - Donjara")
        self.root.geometry("1200x800")
        
        self.game = GameState()
        self.settings = Settings()
        
        self.hand_widgets = []
        self.discarded_widgets = []
        
        self.create_menu()
        self.create_main_layout()
        self.update_display()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ゲーム", menu=game_menu)
        game_menu.add_command(label="新しいゲーム", command=self.new_game)
        game_menu.add_separator()
        game_menu.add_command(label="終了", command=self.root.quit)
        
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="設定", menu=settings_menu)
        settings_menu.add_command(label="画像設定", command=self.open_image_settings)
    
    def create_main_layout(self):
        # メイン情報表示
        info_frame = tk.Frame(self.root)
        info_frame.pack(fill="x", padx=10, pady=5)
        
        self.info_label = tk.Label(info_frame, text="", font=("Arial", 12))
        self.info_label.pack(side="left")
        
        # 山エリア
        mountain_frame = tk.Frame(self.root)
        mountain_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(mountain_frame, text="山:", font=("Arial", 10, "bold")).pack(side="left")
        self.mountain_label = tk.Label(mountain_frame, text="", font=("Arial", 10))
        self.mountain_label.pack(side="left", padx=(10, 0))
        
        self.draw_button = tk.Button(mountain_frame, text="ツモ", command=self.draw_tile)
        self.draw_button.pack(side="right")
        
        # 手牌エリア
        hand_frame = tk.Frame(self.root)
        hand_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(hand_frame, text="手牌:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.hand_frame = tk.Frame(hand_frame)
        self.hand_frame.pack(fill="x", pady=(5, 0))
        
        # 捨て牌エリア
        discarded_frame = tk.Frame(self.root)
        discarded_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(discarded_frame, text="捨て牌:", font=("Arial", 10, "bold")).pack(anchor="w")
        
        # スクロール可能な捨て牌エリア
        canvas = tk.Canvas(discarded_frame, height=200)
        scrollbar = ttk.Scrollbar(discarded_frame, orient="vertical", command=canvas.yview)
        self.discarded_frame = tk.Frame(canvas)
        
        self.discarded_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.discarded_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def update_display(self):
        # 情報ラベル更新
        self.info_label.config(
            text=f"手牌: {self.game.get_hand_count()}枚 | 捨て牌: {self.game.get_discarded_count()}枚"
        )
        
        # 山の残り枚数更新
        self.mountain_label.config(text=f"残り {self.game.get_mountain_count()}枚")
        self.draw_button.config(state="normal" if self.game.can_draw() else "disabled")
        
        self.update_hand_display()
        self.update_discarded_display()
    
    def update_hand_display(self):
        # 既存の手牌ウィジェット削除
        for widget in self.hand_widgets:
            widget.frame.destroy()
        self.hand_widgets = []
        
        # 新しい手牌ウィジェット作成
        for i, tile in enumerate(self.game.hand):
            # カスタム画像があるかチェック
            custom_path = self.settings.get_custom_image(tile.tile_type, tile.number)
            if custom_path:
                tile.image_path = custom_path
            
            widget = TileWidget(self.hand_frame, tile, self.on_tile_click)
            widget.frame.grid(row=0, column=i, padx=2, pady=2)
            self.hand_widgets.append(widget)
    
    def update_discarded_display(self):
        # 既存の捨て牌ウィジェット削除
        for widget in self.discarded_widgets:
            widget.frame.destroy()
        self.discarded_widgets = []
        
        # 新しい捨て牌ウィジェット作成（6列で表示）
        cols = 6
        for i, tile in enumerate(self.game.discarded):
            # カスタム画像があるかチェック
            custom_path = self.settings.get_custom_image(tile.tile_type, tile.number)
            if custom_path:
                tile.image_path = custom_path
            
            widget = TileWidget(self.discarded_frame, tile)
            widget.frame.grid(row=i // cols, column=i % cols, padx=2, pady=2)
            self.discarded_widgets.append(widget)
    
    def draw_tile(self):
        if self.game.can_draw():
            tile = self.game.draw_tile()
            if tile:
                self.update_display()
            else:
                messagebox.showinfo("情報", "山に牌がありません")
    
    def on_tile_click(self, tile: Tile):
        if self.game.can_discard():
            if self.game.discard_tile_by_object(tile):
                self.update_display()
        else:
            messagebox.showwarning("警告", "先にツモを行ってください（14枚の時のみ捨てられます）")
    
    def new_game(self):
        self.game.reset_game()
        self.update_display()
        messagebox.showinfo("情報", "新しいゲームを開始しました")
    
    def open_image_settings(self):
        ImageSettingsWindow(self.root, self.settings, self.update_display)
    
    def run(self):
        self.root.mainloop()

class ImageSettingsWindow:
    def __init__(self, parent, settings: Settings, update_callback):
        self.settings = settings
        self.update_callback = update_callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("画像設定")
        self.window.geometry("600x500")
        self.window.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        # 牌選択フレーム
        select_frame = tk.Frame(self.window)
        select_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(select_frame, text="牌の種類:", font=("Arial", 10, "bold")).pack(anchor="w")
        
        type_frame = tk.Frame(select_frame)
        type_frame.pack(fill="x", pady=5)
        
        self.tile_type_var = tk.StringVar(value="manzu")
        types = [("萬子", "manzu"), ("筒子", "pinzu"), ("索子", "souzu"), ("字牌", "jihai")]
        for text, value in types:
            tk.Radiobutton(type_frame, text=text, variable=self.tile_type_var, 
                          value=value, command=self.update_number_options).pack(side="left")
        
        number_frame = tk.Frame(select_frame)
        number_frame.pack(fill="x", pady=5)
        
        tk.Label(number_frame, text="番号:", font=("Arial", 10)).pack(side="left")
        self.number_var = tk.StringVar()
        self.number_combo = ttk.Combobox(number_frame, textvariable=self.number_var, 
                                        state="readonly", width=5)
        self.number_combo.pack(side="left", padx=(5, 0))
        
        self.update_number_options()
        
        # ボタンフレーム
        button_frame = tk.Frame(select_frame)
        button_frame.pack(fill="x", pady=10)
        
        tk.Button(button_frame, text="画像を選択", command=self.select_image).pack(side="left")
        tk.Button(button_frame, text="画像をリセット", command=self.reset_image).pack(side="left", padx=(10, 0))
        
        # 現在の設定表示
        info_frame = tk.Frame(self.window)
        info_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(info_frame, text="現在のカスタム画像:", font=("Arial", 10, "bold")).pack(anchor="w")
        
        # リストボックスでカスタム画像一覧表示
        self.listbox = tk.Listbox(info_frame)
        self.listbox.pack(fill="both", expand=True, pady=5)
        
        self.update_custom_images_list()
    
    def update_number_options(self):
        tile_type = self.tile_type_var.get()
        if tile_type == "jihai":
            numbers = ["1", "2", "3", "4", "5", "6", "7"]  # 東南西北白發中
        else:
            numbers = [str(i) for i in range(1, 10)]
        
        self.number_combo['values'] = numbers
        if numbers:
            self.number_combo.set(numbers[0])
    
    def select_image(self):
        if not self.number_var.get():
            messagebox.showwarning("警告", "牌の番号を選択してください")
            return
        
        file_path = filedialog.askopenfilename(
            title="牌の画像を選択",
            filetypes=[
                ("画像ファイル", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("すべてのファイル", "*.*")
            ]
        )
        
        if file_path:
            tile_type = TileType(self.tile_type_var.get())
            number = int(self.number_var.get())
            
            if self.settings.set_custom_image(tile_type, number, file_path):
                messagebox.showinfo("成功", f"{tile_type.value} {number} の画像を設定しました")
                self.update_custom_images_list()
                if self.update_callback:
                    self.update_callback()
            else:
                messagebox.showerror("エラー", "画像ファイルの設定に失敗しました")
    
    def reset_image(self):
        if not self.number_var.get():
            messagebox.showwarning("警告", "牌の番号を選択してください")
            return
        
        tile_type = TileType(self.tile_type_var.get())
        number = int(self.number_var.get())
        
        self.settings.remove_custom_image(tile_type, number)
        messagebox.showinfo("成功", f"{tile_type.value} {number} の画像をリセットしました")
        self.update_custom_images_list()
        if self.update_callback:
            self.update_callback()
    
    def update_custom_images_list(self):
        self.listbox.delete(0, tk.END)
        
        for key, path in self.settings.get_all_custom_images().items():
            tile_type, number = key.split('_')
            display_name = f"{tile_type} {number}: {os.path.basename(path)}"
            self.listbox.insert(tk.END, display_name)