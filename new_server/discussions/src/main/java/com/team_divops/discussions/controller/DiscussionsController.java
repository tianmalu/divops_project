package com.team_divops.discussions.controller;

import com.team_divops.discussions.dto.DiscussionCreateRequest;
import com.team_divops.discussions.dto.QuestionCreateRequest;
import com.team_divops.discussions.dto.DiscussionDTO;
import com.team_divops.discussions.dto.LoginRequest;
import com.team_divops.discussions.dto.DiscussionDetailsRequest;
import com.team_divops.discussions.dto.DiscussionDetailsResponse;
import com.team_divops.discussions.dto.LoginResponse;
import com.team_divops.discussions.dto.QuestionDTO;
import com.team_divops.discussions.dto.SuccessResponse;
import com.team_divops.discussions.dto.ErrorResponse;
import com.team_divops.discussions.dto.DiscussionsResponse;
import com.team_divops.discussions.model.Discussion;
import com.team_divops.discussions.model.Question;
import com.team_divops.discussions.repository.DiscussionsRepository;
import com.team_divops.discussions.repository.QuestionsRepository;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import com.team_divops.discussions.security.JwtUtil;
import java.util.Optional;
import jakarta.validation.Valid;

@Tag(name = "Discussions", description = "Discussions Service APIs")
@RestController
@RequestMapping("/api/discussions")
public class DiscussionsController {

    private final DiscussionsRepository discussionsRepository;
    private final QuestionsRepository questionsRepository;
    private final PasswordEncoder passwordEncoder;

    public DiscussionsController(DiscussionsRepository discussionsRepository,QuestionsRepository questionsRepository, PasswordEncoder passwordEncoder) {
        this.discussionsRepository = discussionsRepository;
        this.questionsRepository = questionsRepository;
        this.passwordEncoder = passwordEncoder;
    }
    
    @Operation(summary = "Create a new discussion")
    @ApiResponse(responseCode = "200", description = "Discussion created successfully")
    @ApiResponse(responseCode = "400", description = "", content = @Content)
    @PostMapping("/discussion")
    public ResponseEntity<?> createDiscussion(@Valid @RequestBody DiscussionCreateRequest request, Authentication authentication) {
        Long userId = Long.parseLong((String) authentication.getPrincipal());

        if(discussionsRepository.findByName(request.getName()).isPresent()){
            ErrorResponse error = new ErrorResponse("Discussion already exists");
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
        }

        Discussion discussion = new Discussion();
        discussion.setName(request.getName());
        discussion.setUserId(userId);
        Discussion savedDiscussion = discussionsRepository.save(discussion);

        Question question = new Question();
        question.setText(request.getText());
        question.setDiscussion(savedDiscussion);
        question.setFromUser(true);
        questionsRepository.save(question);

        return ResponseEntity.ok(new SuccessResponse("Discussion created successfully"));
    }



        @Operation(summary = "Create a new question")
    @ApiResponse(responseCode = "200", description = "Question created successfully")
    @ApiResponse(responseCode = "400", description = "", content = @Content)
    @PostMapping("/question")
    public ResponseEntity<?> createQuestion(@Valid @RequestBody QuestionCreateRequest request, Authentication authentication) {
        Long userId = Long.parseLong((String) authentication.getPrincipal());
        Long discussionIdLong = Long.parseLong(request.getDiscussionId());

         Optional<Discussion> optionalDiscussion = discussionsRepository.findByUserIdAndId(userId, discussionIdLong);

              if (optionalDiscussion.isEmpty()) {
            ErrorResponse error = new ErrorResponse("Discussion not found");
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
        }

        Discussion discussion = optionalDiscussion.get();

        Question question = new Question();
        question.setText(request.getText());
        question.setDiscussion(discussion);
        question.setFromUser(true);
        questionsRepository.save(question);

        return ResponseEntity.ok(new SuccessResponse("Question created successfully"));
    }
















    @Operation(summary = "Get user discussions")
    @ApiResponse(responseCode = "200", description = "Successfully fetched discussions",
        content = @Content(schema = @Schema(implementation = DiscussionsResponse.class))
    )
    @ApiResponse(responseCode = "400", description = "", content = @Content)
    @GetMapping("/discussions")
    public ResponseEntity<?> getUserDiscussions(Authentication authentication) {
        
        Long userId = Long.parseLong((String) authentication.getPrincipal());
        List<Discussion> discussions = discussionsRepository.findByUserIdOrderByCreatedAtDesc(userId);

        List<DiscussionDTO> discussionDTOs = discussions.stream()
        .map(DiscussionDTO::fromEntity)
        .toList();

        DiscussionsResponse response = new DiscussionsResponse(discussionDTOs);

        return ResponseEntity.ok(response);
    }

    @Operation(summary = "Get discussion details")
    @ApiResponse(responseCode = "200", description = "Successfully fetched discussion",
        content = @Content(schema = @Schema(implementation = DiscussionDetailsResponse.class))
    )
    @ApiResponse(responseCode = "400", description = "", content = @Content)
    @GetMapping("/discussion")
    public ResponseEntity<?> getDiscussionDetails(Authentication authentication,  @RequestParam String discussionId) {
        Long discussionIdLong = Long.parseLong(discussionId);
        Long userId = Long.parseLong((String) authentication.getPrincipal());
        System.out.println("discussion     " + discussionIdLong);
        System.out.println("user                 "+ userId);

        Optional<Discussion> optionalDiscussion = discussionsRepository.findByUserIdAndId(userId, discussionIdLong);

              if (optionalDiscussion.isEmpty()) {
            ErrorResponse error = new ErrorResponse("Discussion not found");
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
        }

        Discussion discussion = optionalDiscussion.get();

        List<Question> questions = questionsRepository.findByDiscussionIdOrderByCreatedAtAsc(discussionIdLong);

        List<QuestionDTO> questionDTOs = questions.stream()
        .map(QuestionDTO::fromEntity)
        .toList();

        DiscussionDetailsResponse response = new DiscussionDetailsResponse(questionDTOs);

        return ResponseEntity.ok(response);
    }


    @Operation(summary = "Test serivce is working endpoint")
    @GetMapping("/hello")
    public String hello() {
        return "Hello from discussions service fffffccccc";
    }
}
