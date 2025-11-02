@echo off
echo Verifying Java Build...

set JAVA_EXE=C:\Program Files\Java\jdk-25\bin\java.exe
set JAVAFX_PATH=C:\Users\Asus\Desktop\javafx\javafx-sdk-25\lib

echo.
echo Checking JAR files:
dir java_app\build\*.jar

echo.
echo Testing JAR file integrity:
"%JAVA_EXE%" -jar java_app\build\scenario_editor.jar --version 2>nul
if %errorlevel% equ 0 (
    echo scenario_editor.jar: OK
) else (
    echo scenario_editor.jar: MAY BE CORRUPT
)

"%JAVA_EXE%" -jar java_app\build\scenario_player.jar --version 2>nul
if %errorlevel% equ 0 (
    echo scenario_player.jar: OK
) else (
    echo scenario_player.jar: MAY BE CORRUPT
)

echo.
echo Build verification complete!
pause