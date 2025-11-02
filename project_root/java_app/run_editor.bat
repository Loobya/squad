@echo off
echo ========================================
echo Enhanced Scenario Editor - Setup
echo ========================================

echo.
echo Step 1: Creating directory structure...

REM Create Python assets directories
if not exist "python_app\assets\logos" mkdir "python_app\assets\logos"
if not exist "python_app\assets\squad_markers" mkdir "python_app\assets\squad_markers"
if not exist "python_app\assets\backgrounds" mkdir "python_app\assets\backgrounds"

echo ✓ Created assets directories

echo.
echo Step 2: Creating sample assets...

REM Note: You'll need to add actual image files manually
echo Created:
echo   - python_app\assets\logos\ (for decorative icons)
echo   - python_app\assets\squad_markers\ (for unit symbols)
echo   - python_app\assets\backgrounds\ (for map images)

echo.
echo Step 3: Checking Java models...

if not exist "models\PlacedLogo.java" (
    echo ⚠️  WARNING: PlacedLogo.java not found
    echo    You need to create this model class
)

if not exist "models\TextAnnotation.java" (
    echo ⚠️  WARNING: TextAnnotation.java not found
    echo    You need to create this model class
)

echo.
echo Step 4: Checking Python files...

if not exist "..\python_app\windows\assets_manager.py" (
    echo ⚠️  WARNING: assets_manager.py not found
    echo    You need to create this file
) else (
    echo ✓ assets_manager.py found
)

echo.
echo Step 5: Building Java application...
echo.

cd java_app

if exist build.bat (
    echo Running build.bat...
    call build.bat
) else (
    echo ⚠️  WARNING: build.bat not found
    echo    Using manual compilation...
    
    if not exist "build" mkdir "build"
    
    echo Compiling Java files...
    javac --module-path "C:\Users\Asus\Desktop\javafx\javafx-sdk-25\lib" ^
          --add-modules javafx.controls ^
          -d classes ^
          models\*.java ^
          utils\*.java ^
          ScenarioEditor.java ^
          ScenarioPlayer.java
    
    if %errorlevel% neq 0 (
        echo ❌ Compilation failed!
        cd ..
        pause
        exit /b 1
    )
    
    echo Creating JAR files...
    cd classes
    jar cfe ..\build\scenario_editor.jar ScenarioEditor *
    jar cfe ..\build\scenario_player.jar ScenarioPlayer *
    cd ..
)

cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Add sample images to python_app\assets\logos\
echo 2. Add squad marker icons to python_app\assets\squad_markers\
echo 3. Add map backgrounds to python_app\assets\backgrounds\
echo.
echo To upload assets:
echo   - Run: python python_app\main.py
echo   - Login as admin (default: 1234)
echo   - Go to "Assets" tab
echo   - Upload logos and markers
echo.
echo To create scenarios:
echo   - Click "Add New Scenario"
echo   - Load a background image
echo   - Use the drawing tools
echo   - Add squads and write explanations
echo   - Save your scenario
echo.
echo Sample images to download:
echo   - Military logos: https://www.flaticon.com/packs/military
echo   - Squad markers: NATO military symbols
echo   - Map backgrounds: Topographic or tactical maps
echo.
pause