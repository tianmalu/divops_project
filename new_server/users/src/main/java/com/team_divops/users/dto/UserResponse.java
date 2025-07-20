package com.team_divops.users.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;

public class UserResponse {
    @NotBlank(message = "First Name is required")
    @Schema(description = "User First Name", nullable = false)
    private String firstName;
    @NotBlank(message = "Last Name is required")
    @Schema(description = "User Last Name", nullable = false)
    private String lastName;
    @NotBlank(message = "Email is required")
    @Schema(description = "User Email", nullable = false)
    private String email;

    public UserResponse(String firstName, String lastName, String email) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
    }

    public String getFirstName() {
        return firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public String getEmail() {
        return email;
    }
}
