package com.team_divops.discussions.dto;

import com.team_divops.discussions.model.Discussion;
import com.team_divops.discussions.model.Question;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public class QuestionDTO {

    @NotBlank(message = "Id is required")
    private Long id;

    @NotBlank(message = "text is required")
    private String text;

    @NotBlank(message = "fromUser is required")
    private boolean fromUser;

    @NotNull(message = "Discussion ID is required")
    private Long discussionId;

    @NotBlank(message = "createdAt is required")
    private String createdAt;

    public QuestionDTO(Long id, String text, Long discussionId, String createdAt, boolean fromUser) {
        this.id = id;
        this.text = text;
        this.fromUser = fromUser;
        this.discussionId = discussionId;
        this.createdAt = createdAt;
    }

    public Long getId() {
        return id;
    }

    public String getText() {
        return text;
    }

    public boolean getFromUser () {
        return fromUser;
    }

    public Long getDiscussionId() {
        return discussionId;
    }

    public String getCreatedAt() {
        return createdAt;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setText(String text) {
        this.text = text;
    }

    public void setDiscussionId(Long discussionId) {
        this.discussionId = discussionId;
    }

    public void setCreatedAt(String createdAt) {
        this.createdAt = createdAt;
    }

    public static QuestionDTO fromEntity(Question question) {
        return new QuestionDTO(
            question.getId(),
            question.getText(),
            question.getDiscussion().getId(),
            question.getCreatedAt().toString(),
            question.isFromUser()
        );
    }
}
