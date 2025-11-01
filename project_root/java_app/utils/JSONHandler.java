package utils;

import models.Scenario;
import models.Team;
import models.Squad;
import models.MovePoint;
import models.Explanations;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;
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
        scenario.setCreatedBy(rootNode.get("created_by").asText());
        scenario.setDate(rootNode.get("date").asText());
        
        JsonNode teamsNode = rootNode.get("teams");
        if (teamsNode.isArray()) {
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
            explanations.setRight(explanationsNode.get("right").asText());
            explanations.setWrong1(explanationsNode.get("wrong_1").asText());
            explanations.setWrong2(explanationsNode.get("wrong_2").asText());
            team.setExplanations(explanations);
        }
        
        // Parse squads
        JsonNode squadsNode = teamNode.get("squads");
        if (squadsNode.isArray()) {
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
        
        // Parse move points (move_1, move_2, move_3)
        for (int i = 1; i <= 3; i++) {
            String moveKey = "move_" + i;
            JsonNode moveNode = squadNode.get(moveKey);
            if (moveNode != null) {
                MovePoint movePoint = new MovePoint();
                movePoint.setX(moveNode.get("x").asDouble());
                movePoint.setY(moveNode.get("y").asDouble());
                squad.addMovePoint(movePoint);
            }
        }
        
        return squad;
    }
    
    public void saveScenario(Scenario scenario, String filePath) throws IOException {
        String json = objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(scenario);
        try (FileWriter writer = new FileWriter(filePath)) {
            writer.write(json);
        }
    }
}