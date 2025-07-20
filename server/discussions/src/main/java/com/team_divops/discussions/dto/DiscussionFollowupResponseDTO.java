package com.team_divops.discussions.dto;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.stream.Collectors;
import lombok.ToString;
import com.fasterxml.jackson.annotation.JsonProperty;

@ToString
public class DiscussionFollowupResponseDTO {

    private String response;

    // Getters and setters

    public String getResponse() {
        return response;
    }

    public void setResponse(String response) {
        this.response = response;
    }
}
