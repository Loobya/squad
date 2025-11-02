package models;

public class PlacedLogo {
    private String filename;
    private double x;
    private double y;
    private double width;
    private double height;
    
    public PlacedLogo() {}
    
    public PlacedLogo(String filename, double x, double y, double width, double height) {
        this.filename = filename;
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }
    
    // Getters and setters
    public String getFilename() { return filename; }
    public void setFilename(String filename) { this.filename = filename; }
    
    public double getX() { return x; }
    public void setX(double x) { this.x = x; }
    
    public double getY() { return y; }
    public void setY(double y) { this.y = y; }
    
    public double getWidth() { return width; }
    public void setWidth(double width) { this.width = width; }
    
    public double getHeight() { return height; }
    public void setHeight(double height) { this.height = height; }
}