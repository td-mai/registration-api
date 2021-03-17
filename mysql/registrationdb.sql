-- Host: localhost    Database: registrationdb
-- ------------------------------------------------------

CREATE DATABASE IF NOT EXISTS registrationdb ;
CREATE USER 'dailymotion'@'%' IDENTIFIED BY 'dailymoPass123!';
GRANT ALL ON `registrationdb`.* TO 'dailymotion'@'%' ;

USE registrationdb;
--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;

CREATE TABLE `client` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL UNIQUE,
  `email` varchar(255) NOT NULL UNIQUE,
  `password` varchar(255) NOT NULL,
  `firstname` varchar(255) DEFAULT '0X00',
  `famillyname` varchar(255) DEFAULT '0X00',
  `address` varchar(255) DEFAULT '0X00',
  `phone` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
);