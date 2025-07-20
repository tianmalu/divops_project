CREATE TABLE discussions (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    user_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cards TEXT
);


CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    from_user BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    discussion_id BIGINT NOT NULL,
    CONSTRAINT fk_discussion
        FOREIGN KEY(discussion_id)
            REFERENCES discussions(id)
            ON DELETE CASCADE
);