package com.team_divops.discussions.dto;

import java.util.List;
import com.team_divops.discussions.model.Discussion;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;

public class DiscussionsResponse {
    @NotBlank(message = "Data Required")
    @Schema(description = "List of discussions", nullable = false)
    private List<DiscussionDTO> data;

    public DiscussionsResponse(List<DiscussionDTO> data) {
        this.data = data;
    }

    public List<DiscussionDTO> getData() {
        return data;
    }

    public void setData(List<DiscussionDTO> data) {
        this.data = data;
    }
}
