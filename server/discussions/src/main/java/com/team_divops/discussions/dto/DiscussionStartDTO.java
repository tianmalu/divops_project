package com.team_divops.discussions.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.NotBlank;

public class DiscussionStartDTO {

    @NotNull(message = "Discussion ID is required")
    @JsonProperty("discussion_id")
    private String discussionId;

    @NotNull(message = "User ID is required")
    @JsonProperty("user_id")
    private String userId;

    @NotBlank(message = "Initial question is required")
    @JsonProperty("initial_question")
    private String initialQuestion;

    public DiscussionStartDTO(String discussionId, String userId, String initialQuestion) {
        this.discussionId = discussionId;
        this.userId = userId;
        this.initialQuestion = initialQuestion;
    }

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
}
