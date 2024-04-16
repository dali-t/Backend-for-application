CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE images (
    image_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    caption TEXT,
    author_id INTEGER,  -- Author ID referencing users table based on email
    image_link VARCHAR(255),
    CONSTRAINT fk_author_id FOREIGN KEY (author_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE reactions (
    reaction_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),  -- Foreign key referencing users table
    image_id INTEGER REFERENCES images(image_id),  -- Foreign key referencing images table
    reaction_type VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_reaction UNIQUE (user_id, image_id)
    CONSTRAINT valid_reaction_type CHECK (reaction_type IN ('like', 'dislike'))
);

CREATE TABLE analytics (
    analytics_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),  -- Foreign key referencing users table
    analytics_type VARCHAR(50) NOT NULL,
    last_post_timestamp TIMESTAMP
);

INSERT INTO users (email, first_name, last_name, password) VALUES
    ('john@example.com', 'John', 'Doe', 'password123'),
    ('jane@example.com', 'Jane', 'Smith', 'securepass'),
    ('alice@example.com', 'Alice', 'Johnson', 'pass123'),
    ('bob@example.com', 'Bob', 'Brown', 'password'),
    ('sarah@example.com', 'Sarah', 'Wilson', 'qwerty');

INSERT INTO images (caption, image_link, author_id)
VALUES ('Beautiful Sunset', 'https://example.com/sunset.jpg', 1);

CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    image_id INTEGER REFERENCES images(image_id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(user_id),
    comment_text VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);