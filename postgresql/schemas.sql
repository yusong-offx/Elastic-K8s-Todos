DROP TABLE IF EXISTS TODO_ROUTINES;
DROP TABLE IF EXISTS TODOS;
DROP TABLE IF EXISTS USERS;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    login_id VARCHAR(20) UNIQUE NOT NULL,
    login_password CHAR(60) NOT NULL,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    email varchar(100),
    last_login_at TIMESTAMP DEFAULT NOW() NOT NULL,
    join_at TIMESTAMP DEFAULT NOW() NOT NULL
);

CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES USERS(id) ON DELETE CASCADE,
    title VARCHAR(500),
    contents VARCHAR(1000),
    done BOOLEAN DEFAULT FALSE NOT NULL,
    create_at TIMESTAMP DEFAULT NOW() NOT NULL,
    modified_at TIMESTAMP DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_todos_user_id ON todos(user_id);

CREATE TABLE todo_routines (
    id INTEGER REFERENCES todos(id) ON DELETE CASCADE,
    routine char(1) NOT NULL
);

CREATE UNIQUE INDEX idx_todos_routines ON todo_routines(id, routine);
CREATE INDEX idx_todos_routines_routine ON todo_routines(routine);