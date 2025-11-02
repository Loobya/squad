@echo off
echo Cleaning and rebuilding Java applications...

set JAVA_HOME=C:\Java\jdk-25
set PATH=%JAVA_HOME%\bin;%PATH%

echo.
echo Step 1: Cleaning previous builds...
cd java_app

if exist "*.class" del "*.class"
if exist "utils\*.class" del "utils\*.class"
if exist "build\*.jar" (
    echo Deleting old JAR files...
    del "build\*.jar"
)

echo.
echo Step 2: Compiling all Java files together...
javac --module-path "C:\Users\Asus\Desktop\javafx\javafx-sdk-25\lib" --add-modules javafx.controls *.java utils/*.java
if %errorlevel% neq 0 (
    echo ERROR: Compilation failed!
    pause
    exit /b 1
)

echo.
echo Step 3: Creating JAR files...
jar cfe build/scenario_editor.jar ScenarioEditor *.class utils/*.class
if %errorlevel% neq 0 (
    echo ERROR: Failed to create scenario_editor.jar
    pause
    exit /b 1
)

jar cfe build/scenario_player.jar ScenarioPlayer *.class utils/*.class
if %errorlevel% neq 0 (
    echo ERROR: Failed to create scenario_player.jar
    pause
    exit /b 1
)

cd ..
echo.
echo SUCCESS: All Java applications built successfully!
echo.
echo JAR files created:
dir java_app\build\*.jar
echo.
pause