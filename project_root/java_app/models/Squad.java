package models;

import java.util.List;
import java.util.ArrayList;

public class Squad {
    private List<MovePoint> movePoints;
    
    public Squad() {
        this.movePoints = new ArrayList<>();
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
}