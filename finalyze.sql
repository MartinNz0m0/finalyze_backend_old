-- MySQL dump 10.13  Distrib 8.0.33, for Linux (x86_64)
--
-- Host: localhost    Database: finalyze
-- ------------------------------------------------------
-- Server version	8.0.33-0ubuntu0.22.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bankusermodel`
--

DROP TABLE IF EXISTS `bankusermodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bankusermodel` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `details` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `date_added` datetime DEFAULT NULL,
  `statement_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bankusermodel`
--

LOCK TABLES `bankusermodel` WRITE;
/*!40000 ALTER TABLE `bankusermodel` DISABLE KEYS */;
INSERT INTO `bankusermodel` VALUES (1,'marto','MPESA BANK COMMISSION','Transcation Costs','2023-04-21 00:00:00','cooperative'),(2,'marto','SAFARICOM','Transcation Costs','2023-04-21 00:00:00','cooperative'),(3,'marto','COMM. PAYMENT','Transcation Costs','2023-04-21 00:00:00','cooperative'),(4,'marto','EXCISE DUTY','Transcation Costs','2023-04-21 00:00:00','cooperative');
/*!40000 ALTER TABLE `bankusermodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data`
--

DROP TABLE IF EXISTS `data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `data` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `pdf_name` varchar(100) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `date_uploaded` varchar(100) DEFAULT NULL,
  `statement_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data`
--

LOCK TABLES `data` WRITE;
/*!40000 ALTER TABLE `data` DISABLE KEYS */;
INSERT INTO `data` VALUES (1,'marto','MPESA_Statement_2023-01-01_to_2023-01-31_2547xxxxxx607.pdf','2023-01-01 - 2023-01-31','Sat Apr 01 2023 08:39:41 GMT+0300 (East Africa Time)','mpesa'),(2,'marto','MPESA_Statement_2023-02-01_to_2023-02-27_2547xxxxxx607.pdf','2023-02-01 - 2023-02-27','Sat Apr 01 2023 09:19:45 GMT+0300 (East Africa Time)','mpesa'),(5,'marto','MPESA_Statement_2023-03-01_to_2023-03-31_2547xxxxxx607.pdf','2023-03-01 - 2023-03-31','Sun Apr 09 2023 09:11:46 GMT+0300 (East Africa Time)','mpesa'),(6,'sage','MPESA_Statement_2023-02-01_to_2023-02-22_2547xxxxxx364.pdf','2023-02-01 - 2023-02-22','Sun Apr 09 2023 14:12:57 GMT+0300 (East Africa Time)','mpesa'),(7,'sage','MPESA_Statement_2021-02-23_to_2023-02-23_2547xxxxxx364.pdf','2021-02-23 - 2023-02-23','Sun Apr 09 2023 14:17:32 GMT+0300 (East Africa Time)','mpesa'),(15,'marto','MPESA_Statement_2023-04-01_to_2023-05-01_2547xxxxxx607.pdf','2023-04-01 - 2023-05-01','Mon May 01 2023 21:32:47 GMT+0300 (East Africa Time)','mpesa'),(33,'marto','AccountStatement36653223_01MAY2023_21411314.pdf','01 April 2023 to 01 May 2023','Thu May 18 2023 19:54:41 GMT+0300 (East Africa Time)','coop'),(39,'marto','statementequity.pdf','30 December 2022 to 14 March 2023','Sat May 20 2023 08:36:29 GMT+0300 (East Africa Time)','equity'),(40,'demo','demo-mpesa','2023-04-01 - 2023-05-01','2023-05-20','mpesa'),(41,'demo','demo-coop','01 April 2023 to 01 May 2023','2023-05-20','coop'),(42,'demo','demo-equity','14 February 2023 to 14 March 2023','2023-05-20','equity');
/*!40000 ALTER TABLE `data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usermodel`
--

DROP TABLE IF EXISTS `usermodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usermodel` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `details` varchar(255) NOT NULL,
  `category` varchar(255) DEFAULT NULL,
  `date_added` date NOT NULL,
  `statement_type` varchar(50) DEFAULT NULL,
  `budget` decimal(10,2) DEFAULT NULL,
  `priority` varchar(24) DEFAULT 'medium',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=188 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usermodel`
--

LOCK TABLES `usermodel` WRITE;
/*!40000 ALTER TABLE `usermodel` DISABLE KEYS */;
INSERT INTO `usermodel` VALUES (7,'marto','Merchant Payment to 7822434 - ERIC FRANCIS','Entertainment - misc','2023-04-20','mpesa',1500.00,'low'),(8,'marto','Merchant Payment Fuliza M-Pesa to 7822434 - ERIC FRANCIS','Entertainment - misc','2023-04-20','mpesa',1500.00,'low'),(9,'marto','Merchant Payment to 984686 - SWEET WATERS LIQUOR STORE 5','Entertainment - alchohol','2023-04-20','mpesa',2000.00,'medium'),(10,'marto','Merchant Payment Fuliza M-Pesa to 984686 - SWEET WATERS LIQUOR STORE 5','Entertainment - alchohol','2023-04-20','mpesa',2000.00,'medium'),(11,'marto','Customer Transfer to - 2547******432 KELVIN MASAI','Entertainment - misc','2023-04-20','mpesa',1500.00,'low'),(12,'marto','Customer Transfer Fuliza MPesa to - 2547******432 KELVIN MASAI','Entertainment - misc','2023-04-20','mpesa',1500.00,'low'),(13,'marto','Customer Transfer to - 2547******551 ROBERT MUCHIRI','Entertainment - ngwai','2023-04-20','mpesa',3000.00,'medium'),(14,'marto','Customer Transfer Fuliza MPesa to - 2547******551 ROBERT MUCHIRI','Entertainment - ngwai','2023-04-20','mpesa',3000.00,'medium'),(15,'marto','Customer Transfer to - 2547******822 JACKLINE MUTINDA','Home expense - jackie','2023-04-20','mpesa',2000.00,'medium'),(16,'marto','Customer Transfer Fuliza MPesa to - 2547******822 JACKLINE MUTINDA','Home expense - jackie','2023-04-20','mpesa',2000.00,'medium'),(17,'marto','Merchant Payment to 795596 - Msafiri butchery  V','Home expense - meat','2023-04-20','mpesa',2000.00,'medium'),(18,'marto','Merchant Payment Fuliza M-Pesa to 795596 - Msafiri butchery  V','Home expense - meat','2023-04-20','mpesa',2000.00,'medium'),(19,'marto','Merchant Payment to 7851873 - TEREGO WINES','Entertainment - alchohol','2023-04-20','mpesa',2000.00,'medium'),(20,'marto','Merchant Payment Fuliza M-Pesa to 7851873 - TEREGO WINES','Entertainment - alchohol','2023-04-20','mpesa',2000.00,'medium'),(21,'marto','Merchant Payment to 7214379 - ATLAS WINES AND SPIRIT 3','Entertainment - alchohol','2023-04-20','mpesa',2000.00,'medium'),(22,'marto','Merchant Payment Fuliza M-Pesa to 7214379 - ATLAS WINES AND SPIRIT 3','Entertainment - alchohol','2023-04-20','mpesa',2000.00,'medium'),(23,'marto','Pay Bill to 220220 - PesaPal Acc. 0750594250','Airtime purchase','2023-04-20','mpesa',500.00,'low'),(24,'marto','Pay Bill Fuliza M-Pesa to 220220 - PesaPal Acc. 0750594250','Airtime purchase','2023-04-20','mpesa',500.00,'low'),(25,'marto','Merchant Payment to 7721524 - MAGUNANDU SHOP','Home expense - misc','2023-04-20','mpesa',1000.00,'medium'),(26,'marto','Merchant Payment Fuliza M-Pesa to 7721524 - MAGUNANDU SHOP','Home expense - misc','2023-04-20','mpesa',1000.00,'medium'),(27,'marto','Merchant Payment to 7441596 - NYAMORI SARAH AWUOR','Home expense - misc','2023-04-20','mpesa',1000.00,'medium'),(28,'marto','Merchant Payment Fuliza M-Pesa to 7441596 - NYAMORI SARAH AWUOR','Home expense - misc','2023-04-20','mpesa',1000.00,'medium'),(29,'marto','Merchant Payment to 7031759 - WA MALIMALI GEN SHOP','Home expense - misc','2023-04-20','mpesa',1000.00,'medium'),(30,'marto','Merchant Payment Fuliza M-Pesa to 7031759 - WA MALIMALI GEN SHOP','Home expense - misc','2023-04-20','mpesa',1000.00,'medium'),(31,'marto','Customer Transfer to - 2547******239 BONFACE IKONZE','Home expense - ocha','2023-04-20','mpesa',10000.00,'high'),(32,'marto','Customer Transfer Fuliza MPesa to - 2547******239 BONFACE IKONZE','Home expense - ocha','2023-04-20','mpesa',10000.00,'high'),(37,'marto','Customer Transfer to - 2547******526 Leon Kioko','Entertainment - ngwai','2023-04-25','mpesa',3000.00,'medium'),(38,'marto','Customer Transfer Fuliza MPesa to - 2547******526 Leon Kioko','Entertainment - ngwai','2023-04-25','mpesa',3000.00,'medium'),(39,'marto','Customer Transfer to - 07******395 Anna Mutinda','Home expense - ocha','2023-04-25','mpesa',10000.00,'high'),(40,'marto','Customer Transfer Fuliza MPesa to - 07******395 Anna Mutinda','Home expense - ocha','2023-04-25','mpesa',10000.00,'high'),(75,'marto','MPESA BANK COMMISSION','Transcation Costs','2023-04-26','coop',500.00,'low'),(76,'marto','SAFARICOM','Transcation Costs','2023-04-26','coop',500.00,'low'),(77,'marto','COMM. PAYMENT','Transcation Costs','2023-04-26','coop',500.00,'low'),(78,'marto','EXCISE DUTY','Transcation Costs','2023-04-26','coop',500.00,'low'),(79,'marto','TRANSFER TO M-PESA 254720930607','Bank to mpesa','2023-04-26','coop',NULL,'medium'),(80,'marto','TRANSFER TO M-PESA 254722897239','Home expense - ocha','2023-04-28','coop',10000.00,'high'),(81,'marto','TRANSFER TO M-PESA 254728382498','Home expense - esther','2023-04-28','coop',5000.00,'medium'),(82,'marto','NellyKhakasaWamalwa >KISERIANKE 30125684028 01108212586000','Cash withdrawal','2023-04-28','coop',5000.00,'low'),(89,'marto','Customer Transfer to - 07******407 Newton Kakethe','Entertainment - ngwai','2023-04-29','mpesa',3000.00,'medium'),(90,'marto','Customer Transfer Fuliza MPesa to - 07******407 Newton Kakethe','Entertainment - ngwai','2023-04-29','mpesa',3000.00,'medium'),(91,'marto','Customer Transfer to - 07******683 Faith Mbalia','Home expense - misc','2023-05-01','mpesa',1000.00,'medium'),(92,'marto','Customer Transfer Fuliza MPesa to - 07******683 Faith Mbalia','Home expense - misc','2023-05-01','mpesa',1000.00,'medium'),(93,'marto','Customer Transfer Fuliza MPesa to - 07******731 Patrick Njuguna','Home expense - misc','2023-05-01','mpesa',1000.00,'medium'),(94,'marto','Customer Transfer to - 07******731 Patrick Njuguna','Home expense - misc','2023-05-01','mpesa',1000.00,'medium'),(95,'marto','Merchant Payment to 7213197 - QUICK MART Kiserian','Entertainment - misc','2023-05-01','mpesa',1500.00,'low'),(96,'marto','Merchant Payment Fuliza M-Pesa to 7213197 - QUICK MART Kiserian','Entertainment - misc','2023-05-01','mpesa',1500.00,'low'),(97,'marto','Customer Transfer to - 2547******364 FIONA NDEGWA','GF money','2023-05-01','mpesa',1500.00,'low'),(98,'marto','Customer Transfer Fuliza MPesa to - 2547******364 FIONA NDEGWA','GF money','2023-05-01','mpesa',1500.00,'low'),(99,'marto','Merchant Payment to 607229 - BAYLEYS BAR AND RESTAURANT......................','Entertainment - misc','2023-05-01','mpesa',1500.00,'low'),(100,'marto','Merchant Payment Fuliza M-Pesa to 607229 - BAYLEYS BAR AND RESTAURANT......................','Entertainment - misc','2023-05-01','mpesa',1500.00,'low'),(101,'marto','BARLEYSRIMPAGREE N>KISERIANKE 00312360  30125684028 01108212586000','Entertainment - misc','2023-05-01','coop',1500.00,'low'),(102,'marto','TRANSFER TO M-PESA 254712454822','Home expense - jackie','2023-05-01','coop',2000.00,'medium'),(103,'marto','011082125860000038 aliexpress |202 30406','Aliexpress','2023-05-01','coop',2000.00,'low'),(104,'marto','aliexpress>LondonGB','Aliexpress','2023-05-01','coop',2000.00,'low'),(105,'marto','wwwaliexpresscom>LO NDONGB  30125684028 01108212586000','Aliexpress','2023-05-01','coop',2000.00,'low'),(106,'marto','Customer Transfer to - 2547******498 ESTHER MUTINDA','Home expense - esther','2023-05-03','mpesa',5000.00,'medium'),(107,'marto','Customer Transfer Fuliza MPesa to - 2547******498 ESTHER MUTINDA','Home expense - esther','2023-05-03','mpesa',5000.00,'medium'),(134,'marto','Customer Transfer of Funds Charge','Mpesa Transcation Costs','2023-05-04','mpesa',500.00,'low'),(135,'marto','Pay Bill Charge','Mpesa Transcation Costs','2023-05-04','mpesa',500.00,'low'),(136,'marto','Withdrawal Charge','Mpesa Transcation Costs','2023-05-04','mpesa',500.00,'low'),(137,'marto','Pay Merchant Charge','Mpesa Transcation Costs','2023-05-04','mpesa',500.00,'low'),(138,'marto','Customer Transfer of Funds Charges','Mpesa Transcation Costs','2023-05-04','mpesa',500.00,'low'),(139,'marto','Pay Bill Charges','Mpesa Transcation Costs','2023-05-04','mpesa',500.00,'low'),(140,'marto','Withdrawal Charges','Mpesa Transcation Costs','2023-05-04','mpesa',500.00,'low'),(141,'marto','Pay Merchant Charges','Mpesa Transcation Costs','2023-05-04','mpesa',500.00,'low'),(146,'marto','Customer Transfer to - 07******081 john muluka','Weed','2023-05-18','mpesa',2000.00,'low'),(147,'marto','Customer Transfer Fuliza MPesa to - 07******081 john muluka','Weed','2023-05-18','mpesa',2000.00,'low'),(148,'marto','Customer Transfer to - 07******023 charles wamuyu','Weed','2023-05-18','mpesa',2000.00,'low'),(149,'marto','Customer Transfer Fuliza MPesa to - 07******023 charles wamuyu','Weed','2023-05-18','mpesa',2000.00,'low'),(150,'demo','MPESA BANK COMMISSION','Transcation Costs','2023-05-20','coop',500.00,'medium'),(151,'demo','SAFARICOM','Transcation Costs','2023-05-20','coop',500.00,'medium'),(152,'demo','COMM. PAYMENT','Transcation Costs','2023-05-20','coop',500.00,'medium'),(153,'demo','EXCISE DUTY','Transcation Costs','2023-05-20','coop',500.00,'medium'),(165,'demo','Customer Transfer to - 2547******420 Kevin Fisi','Ngwai','2023-05-25','mpesa',1000.00,'medium'),(166,'demo','Customer Transfer Fuliza MPesa to - 2547******420 Kevin Fisi','Ngwai','2023-05-25','mpesa',1000.00,'medium'),(167,'demo','Customer Transfer of Funds Charge','Mpesa Transcation Costs','2023-05-25','mpesa',500.00,'medium'),(168,'demo','Pay Bill Charge','Mpesa Transcation Costs','2023-05-25','mpesa',500.00,'medium'),(169,'demo','Withdrawal Charge','Mpesa Transcation Costs','2023-05-25','mpesa',500.00,'medium'),(170,'demo','Pay Merchant Charge','Mpesa Transcation Costs','2023-05-25','mpesa',500.00,'medium'),(171,'demo','Customer Transfer of Funds Charges','Mpesa Transcation Costs','2023-05-25','mpesa',500.00,'medium'),(172,'demo','Pay Bill Charges','Mpesa Transcation Costs','2023-05-25','mpesa',500.00,'medium'),(173,'demo','Withdrawal Charges','Mpesa Transcation Costs','2023-05-25','mpesa',500.00,'medium'),(174,'demo','Pay Merchant Charges','Mpesa Transcation Costs','2023-05-25','mpesa',500.00,'medium'),(175,'demo','Customer Transfer to - 2547******254 Fatma Sokoni','Groceries','2023-05-26','mpesa',5000.00,'high'),(176,'demo','Customer Transfer Fuliza MPesa to - 2547******254 Fatma Sokoni','Groceries','2023-05-26','mpesa',5000.00,'high'),(177,'demo','Customer Transfer to - 2547******889 Gaddafi Ndungu','Nduthi','2023-05-26','mpesa',500.00,'medium'),(178,'demo','Customer Transfer Fuliza MPesa to - 2547******889 Gaddafi Ndungu','Nduthi','2023-05-26','mpesa',500.00,'medium'),(179,'demo','Merchant Payment to - 6523154 Kwa Base Wines','Alchohol','2023-05-26','mpesa',1500.00,'medium'),(180,'demo','Merchant Payment Fuliza M-Pesa to - 6523154 Kwa Base Wines','Alchohol','2023-05-26','mpesa',1500.00,'medium'),(181,'demo','Merchant Payment to - 6548965 Drinking Water Investments','Home water','2023-05-26','mpesa',1000.00,'high'),(182,'demo','Merchant Payment Fuliza M-Pesa to - 6548965 Drinking Water Investments','Home water','2023-05-26','mpesa',1000.00,'high'),(183,'demo','Customer Transfer to - 2547******546 Simba Kiboko','Smokie / Mayai','2023-05-27','mpesa',2000.00,'low'),(184,'demo','Customer Transfer Fuliza MPesa to - 2547******546 Simba Kiboko','Smokie / Mayai','2023-05-27','mpesa',2000.00,'low'),(185,'demo','MOBILE MONEY CHARGES','Transcation Costs','2023-05-27','equity',500.00,'medium'),(186,'demo','Customer Transfer to - 2547******512 Mary Madeni','mama fua','2023-05-29','mpesa',4000.00,'medium'),(187,'demo','Customer Transfer Fuliza MPesa to - 2547******512 Mary Madeni','Mama fua','2023-05-29','mpesa',4000.00,'medium');
/*!40000 ALTER TABLE `usermodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `hash` varchar(400) NOT NULL,
  `role` varchar(10) DEFAULT 'user',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'TEST','$2a$10$wQw/Xk4lBXlqjvEVU8W37O4qLu2xk.iDW00oZLpI/ZrKmA6iLJKki','user'),(2,'peter','$2a$10$7LWO2.wcuJEr2qjWuvL3feui.WAPZY2eo.SoxspTRSWziEkj0hTHa','user'),(3,'marto','$2a$10$JCZFsJ2dSm2/TKIL9IlZw.ALFliyZERG1Vzt/dKTJQ61sGkuvQZEC','admin'),(4,'ivan','$2a$10$a.l9ZwtYWlBIecp.wZ2vN.QjDb.z89eDKkdv4Jx3tJeK1O6OsabGy','user'),(5,'sage','$2a$10$Z0oVz7lL1hOWBhOGhE71aeVMCr8FhaeGQSW9kxndybiV3GEkecbtW','user'),(6,'demo','$2a$10$CsMmzEwFzy5NDnnSXCA6SezgEkw1jZmuh4aXp6LdWolMKpmpEchBm','user'),(7,'to delete','$2a$10$Aj2ckJWQthZu6Sd7tqCPcOh7rkSLoYm2PLrwV8E2QvYVJj/eW8l9.','user');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-29 17:43:02
