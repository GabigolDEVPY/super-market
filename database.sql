-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: eccomerce
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `supermarket_cart`
--

LOCK TABLES `supermarket_cart` WRITE;
/*!40000 ALTER TABLE `supermarket_cart` DISABLE KEYS */;
INSERT INTO `supermarket_cart` VALUES (2,'2025-10-20 00:22:20.658465','2025-10-20 00:22:20.658488',2),(4,'2025-10-27 01:16:54.147266','2025-10-27 01:16:54.147291',4);
/*!40000 ALTER TABLE `supermarket_cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `supermarket_cartitem`
--

LOCK TABLES `supermarket_cartitem` WRITE;
/*!40000 ALTER TABLE `supermarket_cartitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `supermarket_cartitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `supermarket_category`
--

LOCK TABLES `supermarket_category` WRITE;
/*!40000 ALTER TABLE `supermarket_category` DISABLE KEYS */;
/*!40000 ALTER TABLE `supermarket_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `supermarket_inventory`
--

LOCK TABLES `supermarket_inventory` WRITE;
/*!40000 ALTER TABLE `supermarket_inventory` DISABLE KEYS */;
/*!40000 ALTER TABLE `supermarket_inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `supermarket_inventoryitem`
--

LOCK TABLES `supermarket_inventoryitem` WRITE;
/*!40000 ALTER TABLE `supermarket_inventoryitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `supermarket_inventoryitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `supermarket_payment_code`
--

LOCK TABLES `supermarket_payment_code` WRITE;
/*!40000 ALTER TABLE `supermarket_payment_code` DISABLE KEYS */;
/*!40000 ALTER TABLE `supermarket_payment_code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `supermarket_product`
--

LOCK TABLES `supermarket_product` WRITE;
/*!40000 ALTER TABLE `supermarket_product` DISABLE KEYS */;
INSERT INTO `supermarket_product` VALUES (1,'calça','calça bonita','2025-10-20 00:21:40.000000',150.00,NULL, NULL),(2,'Tênis','Tênis Masculino Grand Court 2.0 Branco | Adidas','2025-10-25 11:00:26.000000',199.99,NULL, NULL),(3,'Tenis Air fox','Tênis Nike Air Winflo 11 Masculino','2025-10-25 17:38:49.000000',199.99,NULL, NULL);
/*!40000 ALTER TABLE `supermarket_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `supermarket_products`
--

LOCK TABLES `supermarket_products` WRITE;
/*!40000 ALTER TABLE `supermarket_products` DISABLE KEYS */;
/*!40000 ALTER TABLE `supermarket_products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `supermarket_stock`
--

LOCK TABLES `supermarket_stock` WRITE;
/*!40000 ALTER TABLE `supermarket_stock` DISABLE KEYS */;
INSERT INTO `supermarket_stock` VALUES (1,1,'2025-10-25 16:04:19.961869',2),(2,14,'2025-10-27 01:17:36.586395',1),(3,10,'2025-10-25 17:40:22.918531',3);
/*!40000 ALTER TABLE `supermarket_stock` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-28 21:03:46
