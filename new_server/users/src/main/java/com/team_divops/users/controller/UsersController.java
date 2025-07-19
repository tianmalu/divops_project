package com.team_divops.users.controller;

import com.team_divops.users.dto.UserRegistrationRequest;
import com.team_divops.users.dto.LoginRequest;
import com.team_divops.users.dto.LoginResponse;
import com.team_divops.users.dto.SuccessResponse;
import com.team_divops.users.model.User;
import com.team_divops.users.repository.UsersRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;
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
        @ApiResponse(responseCode = "400", description = "Email is already registered", content = @Content)
        @PostMapping("/register")
        public ResponseEntity<SuccessResponse> registerUser(@Valid @RequestBody UserRegistrationRequest request) {
            if (usersRepository.findByEmail(request.getEmail()).isPresent()) {
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Email is already registered");
            }

            User user = new User();
            user.setFirstName(request.getFirstName());
            user.setLastName(request.getLastName());
            user.setEmail(request.getEmail());
            user.setPassword(passwordEncoder.encode(request.getPassword()));

            usersRepository.save(user);
            return ResponseEntity.ok(new SuccessResponse("User registered successfully"));
        }

    @Operation(summary = "Login a user and return JWT token with user details")
    @ApiResponse(responseCode = "200", description = "Successful login",
        content = @Content(schema = @Schema(implementation = LoginResponse.class))
    )
    @ApiResponse(responseCode = "401", description = "Invalid email or password",
        content = @Content(mediaType = "text/plain")
    )
    @PostMapping("/login")
    public ResponseEntity<?> loginUser(@Valid @RequestBody LoginRequest request) {
        Optional<User> optionalUser = usersRepository.findByEmail(request.getEmail());

        if (optionalUser.isEmpty()) {
            return ResponseEntity.status(401).body("Email not found");
        }

        User user = optionalUser.get();

        if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
            return ResponseEntity.status(401).body("Invalid password");
        }

        String token = JwtUtil.generateToken(user.getEmail());

        LoginResponse response = new LoginResponse(
                token,
                user.getFirstName(),
                user.getLastName(),
                user.getEmail()
        );

        return ResponseEntity.ok(response);
    }

    @Operation(summary = "Test serivce is working endpoint")
    @GetMapping("/hello")
    public String hello() {
        return "Hello from Users service fffffccccc";
    }
}
