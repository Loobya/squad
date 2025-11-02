import subprocess
import os
import sys
import json
import threading
import time
from typing import Optional

class ProcessLauncher:
    def __init__(self, java_app_path: str):
        self.java_app_path = java_app_path
        self.javafx_path = "C:\\Users\\Asus\\Desktop\\javafx\\javafx-sdk-25\\lib"
        
        # Build libs path
        self.libs_path = os.path.join(java_app_path, "build", "libs")
        
        print(f"🔧 ProcessLauncher initialized:")
        print(f"   Java app path: {java_app_path}")
        print(f"   JavaFX path: {self.javafx_path}")
        print(f"   Libs path: {self.libs_path}")
        
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
            size = os.path.getsize(editor_jar)
            print(f"✅ Scenario Editor JAR found: {editor_jar} ({size} bytes)")
        else:
            print(f"❌ Scenario Editor JAR not found: {editor_jar}")
            
        if os.path.exists(player_jar):
            size = os.path.getsize(player_jar)
            print(f"✅ Scenario Player JAR found: {player_jar} ({size} bytes)")
        else:
            print(f"❌ Scenario Player JAR not found: {player_jar}")
        
        # Check Jackson libraries
        if os.path.exists(self.libs_path):
            libs = os.listdir(self.libs_path)
            if libs:
                print(f"✅ Libraries found: {', '.join(libs)}")
            else:
                print(f"⚠️ Libs folder exists but is empty")
        else:
            print(f"❌ Libs folder not found: {self.libs_path}")
    
    def build_classpath(self, jar_file: str) -> str:
        """Build complete classpath including JAR and libraries"""
        classpath_parts = [jar_file]
        
        # Add all JAR files from libs folder
        if os.path.exists(self.libs_path):
            for lib in os.listdir(self.libs_path):
                if lib.endswith('.jar'):
                    classpath_parts.append(os.path.join(self.libs_path, lib))
        
        # Use semicolon for Windows, colon for Unix
        separator = ';' if os.name == 'nt' else ':'
        return separator.join(classpath_parts)
    
    def launch_scenario_editor(self, scenario_file: Optional[str] = None) -> bool:
        """Launch JavaFX Scenario Editor with comprehensive debugging"""
        try:
            print("\n" + "="*70)
            print("🚀 LAUNCHING SCENARIO EDITOR")
            print("="*70)
            
            editor_jar = os.path.join(self.java_app_path, "build", "scenario_editor.jar")
            print(f"📦 JAR path: {editor_jar}")
            
            if not os.path.exists(editor_jar):
                print(f"❌ CRITICAL: JAR file not found!")
                print(f"   Expected location: {editor_jar}")
                print(f"   Please run the build script first!")
                return False
            
            # Build classpath
            classpath = self.build_classpath(editor_jar)
            print(f"📚 Classpath: {classpath}")
            
            # Build the command - CRITICAL: Use -cp instead of -jar when using classpath
            cmd = [
                "java",
                "-cp", classpath,
                "--module-path", self.javafx_path,
                "--add-modules", "javafx.controls,javafx.fxml,javafx.graphics",
                "ScenarioEditor"  # Main class name, NOT jar file
            ]
            
            if scenario_file:
                if os.path.exists(scenario_file):
                    cmd.append(os.path.abspath(scenario_file))
                    print(f"📁 Loading scenario: {scenario_file}")
                else:
                    print(f"⚠️ Scenario file not found: {scenario_file}")
            
            print(f"\n🖥️ Full command:")
            print(f"   {' '.join(cmd)}")
            print()
            
            # Launch the process
            print("🎬 Starting Java process...")
            
            # Use DETACHED_PROCESS on Windows to prevent console window
            if os.name == 'nt':
                CREATE_NO_WINDOW = 0x08000000
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=CREATE_NO_WINDOW
                )
            else:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            
            # Give it time to start
            time.sleep(3)
            
            # Check if process is still running
            poll_result = process.poll()
            
            if poll_result is None:
                print("✅ SUCCESS: Java process is running!")
                print(f"   Process ID: {process.pid}")
                
                # Start a thread to capture any output
                def monitor_output():
                    try:
                        stdout, stderr = process.communicate(timeout=5)
                        if stdout:
                            print(f"📤 Output: {stdout.decode('utf-8', errors='ignore')}")
                        if stderr:
                            stderr_text = stderr.decode('utf-8', errors='ignore')
                            # Only print if it's an actual error (not JavaFX warnings)
                            if 'error' in stderr_text.lower() or 'exception' in stderr_text.lower():
                                print(f"⚠️ Errors: {stderr_text}")
                    except subprocess.TimeoutExpired:
                        pass  # Process is still running, which is good
                
                monitor_thread = threading.Thread(target=monitor_output, daemon=True)
                monitor_thread.start()
                
                return True
            else:
                print(f"❌ FAILED: Process terminated immediately with code: {poll_result}")
                
                # Read any error output
                stdout, stderr = process.communicate()
                if stdout:
                    print(f"📤 Output: {stdout.decode('utf-8', errors='ignore')}")
                if stderr:
                    print(f"📥 Errors: {stderr.decode('utf-8', errors='ignore')}")
                
                return False
                
        except Exception as e:
            print(f"💥 EXCEPTION in launch_scenario_editor: {e}")
            import traceback
            traceback.print_exc()
            return False

    def launch_scenario_player(self, scenario_file: str, mode: str) -> bool:
        """Launch JavaFX Scenario Player"""
        try:
            print("\n" + "="*70)
            print(f"🎮 LAUNCHING SCENARIO PLAYER (mode: {mode})")
            print("="*70)
            
            player_jar = os.path.join(self.java_app_path, "build", "scenario_player.jar")
            print(f"📦 JAR path: {player_jar}")
            
            if not os.path.exists(player_jar):
                print(f"❌ Player JAR not found!")
                return False
            
            if not os.path.exists(scenario_file):
                print(f"❌ Scenario file not found: {scenario_file}")
                return False
            
            # Build classpath
            classpath = self.build_classpath(player_jar)
            print(f"📚 Classpath: {classpath}")
            
            # Build the command
            cmd = [
                "java",
                "-cp", classpath,
                "--module-path", self.javafx_path,
                "--add-modules", "javafx.controls,javafx.fxml,javafx.graphics",
                "ScenarioPlayer",  # Main class name
                os.path.abspath(scenario_file),
                mode
            ]
                
            print(f"\n🖥️ Full command:")
            print(f"   {' '.join(cmd)}")
            print()
            
            # Launch the process
            print("🎬 Starting Java process...")
            
            if os.name == 'nt':
                CREATE_NO_WINDOW = 0x08000000
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=CREATE_NO_WINDOW
                )
            else:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            
            time.sleep(3)
            
            poll_result = process.poll()
            
            if poll_result is None:
                print("✅ SUCCESS: Player process is running!")
                print(f"   Process ID: {process.pid}")
                return True
            else:
                print(f"❌ FAILED: Process terminated with code: {poll_result}")
                stdout, stderr = process.communicate()
                if stdout:
                    print(f"📤 Output: {stdout.decode('utf-8', errors='ignore')}")
                if stderr:
                    print(f"📥 Errors: {stderr.decode('utf-8', errors='ignore')}")
                return False
                
        except Exception as e:
            print(f"💥 EXCEPTION in launch_scenario_player: {e}")
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