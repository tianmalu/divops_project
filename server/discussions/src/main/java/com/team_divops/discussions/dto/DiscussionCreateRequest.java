package com.team_divops.discussions.dto;


import lombok.Data;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Email;

@Data
public class DiscussionCreateRequest {
    @NotBlank(message = "Name")
    private String name;

    @NotBlank(message = "Question is required")
    private String text;
}
