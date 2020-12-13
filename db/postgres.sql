-- Creating database
CREATE DATABASE webserver;

-- Creating table
CREATE TABLE users (
  id serial NOT NULL, 
  name character varying(200) DEFAULT '' NOT NULL,
  age character varying(10) DEFAULT '' NOT NULL, 
  sex character varying(10) DEFAULT '' NOT NULL,
  email character varying(200) DEFAULT '' NOT NULL,
  phone character varying(20) DEFAULT '' NOT NULL
);