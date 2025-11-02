import models.*;
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
import javafx.scene.shape.*;
import javafx.scene.image.*;
import javafx.scene.input.MouseButton;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.text.Font;
import javafx.scene.Cursor;
import java.io.File;
import java.io.IOException;
import java.util.*;

public class ScenarioEditor extends Application {
    // Data models
    private Scenario currentScenario;
    private JSONHandler jsonHandler;
    private String currentFilePath = null;
    
    // UI Components
    private BorderPane mainLayout;
    private StackPane canvasContainer;
    private ImageView backgroundImageView;
    private Canvas drawingCanvas;
    private Pane overlayPane;
    private VBox leftPanel;
    private VBox rightPanel;
    
    // Drawing state
    private GraphicsContext gc;
    private DrawingTool currentTool = DrawingTool.SELECT;
    private Color currentDrawColor = Color.BLACK;
    private double lineWidth = 2.0;
    
    // Selection state
    private Team selectedTeam;
    private Squad selectedSquad;
    
    // Drawing tools enum
    enum DrawingTool {
        SELECT, BRUSH, LINE, TEXT, LOGO, SQUAD_MARKER
    }
    
    // Constants
    private static final double CANVAS_WIDTH = 1000;
    private static final double CANVAS_HEIGHT = 700;
    
    // Logos and markers storage
    private List<File> availableLogos = new ArrayList<>();
    private List<File> squadMarkers = new ArrayList<>();
    
    // Line drawing state
    private double lineStartX, lineStartY;
    private boolean isDrawingLine = false;
    
    @Override
    public void start(Stage primaryStage) {
        this.jsonHandler = new JSONHandler();
        
        // Load scenario
        List<String> args = getParameters().getRaw();
        if (!args.isEmpty() && args.get(0) != null && !args.get(0).isEmpty()) {
            loadScenario(args.get(0));
        } else {
            createNewScenario();
        }
        
        // Load available logos and markers
        loadLogosAndMarkers();
        
        setupUI(primaryStage);
    }
    
    private void loadLogosAndMarkers() {
        // Load logos from assets folder
        File logosDir = new File("../python_app/assets/logos");
        if (!logosDir.exists()) {
            logosDir = new File("python_app/assets/logos");
        }
        if (!logosDir.exists()) {
            logosDir.mkdirs();
        }
        
        if (logosDir.exists() && logosDir.isDirectory()) {
            File[] logoFiles = logosDir.listFiles((dir, name) -> 
                name.toLowerCase().endsWith(".png") || 
                name.toLowerCase().endsWith(".jpg") ||
                name.toLowerCase().endsWith(".jpeg")
            );
            if (logoFiles != null) {
                availableLogos.addAll(Arrays.asList(logoFiles));
            }
        }
        
        // Load squad markers
        File markersDir = new File("../python_app/assets/squad_markers");
        if (!markersDir.exists()) {
            markersDir = new File("python_app/assets/squad_markers");
        }
        if (!markersDir.exists()) {
            markersDir.mkdirs();
        }
        
        if (markersDir.exists() && markersDir.isDirectory()) {
            File[] markerFiles = markersDir.listFiles((dir, name) -> 
                name.toLowerCase().endsWith(".png")
            );
            if (markerFiles != null) {
                squadMarkers.addAll(Arrays.asList(markerFiles));
            }
        }
        
        System.out.println("Loaded " + availableLogos.size() + " logos");
        System.out.println("Loaded " + squadMarkers.size() + " squad markers");
    }
    
    private void loadScenario(String filePath) {
        try {
            this.currentScenario = jsonHandler.loadScenario(filePath);
            this.currentFilePath = filePath;
            System.out.println("Loaded scenario: " + currentScenario.getTitle());
        } catch (IOException e) {
            showErrorDialog("Error loading scenario", "Could not load scenario from: " + filePath);
            e.printStackTrace();
            createNewScenario();
        }
    }
    
    private void createNewScenario() {
        currentScenario = new Scenario();
        currentScenario.setTitle("New Scenario - سيناريو جديد");
        currentScenario.setBackground("default_map.png");
        currentScenario.setCreatedBy("editor");
        currentScenario.setDate(java.time.LocalDate.now().toString());
        
        // Create 3 teams with empty squads initially
        String[] colors = {"red", "blue", "green"};
        for (String color : colors) {
            Team team = new Team(color);
            team.setRightMove(0);
            
            Explanations explanations = new Explanations();
            explanations.setRight("");
            explanations.setWrong1("");
            explanations.setWrong2("");
            team.setExplanations(explanations);
            
            currentScenario.addTeam(team);
        }
        
        this.currentFilePath = null;
        System.out.println("Created new blank scenario");
    }
    
    private void setupUI(Stage primaryStage) {
        primaryStage.setTitle("Enhanced Scenario Editor - " + currentScenario.getTitle());
        
        mainLayout = new BorderPane();
        
        // Top: Menu and Toolbar
        VBox topSection = new VBox();
        topSection.getChildren().addAll(createMenuBar(primaryStage), createToolbar());
        mainLayout.setTop(topSection);
        
        // Center: Canvas with background, drawing layer, and overlay
        canvasContainer = createCanvasArea();
        mainLayout.setCenter(canvasContainer);
        
        // Left: Teams and tools
        leftPanel = createLeftPanel();
        mainLayout.setLeft(leftPanel);
        
        // Right: Properties and explanations
        rightPanel = createRightPanel();
        mainLayout.setRight(rightPanel);
        
        Scene scene = new Scene(mainLayout, 1600, 900);
        primaryStage.setScene(scene);
        primaryStage.show();
        
        // Show welcome message
        if (currentFilePath == null) {
            Platform.runLater(() -> {
                showInfoDialog(
                    "Enhanced Scenario Editor",
                    "Welcome to the Enhanced Scenario Editor!\n\n" +
                    "Features:\n" +
                    "• Load custom background map\n" +
                    "• Draw with brush and lines\n" +
                    "• Add text annotations\n" +
                    "• Place squad markers\n" +
                    "• Drag & drop logos\n" +
                    "• Write explanations for teams\n\n" +
                    "Start by loading a background image!"
                );
            });
        }
    }
    
    private MenuBar createMenuBar(Stage primaryStage) {
        MenuBar menuBar = new MenuBar();
        
        // File menu
        Menu fileMenu = new Menu("File");
        
        MenuItem newItem = new MenuItem("New Scenario");
        newItem.setOnAction(e -> {
            if (confirmAction("Create new scenario? Unsaved changes will be lost.")) {
                createNewScenario();
                primaryStage.setTitle("Enhanced Scenario Editor - " + currentScenario.getTitle());
                refreshUI();
            }
        });
        
        MenuItem openItem = new MenuItem("Open Scenario");
        openItem.setOnAction(e -> showOpenDialog(primaryStage));
        
        MenuItem saveItem = new MenuItem("Save");
        saveItem.setOnAction(e -> saveScenario(null));
        
        MenuItem saveAsItem = new MenuItem("Save As...");
        saveAsItem.setOnAction(e -> showSaveDialog(primaryStage));
        
        MenuItem loadBackgroundItem = new MenuItem("Load Background Image...");
        loadBackgroundItem.setOnAction(e -> loadBackgroundImage());
        
        MenuItem exitItem = new MenuItem("Exit");
        exitItem.setOnAction(e -> {
            if (confirmAction("Exit? Make sure you saved your work!")) {
                primaryStage.close();
            }
        });
        
        fileMenu.getItems().addAll(
            newItem, openItem, new SeparatorMenuItem(),
            saveItem, saveAsItem, new SeparatorMenuItem(),
            loadBackgroundItem, new SeparatorMenuItem(),
            exitItem
        );
        
        // Edit menu
        Menu editMenu = new Menu("Edit");
        
        MenuItem clearDrawingsItem = new MenuItem("Clear All Drawings");
        clearDrawingsItem.setOnAction(e -> clearDrawings());
        
        MenuItem setCorrectTeamItem = new MenuItem("Set as Correct Team");
        setCorrectTeamItem.setOnAction(e -> setCorrectTeam());
        
        editMenu.getItems().addAll(clearDrawingsItem, setCorrectTeamItem);
        
        // Help menu
        Menu helpMenu = new Menu("Help");
        
        MenuItem instructionsItem = new MenuItem("Instructions");
        instructionsItem.setOnAction(e -> showInstructions());
        
        MenuItem aboutItem = new MenuItem("About");
        aboutItem.setOnAction(e -> showAbout());
        
        helpMenu.getItems().addAll(instructionsItem, aboutItem);
        
        menuBar.getMenus().addAll(fileMenu, editMenu, helpMenu);
        return menuBar;
    }
    
    private ToolBar createToolbar() {
        ToolBar toolbar = new ToolBar();
        
        // Tool selection buttons
        ToggleGroup toolGroup = new ToggleGroup();
        
        ToggleButton selectBtn = new ToggleButton("Select");
        selectBtn.setToggleGroup(toolGroup);
        selectBtn.setSelected(true);
        selectBtn.setOnAction(e -> currentTool = DrawingTool.SELECT);
        
        ToggleButton brushBtn = new ToggleButton("✏️ Brush");
        brushBtn.setToggleGroup(toolGroup);
        brushBtn.setOnAction(e -> currentTool = DrawingTool.BRUSH);
        
        ToggleButton lineBtn = new ToggleButton("📏 Line");
        lineBtn.setToggleGroup(toolGroup);
        lineBtn.setOnAction(e -> currentTool = DrawingTool.LINE);
        
        ToggleButton textBtn = new ToggleButton("📝 Text");
        textBtn.setToggleGroup(toolGroup);
        textBtn.setOnAction(e -> currentTool = DrawingTool.TEXT);
        
        ToggleButton logoBtn = new ToggleButton("🖼️ Logo");
        logoBtn.setToggleGroup(toolGroup);
        logoBtn.setOnAction(e -> currentTool = DrawingTool.LOGO);
        
        ToggleButton markerBtn = new ToggleButton("📍 Squad Marker");
        markerBtn.setToggleGroup(toolGroup);
        markerBtn.setOnAction(e -> currentTool = DrawingTool.SQUAD_MARKER);
        
        // Color picker
        ColorPicker colorPicker = new ColorPicker(currentDrawColor);
        colorPicker.setOnAction(e -> currentDrawColor = colorPicker.getValue());
        
        // Line width
        Label widthLabel = new Label("Width:");
        Slider widthSlider = new Slider(1, 10, lineWidth);
        widthSlider.setShowTickLabels(true);
        widthSlider.setMajorTickUnit(3);
        widthSlider.setPrefWidth(150);
        widthSlider.valueProperty().addListener((obs, old, newVal) -> {
            lineWidth = newVal.doubleValue();
        });
        
        toolbar.getItems().addAll(
            selectBtn, new Separator(),
            brushBtn, lineBtn, textBtn, new Separator(),
            logoBtn, markerBtn, new Separator(),
            colorPicker, widthLabel, widthSlider
        );
        
        return toolbar;
    }
    
    private StackPane createCanvasArea() {
        StackPane container = new StackPane();
        container.setPrefSize(CANVAS_WIDTH, CANVAS_HEIGHT);
        container.setStyle("-fx-background-color: #e0e0e0;");
        
        // Background image layer
        backgroundImageView = new ImageView();
        backgroundImageView.setFitWidth(CANVAS_WIDTH);
        backgroundImageView.setFitHeight(CANVAS_HEIGHT);
        backgroundImageView.setPreserveRatio(false);
        
        // Drawing canvas layer
        drawingCanvas = new Canvas(CANVAS_WIDTH, CANVAS_HEIGHT);
        gc = drawingCanvas.getGraphicsContext2D();
        gc.setLineWidth(lineWidth);
        gc.setStroke(currentDrawColor);
        
        // Overlay pane for draggable elements
        overlayPane = new Pane();
        overlayPane.setPrefSize(CANVAS_WIDTH, CANVAS_HEIGHT);
        
        // Setup canvas interactions
        setupCanvasInteractions();
        
        container.getChildren().addAll(backgroundImageView, drawingCanvas, overlayPane);
        
        return container;
    }
    
    private void setupCanvasInteractions() {
        // Mouse press
        drawingCanvas.setOnMousePressed(e -> {
            switch (currentTool) {
                case BRUSH:
                    gc.beginPath();
                    gc.moveTo(e.getX(), e.getY());
                    break;
                case LINE:
                    lineStartX = e.getX();
                    lineStartY = e.getY();
                    isDrawingLine = true;
                    break;
                case TEXT:
                    addTextToCanvas(e.getX(), e.getY());
                    break;
                case LOGO:
                    showLogoSelector(e.getX(), e.getY());
                    break;
                case SQUAD_MARKER:
                    showMarkerSelector(e.getX(), e.getY());
                    break;
            }
        });
        
        // Mouse drag
        drawingCanvas.setOnMouseDragged(e -> {
            if (currentTool == DrawingTool.BRUSH) {
                gc.setStroke(currentDrawColor);
                gc.setLineWidth(lineWidth);
                gc.lineTo(e.getX(), e.getY());
                gc.stroke();
            }
        });
        
        // Mouse release
        drawingCanvas.setOnMouseReleased(e -> {
            if (currentTool == DrawingTool.LINE && isDrawingLine) {
                gc.setStroke(currentDrawColor);
                gc.setLineWidth(lineWidth);
                gc.strokeLine(lineStartX, lineStartY, e.getX(), e.getY());
                isDrawingLine = false;
            }
        });
    }
    
    private VBox createLeftPanel() {
        VBox panel = new VBox(10);
        panel.setPadding(new Insets(10));
        panel.setPrefWidth(280);
        panel.setStyle("-fx-background-color: #f5f5f5; -fx-border-color: #ccc; -fx-border-width: 0 1 0 0;");
        
        Label title = new Label("Teams & Squads");
        title.setStyle("-fx-font-size: 16px; -fx-font-weight: bold;");
        
        // Teams list
        ListView<String> teamsList = new ListView<>();
        teamsList.setPrefHeight(200);
        for (Team team : currentScenario.getTeams()) {
            String indicator = team.isCorrectTeam() ? "✓ " : "";
            teamsList.getItems().add(indicator + "Team " + team.getColor().toUpperCase());
        }
        
        teamsList.getSelectionModel().selectedIndexProperty().addListener((obs, oldVal, newVal) -> {
            if (newVal.intValue() >= 0) {
                selectedTeam = currentScenario.getTeams().get(newVal.intValue());
                refreshRightPanel();
            }
        });
        
        // Add squad button
        Button addSquadBtn = new Button("➕ Add Squad to Selected Team");
        addSquadBtn.setMaxWidth(Double.MAX_VALUE);
        addSquadBtn.setOnAction(e -> addSquadToTeam());
        
        // Squads list
        Label squadsLabel = new Label("Squads:");
        squadsLabel.setStyle("-fx-font-weight: bold;");
        
        ListView<String> squadsList = new ListView<>();
        squadsList.setPrefHeight(150);
        updateSquadsList(squadsList);
        
        // Logos panel
        Label logosLabel = new Label("Available Logos:");
        logosLabel.setStyle("-fx-font-weight: bold; -fx-padding: 10 0 0 0;");
        
        Label logosInfo = new Label("Use Logo tool and click on map");
        logosInfo.setStyle("-fx-font-size: 10px; -fx-text-fill: #666;");
        
        panel.getChildren().addAll(
            title, teamsList, addSquadBtn,
            new Separator(),
            squadsLabel, squadsList,
            new Separator(),
            logosLabel, logosInfo
        );
        
        return panel;
    }
    
    private VBox createRightPanel() {
        VBox panel = new VBox(15);
        panel.setPadding(new Insets(15));
        panel.setPrefWidth(350);
        panel.setStyle("-fx-background-color: #f5f5f5; -fx-border-color: #ccc; -fx-border-width: 0 0 0 1;");
        
        Label title = new Label("Scenario Properties");
        title.setStyle("-fx-font-size: 16px; -fx-font-weight: bold;");
        
        // Scenario title
        Label titleLabel = new Label("Scenario Title:");
        TextField titleField = new TextField(currentScenario.getTitle());
        titleField.textProperty().addListener((obs, old, newVal) -> {
            currentScenario.setTitle(newVal);
        });
        
        // Background
        Label bgLabel = new Label("Background:");
        TextField bgField = new TextField(currentScenario.getBackground());
        bgField.setEditable(false);
        Button loadBgBtn = new Button("Load Image");
        loadBgBtn.setOnAction(e -> loadBackgroundImage());
        
        HBox bgBox = new HBox(5, bgField, loadBgBtn);
        HBox.setHgrow(bgField, Priority.ALWAYS);
        
        // Team explanations section
        Label explainLabel = new Label("Team Explanations:");
        explainLabel.setStyle("-fx-font-weight: bold; -fx-font-size: 14px; -fx-padding: 10 0 0 0;");
        
        Label selectedTeamLabel = new Label("No team selected");
        selectedTeamLabel.setStyle("-fx-text-fill: #666;");
        
        // Correct reason
        Label correctLabel = new Label("Why this team is CORRECT:");
        TextArea correctArea = new TextArea();
        correctArea.setPrefRowCount(3);
        correctArea.setWrapText(true);
        correctArea.setPromptText("Explain why this is the correct approach...");
        
        // Wrong reason 1
        Label wrong1Label = new Label("Wrong Reason 1:");
        TextArea wrong1Area = new TextArea();
        wrong1Area.setPrefRowCount(2);
        wrong1Area.setWrapText(true);
        wrong1Area.setPromptText("Explain first mistake...");
        
        // Wrong reason 2
        Label wrong2Label = new Label("Wrong Reason 2:");
        TextArea wrong2Area = new TextArea();
        wrong2Area.setPrefRowCount(2);
        wrong2Area.setWrapText(true);
        wrong2Area.setPromptText("Explain second mistake...");
        
        // Store references for updates
        Map<String, Object> refs = new HashMap<>();
        refs.put("selectedTeamLabel", selectedTeamLabel);
        refs.put("correctArea", correctArea);
        refs.put("wrong1Area", wrong1Area);
        refs.put("wrong2Area", wrong2Area);
        panel.setUserData(refs);
        
        ScrollPane scroll = new ScrollPane();
        VBox content = new VBox(10,
            title, titleLabel, titleField,
            bgLabel, bgBox,
            explainLabel, selectedTeamLabel,
            correctLabel, correctArea,
            wrong1Label, wrong1Area,
            wrong2Label, wrong2Area
        );
        scroll.setContent(content);
        scroll.setFitToWidth(true);
        
        panel.getChildren().add(scroll);
        
        return panel;
    }
    
    private void loadBackgroundImage() {
        FileChooser fc = new FileChooser();
        fc.setTitle("Select Background Image");
        fc.getExtensionFilters().add(
            new FileChooser.ExtensionFilter("Images", "*.png", "*.jpg", "*.jpeg")
        );
        
        File file = fc.showOpenDialog(mainLayout.getScene().getWindow());
        if (file != null) {
            try {
                Image img = new Image(file.toURI().toString());
                backgroundImageView.setImage(img);
                currentScenario.setBackground(file.getName());
                showInfoDialog("Success", "Background image loaded successfully!");
            } catch (Exception e) {
                showErrorDialog("Error", "Could not load image: " + e.getMessage());
            }
        }
    }
    
    private void clearDrawings() {
        if (confirmAction("Clear all drawings?")) {
            gc.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
        }
    }
    
    private void setCorrectTeam() {
        if (selectedTeam != null) {
            for (Team team : currentScenario.getTeams()) {
                team.setRightMove(0);
            }
            selectedTeam.setRightMove(1);
            refreshUI();
            showInfoDialog("Success", "Team " + selectedTeam.getColor() + " set as correct!");
        } else {
            showInfoDialog("Info", "Please select a team first.");
        }
    }
    
    private void addSquadToTeam() {
        if (selectedTeam != null) {
            Squad newSquad = new Squad();
            // Add default 3 move points
            for (int i = 0; i < 3; i++) {
                newSquad.addMovePoint(new MovePoint(100 + i * 100, 100));
            }
            selectedTeam.addSquad(newSquad);
            refreshUI();
            showInfoDialog("Success", "Squad added to team " + selectedTeam.getColor());
        } else {
            showInfoDialog("Info", "Please select a team first.");
        }
    }
    
    private void updateSquadsList(ListView<String> list) {
        list.getItems().clear();
        if (selectedTeam != null) {
            int index = 1;
            for (Squad squad : selectedTeam.getSquads()) {
                list.getItems().add("Squad " + index + " (" + squad.getMovePoints().size() + " points)");
                index++;
            }
        }
    }
    
    private void addTextToCanvas(double x, double y) {
        TextInputDialog dialog = new TextInputDialog();
        dialog.setTitle("Add Text");
        dialog.setHeaderText("Enter text to add:");
        dialog.setContentText("Text:");
        
        dialog.showAndWait().ifPresent(text -> {
            gc.setFill(currentDrawColor);
            gc.setFont(new Font(16));
            gc.fillText(text, x, y);
        });
    }
    
    private void showLogoSelector(double x, double y) {
        showInfoDialog("Info", "Logo placement - Select a logo from assets folder\nFeature in development");
    }
    
    private void showMarkerSelector(double x, double y) {
        showInfoDialog("Info", "Squad marker placement - Feature in development");
    }
    
    private void refreshUI() {
        mainLayout.setLeft(createLeftPanel());
        refreshRightPanel();
    }
    
    private void refreshRightPanel() {
        if (selectedTeam != null && rightPanel.getUserData() != null) {
            @SuppressWarnings("unchecked")
            Map<String, Object> refs = (Map<String, Object>) rightPanel.getUserData();
            
            Label label = (Label) refs.get("selectedTeamLabel");
            label.setText("Selected: Team " + selectedTeam.getColor().toUpperCase());
            
            TextArea correctArea = (TextArea) refs.get("correctArea");
            correctArea.setText(selectedTeam.getExplanations().getRight());
            correctArea.textProperty().addListener((obs, old, newVal) -> {
                selectedTeam.getExplanations().setRight(newVal);
            });
            
            TextArea wrong1Area = (TextArea) refs.get("wrong1Area");
            wrong1Area.setText(selectedTeam.getExplanations().getWrong1());
            wrong1Area.textProperty().addListener((obs, old, newVal) -> {
                selectedTeam.getExplanations().setWrong1(newVal);
            });
            
            TextArea wrong2Area = (TextArea) refs.get("wrong2Area");
            wrong2Area.setText(selectedTeam.getExplanations().getWrong2());
            wrong2Area.textProperty().addListener((obs, old, newVal) -> {
                selectedTeam.getExplanations().setWrong2(newVal);
            });
        }
    }
    
    private void showOpenDialog(Stage stage) {
        FileChooser fc = new FileChooser();
        fc.setTitle("Open Scenario");
        fc.getExtensionFilters().add(new FileChooser.ExtensionFilter("JSON", "*.json"));
        File file = fc.showOpenDialog(stage);
        if (file != null) {
            loadScenario(file.getAbsolutePath());
            refreshUI();
        }
    }
    
    private void showSaveDialog(Stage stage) {
        saveScenario(null);
    }
    
    private void saveScenario(String path) {
        if (path == null && currentFilePath != null) {
            path = currentFilePath;
        }
        
        if (path == null) {
            FileChooser fc = new FileChooser();
            fc.setTitle("Save Scenario");
            fc.getExtensionFilters().add(new FileChooser.ExtensionFilter("JSON", "*.json"));
            fc.setInitialFileName(currentScenario.getTitle().toLowerCase().replace(" ", "_") + ".json");
            
            File initialDir = new File("../python_app/data/scenarios");
            if (initialDir.exists()) fc.setInitialDirectory(initialDir);
            
            File file = fc.showSaveDialog(mainLayout.getScene().getWindow());
            if (file == null) return;
            path = file.getAbsolutePath();
        }
        
        try {
            jsonHandler.saveScenario(currentScenario, path);
            currentFilePath = path;
            showInfoDialog("Success", "Scenario saved successfully!");
        } catch (IOException e) {
            showErrorDialog("Error", "Could not save: " + e.getMessage());
        }
    }
    
    private void showInstructions() {
        showInfoDialog("Instructions",
            "TOOLS:\n" +
            "• Select - Select and move objects\n" +
            "• Brush - Free-hand drawing\n" +
            "• Line - Draw straight lines\n" +
            "• Text - Add text annotations\n" +
            "• Logo - Place logos on map\n" +
            "• Squad Marker - Place squad markers\n\n" +
            "WORKFLOW:\n" +
            "1. Load background image\n" +
            "2. Select a team\n" +
            "3. Add squads to team\n" +
            "4. Place squad markers on map\n" +
            "5. Draw and annotate\n" +
            "6. Write explanations\n" +
            "7. Set correct team\n" +
            "8. Save scenario"
        );
    }
    
    private void showAbout() {
        showInfoDialog("About",
            "Enhanced Scenario Editor\n" +
            "Version 2.0\n\n" +
            "Created for Interactive Tactical Training System"
        );
    }
    
    private boolean confirmAction(String message) {
        Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
        alert.setTitle("Confirm");
        alert.setContentText(message);
        return alert.showAndWait().get() == ButtonType.OK;
    }
    
    private void showErrorDialog(String title, String message) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle(title);
        alert.setContentText(message);
        alert.showAndWait();
    }
    
    private void showInfoDialog(String title, String message) {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle(title);
        alert.setContentText(message);
        alert.showAndWait();
    }
    
    public static void main(String[] args) {
        launch(args);
    }
}