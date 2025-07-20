package com.team_divops.discussions.repository;

import com.team_divops.discussions.model.Discussion;
import com.team_divops.discussions.model.Question;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface QuestionsRepository extends JpaRepository<Question, Long> {
    List<Question> findByDiscussionIdOrderByCreatedAtAsc(Long discussionId);
}
