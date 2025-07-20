package com.team_divops.discussions.dto;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.stream.Collectors;
import lombok.ToString;
import com.fasterxml.jackson.annotation.JsonProperty;

@ToString
public class DiscussionStartResponseDto {

    private String discussionId;
    private String userId;
    private String initialQuestion;
    @JsonProperty("initial_response")
    private String initialResponse;
    @JsonProperty("cards_drawn")
    private List<CardDto> cardsDrawn;
    private OffsetDateTime createdAt;

    // Getters and setters

    public String getDiscussionId() {
        return discussionId;
    }

    public void setDiscussionId(String discussionId) {
        this.discussionId = discussionId;
    }

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getInitialQuestion() {
        return initialQuestion;
    }

    public void setInitialQuestion(String initialQuestion) {
        this.initialQuestion = initialQuestion;
    }

    public String getInitialResponse() {
        return initialResponse;
    }

    public void setInitialResponse(String initialResponse) {
        this.initialResponse = initialResponse;
    }

    public List<CardDto> getCardsDrawn() {
        return cardsDrawn;
    }

    public void setCardsDrawn(List<CardDto> cardsDrawn) {
        this.cardsDrawn = cardsDrawn;
    }

    public OffsetDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(OffsetDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public String getCardNames(){
        String mergedNames = this.cardsDrawn.stream()
    .map(CardDto::getName)
    .collect(Collectors.joining(","));
    return mergedNames;
    }

    // Inner DTO for each card
    public static class CardDto {
        private String name;
        private String position;
        private boolean upright;
        private String meaning;
        private List<String> positionKeywords;

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public String getPosition() {
            return position;
        }

        public void setPosition(String position) {
            this.position = position;
        }

        public boolean isUpright() {
            return upright;
        }

        public void setUpright(boolean upright) {
            this.upright = upright;
        }

        public String getMeaning() {
            return meaning;
        }

        public void setMeaning(String meaning) {
            this.meaning = meaning;
        }

        public List<String> getPositionKeywords() {
            return positionKeywords;
        }

        public void setPositionKeywords(List<String> positionKeywords) {
            this.positionKeywords = positionKeywords;
        }
    }
}
