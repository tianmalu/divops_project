package com.example.backend.client;

import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.ResponseEntity;
import java.net.URI;

@Component
public class WeaviateClient {

    private final RestTemplate restTemplate;
    private final String WEAVIATE_URL = "http://localhost:8081";  

    public WeaviateClient() {
        this.restTemplate = new RestTemplate();
    }

    public String queryTarotCard(String question) {
        String url = WEAVIATE_URL + "/v1/graphql";

        String graphqlQuery = "{ \"query\": \"{ Get { TarotCard { name meaning } } }\" }";

        ResponseEntity<String> response = restTemplate.postForEntity(
            url,
            org.springframework.http.RequestEntity
                .post(java.net.URI.create(url))
                .header("Content-Type", "application/json")
                .body(graphqlQuery),
            String.class
        );

        return response.getBody();
    }
}
