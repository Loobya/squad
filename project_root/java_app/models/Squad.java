package models;

import java.util.List;
import java.util.ArrayList;

public class Squad {
    private List<MovePoint> movePoints;
    private List<String> members;  // NEW: Squad member names
    private String markerIcon;     // NEW: Custom marker icon filename
    
    public Squad() {
        this.movePoints = new ArrayList<>();
        this.members = new ArrayList<>();  // NEW
    }
    
    // Getters and setters
    public List<MovePoint> getMovePoints() { return movePoints; }
    public void setMovePoints(List<MovePoint> movePoints) { this.movePoints = movePoints; }
    
    public void addMovePoint(MovePoint movePoint) {
        this.movePoints.add(movePoint);
    }
    
    public MovePoint getMovePoint(int index) {
        if (index >= 0 && index < movePoints.size()) {
            return movePoints.get(index);
        }
        return null;
    }
    public List<String> getMembers() { return members; }
    public void setMembers(List<String> members) { this.members = members; }
    public void addMember(String member) { this.members.add(member); }
    
    public String getMarkerIcon() { return markerIcon; }
    public void setMarkerIcon(String markerIcon) { this.markerIcon = markerIcon; }
}