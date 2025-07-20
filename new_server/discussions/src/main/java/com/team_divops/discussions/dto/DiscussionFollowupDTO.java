package com.team_divops.discussions.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.NotBlank;

public class DiscussionFollowupDTO {

    @NotBlank(message = "question is required")
    @JsonProperty("question")
    private String question;

    public DiscussionFollowupDTO(String question) {
        this.question = question;
    }

    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
    }
}
