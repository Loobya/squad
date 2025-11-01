import subprocess
import os
import sys
import json
import threading
from typing import Optional

class ProcessLauncher:
    def __init__(self, java_app_path: str):
        self.java_app_path = java_app_path
        self.javafx_path = "C:\\Users\\Asus\\Desktop\\javafx\\javafx-sdk-25\\lib"
        print(f"🔧 ProcessLauncher initialized:")
        print(f"   Java app path: {java_app_path}")
        print(f"   JavaFX path: {self.javafx_path}")
        
        # Verify paths exist
        self.verify_paths()
        
    def verify_paths(self):
        """Verify all required paths exist"""
        print("\n🔍 Verifying paths...")
        
        # Check Java
        try:
            result = subprocess.run(["java", "-version"], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print("✅ Java is accessible")
            else:
                print("❌ Java not found in PATH")
        except Exception as e:
            print(f"❌ Java check failed: {e}")
        
        # Check JavaFX
        if os.path.exists(self.javafx_path):
            print(f"✅ JavaFX found: {self.javafx_path}")
        else:
            print(f"❌ JavaFX not found: {self.javafx_path}")
        
        # Check JAR files
        editor_jar = os.path.join(self.java_app_path, "build", "scenario_editor.jar")
        player_jar = os.path.join(self.java_app_path, "build", "scenario_player.jar")
        
        if os.path.exists(editor_jar):
            print(f"✅ Scenario Editor JAR found: {editor_jar}")
        else:
            print(f"❌ Scenario Editor JAR not found: {editor_jar}")
            print(f"   Build directory contents: {os.listdir(os.path.join(self.java_app_path, 'build')) if os.path.exists(os.path.join(self.java_app_path, 'build')) else 'Build directory not found'}")
        
        if os.path.exists(player_jar):
            print(f"✅ Scenario Player JAR found: {player_jar}")
        else:
            print(f"❌ Scenario Player JAR not found: {player_jar}")
    
    def launch_scenario_editor(self, scenario_file: Optional[str] = None) -> bool:
        """Launch JavaFX Scenario Editor with comprehensive debugging"""
        try:
            print("\n🚀 LAUNCHING SCENARIO EDITOR ==================================")
            
            editor_jar = os.path.join(self.java_app_path, "build", "scenario_editor.jar")
            print(f"📦 JAR path: {editor_jar}")
            
            if not os.path.exists(editor_jar):
                print(f"❌ CRITICAL: JAR file not found!")
                return False
            
            # Build the command
            cmd = [
                "java",
                "--module-path", self.javafx_path,
                "--add-modules", "javafx.controls,javafx.fxml,javafx.graphics",
                "-jar", editor_jar
            ]
            
            if scenario_file:
                if os.path.exists(scenario_file):
                    cmd.append(os.path.abspath(scenario_file))
                    print(f"📁 Loading scenario: {scenario_file}")
                else:
                    print(f"⚠️  Scenario file not found, creating new: {scenario_file}")
            
            print(f"🖥️  Full command: {' '.join(cmd)}")
            
            # Create a thread to capture output
            def capture_output(process):
                stdout, stderr = process.communicate()
                if stdout:
                    print(f"📤 STDOUT: {stdout.decode('utf-8', errors='ignore')}")
                if stderr:
                    print(f"📥 STDERR: {stderr.decode('utf-8', errors='ignore')}")
            
            # Launch the process
            print("🎬 Starting Java process...")
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False  # Changed to False for better error handling
            )
            
            # Start output capture in a separate thread
            output_thread = threading.Thread(target=capture_output, args=(process,))
            output_thread.daemon = True
            output_thread.start()
            
            # Check if process started successfully
            import time
            time.sleep(2)  # Give it a moment to start
            
            if process.poll() is None:
                print("✅ Java process is running!")
                return True
            else:
                print("❌ Java process terminated immediately!")
                return False
                
        except Exception as e:
            print(f"💥 EXCEPTION: {e}")
            import traceback
            traceback.print_exc()
            return False

    def launch_scenario_player(self, scenario_file: str, mode: str) -> bool:
        """Launch JavaFX Scenario Player"""
        try:
            print(f"\n🎮 LAUNCHING SCENARIO PLAYER ({mode}) ===========================")
            
            player_jar = os.path.join(self.java_app_path, "build", "scenario_player.jar")
            print(f"📦 JAR path: {player_jar}")
            
            if not os.path.exists(player_jar):
                print(f"❌ Player JAR not found!")
                return False
            
            if not os.path.exists(scenario_file):
                print(f"❌ Scenario file not found: {scenario_file}")
                return False
            
            # Build the command
            cmd = [
                "java",
                "--module-path", self.javafx_path,
                "--add-modules", "javafx.controls,javafx.fxml,javafx.graphics,javafx.media",
                "-jar", player_jar,
                os.path.abspath(scenario_file),
                mode
            ]
                
            print(f"🖥️  Full command: {' '.join(cmd)}")
            
            # Launch the process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False
            )
            
            # Capture output in thread
            def capture_output(process):
                stdout, stderr = process.communicate()
                if stdout:
                    print(f"📤 PLAYER STDOUT: {stdout.decode('utf-8', errors='ignore')}")
                if stderr:
                    print(f"📥 PLAYER STDERR: {stderr.decode('utf-8', errors='ignore')}")
            
            output_thread = threading.Thread(target=capture_output, args=(process,))
            output_thread.daemon = True
            output_thread.start()
            
            import time
            time.sleep(2)
            
            if process.poll() is None:
                print("✅ Player process is running!")
                return True
            else:
                print("❌ Player process terminated immediately!")
                return False
                
        except Exception as e:
            print(f"💥 PLAYER EXCEPTION: {e}")
            import traceback
            traceback.print_exc()
            return False

    def get_scenario_result(self, temp_result_path: str) -> Optional[dict]:
        """Read temporary result file created by Java player"""
        try:
            if os.path.exists(temp_result_path):
                with open(temp_result_path, 'r', encoding='utf-8') as f:
                    result = json.load(f)
                os.remove(temp_result_path)
                print(f"📊 Scenario result: {result}")
                return result
            return None
        except Exception as e:
            print(f"❌ Error reading result: {e}")
            return None