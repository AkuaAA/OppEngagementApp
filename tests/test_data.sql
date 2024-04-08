INSERT INTO user (username, password) VALUES ('test_user', 'test_password');
INSERT INTO post (author_id, title, body) VALUES (1, 'Test Post', 'This is a test post');
INSERT INTO opportunity (name, description, status, employee_id) VALUES ('Test Opportunity', 'This is a test opportunity', 'Open', 1);
INSERT INTO comments (post_id, author_id, body) VALUES (1, 1, 'This is a test comment');