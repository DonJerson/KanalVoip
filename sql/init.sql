-- init.sql
CREATE DATABASE IF NOT EXISTS kamailio;
USE kamailio;

CREATE TABLE IF NOT EXISTS subscriber (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL,
    domain VARCHAR(64) NOT NULL,
    password VARCHAR(64) NOT NULL
);
