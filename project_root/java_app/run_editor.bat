@echo off
setlocal

set "JAVA_FX_PATH=C:\Users\Asus\Desktop\javafx\javafx-sdk-25\lib"

echo Starting Scenario Editor...
java -jar --module-path "%JAVA_FX_PATH%" --add-modules javafx.controls,javafx.graphics build\scenario_editor.jar

pause