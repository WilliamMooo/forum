CREATE DATABASE stock_forum DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE stock_forum;

CREATE TABLE `stock_list` (
  `code` CHAR(6) NOT NULL,
  `name` CHAR(20),
  `listing_date` DATE,
  PRIMARY KEY(`code`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE `user`(
  `id` VARCHAR(30) NOT NULL,
  `nickname` VARCHAR(30) NOT NULL,
  `password` VARCHAR(30) NOT NULL,
  `question` VARCHAR(30) NOT NULL,
  `answer` VARCHAR(30) NOT NULL,
  PRIMARY KEY(`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE `thread_list`(
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `owner` VARCHAR(30) NOT NULL,
  `owner_name` VARCHAR(30) NOT NULL,
  `theme` VARCHAR(30) NOT NULL,
  `content` VARCHAR(300) NOT NULL,
  `pub_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE `strategy`(
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  `description` VARCHAR(300) NOT NULL,
  `equity_sum` FLOAT NOT NULL,
  `annualised_return` FLOAT NOT NULL,
  `win_count` INT NOT NULL,
  `max_win` FLOAT NOT NULL,
  `lose_count` INT NOT NULL,
  `max_lose` FLOAT NOT NULL,
  `average_hold` VARCHAR(30) NULL,
  PRIMARY KEY(`id`),
  KEY(`name`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;