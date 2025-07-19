package com.team_divops.users.controller;

import com.team_divops.users.dto.UserRegistrationRequest;
import com.team_divops.users.dto.LoginRequest;
import com.team_divops.users.dto.LoginResponse;
import com.team_divops.users.dto.SuccessResponse;
import com.team_divops.users.dto.ErrorResponse;
import com.team_divops.users.dto.UserResponse;
import com.team_divops.users.model.User;
import com.team_divops.users.repository.UsersRepository;
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
import com.team_divops.users.security.JwtUtil;
import java.util.Optional;
import jakarta.validation.Valid;

@Tag(name = "Users", description = "Users Service APIs")
@RestController
@RequestMapping("/api/users")
public class UsersController {

    private final UsersRepository usersRepository;
    private final PasswordEncoder passwordEncoder;

    public UsersController(UsersRepository usersRepository, PasswordEncoder passwordEncoder) {
        this.usersRepository = usersRepository;
        this.passwordEncoder = passwordEncoder;
    }

        @Operation(summary = "Register a new user")
        @ApiResponse(responseCode = "200", description = "User registered successfully")
        @ApiResponse(responseCode = "400", description = "", content = @Content)
        @PostMapping("/register")
        public ResponseEntity<?> registerUser(@Valid @RequestBody UserRegistrationRequest request) {
            if (usersRepository.findByEmail(request.getEmail()).isPresent()) {
                ErrorResponse error = new ErrorResponse("Email is already registered");
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
            }

            User user = new User();
            user.setFirstName(request.getFirstName());
            user.setLastName(request.getLastName());
            user.setEmail(request.getEmail());
            user.setPassword(passwordEncoder.encode(request.getPassword()));

            usersRepository.save(user);
            return ResponseEntity.ok(new SuccessResponse("User registered successfully"));
        }

    @Operation(summary = "Login a user and return JWT token")
    @ApiResponse(responseCode = "200", description = "Successful login",
        content = @Content(schema = @Schema(implementation = LoginResponse.class))
    )
    @ApiResponse(responseCode = "400", description = "", content = @Content)
    @PostMapping("/login")
    public ResponseEntity<?> loginUser(@Valid @RequestBody LoginRequest request) {
        Optional<User> optionalUser = usersRepository.findByEmail(request.getEmail());

        if (optionalUser.isEmpty()) {
            ErrorResponse error = new ErrorResponse("Email not found");
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
        }

        User user = optionalUser.get();

        if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
            ErrorResponse error = new ErrorResponse("Invalid password");
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
        }

        String token = JwtUtil.generateToken(user.getEmail(), user.getId());

        LoginResponse response = new LoginResponse(
                token
        );

        return ResponseEntity.ok(response);
    }































    @Operation(summary = "Get user profile")
    @ApiResponse(responseCode = "200", description = "Successfully fetched user",
        content = @Content(schema = @Schema(implementation = UserResponse.class))
    )
    @ApiResponse(responseCode = "400", description = "", content = @Content)
    @GetMapping("/profile")
    public ResponseEntity<?> getUserProfile(Authentication authentication) {
        System.out.println("Authentication: " + authentication);
        System.out.println("Principal: " + authentication.getPrincipal());
        System.out.println("Authorities: " + authentication.getAuthorities());
        
        String principal = (String) authentication.getPrincipal();
        Optional<User> optionalUser;
        
        // Try to parse as userId first (new tokens)
        try {
            Long userId = Long.parseLong(principal);
            System.out.println("userId " + userId);
            optionalUser = usersRepository.findById(userId);
        } catch (NumberFormatException e) {
            // Fallback: treat as email (old tokens)
            System.out.println("Treating principal as email: " + principal);
            optionalUser = usersRepository.findByEmail(principal);
        }

        if (optionalUser.isEmpty()) {
            ErrorResponse error = new ErrorResponse("Id not found");
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
        }

        User user = optionalUser.get();

        UserResponse response = new UserResponse(
            user.getFirstName(), user.getLastName(), user.getEmail()
        );

        return ResponseEntity.ok(response);
    }


    @Operation(summary = "Test serivce is working endpoint")
    @GetMapping("/hello")
    public String hello() {
        return "Hello from Users service fffffccccc";
    }
}
