@echo off
echo Checking Python and Java environment...

echo.
echo Python environment:
python --version
where python

echo.
echo Java environment:
java -version
where java

echo.
echo JavaFX check:
if exist "C:\Users\Asus\Desktop\javafx\javafx-sdk-25\lib" (
    echo JavaFX found
) else (
    echo JavaFX NOT found
)

echo.
echo JAR files check:
if exist "java_app\build\scenario_editor.jar" (
    echo scenario_editor.jar found
) else (
    echo scenario_editor.jar NOT found
)

if exist "java_app\build\scenario_player.jar" (
    echo scenario_player.jar found
) else (
    echo scenario_player.jar NOT found
)

pause