package models;

import java.util.List;
import java.util.ArrayList;

public class Scenario {
    private String title;
    private String background;
    private List<Team> teams;
    private String created_by;
    private String date;
    private String drawing_data;  // NEW: Stores canvas drawings as Base64
    private List<PlacedLogo> logos;  // NEW: Placed logos
    private List<TextAnnotation> annotations;  // NEW: Text annotations
    
    public Scenario() {
        this.teams = new ArrayList<>();
        this.logos = new ArrayList<>();
        this.annotations = new ArrayList<>();
    }
    
    // ... existing getters/setters ...
    
    // NEW getters/setters
    public String getDrawingData() { return drawing_data; }
    public void setDrawingData(String drawing_data) { this.drawing_data = drawing_data; }
    
    public List<PlacedLogo> getLogos() { return logos; }
    public void setLogos(List<PlacedLogo> logos) { this.logos = logos; }
    
    public List<TextAnnotation> getAnnotations() { return annotations; }
    public void setAnnotations(List<TextAnnotation> annotations) { this.annotations = annotations; }
}