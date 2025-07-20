package com.team_divops.discussions.dto;

import com.team_divops.discussions.model.Discussion;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public class DiscussionDTO {

    @NotBlank(message = "Id is required")
    private Long id;

    @NotBlank(message = "Name is required")
    private String name;

    @NotNull(message = "User ID is required")
    private Long userId;

    @NotBlank(message = "createdAt is required")
    private String createdAt;

    public DiscussionDTO(Long id, String name, Long userId, String createdAt) {
        this.id = id;
        this.name = name;
        this.userId = userId;
        this.createdAt = createdAt;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public Long getUserId() {
        return userId;
    }

    public String getCreatedAt() {
        return createdAt;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public void setCreatedAt(String createdAt) {
        this.createdAt = createdAt;
    }

    public static DiscussionDTO fromEntity(Discussion discussion) {
        return new DiscussionDTO(
            discussion.getId(),
            discussion.getName(),
            discussion.getUserId(),
            discussion.getCreatedAt().toString()
        );
    }
}
