#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麻雀風アプリ - Donjara
144牌を使った麻雀風のゲームアプリケーション
"""

import sys
import os

# 必要なライブラリのインポートと依存関係チェック
try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    print("エラー: tkinterが見つかりません。Pythonの標準ライブラリに含まれているはずです。")
    sys.exit(1)

try:
    from PIL import Image, ImageTk
except ImportError:
    print("エラー: Pillowライブラリが必要です。")
    print("インストール方法: pip install Pillow")
    sys.exit(1)

# アプリケーションモジュールのインポート
try:
    from multiplayer_gui import MultiPlayerMahjongGUI
    from gui import MahjongGUI
except ImportError as e:
    print(f"エラー: アプリケーションモジュールの読み込みに失敗しました: {e}")
    sys.exit(1)

def main():
    """メイン関数"""
    try:
        # アプリケーションの初期化と実行
        # 4人対戦版を使用
        app = MultiPlayerMahjongGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("エラー", f"アプリケーションの実行中にエラーが発生しました:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    # 作業ディレクトリの設定
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    main()