package com.team_divops.discussions.dto;

import java.util.List;
import com.team_divops.discussions.model.Discussion;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;

public class DiscussionDetailsResponse {
    @NotBlank(message = "Data Required")
    @Schema(description = "List of questions", nullable = false)
    private List<QuestionDTO> questions;

    public DiscussionDetailsResponse(List<QuestionDTO> questions) {
        this.questions = questions;
    }

    public List<QuestionDTO> getQuestions() {
        return questions;
    }

    public void setQuestions(List<QuestionDTO> questions) {
        this.questions = questions;
    }
}
