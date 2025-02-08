CREATE DATABASE  log_bd_linux;
\connect  log_bd_linux
CREATE TABLE classify_logs (
    user_id INTEGER NOT NULL,        
    time timestamp without time zone NOT NULL, 
    label BOOLEAN,
    promt TEXT);

