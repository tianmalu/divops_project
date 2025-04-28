package com.example.backend.service;

import com.example.backend.client.WeaviateClient; 
import org.springframework.stereotype.Service;      
import java.util.HashMap;                          
import java.util.Map;                 
import java.net.URI;


@Service
public class TarotService {

    private final WeaviateClient weaviateClient;

    public TarotService(WeaviateClient weaviateClient) {
        this.weaviateClient = weaviateClient;
    }

    public Map<String, String> getPrediction(String question) {
        Map<String, String> response = new HashMap<>();
        response.put("question", question);
        response.put("answer", "You will find success!");
        

        return response;
    }
}
