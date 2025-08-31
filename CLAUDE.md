# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

ドンジャラ - 144枚の牌を使用した麻雀風ゲーム。Python (tkinter + PIL) で実装。4人対戦モード（人間1人 + CPU3人）をサポート。

## コマンド

### アプリケーション実行
```bash
python app.py
```

### 依存関係インストール
```bash
pip install -r requirements.txt
```

必要な外部ライブラリはPillow（PIL）のみ。Python 3.10以上、tkinter（標準ライブラリ）が必要。

## アーキテクチャ

### コアコンポーネント

**ゲームロジック層**
- `tile.py`: 144枚の麻雀牌を表現するTileクラスとTileType（萬子、筒子、索子、字牌）を定義
- `game_logic.py`: 4人プレイヤーのゲーム状態管理。`MultiPlayerGameState`と`Player`クラスでターン制御
- `game_controller.py`: ゲームフロー制御、CPUプレイヤーの自動実行（スレッド処理）、ターン遷移管理

**GUI層**  
- `multiplayer_gui.py`: 4人対戦モードのメインGUI。各プレイヤーエリア表示、牌レンダリング、ユーザー操作処理
- `gui.py`: 旧シングルプレイヤーGUI実装（現在未使用、参考用）

**AI システム**
- `cpu_player.py`: CPUプレイヤーのAIロジック実装（牌選択・捨て牌戦略）

**設定**
- `settings.py`: ゲーム設定定数

### 主要な設計パターン

1. **MVCパターン**: ゲームロジック（Model）、GUI（View）、コントローラー（Controller）の明確な分離

2. **CPUプレイヤーのスレッド処理**: UIブロッキング防止のため別スレッドで実行、コールバックで同期

3. **ターン制御**: 厳密なターン順序（0→1→2→3→0）と各遷移での状態検証

4. **牌管理**: 各牌は状態（手牌中、捨て牌済み）を保持、プレイヤーは手牌と捨て牌を個別管理

### アセット構造

牌画像は`assets/`配下のサブディレクトリに配置：
- `assets/wan/` - 萬子牌（1-9.png）
- `assets/pin/` - 筒子牌（1-9.png）  
- `assets/sou/` - 索子牌（1-9.png）
- `assets/honor/` - 字牌（1-7.png）

注：現在のアセットディレクトリ名（assetshonor、assetspin等）は修正が必要な可能性あり。

## 開発上の注意点

- 人間プレイヤーのターンで手牌13枚の場合、自動的にツモを実行
- 人間プレイヤーは14枚になったら手動で牌をクリックして捨てる必要がある
- CPUプレイヤーは設定可能な遅延で自動処理
- GUIはグリッドレイアウトで各プレイヤーの手牌、捨て牌、ゲーム状態を個別表示