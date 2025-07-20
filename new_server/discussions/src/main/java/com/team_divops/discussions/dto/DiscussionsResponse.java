package com.team_divops.discussions.dto;

import java.util.List;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;

public class DiscussionsResponse {
    @Schema(description = "List of discussions", nullable = false)
    private List<Discussion> data;

    public DiscussionsResponse(List<Discussion> data) {
        this.data = data;
    }

    public List<Discussion> getData() {
        return data;
    }

    public void setData(List<Discussion> data) {
        this.data = data;
    }
}
