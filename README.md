# Donjara - 麻雀風アプリ

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Donjara is a Mahjong-style tile game application built with Python and tkinter. It features 4-player gameplay with CPU opponents, automatic turn progression, and customizable tile images.

**Donjara** は Python と tkinter で作られた麻雀風のタイル ゲーム アプリケーションです。4 人対戦、CPU 対戦相手、自動ターン進行、カスタマイズ可能なタイル画像が特徴です。

## 🎯 Features / 特徴

- **4-Player Game** / **4人対戦**: 1 human player vs 3 CPU players / 人間1人対CPU3人
- **Automatic Turn Progression** / **自動ターン進行**: CPUs play automatically / CPUが自動で進行
- **Custom Tile Images** / **カスタム牌画像**: Use your own tile images / 独自の牌画像を使用可能
- **144 Tiles System** / **144牌システム**: Complete Mahjong tile set / 完全な麻雀牌セット
- **Compact GUI** / **コンパクトGUI**: Optimized for various screen sizes / 様々な画面サイズに最適化

## 📸 Screenshots / スクリーンショット

<!-- Add screenshots here -->
*Screenshots will be added soon / スクリーンショットは近日追加予定*

## 🚀 Installation / インストール

### Requirements / 必要環境

- Python 3.8+ / Python 3.8以上
- tkinter (usually included with Python) / tkinter（通常Pythonに含まれています）

### Setup / セットアップ

1. **Clone the repository / リポジトリをクローン**
   ```bash
   git clone https://github.com/yourusername/donjara.git
   cd donjara
   ```

2. **Install dependencies / 依存関係をインストール**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application / アプリケーションを実行**
   ```bash
   python app.py
   ```

## 🎮 How to Play / 遊び方

### Basic Gameplay / 基本的な遊び方

1. **Start the game** / **ゲーム開始**: Run `python app.py` / `python app.py`を実行
2. **Automatic Draw** / **自動ツモ**: When it's your turn, a tile is automatically drawn / あなたのターンになると自動でツモされます
3. **Discard Tiles** / **牌を捨てる**: Click on a tile in your hand to discard it / 手牌の牌をクリックして捨てます
4. **CPU Turns** / **CPUのターン**: CPU players play automatically / CPUは自動で進行します

### Game Controls / ゲーム操作

- **Menu > New Game** / **メニュー > 新しいゲーム**: Start a new game / 新しいゲームを開始
- **Menu > Settings > Image Settings** / **メニュー > 設定 > 画像設定**: Customize tile images / 牌画像をカスタマイズ
- **Menu > Settings > CPU Speed** / **メニュー > 設定 > CPU速度**: Adjust CPU thinking time / CPUの思考時間を調整

## 🎨 Custom Tile Images / カスタム牌画像

### Method 1: Settings Menu / 方法1: 設定メニュー

1. Go to **Settings > Image Settings** / **設定 > 画像設定**へ移動
2. Select tile type and number / 牌の種類と番号を選択
3. Choose your image file / 画像ファイルを選択
4. Click "Apply" / "適用"をクリック

### Method 2: Asset Folders / 方法2: アセットフォルダ

Place your images in the following structure:
以下の構造で画像を配置してください：

```
assets/
├── wan/     # 萬子 (1.png to 9.png)
├── pin/     # 筒子 (1.png to 9.png)  
├── sou/     # 索子 (1.png to 9.png)
└── honor/   # 字牌 (1.png to 7.png)
    # 1: 東, 2: 南, 3: 西, 4: 北, 5: 白, 6: 發, 7: 中
```

**Supported formats** / **対応形式**: PNG, JPG, JPEG, GIF, BMP
**Recommended size** / **推奨サイズ**: 40x60 pixels / 40x60ピクセル

## 🏗️ Architecture / アーキテクチャ

### File Structure / ファイル構成

```
donjara/
├── app.py              # Main application / メインアプリケーション
├── tile.py             # Tile classes / 牌クラス
├── game_logic.py       # Game state management / ゲーム状態管理
├── game_controller.py  # Turn management / ターン管理
├── cpu_player.py       # CPU AI logic / CPU AIロジック
├── multiplayer_gui.py  # 4-player GUI / 4人対戦GUI
├── gui.py              # Single-player GUI / 1人用GUI
├── settings.py         # Settings management / 設定管理
├── requirements.txt    # Dependencies / 依存関係
└── assets/            # Tile images / 牌画像
    ├── wan/           # 萬子
    ├── pin/           # 筒子
    ├── sou/           # 索子
    └── honor/         # 字牌
```

### Key Components / 主要コンポーネント

- **MultiPlayerGameState**: Manages 4-player game state / 4人対戦のゲーム状態管理
- **GameController**: Handles turn progression and CPU automation / ターン進行とCPU自動化を処理
- **CPUPlayer**: AI logic for computer opponents / CPU対戦相手のAIロジック
- **Settings**: Persistent storage for custom configurations / カスタム設定の永続化

## 🛠️ Development / 開発

### Running in Development Mode / 開発モードでの実行

```bash
# Enable debug logging
python app.py

# The application will print turn information to console
# アプリケーションはターン情報をコンソールに出力します
```

### Contributing / 貢献

1. Fork the repository / リポジトリをフォーク
2. Create a feature branch / フィーチャーブランチを作成
3. Make your changes / 変更を行う
4. Add tests if applicable / 該当する場合はテストを追加
5. Submit a pull request / プルリクエストを送信

### Future Enhancements / 今後の機能拡張

- [ ] Network multiplayer support / ネットワーク対戦対応
- [ ] Advanced AI strategies / 高度なAI戦略  
- [ ] Sound effects / サウンドエフェクト
- [ ] Game statistics / ゲーム統計
- [ ] Tournament mode / トーナメントモード

## 🐛 Known Issues / 既知の問題

- Custom images require restart for some changes / カスタム画像の一部変更には再起動が必要
- Large image files may affect performance / 大きな画像ファイルはパフォーマンスに影響する場合があります

## 📝 License / ライセンス

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

このプロジェクトは MIT ライセンスの下でライセンスされています - 詳細は [LICENSE](LICENSE) ファイルをご覧ください。

## 🙏 Acknowledgments / 謝辞

- Built with Python's tkinter GUI framework / Python の tkinter GUI フレームワークで構築
- Image processing powered by Pillow / 画像処理は Pillow を使用
- Inspired by traditional Mahjong gameplay / 伝統的な麻雀のゲームプレイからインスピレーションを得ています

---

**Note**: This is a recreational project for learning purposes. It is not affiliated with any commercial Mahjong products.

**注意**: これは学習目的のレクリエーションプロジェクトです。商用の麻雀製品とは関係ありません。