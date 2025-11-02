@echo off
echo Testing fixed JAR files...

set JAVA_HOME=C:\Java\jdk-25
set PATH=%JAVA_HOME%\bin;%PATH%

set JAVAFX_PATH=C:\Users\Asus\Desktop\javafx\javafx-sdk-25\lib

echo.
echo Testing ScenarioEditor JAR...
java --module-path "%JAVAFX_PATH%" --add-modules javafx.controls,javafx.fxml -jar java_app\build\scenario_editor.jar

if %errorlevel% neq 0 (
    echo.
    echo ERROR: ScenarioEditor failed to start
) else (
    echo.
    echo SUCCESS: ScenarioEditor started!
)

echo.
pause