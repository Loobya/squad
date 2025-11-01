@echo off
setlocal enabledelayedexpansion

echo JavaFX Scenario Applications - Build Script
echo ===========================================

:: Find Java installation
set "JAVA_HOME="
for /f "tokens=*" %%i in ('java -XshowSettings:properties 2^>^&1 ^| find "java.home"') do (
    set "JAVA_HOME_LINE=%%i"
    set "JAVA_HOME=!JAVA_HOME_LINE:*java.home =!"
)
if "%JAVA_HOME%"=="" (
    echo ❌ ERROR: Java not found. Please install Java JDK first.
    pause
    exit /b 1
)

echo Found Java at: %JAVA_HOME%
set "JAVA_BIN=%JAVA_HOME%\bin"

:: Set paths
set "JAVA_FX_PATH=C:\Users\Asus\Desktop\javafx\javafx-sdk-25\lib"
set "JACKSON_LIBS=libs"

echo.
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "classes" rmdir /s /q "classes"

echo Creating directories...
mkdir classes 2>nul
mkdir build 2>nul
mkdir build\libs 2>nul

echo.
echo Compiling Java files...
"%JAVA_BIN%\javac" -cp "%JAVA_FX_PATH%\*;%JACKSON_LIBS%\*" ^
      --module-path "%JAVA_FX_PATH%" ^
      --add-modules javafx.controls,javafx.fxml,javafx.graphics ^
      -d classes ^
      models\*.java ^
      utils\*.java ^
      ScenarioPlayer.java ^
      ScenarioEditor.java

if !ERRORLEVEL! NEQ 0 (
    echo.
    echo ❌ Compilation failed!
    pause
    exit /b 1
)

echo.
echo Creating JAR files...

:: Create manifest files
echo Creating manifest files...
echo Manifest-Version: 1.0 > manifest_player.txt
echo Main-Class: ScenarioPlayer >> manifest_player.txt
echo Class-Path: libs/jackson-core-2.15.2.jar libs/jackson-databind-2.15.2.jar libs/jackson-annotations-2.15.2.jar >> manifest_player.txt

echo Manifest-Version: 1.0 > manifest_editor.txt
echo Main-Class: ScenarioEditor >> manifest_editor.txt
echo Class-Path: libs/jackson-core-2.15.2.jar libs/jackson-databind-2.15.2.jar libs/jackson-annotations-2.15.2.jar >> manifest_editor.txt

cd classes

echo Creating scenario_player.jar...
"%JAVA_BIN%\jar" cfm ..\build\scenario_player.jar ..\manifest_player.txt *.class models utils

echo Creating scenario_editor.jar...
"%JAVA_BIN%\jar" cfm ..\build\scenario_editor.jar ..\manifest_editor.txt *.class models utils

cd ..

echo Copying dependencies...
xcopy %JACKSON_LIBS%\* build\libs\ /Y >nul

:: Clean up manifest files
del manifest_player.txt 2>nul
del manifest_editor.txt 2>nul

echo.
echo ✅ Build completed successfully!
echo.
echo 📁 Built files location: build\
echo 📦 scenario_player.jar - Run this to play scenarios
echo 📦 scenario_editor.jar - Run this to edit/create scenarios
echo 📚 libs/ - Jackson JSON libraries
echo.
echo Java found at: %JAVA_HOME%
echo.
pause