package models;

public class Explanations {
    private String right;
    private String wrong_1;
    private String wrong_2;
    
    public Explanations() {}
    
    public Explanations(String right, String wrong_1, String wrong_2) {
        this.right = right;
        this.wrong_1 = wrong_1;
        this.wrong_2 = wrong_2;
    }
    
    // Getters and setters
    public String getRight() { return right; }
    public void setRight(String right) { this.right = right; }
    
    public String getWrong1() { return wrong_1; }
    public void setWrong1(String wrong_1) { this.wrong_1 = wrong_1; }
    
    public String getWrong2() { return wrong_2; }
    public void setWrong2(String wrong_2) { this.wrong_2 = wrong_2; }
}