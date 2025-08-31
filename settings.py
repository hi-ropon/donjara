import json
import os
from typing import Dict, Optional
from tile import TileType

class Settings:
    def __init__(self, settings_file="settings.json"):
        self.settings_file = settings_file
        self.custom_images = {}
        self.load_settings()
    
    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.custom_images = data.get('custom_images', {})
            except (json.JSONDecodeError, FileNotFoundError):
                self.custom_images = {}
    
    def save_settings(self):
        data = {
            'custom_images': self.custom_images
        }
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"設定の保存に失敗しました: {e}")
    
    def set_custom_image(self, tile_type: TileType, number: int, image_path: str):
        key = f"{tile_type.value}_{number}"
        if os.path.exists(image_path):
            self.custom_images[key] = image_path
            self.save_settings()
            return True
        return False
    
    def get_custom_image(self, tile_type: TileType, number: int) -> Optional[str]:
        key = f"{tile_type.value}_{number}"
        return self.custom_images.get(key)
    
    def remove_custom_image(self, tile_type: TileType, number: int):
        key = f"{tile_type.value}_{number}"
        if key in self.custom_images:
            del self.custom_images[key]
            self.save_settings()
    
    def clear_all_custom_images(self):
        self.custom_images = {}
        self.save_settings()
    
    def get_all_custom_images(self) -> Dict[str, str]:
        return self.custom_images.copy()
    
    def has_custom_image(self, tile_type: TileType, number: int) -> bool:
        key = f"{tile_type.value}_{number}"
        return key in self.custom_images