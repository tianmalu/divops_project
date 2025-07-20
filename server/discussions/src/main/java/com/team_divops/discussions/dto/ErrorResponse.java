package com.team_divops.discussions.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;

public class ErrorResponse {
    @NotBlank(message = "Error Message Required")
    @Schema(description = "Error Message", nullable = false)
    private String message;

    public ErrorResponse(String message) {
        this.message = message;
    }

    public String getMessage() {
        return message;
    }
}
