package com.team_divops.discussions.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;

public class LoginResponse {
    @NotBlank(message = "Token is required")
    @Schema(description = "User Token", nullable = false)
    private String token;

    public LoginResponse(String token) {
        this.token = token;
    }

    public String getToken() {
        return token;
    }
}
