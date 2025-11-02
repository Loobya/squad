package utils;

import models.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.fasterxml.jackson.databind.node.ArrayNode;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Iterator;

public class JSONHandler {
    private ObjectMapper objectMapper;
    
    public JSONHandler() {
        this.objectMapper = new ObjectMapper();
    }
    
    public Scenario loadScenario(String filePath) throws IOException {
        String content = new String(Files.readAllBytes(Paths.get(filePath)));
        JsonNode rootNode = objectMapper.readTree(content);
        
        Scenario scenario = new Scenario();
        scenario.setTitle(rootNode.get("title").asText());
        scenario.setBackground(rootNode.get("background").asText());
        
        // Load created_by and date if available
        if (rootNode.has("created_by")) {
            scenario.setCreatedBy(rootNode.get("created_by").asText());
        }
        if (rootNode.has("date")) {
            scenario.setDate(rootNode.get("date").asText());
        }
        
        // Load teams
        JsonNode teamsNode = rootNode.get("teams");
        if (teamsNode != null && teamsNode.isArray()) {
            Iterator<JsonNode> teamsIterator = teamsNode.elements();
            while (teamsIterator.hasNext()) {
                JsonNode teamNode = teamsIterator.next();
                Team team = parseTeam(teamNode);
                scenario.addTeam(team);
            }
        }
        
        return scenario;
    }
    
    private Team parseTeam(JsonNode teamNode) {
        Team team = new Team();
        team.setColor(teamNode.get("color").asText());
        team.setRightMove(teamNode.get("right_move").asInt());
        
        // Parse explanations
        JsonNode explanationsNode = teamNode.get("explanations");
        if (explanationsNode != null) {
            Explanations explanations = new Explanations();
            if (explanationsNode.has("right")) {
                explanations.setRight(explanationsNode.get("right").asText());
            }
            if (explanationsNode.has("wrong_1")) {
                explanations.setWrong1(explanationsNode.get("wrong_1").asText());
            }
            if (explanationsNode.has("wrong_2")) {
                explanations.setWrong2(explanationsNode.get("wrong_2").asText());
            }
            team.setExplanations(explanations);
        }
        
        // Parse squads
        JsonNode squadsNode = teamNode.get("squads");
        if (squadsNode != null && squadsNode.isArray()) {
            Iterator<JsonNode> squadsIterator = squadsNode.elements();
            while (squadsIterator.hasNext()) {
                JsonNode squadNode = squadsIterator.next();
                Squad squad = parseSquad(squadNode);
                team.addSquad(squad);
            }
        }
        
        return team;
    }
    
    private Squad parseSquad(JsonNode squadNode) {
        Squad squad = new Squad();
        
        // Parse move points (move_1, move_2, move_3, etc.)
        for (int i = 1; i <= 10; i++) {  // Support up to 10 move points
            String moveKey = "move_" + i;
            JsonNode moveNode = squadNode.get(moveKey);
            if (moveNode != null) {
                MovePoint movePoint = new MovePoint();
                movePoint.setX(moveNode.get("x").asDouble());
                movePoint.setY(moveNode.get("y").asDouble());
                squad.addMovePoint(movePoint);
            } else {
                break;  // No more move points
            }
        }
        
        // Parse squad members if available
        JsonNode membersNode = squadNode.get("members");
        if (membersNode != null && membersNode.isArray()) {
            Iterator<JsonNode> membersIterator = membersNode.elements();
            while (membersIterator.hasNext()) {
                squad.addMember(membersIterator.next().asText());
            }
        }
        
        // Parse marker icon if available
        if (squadNode.has("marker_icon")) {
            squad.setMarkerIcon(squadNode.get("marker_icon").asText());
        }
        
        return squad;
    }
    
    public void saveScenario(Scenario scenario, String filePath) throws IOException {
        ObjectNode rootNode = objectMapper.createObjectNode();
        
        // Basic scenario info
        rootNode.put("title", scenario.getTitle());
        rootNode.put("background", scenario.getBackground());
        rootNode.put("created_by", scenario.getCreatedBy());
        rootNode.put("date", scenario.getDate());
        
        // Teams array
        ArrayNode teamsArray = rootNode.putArray("teams");
        
        for (Team team : scenario.getTeams()) {
            ObjectNode teamNode = teamsArray.addObject();
            teamNode.put("color", team.getColor());
            teamNode.put("right_move", team.getRightMove());
            
            // Explanations
            ObjectNode explanationsNode = teamNode.putObject("explanations");
            Explanations exp = team.getExplanations();
            explanationsNode.put("right", exp.getRight() != null ? exp.getRight() : "");
            explanationsNode.put("wrong_1", exp.getWrong1() != null ? exp.getWrong1() : "");
            explanationsNode.put("wrong_2", exp.getWrong2() != null ? exp.getWrong2() : "");
            
            // Squads array
            ArrayNode squadsArray = teamNode.putArray("squads");
            
            for (Squad squad : team.getSquads()) {
                ObjectNode squadNode = squadsArray.addObject();
                
                // Move points
                int moveIndex = 1;
                for (MovePoint point : squad.getMovePoints()) {
                    ObjectNode moveNode = squadNode.putObject("move_" + moveIndex);
                    moveNode.put("x", point.getX());
                    moveNode.put("y", point.getY());
                    moveIndex++;
                }
                
                // Squad members
                if (squad.getMembers() != null && !squad.getMembers().isEmpty()) {
                    ArrayNode membersArray = squadNode.putArray("members");
                    for (String member : squad.getMembers()) {
                        membersArray.add(member);
                    }
                }
                
                // Marker icon
                if (squad.getMarkerIcon() != null) {
                    squadNode.put("marker_icon", squad.getMarkerIcon());
                }
            }
        }
        
        // Write to file with pretty printing
        String json = objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(rootNode);
        try (FileWriter writer = new FileWriter(filePath)) {
            writer.write(json);
        }
    }
}