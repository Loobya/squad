import models.Scenario;
import models.Team;
import models.Squad;
import models.MovePoint;
import models.Explanations;
import utils.JSONHandler;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.stage.Stage;
import javafx.stage.FileChooser;
import javafx.geometry.*;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Line;
import javafx.scene.input.MouseButton;
import javafx.scene.input.MouseEvent;
import java.io.File;
import java.io.IOException;
import java.util.List;

public class ScenarioEditor extends Application {
    private Scenario currentScenario;
    private Pane canvas;
    private JSONHandler jsonHandler;
    private Team selectedTeam;
    private Squad selectedSquad;
    private int selectedMoveIndex = -1;
    private boolean isSettingStartPosition = true;
    
    private static final double CANVAS_WIDTH = 800;
    private static final double CANVAS_HEIGHT = 600;
    
    @Override
    public void start(Stage primaryStage) {
        this.jsonHandler = new JSONHandler();
        
        // Get scenario path from parameters or show file chooser
        List<String> args = getParameters().getRaw();
        if (!args.isEmpty()) {
            loadScenario(args.get(0));
        } else {
            showFileChooser(primaryStage, true);
            return;
        }
        
        setupUI(primaryStage);
    }
    
    private void showFileChooser(Stage primaryStage, boolean isOpen) {
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle(isOpen ? "Open Scenario File" : "Save Scenario File");
        fileChooser.getExtensionFilters().add(
            new FileChooser.ExtensionFilter("JSON Files", "*.json")
        );
        
        // Set initial directory to python_app data scenarios
        File initialDir = new File("../python_app/data/scenarios");
        if (initialDir.exists()) {
            fileChooser.setInitialDirectory(initialDir);
        }
        
        File file;
        if (isOpen) {
            file = fileChooser.showOpenDialog(primaryStage);
            if (file != null) {
                loadScenario(file.getAbsolutePath());
                setupUI(primaryStage);
            } else {
                Platform.exit();
            }
        } else {
            file = fileChooser.showSaveDialog(primaryStage);
            if (file != null) {
                saveScenario(file.getAbsolutePath());
            }
        }
    }
    
    private void loadScenario(String filePath) {
        try {
            this.currentScenario = jsonHandler.loadScenario(filePath);
            System.out.println("Loaded scenario: " + currentScenario.getTitle());
        } catch (IOException e) {
            showErrorDialog("Error loading scenario", "Could not load scenario from: " + filePath);
            e.printStackTrace();
            createNewScenario(); // Fallback to new scenario
        }
    }
    
    private void createNewScenario() {
        currentScenario = new Scenario();
        currentScenario.setTitle("New Scenario");
        currentScenario.setBackground("default_map.png");
        currentScenario.setCreatedBy("editor");
        currentScenario.setDate(java.time.LocalDate.now().toString());
        
        // Create 3 teams with 3 squads each
        String[] colors = {"red", "blue", "green"};
        for (String color : colors) {
            Team team = new Team(color);
            team.setRightMove(0); // Default: first team is correct
            
            // Create explanations
            Explanations explanations = new Explanations();
            explanations.setRight("This team executed the movement correctly with proper coordination.");
            explanations.setWrong1("This team exposed themselves to enemy fire during movement.");
            explanations.setWrong2("This team failed to maintain proper formation and cover.");
            team.setExplanations(explanations);
            
            // Create 3 squads for each team
            for (int i = 0; i < 3; i++) {
                Squad squad = new Squad();
                
                // Create 3 move points for each squad
                for (int j = 0; j < 3; j++) {
                    // Default positions spread out
                    double baseX = 100 + (j * 200) + (i * 50);
                    double baseY = 100 + (i * 150);
                    MovePoint movePoint = new MovePoint(baseX, baseY);
                    squad.addMovePoint(movePoint);
                }
                
                team.addSquad(squad);
            }
            
            currentScenario.addTeam(team);
        }
        
        // Set first team as correct
        currentScenario.getTeams().get(0).setRightMove(1);
    }
    
    private void setupUI(Stage primaryStage) {
        primaryStage.setTitle("Scenario Editor - " + currentScenario.getTitle());
        
        BorderPane root = new BorderPane();
        
        // Top: Menu bar
        root.setTop(createMenuBar(primaryStage));
        
        // Left: Team and squad inspector
        root.setLeft(createInspectorPanel());
        
        // Center: Editing canvas
        canvas = new Pane();
        canvas.setPrefSize(CANVAS_WIDTH, CANVAS_HEIGHT);
        canvas.setStyle("-fx-background-color: #f0f0f0; -fx-border-color: #ccc; -fx-border-width: 1;");
        setupCanvasInteractions();
        root.setCenter(canvas);
        
        // Right: Properties panel
        root.setRight(createPropertiesPanel());
        
        Scene scene = new Scene(root, 1400, 800);
        primaryStage.setScene(scene);
        primaryStage.show();
        
        refreshCanvas();
    }
    
    private MenuBar createMenuBar(Stage primaryStage) {
        MenuBar menuBar = new MenuBar();
        
        // File menu
        Menu fileMenu = new Menu("File");
        MenuItem newItem = new MenuItem("New Scenario");
        MenuItem openItem = new MenuItem("Open Scenario");
        MenuItem saveItem = new MenuItem("Save Scenario");
        MenuItem saveAsItem = new MenuItem("Save As");
        MenuItem exitItem = new MenuItem("Exit");
        
        newItem.setOnAction(e -> {
            createNewScenario();
            refreshCanvas();
            refreshProperties();
        });
        
        openItem.setOnAction(e -> showFileChooser(primaryStage, true));
        saveItem.setOnAction(e -> saveScenario(null));
        saveAsItem.setOnAction(e -> showFileChooser(primaryStage, false));
        exitItem.setOnAction(e -> primaryStage.close());
        
        fileMenu.getItems().addAll(newItem, openItem, new SeparatorMenuItem(), saveItem, saveAsItem, new SeparatorMenuItem(), exitItem);
        
        // Edit menu
        Menu editMenu = new Menu("Edit");
        MenuItem setCorrectTeamItem = new MenuItem("Set as Correct Team");
        setCorrectTeamItem.setOnAction(e -> setCorrectTeam());
        
        editMenu.getItems().addAll(setCorrectTeamItem);
        
        menuBar.getMenus().addAll(fileMenu, editMenu);
        return menuBar;
    }
    
    private VBox createInspectorPanel() {
        VBox inspector = new VBox(10);
        inspector.setPadding(new Insets(10));
        inspector.setPrefWidth(300);
        inspector.setStyle("-fx-background-color: #f8f8f8; -fx-border-color: #ccc; -fx-border-width: 0 1 0 0;");
        
        Label titleLabel = new Label("Teams & Squads");
        titleLabel.setStyle("-fx-font-size: 14px; -fx-font-weight: bold;");
        inspector.getChildren().add(titleLabel);
        
        // Team selection
        ToggleGroup teamGroup = new ToggleGroup();
        for (Team team : currentScenario.getTeams()) {
            VBox teamBox = new VBox(5);
            teamBox.setStyle("-fx-border-color: #ddd; -fx-border-width: 1; -fx-padding: 8; -fx-background-color: white;");
            
            RadioButton teamRadio = new RadioButton("Team " + team.getColor().toUpperCase());
            teamRadio.setToggleGroup(teamGroup);
            teamRadio.setUserData(team);
            teamRadio.setSelected(team == selectedTeam);
            teamRadio.setOnAction(e -> {
                selectedTeam = (Team) teamRadio.getUserData();
                selectedSquad = null;
                selectedMoveIndex = -1;
                refreshCanvas();
                refreshProperties();
            });
            
            // Correct team indicator
            if (team.isCorrectTeam()) {
                Label correctLabel = new Label("✓ CORRECT TEAM");
                correctLabel.setStyle("-fx-font-size: 10px; -fx-text-fill: green; -fx-font-weight: bold;");
                teamBox.getChildren().add(correctLabel);
            }
            
            // Squad selection
            VBox squadsBox = new VBox(3);
            Label squadsLabel = new Label("Squads:");
            squadsLabel.setStyle("-fx-font-size: 11px; -fx-font-weight: bold;");
            squadsBox.getChildren().add(squadsLabel);
            
            ToggleGroup squadGroup = new ToggleGroup();
            int squadIndex = 1;
            for (Squad squad : team.getSquads()) {
                RadioButton squadRadio = new RadioButton("Squad " + squadIndex);
                squadRadio.setToggleGroup(squadGroup);
                squadRadio.setUserData(squad);
                squadRadio.setStyle("-fx-font-size: 11px;");
                squadRadio.setOnAction(e -> {
                    selectedSquad = (Squad) squadRadio.getUserData();
                    selectedMoveIndex = -1;
                    refreshCanvas();
                    refreshProperties();
                });
                squadsBox.getChildren().add(squadRadio);
                squadIndex++;
            }
            
            teamBox.getChildren().addAll(teamRadio, squadsBox);
            inspector.getChildren().add(teamBox);
        }
        
        return inspector;
    }
    
    private VBox createPropertiesPanel() {
        VBox properties = new VBox(15);
        properties.setPadding(new Insets(15));
        properties.setPrefWidth(350);
        properties.setStyle("-fx-background-color: #f8f8f8; -fx-border-color: #ccc; -fx-border-width: 0 0 0 1;");
        
        Label titleLabel = new Label("Properties");
        titleLabel.setStyle("-fx-font-size: 16px; -fx-font-weight: bold;");
        properties.getChildren().add(titleLabel);
        
        // Scenario properties
        VBox scenarioBox = new VBox(8);
        scenarioBox.setStyle("-fx-border-color: #ccc; -fx-border-width: 1; -fx-padding: 10; -fx-background-color: white;");
        Label scenarioLabel = new Label("Scenario Properties:");
        scenarioLabel.setStyle("-fx-font-weight: bold; -fx-font-size: 14px;");
        
        VBox scenarioNameBox = new VBox(3);
        Label scenarioNameLabel = new Label("Scenario Title:");
        TextField scenarioNameField = new TextField(currentScenario.getTitle());
        scenarioNameField.textProperty().addListener((obs, oldVal, newVal) -> {
            currentScenario.setTitle(newVal);
        });
        scenarioNameBox.getChildren().addAll(scenarioNameLabel, scenarioNameField);
        
        VBox backgroundBox = new VBox(3);
        Label backgroundLabel = new Label("Background Image:");
        TextField backgroundField = new TextField(currentScenario.getBackground());
        backgroundField.textProperty().addListener((obs, oldVal, newVal) -> {
            currentScenario.setBackground(newVal);
        });
        backgroundBox.getChildren().addAll(backgroundLabel, backgroundField);
        
        scenarioBox.getChildren().addAll(scenarioLabel, scenarioNameBox, backgroundBox);
        
        // Team properties
        VBox teamBox = new VBox(8);
        teamBox.setStyle("-fx-border-color: #ccc; -fx-border-width: 1; -fx-padding: 10; -fx-background-color: white;");
        Label teamLabel = new Label("Team Properties:");
        teamLabel.setStyle("-fx-font-weight: bold; -fx-font-size: 14px;");
        
        VBox teamColorBox = new VBox(3);
        Label teamColorLabel = new Label("Team Color:");
        TextField teamColorField = new TextField();
        teamColorField.setDisable(true);
        
        VBox correctTeamBox = new VBox(3);
        CheckBox correctTeamCheck = new CheckBox("This is the correct team");
        correctTeamCheck.setDisable(true);
        correctTeamCheck.setOnAction(e -> {
            if (selectedTeam != null && correctTeamCheck.isSelected()) {
                // Set all teams to not correct first
                for (Team team : currentScenario.getTeams()) {
                    team.setRightMove(0);
                }
                selectedTeam.setRightMove(1);
                refreshInspector();
            }
        });
        
        teamColorBox.getChildren().addAll(teamColorLabel, teamColorField);
        correctTeamBox.getChildren().add(correctTeamCheck);
        
        // Explanations
        VBox explanationsBox = new VBox(8);
        Label explanationsLabel = new Label("Explanations:");
        explanationsLabel.setStyle("-fx-font-weight: bold;");
        
        VBox rightExplanationBox = new VBox(3);
        Label rightExplanationLabel = new Label("Correct Reason:");
        TextArea rightExplanationArea = new TextArea();
        rightExplanationArea.setPrefRowCount(3);
        rightExplanationArea.setDisable(true);
        
        VBox wrong1ExplanationBox = new VBox(3);
        Label wrong1ExplanationLabel = new Label("Wrong Reason 1:");
        TextArea wrong1ExplanationArea = new TextArea();
        wrong1ExplanationArea.setPrefRowCount(2);
        wrong1ExplanationArea.setDisable(true);
        
        VBox wrong2ExplanationBox = new VBox(3);
        Label wrong2ExplanationLabel = new Label("Wrong Reason 2:");
        TextArea wrong2ExplanationArea = new TextArea();
        wrong2ExplanationArea.setPrefRowCount(2);
        wrong2ExplanationArea.setDisable(true);
        
        rightExplanationBox.getChildren().addAll(rightExplanationLabel, rightExplanationArea);
        wrong1ExplanationBox.getChildren().addAll(wrong1ExplanationLabel, wrong1ExplanationArea);
        wrong2ExplanationBox.getChildren().addAll(wrong2ExplanationLabel, wrong2ExplanationArea);
        
        explanationsBox.getChildren().addAll(explanationsLabel, rightExplanationBox, wrong1ExplanationBox, wrong2ExplanationBox);
        
        teamBox.getChildren().addAll(teamLabel, teamColorBox, correctTeamBox, explanationsBox);
        
        // Move Point properties
        VBox movePointBox = new VBox(8);
        movePointBox.setStyle("-fx-border-color: #ccc; -fx-border-width: 1; -fx-padding: 10; -fx-background-color: white;");
        Label movePointLabel = new Label("Move Point Properties:");
        movePointLabel.setStyle("-fx-font-weight: bold; -fx-font-size: 14px;");
        
        VBox coordinatesBox = new VBox(5);
        Label coordinatesLabel = new Label("Coordinates:");
        HBox xBox = new HBox(5);
        Label xLabel = new Label("X:");
        Label xValue = new Label("Not set");
        HBox yBox = new HBox(5);
        Label yLabel = new Label("Y:");
        Label yValue = new Label("Not set");
        
        xBox.getChildren().addAll(xLabel, xValue);
        yBox.getChildren().addAll(yLabel, yValue);
        coordinatesBox.getChildren().addAll(coordinatesLabel, xBox, yBox);
        
        VBox moveControlsBox = new VBox(5);
        Label moveControlsLabel = new Label("Move Point Controls:");
        Button setPositionBtn = new Button("Set Selected Move Point Position");
        setPositionBtn.setDisable(true);
        setPositionBtn.setOnAction(e -> {
            if (selectedSquad != null && selectedMoveIndex >= 0) {
                showInfoDialog("Set Position", 
                    "Click on the canvas to set position for Move " + (selectedMoveIndex + 1) + 
                    " of selected squad.\nCurrent selection: " + 
                    (selectedTeam != null ? "Team " + selectedTeam.getColor().toUpperCase() : "None") +
                    (selectedSquad != null ? ", Squad " + (currentScenario.getTeams().get(0).getSquads().indexOf(selectedSquad) + 1) : ""));
            }
        });
        
        moveControlsBox.getChildren().addAll(moveControlsLabel, setPositionBtn);
        movePointBox.getChildren().addAll(movePointLabel, coordinatesBox, moveControlsBox);
        
        properties.getChildren().addAll(scenarioBox, teamBox, movePointBox);
        
        // Store references for updates
        properties.getProperties().put("teamColorField", teamColorField);
        properties.getProperties().put("correctTeamCheck", correctTeamCheck);
        properties.getProperties().put("rightExplanationArea", rightExplanationArea);
        properties.getProperties().put("wrong1ExplanationArea", wrong1ExplanationArea);
        properties.getProperties().put("wrong2ExplanationArea", wrong2ExplanationArea);
        properties.getProperties().put("xValue", xValue);
        properties.getProperties().put("yValue", yValue);
        properties.getProperties().put("setPositionBtn", setPositionBtn);
        
        return properties;
    }
    
    private void setupCanvasInteractions() {
        canvas.setOnMouseClicked(e -> {
            if (e.getButton() == MouseButton.PRIMARY) {
                if (selectedSquad != null && selectedMoveIndex >= 0) {
                    // Update move point position
                    MovePoint movePoint = selectedSquad.getMovePoint(selectedMoveIndex);
                    if (movePoint != null) {
                        movePoint.setX(e.getX());
                        movePoint.setY(e.getY());
                        refreshCanvas();
                        refreshProperties();
                    }
                }
            }
        });
        
        // Add hover effect for move points
        canvas.setOnMouseMoved(e -> {
            boolean found = false;
            for (Team team : currentScenario.getTeams()) {
                Color teamColor = getColorFromString(team.getColor());
                int squadIndex = 0;
                for (Squad squad : team.getSquads()) {
                    List<MovePoint> moves = squad.getMovePoints();
                    for (int i = 0; i < moves.size(); i++) {
                        MovePoint point = moves.get(i);
                        double distance = Math.sqrt(Math.pow(e.getX() - point.getX(), 2) + Math.pow(e.getY() - point.getY(), 2));
                        if (distance < 10) { // Within 10 pixels
                            canvas.setStyle("-fx-cursor: hand; -fx-background-color: #f0f0f0; -fx-border-color: #ccc; -fx-border-width: 1;");
                            found = true;
                            // You could show a tooltip here with move point info
                            break;
                        }
                    }
                    if (found) break;
                    squadIndex++;
                }
                if (found) break;
            }
            if (!found) {
                canvas.setStyle("-fx-cursor: default; -fx-background-color: #f0f0f0; -fx-border-color: #ccc; -fx-border-width: 1;");
            }
        });
    }
    
    private void refreshCanvas() {
        canvas.getChildren().clear();
        
        // Draw movement paths and points
        for (Team team : currentScenario.getTeams()) {
            Color teamColor = getColorFromString(team.getColor());
            if (teamColor == null) teamColor = Color.GRAY;
            
            boolean isSelectedTeam = (team == selectedTeam);
            int squadIndex = 0;
            
            for (Squad squad : team.getSquads()) {
                boolean isSelectedSquad = (squad == selectedSquad);
                List<MovePoint> moves = squad.getMovePoints();
                
                // Draw movement lines
                for (int i = 0; i < moves.size() - 1; i++) {
                    MovePoint start = moves.get(i);
                    MovePoint end = moves.get(i + 1);
                    
                    Line movementLine = new Line(start.getX(), start.getY(), end.getX(), end.getY());
                    movementLine.setStroke(teamColor);
                    movementLine.setOpacity(isSelectedTeam ? 0.8 : 0.4);
                    movementLine.setStrokeWidth(isSelectedTeam ? 3 : 2);
                    if (isSelectedSquad) {
                        movementLine.getStrokeDashArray().clear();
                        movementLine.setStrokeWidth(4);
                    } else {
                        movementLine.getStrokeDashArray().addAll(5d, 5d);
                    }
                    
                    canvas.getChildren().add(movementLine);
                }
                
                // Draw move points
                for (int i = 0; i < moves.size(); i++) {
                    MovePoint point = moves.get(i);
                    boolean isSelectedMove = (isSelectedSquad && i == selectedMoveIndex);
                    
                    Circle pointCircle = new Circle(point.getX(), point.getY(), isSelectedMove ? 8 : 6, teamColor);
                    if (isSelectedMove) {
                        pointCircle.setStroke(Color.BLACK);
                        pointCircle.setStrokeWidth(2);
                    }
                    
                    // Add click handler for move points
                    final int moveIndex = i;
                    final Squad currentSquad = squad;
                    final Team currentTeam = team;
                    pointCircle.setOnMouseClicked(e -> {
                        selectedTeam = currentTeam;
                        selectedSquad = currentSquad;
                        selectedMoveIndex = moveIndex;
                        refreshCanvas();
                        refreshProperties();
                        e.consume();
                    });
                    
                    // Label move points
                    Label pointLabel = new Label("M" + (i + 1));
                    pointLabel.setStyle("-fx-font-size: 10px; -fx-text-fill: #333; -fx-background-color: rgba(255,255,255,0.8);");
                    pointLabel.setLayoutX(point.getX() + 8);
                    pointLabel.setLayoutY(point.getY() - 15);
                    
                    // Squad label at first move point
                    if (i == 0) {
                        Label squadLabel = new Label("S" + (squadIndex + 1));
                        squadLabel.setStyle("-fx-font-size: 11px; -fx-text-fill: #333; -fx-font-weight: bold; -fx-background-color: rgba(255,255,255,0.9);");
                        squadLabel.setLayoutX(point.getX() - 10);
                        squadLabel.setLayoutY(point.getY() - 30);
                        canvas.getChildren().add(squadLabel);
                    }
                    
                    canvas.getChildren().addAll(pointCircle, pointLabel);
                }
                squadIndex++;
            }
        }
    }
    
    private void refreshProperties() {
        // This would update the properties panel based on current selection
        // Implementation depends on how you store property references
    }
    
    private void refreshInspector() {
        // This would refresh the inspector panel
        // For simplicity, we'll just refresh the entire canvas
        refreshCanvas();
    }
    
    private void setCorrectTeam() {
        if (selectedTeam != null) {
            // Set all teams to not correct first
            for (Team team : currentScenario.getTeams()) {
                team.setRightMove(0);
            }
            selectedTeam.setRightMove(1);
            refreshInspector();
            showInfoDialog("Correct Team Set", "Team " + selectedTeam.getColor().toUpperCase() + " is now set as the correct team.");
        } else {
            showInfoDialog("No Team Selected", "Please select a team first.");
        }
    }
    
    private void saveScenario(String filePath) {
        try {
            if (filePath == null) {
                // Generate default path
                String fileName = currentScenario.getTitle().toLowerCase().replace(" ", "_") + ".json";
                filePath = "../python_app/data/scenarios/" + fileName;
            }
            jsonHandler.saveScenario(currentScenario, filePath);
            showInfoDialog("Scenario Saved", "Scenario saved successfully to: " + filePath);
        } catch (IOException e) {
            showErrorDialog("Error saving scenario", "Could not save scenario: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    private Color getColorFromString(String colorStr) {
        switch (colorStr.toLowerCase()) {
            case "red": return Color.RED;
            case "blue": return Color.BLUE;
            case "green": return Color.GREEN;
            case "yellow": return Color.YELLOW;
            case "orange": return Color.ORANGE;
            case "purple": return Color.PURPLE;
            default: return Color.GRAY;
        }
    }
    
    private void showErrorDialog(String title, String message) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }
    
    private void showInfoDialog(String title, String message) {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }
    
    public static void main(String[] args) {
        launch(args);
    }
}