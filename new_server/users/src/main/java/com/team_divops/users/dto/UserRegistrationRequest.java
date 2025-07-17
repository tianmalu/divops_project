package com.team_divops.users.dto;

import lombok.Data;

@Data
public class UserRegistrationRequest {
    private String firstName;
    private String lastName;
    private String email;
    private String password;
}
