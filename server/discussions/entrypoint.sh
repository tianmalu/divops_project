#!/bin/bash
# Run gradle continuous build in background
./gradlew build --continuous -x test --no-daemon &

# Run Spring Boot app (bootRun) in foreground
./gradlew bootRun --no-daemon
