package models;

import java.util.List;
import java.util.ArrayList;

public class Scenario {
    private String title;
    private String background;
    private List<Team> teams;
    private String created_by;
    private String date;
    
    public Scenario() {
        this.teams = new ArrayList<>();
    }
    
    public Scenario(String title, String background) {
        this();
        this.title = title;
        this.background = background;
    }
    
    // Getters and setters
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    
    public String getBackground() { return background; }
    public void setBackground(String background) { this.background = background; }
    
    public List<Team> getTeams() { return teams; }
    public void setTeams(List<Team> teams) { this.teams = teams; }
    
    public String getCreatedBy() { return created_by; }
    public void setCreatedBy(String created_by) { this.created_by = created_by; }
    
    public String getDate() { return date; }
    public void setDate(String date) { this.date = date; }
    
    public void addTeam(Team team) {
        this.teams.add(team);
    }
    
    public Team getCorrectTeam() {
        for (Team team : teams) {
            if (team.isCorrectTeam()) {
                return team;
            }
        }
        return null;
    }
}