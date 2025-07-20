package com.team_divops.discussions.dto;

import java.util.List;
import com.team_divops.discussions.model.Discussion;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;

public class DiscussionDetailsResponse {
    @NotBlank(message = "Data Required")
    @Schema(description = "List of questions", nullable = false)
    private List<QuestionDTO> questions;

    @NotBlank(message = "Cards Required")
    @Schema(description = "Cards", nullable = false)
    private String cards;

    public DiscussionDetailsResponse(List<QuestionDTO> questions, String cards) {
        this.questions = questions;
        this.cards = cards;
    }

    public List<QuestionDTO> getQuestions() {
        return questions;
    }

    public void setQuestions(List<QuestionDTO> questions) {
        this.questions = questions;
    }

    public String getCards(){
        return cards;
    }

    public void setCards(String cards) {
        this.cards = cards;
    }
}

