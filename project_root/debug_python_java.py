import os
import sys
import time

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, "python_app", "utils"))

from python_app.utils.process_launcher import ProcessLauncher

def debug_java_launch():
    print("=== PYTHON TO JAVA DEBUG TEST ===")
    
    # Get absolute paths
    project_root = os.path.dirname(current_dir)
    java_app_path = os.path.join(project_root, "java_app")
    
    print(f"Project root: {project_root}")
    print(f"Java app path: {java_app_path}")
    
    # Create launcher
    launcher = ProcessLauncher(java_app_path)
    
    print("\n" + "="*50)
    print("TEST 1: Launching Scenario Editor")
    print("="*50)
    
    success = launcher.launch_scenario_editor()
    
    if success:
        print("🎉 SUCCESS: Scenario Editor was launched!")
        print("If you can't see the window, it might be behind other windows.")
    else:
        print("💥 FAILED: Scenario Editor failed to launch")
    
    # Wait a bit
    time.sleep(3)
    
    print("\n" + "="*50)
    print("TEST 2: Launching Scenario Player")
    print("="*50)
    
    # Test with a scenario file if it exists
    test_scenario = os.path.join(project_root, "python_app", "data", "scenarios", "test_scenario.json")
    if os.path.exists(test_scenario):
        success = launcher.launch_scenario_player(test_scenario, "practice")
        if success:
            print("🎉 SUCCESS: Scenario Player was launched!")
        else:
            print("💥 FAILED: Scenario Player failed to launch")
    else:
        print("⚠️  Test scenario not found, skipping player test")
        print(f"Expected at: {test_scenario}")
    
    print("\n" + "="*50)
    print("DEBUG COMPLETE")
    print("="*50)
    
    # Keep the script running to see any delayed output
    input("Press Enter to exit...")

if __name__ == "__main__":
    debug_java_launch()