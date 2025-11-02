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
import javafx.animation.TranslateTransition;
import javafx.util.Duration;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class ScenarioPlayer extends Application {
    private Scenario currentScenario;
    private Pane animationPane;
    private ControlPanel controlPanel;
    private List<TranslateTransition> currentAnimations;
    private Team selectedTeam;
    private JSONHandler jsonHandler;
    
    private static final double CANVAS_WIDTH = 800;
    private static final double CANVAS_HEIGHT = 600;
    
    @Override
    public void start(Stage primaryStage) {
        this.jsonHandler = new JSONHandler();
        this.currentAnimations = new ArrayList<>();
        
        // Get scenario path from parameters or show file chooser
        List<String> args = getParameters().getRaw();
        if (!args.isEmpty()) {
            loadScenario(args.get(0));
        } else {
            showFileChooser(primaryStage);
            return;
        }
        
        setupUI(primaryStage);
    }
    
    private void showFileChooser(Stage primaryStage) {
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Open Scenario File");
        fileChooser.getExtensionFilters().add(
            new FileChooser.ExtensionFilter("JSON Files", "*.json")
        );
        
        // Set initial directory to python_app data scenarios
        File initialDir = new File("../python_app/data/scenarios");
        if (initialDir.exists()) {
            fileChooser.setInitialDirectory(initialDir);
        }
        
        File file = fileChooser.showOpenDialog(primaryStage);
        if (file != null) {
            loadScenario(file.getAbsolutePath());
            setupUI(primaryStage);
        } else {
            Platform.exit();
        }
    }
    
    private void loadScenario(String filePath) {
        try {
            this.currentScenario = jsonHandler.loadScenario(filePath);
            System.out.println("Loaded scenario: " + currentScenario.getTitle());
        } catch (IOException e) {
            showErrorDialog("Error loading scenario", "Could not load scenario from: " + filePath);
            e.printStackTrace();
        }
    }
    
    private void setupUI(Stage primaryStage) {
        primaryStage.setTitle("Scenario Player - " + currentScenario.getTitle());
        
        BorderPane root = new BorderPane();
        
        // Top: Scenario info
        root.setTop(createInfoPanel());
        
        // Center: Animation canvas
        animationPane = new Pane();
        animationPane.setPrefSize(CANVAS_WIDTH, CANVAS_HEIGHT);
        animationPane.setStyle("-fx-background-color: #f0f0f0; -fx-border-color: #ccc; -fx-border-width: 1;");
        root.setCenter(animationPane);
        
        // Right: Team selection panel
        root.setRight(createTeamSelectionPanel());
        
        // Bottom: Control panel
        controlPanel = new ControlPanel();
        root.setBottom(controlPanel);
        
        Scene scene = new Scene(root, 1200, 800);
        primaryStage.setScene(scene);
        primaryStage.show();
        
        // Draw initial positions and movement paths
        drawMovementPaths();
    }
    
    private HBox createInfoPanel() {
        HBox infoPanel = new HBox(10);
        infoPanel.setPadding(new Insets(10));
        infoPanel.setStyle("-fx-background-color: #e0e0e0;");
        
        Label titleLabel = new Label("Scenario: " + currentScenario.getTitle());
        titleLabel.setStyle("-fx-font-size: 16px; -fx-font-weight: bold;");
        
        VBox infoBox = new VBox(5);
        Label backgroundLabel = new Label("Background: " + currentScenario.getBackground());
        Label createdByLabel = new Label("Created by: " + currentScenario.getCreatedBy());
        Label dateLabel = new Label("Date: " + currentScenario.getDate());
        
        infoBox.getChildren().addAll(backgroundLabel, createdByLabel, dateLabel);
        infoPanel.getChildren().addAll(titleLabel, infoBox);
        
        return infoPanel;
    }
    
    private VBox createTeamSelectionPanel() {
        VBox teamPanel = new VBox(10);
        teamPanel.setPadding(new Insets(10));
        teamPanel.setPrefWidth(300);
        teamPanel.setStyle("-fx-background-color: #f8f8f8; -fx-border-color: #ccc; -fx-border-width: 0 0 0 1;");
        
        Label titleLabel = new Label("Select the Correct Team");
        titleLabel.setStyle("-fx-font-size: 14px; -fx-font-weight: bold;");
        teamPanel.getChildren().add(titleLabel);
        
        ToggleGroup teamGroup = new ToggleGroup();
        
        for (Team team : currentScenario.getTeams()) {
            VBox teamBox = new VBox(5);
            teamBox.setStyle("-fx-border-color: #ddd; -fx-border-width: 1; -fx-padding: 8; -fx-background-color: white;");
            
            RadioButton radioButton = new RadioButton("Team " + team.getColor().toUpperCase());
            radioButton.setToggleGroup(teamGroup);
            radioButton.setUserData(team);
            radioButton.setWrapText(true);
            
            // Add squad information
            Label squadInfo = new Label(team.getSquads().size() + " squads, " + 
                                      team.getSquads().get(0).getMovePoints().size() + " movement points each");
            squadInfo.setStyle("-fx-font-size: 11px; -fx-text-fill: #666;");
            
            teamBox.getChildren().addAll(radioButton, squadInfo);
            teamPanel.getChildren().add(teamBox);
        }
        
        Button submitButton = new Button("Submit Selection");
        submitButton.setStyle("-fx-font-size: 14px; -fx-padding: 10;");
        submitButton.setOnAction(e -> {
            RadioButton selected = (RadioButton) teamGroup.getSelectedToggle();
            if (selected != null) {
                selectedTeam = (Team) selected.getUserData();
                evaluateSelection();
            } else {
                showInfoDialog("No Selection", "Please select a team first.");
            }
        });
        
        teamPanel.getChildren().add(submitButton);
        return teamPanel;
    }
    
    private void drawMovementPaths() {
        animationPane.getChildren().clear();
        
        Color[] teamColors = {Color.RED, Color.BLUE, Color.GREEN};
        int colorIndex = 0;
        
        for (Team team : currentScenario.getTeams()) {
            Color teamColor = getColorFromString(team.getColor());
            if (teamColor == null) {
                teamColor = teamColors[colorIndex % teamColors.length];
            }
            
            for (Squad squad : team.getSquads()) {
                List<MovePoint> moves = squad.getMovePoints();
                
                // Draw movement lines
                for (int i = 0; i < moves.size() - 1; i++) {
                    MovePoint start = moves.get(i);
                    MovePoint end = moves.get(i + 1);
                    
                    Line movementLine = new Line(start.getX(), start.getY(), end.getX(), end.getY());
                    movementLine.setStroke(teamColor);
                    movementLine.setOpacity(0.6);
                    movementLine.setStrokeWidth(2);
                    movementLine.getStrokeDashArray().addAll(5d, 5d);
                    
                    animationPane.getChildren().add(movementLine);
                }
                
                // Draw move points
                for (int i = 0; i < moves.size(); i++) {
                    MovePoint point = moves.get(i);
                    Circle pointCircle = new Circle(point.getX(), point.getY(), 4, teamColor);
                    
                    // Label move points
                    Label pointLabel = new Label("M" + (i + 1));
                    pointLabel.setStyle("-fx-font-size: 10px; -fx-text-fill: #333;");
                    pointLabel.setLayoutX(point.getX() + 5);
                    pointLabel.setLayoutY(point.getY() - 10);
                    
                    animationPane.getChildren().addAll(pointCircle, pointLabel);
                }
            }
            colorIndex++;
        }
    }
    
    private void playAnimation() {
        // Clear previous animations
        stopAnimation();
        
        Color[] teamColors = {Color.RED, Color.BLUE, Color.GREEN};
        int colorIndex = 0;
        
        for (Team team : currentScenario.getTeams()) {
            Color teamColor = getColorFromString(team.getColor());
            if (teamColor == null) {
                teamColor = teamColors[colorIndex % teamColors.length];
            }
            
            int squadIndex = 0;
            for (Squad squad : team.getSquads()) {
                List<MovePoint> moves = squad.getMovePoints();
                
                // Create squad circle for animation (larger than path points)
                Circle squadCircle = new Circle(8, teamColor);
                squadCircle.setCenterX(moves.get(0).getX());
                squadCircle.setCenterY(moves.get(0).getY());
                
                // Add squad label
                Label squadLabel = new Label("S" + (squadIndex + 1));
                squadLabel.setStyle("-fx-font-size: 10px; -fx-text-fill: #333; -fx-background-color: rgba(255,255,255,0.7);");
                squadLabel.setLayoutX(moves.get(0).getX() + 10);
                squadLabel.setLayoutY(moves.get(0).getY() - 20);
                
                animationPane.getChildren().addAll(squadCircle, squadLabel);
                
                // Create sequential animation for all movement points
                TranslateTransition finalTransition = createSequentialAnimation(squadCircle, moves, squadLabel);
                currentAnimations.add(finalTransition);
                finalTransition.play();
                
                squadIndex++;
            }
            colorIndex++;
        }
        
        controlPanel.setPlaying(true);
    }
    
    private TranslateTransition createSequentialAnimation(Circle circle, List<MovePoint> moves, Label label) {
        if (moves.isEmpty()) return null;
        
        TranslateTransition transition = new TranslateTransition(Duration.seconds(2), circle);
        MovePoint firstMove = moves.get(0);
        
        // Start from first position
        circle.setCenterX(firstMove.getX());
        circle.setCenterY(firstMove.getY());
        
        if (moves.size() > 1) {
            // Animate through all points
            for (int i = 1; i < moves.size(); i++) {
                MovePoint current = moves.get(i);
                MovePoint previous = moves.get(i - 1);
                
                TranslateTransition segment = new TranslateTransition(Duration.seconds(2), circle);
                segment.setToX(current.getX() - previous.getX());
                segment.setToY(current.getY() - previous.getY());
                
                final int currentIndex = i;
                segment.setOnFinished(e -> {
                    // Update label position
                    label.setLayoutX(circle.getCenterX() + circle.getTranslateX() + 10);
                    label.setLayoutY(circle.getCenterY() + circle.getTranslateY() - 20);
                });
                
                if (i == 1) {
                    transition = segment;
                } else {
                    transition = chainTransitions(transition, segment);
                }
            }
        }
        
        return transition;
    }
    
    private TranslateTransition chainTransitions(TranslateTransition first, TranslateTransition second) {
        first.setOnFinished(e -> second.play());
        return first;
    }
    
    private void stopAnimation() {
        for (TranslateTransition animation : currentAnimations) {
            if (animation != null) {
                animation.stop();
            }
        }
        currentAnimations.clear();
        
        // Remove animation circles and labels
        animationPane.getChildren().removeIf(node -> 
            (node instanceof Circle && ((Circle) node).getRadius() == 8) || 
            (node instanceof Label && ((Label) node).getText().startsWith("S"))
        );
        
        controlPanel.setPlaying(false);
    }
    
    private void evaluateSelection() {
        if (selectedTeam == null) return;
        
        Team correctTeam = currentScenario.getCorrectTeam();
        boolean isCorrect = selectedTeam.isCorrectTeam();
        
        String title = isCorrect ? "Correct Selection!" : "Incorrect Selection";
        String message;
        
        if (isCorrect) {
            message = selectedTeam.getExplanations().getRight();
        } else {
            message = "You selected: Team " + selectedTeam.getColor().toUpperCase() + "\n\n" +
                     "Correct team was: Team " + correctTeam.getColor().toUpperCase() + "\n\n" +
                     "Reason: " + getWrongReason(selectedTeam, correctTeam);
        }
        
        Alert alert = new Alert(isCorrect ? Alert.AlertType.INFORMATION : Alert.AlertType.WARNING);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.getDialogPane().setPrefSize(400, 200);
        alert.showAndWait();
    }
    
    private String getWrongReason(Team selectedTeam, Team correctTeam) {
        // Determine which wrong reason to show based on team selection
        int selectedIndex = currentScenario.getTeams().indexOf(selectedTeam);
        int correctIndex = currentScenario.getTeams().indexOf(correctTeam);
        
        if (selectedIndex == 0 && correctIndex == 1) {
            return selectedTeam.getExplanations().getWrong1();
        } else {
            return selectedTeam.getExplanations().getWrong2();
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
            default: return null;
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
    
    // Inner class for control panel
    private class ControlPanel extends HBox {
        private Button playButton;
        private Button stopButton;
        private Button replayButton;
        private boolean isPlaying;
        
        public ControlPanel() {
            setSpacing(10);
            setPadding(new Insets(10));
            setAlignment(Pos.CENTER);
            setStyle("-fx-background-color: #e8e8e8;");
            
            playButton = new Button("Play Animation");
            stopButton = new Button("Stop");
            replayButton = new Button("Replay");
            
            playButton.setOnAction(e -> playAnimation());
            stopButton.setOnAction(e -> stopAnimation());
            replayButton.setOnAction(e -> {
                stopAnimation();
                playAnimation();
            });
            
            getChildren().addAll(playButton, stopButton, replayButton);
            setPlaying(false);
        }
        
        public void setPlaying(boolean playing) {
            this.isPlaying = playing;
            playButton.setDisable(playing);
            stopButton.setDisable(!playing);
            replayButton.setDisable(playing);
        }
    }
    
    public static void main(String[] args) {
        launch(args);
    }
}