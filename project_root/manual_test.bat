@echo off
echo ========================================
echo Tactical Training System - Manual Test
echo ========================================

echo.
echo Step 1: Checking Python dependencies...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Step 2: Setting up Java paths...
set JAVA_HOME=C:\Java\jdk-25
set PATH=%JAVA_HOME%\bin;%PATH%

echo Java Home: %JAVA_HOME%
echo.

echo Step 3: Checking Java installation...
java -version
if %errorlevel% neq 0 (
    echo ERROR: Java is not installed or not accessible at C:\Java\jdk-25
    pause
    exit /b 1
)

echo.
echo Step 4: Creating test directories...
if not exist "python_app\data\scenarios" mkdir "python_app\data\scenarios"
if not exist "java_app\build" mkdir "java_app\build"

echo.
echo Step 5: Creating test scenario...
echo Creating test scenario file...

set SCENARIO_FILE=python_app\data\scenarios\test_scenario.json

(
echo {
echo   "title": "Test Scenario - سيناريو اختبار",
echo   "background": "test_map.jpg",
echo   "teams": [
echo     {
echo       "color": "red",
echo       "squads": [
echo         {
echo           "move_1": [{"x": 100, "y": 100, "order": 1}],
echo           "move_2": [{"x": 200, "y": 200, "order": 1}],
echo           "move_3": [{"x": 300, "y": 300, "order": 1}]
echo         }
echo       ],
echo       "right_move": 0,
echo       "explanations": {
echo         "right": "This is the correct move explanation",
echo         "wrong_1": "This is the first wrong move explanation",
echo         "wrong_2": "This is the second wrong move explanation"
echo       }
echo     }
echo   ],
echo   "created_by": "admin",
echo   "date": "2024-01-10"
echo }
) > "%SCENARIO_FILE%"

echo Test scenario created: %SCENARIO_FILE%

echo.
echo Step 6: Compiling Java applications...
cd java_app

echo Compiling JSONHandler...
javac --module-path "C:\Users\Asus\Desktop\javafx\javafx-sdk-25\lib" --add-modules javafx.controls utils/JSONHandler.java

echo Compiling ScenarioEditor...
javac --module-path "C:\Users\Asus\Desktop\javafx\javafx-sdk-25\lib" --add-modules javafx.controls ScenarioEditor.java

echo Compiling ScenarioPlayer...
javac --module-path "C:\Users\Asus\Desktop\javafx\javafx-sdk-25\lib" --add-modules javafx.controls ScenarioPlayer.java

if %errorlevel% neq 0 (
    echo ERROR: Java compilation failed!
    cd ..
    pause
    exit /b 1
)

echo.
echo Step 7: Creating JAR files...
echo Creating ScenarioEditor JAR...
jar cfe build/scenario_editor.jar ScenarioEditor *.class utils/*.class

echo Creating ScenarioPlayer JAR...
jar cfe build/scenario_player.jar ScenarioPlayer *.class utils/*.class

cd ..

echo.
echo Step 8: Testing Python application...
echo Starting Python main application...
cd python_app
start python main.py
cd ..

echo.
echo Step 9: Testing Java applications...
echo You can now test:
echo 1. Python main application (should be running)
echo 2. Scenario Editor: Use test_scenario_editor.bat
echo 3. Scenario Player: Use test_scenario_player.bat

echo.
echo ========================================
echo Manual Test Completed!
echo ========================================
echo.
pause