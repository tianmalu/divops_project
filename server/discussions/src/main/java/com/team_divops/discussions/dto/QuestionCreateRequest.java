package com.team_divops.discussions.dto;


import lombok.Data;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Email;

@Data
public class QuestionCreateRequest {
    @NotBlank(message = "Id")
    private String discussionId;

    @NotBlank(message = "Question is required")
    private String text;
}
