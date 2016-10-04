-- mysql -u root -p < schema.sql

-- DROP database if EXISTS nlp_web;

-- CREATE database nlp_web;

use nlp_web;

-- GRANT SELECT , INSERT , UPDATE ,DELETE on nlp_web.*  to 'client'@'localhost' identified by 'client';
-- grant all privileges on nlp_web.* to client@localhost identified by 'root_passwd';
-- flush privileges;

CREATE TABLE users(
  `id` varchar(50) NOT NULL ,
  `email` varchar(50) NOT NULL ,
  `passwd` varchar(50) NOT NULL ,
  `admin` bool NOT NULL ,
  `name` varchar(50) NOT NULL ,
  `image` varchar(500) NOT NULL ,
  `created_at` REAL NOT NULL ,
  UNIQUE KEY `idx_email` (`email`),
  KEY `idx_created_at` (`created_at`),
  PRIMARY KEY (`id`)
)engine=innodb DEFAULT charset=utf8;

CREATE TABLE blogs(
  `id` varchar(50) NOT NULL ,
  `user_id` varchar(50) NOT NULL ,
  `user_name` varchar(50) NOT NULL ,
  `user_image` varchar(500) NOT NULL ,
  `name` varchar(50) NOT NULL ,
  `summary` varchar(200) NOT NULL ,
  `content` mediumtext NOT NULL ,
  `created_at` REAL NOT NULL ,
  KEY `idx_created_at` (`created_at`),
  PRIMARY KEY (`id`)
)engine=innodb DEFAULT charset=utf8;

CREATE TABLE comments(
  `id` varchar(50) NOT NULL ,
  `blog_id` varchar(50) NOT NULL ,
  `user_id` varchar(50) NOT NULL ,
  `user_name` varchar(50) NOT NULL ,
  `user_image` varchar(500) NOT NULL ,
  `content` mediumtext NOT NULL ,
  `created_at` REAL NOT NULL ,
  KEY `idx_created_at` (`created_at`),
  PRIMARY KEY (`id`)
)engine=innodb DEFAULT charset=utf8;