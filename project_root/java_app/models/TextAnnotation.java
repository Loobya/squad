package models;

public class TextAnnotation {
    private String text;
    private double x;
    private double y;
    private String color;
    private int fontSize;
    
    public TextAnnotation() {}
    
    public TextAnnotation(String text, double x, double y, String color, int fontSize) {
        this.text = text;
        this.x = x;
        this.y = y;
        this.color = color;
        this.fontSize = fontSize;
    }
    
    // Getters and setters
    public String getText() { return text; }
    public void setText(String text) { this.text = text; }
    
    public double getX() { return x; }
    public void setX(double x) { this.x = x; }
    
    public double getY() { return y; }
    public void setY(double y) { this.y = y; }
    
    public String getColor() { return color; }
    public void setColor(String color) { this.color = color; }
    
    public int getFontSize() { return fontSize; }
    public void setFontSize(int fontSize) { this.fontSize = fontSize; }
}