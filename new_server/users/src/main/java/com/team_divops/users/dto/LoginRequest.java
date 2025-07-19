package com.team_divops.users.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;

public class LoginRequest {

    @NotBlank(message = "Email is required")
    @Schema(description = "User email", example = "user@example.com", nullable = false)
    private String email;

    @NotBlank(message = "Password is required")
    @Schema(description = "User password", example = "strongPassword123", nullable = false)
    private String password;

    // Getters and Setters
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
}
