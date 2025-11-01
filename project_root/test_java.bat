@echo off
echo Final Test with Your Exact Paths

set JAVAFX_PATH=C:\Users\Asus\Desktop\javafx\javafx-sdk-25\lib
set JAVA_EXE=C:\Java\jdk-25\bin\java.exe

echo.
echo Java Path: %JAVA_EXE%
echo JavaFX Path: %JAVAFX_PATH%
echo.

echo 1. Testing Java...
"%JAVA_EXE%" -version
if %errorlevel% neq 0 (
    echo ERROR: Java test failed!
    pause
    exit /b 1
)

echo.
echo 2. Testing JavaFX...
if not exist "%JAVAFX_PATH%" (
    echo ERROR: JavaFX path not found!
    pause
    exit /b 1
)
dir "%JAVAFX_PATH%\*.jar" | find "javafx" >nul
if %errorlevel% neq 0 (
    echo ERROR: JavaFX JAR files not found!
    pause
    exit /b 1
)
echo JavaFX JAR files found.

echo.
echo 3. Testing JAR files...
if not exist "java_app\build\scenario_editor.jar" (
    echo ERROR: scenario_editor.jar not found!
    echo Please build the Java applications first.
    pause
    exit /b 1
)
if not exist "java_app\build\scenario_player.jar" (
    echo ERROR: scenario_player.jar not found!
    echo Please build the Java applications first.
    pause
    exit /b 1
)
echo JAR files found.

echo.
echo 4. Testing Scenario Editor (will open window)...
echo Starting Scenario Editor...
"%JAVA_EXE%" --module-path="%JAVAFX_PATH%" --add-modules=javafx.controls,javafx.fxml -jar java_app\build\scenario_editor.jar
echo Scenario Editor test completed.

echo.
echo 5. Testing Scenario Player (will open window)...
echo Starting Scenario Player...
"%JAVA_EXE%" --module-path="%JAVAFX_PATH%" --add-modules=javafx.controls,javafx.fxml -jar java_app\build\scenario_player.jar python_app\data\scenarios\scenario_01.json practice
echo Scenario Player test completed.

echo.
echo ====================================
echo   ALL TESTS COMPLETED!
echo ====================================
echo If both Java applications opened windows successfully,
echo then they should work from the Python application.
pause