@echo off
echo Ultimate fix - moving everything to one directory...

set JAVA_HOME=C:\Java\jdk-25
set PATH=%JAVA_HOME%\bin;%PATH%

cd java_app

echo.
echo Step 1: Clean everything...
if exist "*.class" del "*.class"
if exist "utils\*.class" del "utils\*.class"
if exist "build" rmdir /s /q "build"
mkdir build

echo.
echo Step 2: Move JSONHandler to main directory...
copy utils\JSONHandler.java JSONHandler.java

echo.
echo Step 3: Compile everything in one directory...
javac --module-path "C:\Users\Asus\Desktop\javafx\javafx-sdk-25\lib" --add-modules javafx.controls *.java

if %errorlevel% neq 0 (
    echo ERROR: Compilation failed!
    goto cleanup
)

echo.
echo Step 4: Create JAR files...
jar cfe build/scenario_editor.jar ScenarioEditor *.class
jar cfe build/scenario_player.jar ScenarioPlayer *.class

echo.
echo Step 5: Verify JAR creation...
if exist "build\scenario_editor.jar" (
    echo ✓ scenario_editor.jar: %%~zF bytes
) else (
    echo ✗ scenario_editor.jar failed
)

if exist "build\scenario_player.jar" (
    echo ✓ scenario_player.jar: %%~zF bytes
) else (
    echo ✗ scenario_player.jar failed
)

echo.
echo Step 6: List JAR contents...
echo ScenarioEditor contents:
jar tf build\scenario_editor.jar | findstr -i "jsonhandler\|scenario"

echo.
echo ScenarioPlayer contents:
jar tf build\scenario_player.jar | findstr -i "jsonhandler\|scenario"

:cleanup
echo.
echo Step 7: Cleanup - moving JSONHandler back...
if exist "JSONHandler.java" move JSONHandler.java utils\JSONHandler.java
if exist "JSONHandler.class" del JSONHandler.class

cd ..
echo.
echo Process completed!
pause