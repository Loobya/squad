package models;

import java.util.List;
import java.util.ArrayList;

public class Team {
    private String color;
    private List<Squad> squads;
    private int right_move; // 0-based index of correct team
    private Explanations explanations;
    
    public Team() {
        this.squads = new ArrayList<>();
        this.explanations = new Explanations();
    }
    
    public Team(String color) {
        this();
        this.color = color;
    }
    
    // Getters and setters
    public String getColor() { return color; }
    public void setColor(String color) { this.color = color; }
    
    public List<Squad> getSquads() { return squads; }
    public void setSquads(List<Squad> squads) { this.squads = squads; }
    
    public int getRightMove() { return right_move; }
    public void setRightMove(int right_move) { this.right_move = right_move; }
    
    public Explanations getExplanations() { return explanations; }
    public void setExplanations(Explanations explanations) { this.explanations = explanations; }
    
    public void addSquad(Squad squad) {
        this.squads.add(squad);
    }
    
    public boolean isCorrectTeam() {
        // The team with right_move = 1 is the correct one (based on JSON structure)
        return right_move == 1;
    }
}