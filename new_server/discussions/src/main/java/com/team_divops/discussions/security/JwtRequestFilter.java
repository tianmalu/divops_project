package com.team_divops.discussions.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

@Component
public class JwtRequestFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain)
            throws ServletException, IOException {

        String requestURI = request.getRequestURI();
        
        // Skip JWT processing for public routes
        if (isPublicRoute(requestURI)) {
            System.out.println("Skipping JWT processing for public route: " + requestURI);
            chain.doFilter(request, response);
            return;
        }

        final String authHeader = request.getHeader("Authorization");
        System.out.println("Processing JWT for route: " + requestURI);
        System.out.println("Auth header: " + authHeader);

        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String token = authHeader.substring(7);
            System.out.println("Token: " + token);
            System.out.println("Token valid: " + JwtUtil.isValidToken(token));
            if (JwtUtil.isValidToken(token) && SecurityContextHolder.getContext().getAuthentication() == null) {
                Long userId = JwtUtil.getUserIdFromToken(token);
                System.out.println("Extracted userId: " + userId);
                
                if (userId != null) {
                    UsernamePasswordAuthenticationToken authentication =
                            new UsernamePasswordAuthenticationToken(userId.toString(), null, null);
                    authentication.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
                    SecurityContextHolder.getContext().setAuthentication(authentication);
                    System.out.println("Authentication set: " + authentication);
                } else {
                    // Fallback for old tokens that only contain email
                    String email = JwtUtil.getEmailFromToken(token);
                    System.out.println("Fallback: using email as principal: " + email);
                    UsernamePasswordAuthenticationToken authentication =
                            new UsernamePasswordAuthenticationToken(email, null, null);
                    authentication.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
                    SecurityContextHolder.getContext().setAuthentication(authentication);
                    System.out.println("Authentication set with email: " + authentication);
                }
            }
        }

        chain.doFilter(request, response);
    }

    private boolean isPublicRoute(String requestURI) {
        return requestURI.equals("/api/discussions/hello") ||
               requestURI.startsWith("/swagger-ui/") ||
               requestURI.startsWith("/v3/api-docs/") ||
               requestURI.equals("/v3/api-docs.yaml") ||
               requestURI.startsWith("/swagger-resources/");
    }
}
