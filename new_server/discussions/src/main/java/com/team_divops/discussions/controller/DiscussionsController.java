package com.team_divops.discussions.controller;

import com.team_divops.discussions.dto.DiscussionCreateRequest;
import com.team_divops.discussions.dto.LoginRequest;
import com.team_divops.discussions.dto.LoginResponse;
import com.team_divops.discussions.dto.SuccessResponse;
import com.team_divops.discussions.dto.ErrorResponse;
import com.team_divops.discussions.dto.DiscussionsResponse;
import com.team_divops.discussions.model.Discussion;
import com.team_divops.discussions.model.Question;
import com.team_divops.discussions.repository.DiscussionsRepository;
import com.team_divops.discussions.repository.QuestionsRepository;

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
        questionsRepository.save(question);

        return ResponseEntity.ok(new SuccessResponse("Discussion created successfully"));
    }


    @Operation(summary = "Get user discussions")
    @ApiResponse(responseCode = "200", description = "Successfully fetched user",
        content = @Content(schema = @Schema(implementation = DiscussionsResponse.class))
    )
    @ApiResponse(responseCode = "400", description = "", content = @Content)
    @GetMapping("/discussions")
    public ResponseEntity<?> getUserDiscussions(Authentication authentication) {
        
        Long userId = Long.parseLong((String) authentication.getPrincipal());
        List<Discussion> discussions = discussionsRepository.findByUserId(userId);

        DiscussionsResponse response = new DiscussionsResponse(discussions);

        return ResponseEntity.ok(response);
    }








        // @Operation(summary = "Register a new user")
        // @ApiResponse(responseCode = "200", description = "User registered successfully")
        // @ApiResponse(responseCode = "400", description = "", content = @Content)
        // @PostMapping("/register")
        // public ResponseEntity<?> registerUser(@Valid @RequestBody UserRegistrationRequest request) {
        //     if (usersRepository.findByEmail(request.getEmail()).isPresent()) {
        //         ErrorResponse error = new ErrorResponse("Email is already registered");
        //         return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
        //     }

        //     User user = new User();
        //     user.setFirstName(request.getFirstName());
        //     user.setLastName(request.getLastName());
        //     user.setEmail(request.getEmail());
        //     user.setPassword(passwordEncoder.encode(request.getPassword()));

        //     usersRepository.save(user);
        //     return ResponseEntity.ok(new SuccessResponse("User registered successfully"));
        // }

    // @Operation(summary = "Login a user and return JWT token")
    // @ApiResponse(responseCode = "200", description = "Successful login",
    //     content = @Content(schema = @Schema(implementation = LoginResponse.class))
    // )
    // @ApiResponse(responseCode = "400", description = "", content = @Content)
    // @PostMapping("/login")
    // public ResponseEntity<?> loginUser(@Valid @RequestBody LoginRequest request) {
    //     Optional<User> optionalUser = usersRepository.findByEmail(request.getEmail());

    //     if (optionalUser.isEmpty()) {
    //         ErrorResponse error = new ErrorResponse("Email not found");
    //         return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
    //     }

    //     User user = optionalUser.get();

    //     if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
    //         ErrorResponse error = new ErrorResponse("Invalid password");
    //         return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
    //     }

    //     String token = JwtUtil.generateToken(user.getEmail(), user.getId());

    //     LoginResponse response = new LoginResponse(
    //             token
    //     );

    //     return ResponseEntity.ok(response);
    // }

    // @Operation(summary = "Get user profile")
    // @ApiResponse(responseCode = "200", description = "Successfully fetched user",
    //     content = @Content(schema = @Schema(implementation = UserResponse.class))
    // )
    // @ApiResponse(responseCode = "400", description = "", content = @Content)
    // @GetMapping("/profile")
    // public ResponseEntity<?> getUserProfile(Authentication authentication) {
    //     System.out.println("Authentication: " + authentication);
    //     System.out.println("Principal: " + authentication.getPrincipal());
    //     System.out.println("Authorities: " + authentication.getAuthorities());
        
    //     Long userId = Long.parseLong((String) authentication.getPrincipal());
    //     System.out.println("userId " + userId);
    //     Optional<User> optionalUser = usersRepository.findById(userId);

    //     if (optionalUser.isEmpty()) {
    //         ErrorResponse error = new ErrorResponse("Id not found");
    //         return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
    //     }

    //     User user = optionalUser.get();

    //     UserResponse response = new UserResponse(
    //         user.getFirstName(), user.getLastName(), user.getEmail()
    //     );

    //     return ResponseEntity.ok(response);
    // }


    @Operation(summary = "Test serivce is working endpoint")
    @GetMapping("/hello")
    public String hello() {
        return "Hello from discussions service fffffccccc";
    }
}
