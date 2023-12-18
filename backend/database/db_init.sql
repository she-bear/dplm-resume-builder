USE resume;

CREATE TABLE IF NOT EXISTS users(
    id int NOT NULL AUTO_INCREMENT,
    login varchar(255) UNIQUE NOT NULL,
    password varchar(255) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS resumes(
    id int NOT NULL AUTO_INCREMENT,
    user_id int NOT NULL,
    resume_title VARCHAR(100),
    resume_text TEXT,
    PRIMARY KEY(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE
);