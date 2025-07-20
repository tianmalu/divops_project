package com.team_divops.discussions.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;

public class DiscussionDetailsRequest {

    @NotBlank(message = "discussion id is required")
    @Schema(nullable = false)
    private String discussionId;

    // Getters and Setters
    public String getDiscussionId() { return discussionId; }
    public void setDiscussionId(String discussionId) { this.discussionId = discussionId; }
}
