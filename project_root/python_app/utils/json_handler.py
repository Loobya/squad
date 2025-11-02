import json
import os
from typing import Any, Dict, List, Optional

class JSONHandler:
    @staticmethod
    def read_json(file_path: str) -> Any:
        """Read JSON file and return data"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            if not os.path.exists(file_path):
                # Create file with empty data if it doesn't exist
                if "config" in file_path:
                    default_data = {"admin_password": "1234", "language": "ar", "theme": "dark"}
                elif "history" in file_path:
                    default_data = []
                elif "courses" in file_path:
                    default_data = []
                else:
                    default_data = {}
                
                JSONHandler.write_json(file_path, default_data)
                return default_data
            
            # Check if file is empty
            if os.path.getsize(file_path) == 0:
                print(f"File is empty, creating default: {file_path}")
                if "config" in file_path:
                    default_data = {"admin_password": "1234", "language": "ar", "theme": "dark"}
                elif "history" in file_path:
                    default_data = []
                elif "courses" in file_path:
                    default_data = []
                else:
                    default_data = {}
                JSONHandler.write_json(file_path, default_data)
                return default_data
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    # File exists but is empty
                    print(f"File is empty: {file_path}")
                    if "history" in file_path:
                        default_data = []
                        JSONHandler.write_json(file_path, default_data)
                        return default_data
                    return None
                
                return json.loads(content)
                
        except json.JSONDecodeError as e:
            print(f"JSON decode error in {file_path}: {e}")
            # If it's history.json and corrupted, reset it
            if "history" in file_path:
                print("Resetting corrupted history.json")
                default_data = []
                JSONHandler.write_json(file_path, default_data)
                return default_data
            return None
        except Exception as e:
            print(f"Error reading JSON file {file_path}: {e}")
            return None

    @staticmethod
    def write_json(file_path: str, data: Any) -> bool:
        """Write data to JSON file"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error writing JSON file {file_path}: {e}")
            return False

    @staticmethod
    def update_json(file_path: str, updates: Dict[str, Any]) -> bool:
        """Update specific fields in JSON file"""
        try:
            data = JSONHandler.read_json(file_path)
            if data is None:
                return False
            
            data.update(updates)
            return JSONHandler.write_json(file_path, data)
        except Exception as e:
            print(f"Error updating JSON file {file_path}: {e}")
            return False