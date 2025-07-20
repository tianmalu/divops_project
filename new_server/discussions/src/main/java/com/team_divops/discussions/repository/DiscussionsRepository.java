package com.team_divops.discussions.repository;

import com.team_divops.discussions.model.Discussion;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface DiscussionsRepository extends JpaRepository<Discussion, Long> {
    Optional<Discussion> findById(Long id);

    List<Discussion> findByUserId(Long userId);

    Optional<Discussion> findByName(String name);
}
