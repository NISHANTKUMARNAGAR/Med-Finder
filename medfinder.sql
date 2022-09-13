/*
SQLyog Community v13.1.7 (64 bit)
MySQL - 10.4.17-MariaDB : Database - medfinder
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`medfinder` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `medfinder`;

/*Table structure for table `admindata` */

DROP TABLE IF EXISTS `admindata`;

CREATE TABLE `admindata` (
  `name` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `admindata` */

insert  into `admindata`(`name`,`address`,`contact`,`email`) values 
('nishant','kota','7559987999','nishant@gmail.com');

/*Table structure for table `logindata` */

DROP TABLE IF EXISTS `logindata`;

CREATE TABLE `logindata` (
  `email` varchar(100) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  `usertype` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `logindata` */

insert  into `logindata`(`email`,`password`,`usertype`) values 
('aman@gmail.com','232f3','medical'),
('amit@gmail.com','s3v34','medical'),
('arun@gmail.com','v33gd','medical'),
('nishant@gmail.com','3564n','admin'),
('rakhi@gmail.com','d1d3d','medical'),
('sunir@gmail.com','878hh','medical');

/*Table structure for table `medicaldata` */

DROP TABLE IF EXISTS `medicaldata`;

CREATE TABLE `medicaldata` (
  `name` varchar(100) DEFAULT NULL,
  `owner` varchar(100) DEFAULT NULL,
  `lno` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `medicaldata` */

insert  into `medicaldata`(`name`,`owner`,`lno`,`address`,`contact`,`email`) values 
('A.H. Medicals','Aman','8pue4f','pune','9645347433','aman@gmail.com'),
('Aadi Medicose','Amit','3jb5sd','jabalpur','6443438874','amit@gmail.com'),
('arun pharma','arun','2dhl2t','jabalpur','9436642674','arun@gmail.com'),
('aunima medicals','rakhi','2rj345','rewa','8534264534','rakhi@gmail.com'),
('Packo Plast','sunir','1gj34f','ahemdabad','9327234546','sunir@gmail.com');

/*Table structure for table `medicine` */

DROP TABLE IF EXISTS `medicine`;

CREATE TABLE `medicine` (
  `med_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `company` varchar(100) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `storeid` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`med_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

/*Data for the table `medicine` */

insert  into `medicine`(`med_id`,`name`,`company`,`price`,`storeid`) values 
(1,'nise','CadexLaboratories',90,'amit@gmail.com'),
(2,'noblespas','Cadila Health Care ltd.',200,'aman@gmail.com'),
(3,'paracetamol','Cachet Pharmeceuticals Pvt. Ltd.',140,'sunir@gmail.com'),
(4,'pudinhara','A.S LifeSciences',110,'arun@gmail.com'),
(5,'sporlac','Aaron Healthcare And Export Pvt. Ltd.',50,'rakhi@gmail.com');

/*Table structure for table `photodata` */

DROP TABLE IF EXISTS `photodata`;

CREATE TABLE `photodata` (
  `email` varchar(100) NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `photodata` */

insert  into `photodata`(`email`,`photo`) values 
('aman@gmail.com','1662568703.jpg'),
('nishant@gmail.com','1662701967.jpeg');

/*Table structure for table `medicine_medical_info` */

DROP TABLE IF EXISTS `medicine_medical_info`;

/*!50001 DROP VIEW IF EXISTS `medicine_medical_info` */;
/*!50001 DROP TABLE IF EXISTS `medicine_medical_info` */;

/*!50001 CREATE TABLE  `medicine_medical_info`(
 `name` varchar(100) ,
 `company` varchar(100) ,
 `price` int(11) ,
 `medical` varchar(100) ,
 `owner` varchar(100) ,
 `address` varchar(100) ,
 `contact` varchar(100) 
)*/;

/*View structure for view medicine_medical_info */

/*!50001 DROP TABLE IF EXISTS `medicine_medical_info` */;
/*!50001 DROP VIEW IF EXISTS `medicine_medical_info` */;

/*!50001 CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `medicine_medical_info` AS (select `medicine`.`name` AS `name`,`medicine`.`company` AS `company`,`medicine`.`price` AS `price`,`medicaldata`.`name` AS `medical`,`medicaldata`.`owner` AS `owner`,`medicaldata`.`address` AS `address`,`medicaldata`.`contact` AS `contact` from (`medicine` join `medicaldata`) where `medicine`.`storeid` = `medicaldata`.`email`) */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
