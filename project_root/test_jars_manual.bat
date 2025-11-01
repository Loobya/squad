@echo off
echo Fixing JAR creation with proper packaging...

set JAVA_HOME=C:\Java\jdk-25
set PATH=%JAVA_HOME%\bin;%PATH%

cd java_app

echo.
echo Step 1: Cleaning previous builds...
if exist "*.class" del "*.class"
if exist "utils\*.class" del "utils\*.class"
if exist "build\*.jar" del "build\*.jar"

echo.
echo Step 2: Creating proper directory structure for packages...
if exist "classes" rmdir /s /q "classes"
mkdir classes
mkdir classes\utils

echo.
echo Step 3: Compiling with proper output directory...
javac --module-path "C:\Users\Asus\Desktop\javafx\javafx-sdk-25\lib" --add-modules javafx.controls -d classes *.java utils/*.java

if %errorlevel% neq 0 (
    echo ERROR: Compilation failed!
    pause
    exit /b 1
)

echo.
echo Step 4: Creating JAR files with proper classpath...
cd classes

echo Creating ScenarioEditor JAR...
jar cfe ..\build\scenario_editor.jar ScenarioEditor *.class utils/*.class

echo Creating ScenarioPlayer JAR...
jar cfe ..\build\scenario_player.jar ScenarioPlayer *.class utils/*.class

cd ..

echo.
echo Step 5: Verifying JAR contents...
echo ScenarioEditor JAR contents:
jar tf build\scenario_editor.jar | findstr JSONHandler

echo ScenarioPlayer JAR contents:
jar tf build\scenario_player.jar | findstr JSONHandler

cd ..
echo.
echo JAR creation completed!
pause