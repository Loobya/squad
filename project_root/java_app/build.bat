@echo off
echo ====================================
echo COMPLETE BUILD FIX FOR JAVA APPS
echo ====================================

set JAVA_HOME=C:\Java\jdk-25
set PATH=%JAVA_HOME%\bin;%PATH%
set JAVAFX_PATH=C:\Users\Asus\Desktop\javafx\javafx-sdk-25\lib
set JACKSON_PATH=C:\Users\Asus\Desktop\tlili app\project_root\java_app\libs

echo.
echo Step 1: Verify Jackson libraries exist...
if not exist "%JACKSON_PATH%\jackson-core-2.15.2.jar" (
    echo ERROR: Jackson libraries not found in java_app\libs\
    echo Please download Jackson libraries and place them in java_app\libs\
    echo Required files:
    echo   - jackson-core-2.15.2.jar
    echo   - jackson-databind-2.15.2.jar
    echo   - jackson-annotations-2.15.2.jar
    pause
    exit /b 1
)
echo ✓ Jackson libraries found

echo.
echo Step 2: Clean previous builds...
cd java_app
if exist "build" rmdir /s /q "build"
if exist "classes" rmdir /s /q "classes"
mkdir build
mkdir classes

echo.
echo Step 3: Compile all Java files with proper classpath...
javac -cp ".;%JAVAFX_PATH%\*;%JACKSON_PATH%\*" ^
      --module-path "%JAVAFX_PATH%" ^
      --add-modules javafx.controls,javafx.fxml,javafx.graphics ^
      -d classes ^
      models\*.java ^
      utils\*.java ^
      ScenarioEditor.java ^
      ScenarioPlayer.java

if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Compilation failed!
    echo Please check if all model files exist in java_app\models\
    cd ..
    pause
    exit /b 1
)
echo ✓ Compilation successful

echo.
echo Step 4: Copy Jackson libraries to build folder...
if not exist "build\libs" mkdir "build\libs"
copy "%JACKSON_PATH%\*.jar" "build\libs\" >nul

echo.
echo Step 5: Create manifest files...
echo Manifest-Version: 1.0 > manifest_editor.txt
echo Main-Class: ScenarioEditor >> manifest_editor.txt
echo Class-Path: libs/jackson-core-2.15.2.jar libs/jackson-databind-2.15.2.jar libs/jackson-annotations-2.15.2.jar >> manifest_editor.txt

echo Manifest-Version: 1.0 > manifest_player.txt
echo Main-Class: ScenarioPlayer >> manifest_player.txt
echo Class-Path: libs/jackson-core-2.15.2.jar libs/jackson-databind-2.15.2.jar libs/jackson-annotations-2.15.2.jar >> manifest_player.txt

echo.
echo Step 6: Create JAR files with proper structure...
cd classes
jar cfm ..\build\scenario_editor.jar ..\manifest_editor.txt *
jar cfm ..\build\scenario_player.jar ..\manifest_player.txt *
cd ..

echo.
echo Step 7: Verify JAR files...
if exist "build\scenario_editor.jar" (
    echo ✓ scenario_editor.jar created
    jar tf build\scenario_editor.jar | findstr "ScenarioEditor.class" >nul
    if %errorlevel% equ 0 (
        echo   ✓ Main class found
    ) else (
        echo   ❌ Main class NOT found!
    )
) else (
    echo ❌ scenario_editor.jar NOT created!
)

if exist "build\scenario_player.jar" (
    echo ✓ scenario_player.jar created
    jar tf build\scenario_player.jar | findstr "ScenarioPlayer.class" >nul
    if %errorlevel% equ 0 (
        echo   ✓ Main class found
    ) else (
        echo   ❌ Main class NOT found!
    )
) else (
    echo ❌ scenario_player.jar NOT created!
)

echo.
echo Step 8: Test scenario_editor.jar...
echo Testing JAR integrity...
java -cp "build\scenario_editor.jar;build\libs\*" --module-path "%JAVAFX_PATH%" --add-modules javafx.controls ScenarioEditor --version 2>nul
if %errorlevel% equ 0 (
    echo ✓ scenario_editor.jar is valid
) else (
    echo ⚠ scenario_editor.jar test returned error (this may be normal if --version is not supported)
)

del manifest_editor.txt >nul 2>&1
del manifest_player.txt >nul 2>&1

cd ..

echo.
echo ====================================
echo BUILD COMPLETED!
echo ====================================
echo.
echo JAR files created in: java_app\build\
echo Libraries copied to: java_app\build\libs\
echo.
pause