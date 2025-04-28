package com.example.backend.controller;

import com.example.backend.service.TarotService;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.http.ResponseEntity;
import java.util.Map;
import java.net.URI;


@RestController
@RequestMapping("/api")
public class TarotController {

    private final TarotService tarotService;

    public TarotController(TarotService tarotService) {
        this.tarotService = tarotService;
    }

    @GetMapping("/predict")
    public ResponseEntity<Map<String, String>> predict(@RequestParam String question) {
        Map<String, String> result = tarotService.getPrediction(question);
        return ResponseEntity.ok(result);
    }
}