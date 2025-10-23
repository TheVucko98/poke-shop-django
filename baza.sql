CREATE DATABASE  IF NOT EXISTS `pokeprodavnica` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pokeprodavnica`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: pokeprodavnica
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS auth_group;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_group (
  id int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES auth_group WRITE;
/*!40000 ALTER TABLE auth_group DISABLE KEYS */;
INSERT INTO auth_group VALUES (1,'moderator'),(2,'registrovanKorisnik');
/*!40000 ALTER TABLE auth_group ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS auth_group_permissions;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_group_permissions (
  id bigint NOT NULL AUTO_INCREMENT,
  group_id int NOT NULL,
  permission_id int NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY auth_group_permissions_group_id_permission_id_0cd325b0_uniq (group_id,permission_id),
  KEY auth_group_permissio_permission_id_84c5c92e_fk_auth_perm (permission_id),
  CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES auth_permission (id),
  CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group (id)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES auth_group_permissions WRITE;
/*!40000 ALTER TABLE auth_group_permissions DISABLE KEYS */;
INSERT INTO auth_group_permissions VALUES (12,1,21),(13,1,22),(14,1,23),(15,1,24),(16,1,25),(17,1,27),(18,1,28),(1,1,32),(2,1,33),(3,1,35),(4,1,36),(5,1,37),(6,1,38),(7,1,39),(8,1,40),(9,1,41),(10,1,42),(11,1,44),(29,2,24),(30,2,29),(31,2,31),(19,2,32),(20,2,33),(21,2,35),(22,2,36),(23,2,37),(24,2,38),(25,2,39),(26,2,40),(27,2,41),(28,2,42);
/*!40000 ALTER TABLE auth_group_permissions ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS auth_permission;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_permission (
  id int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  content_type_id int NOT NULL,
  codename varchar(100) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY auth_permission_content_type_id_codename_01ab375a_uniq (content_type_id,codename),
  CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES django_content_type (id)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES auth_permission WRITE;
/*!40000 ALTER TABLE auth_permission DISABLE KEYS */;
INSERT INTO auth_permission VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add karta',6,'add_karta'),(22,'Can change karta',6,'change_karta'),(23,'Can delete karta',6,'delete_karta'),(24,'Can view karta',6,'view_karta'),(25,'Can add registrovan korisnik',7,'add_registrovankorisnik'),(26,'Can change registrovan korisnik',7,'change_registrovankorisnik'),(27,'Can delete registrovan korisnik',7,'delete_registrovankorisnik'),(28,'Can view registrovan korisnik',7,'view_registrovankorisnik'),(29,'Can add informacije porudzbine',8,'add_informacijeporudzbine'),(30,'Can change informacije porudzbine',8,'change_informacijeporudzbine'),(31,'Can delete informacije porudzbine',8,'delete_informacijeporudzbine'),(32,'Can view informacije porudzbine',8,'view_informacijeporudzbine'),(33,'Can add korpa',9,'add_korpa'),(34,'Can change korpa',9,'change_korpa'),(35,'Can delete korpa',9,'delete_korpa'),(36,'Can view korpa',9,'view_korpa'),(37,'Can add lista zelja',10,'add_listazelja'),(38,'Can change lista zelja',10,'change_listazelja'),(39,'Can delete lista zelja',10,'delete_listazelja'),(40,'Can view lista zelja',10,'view_listazelja'),(41,'Can add je ocenio',11,'add_jeocenio'),(42,'Can change je ocenio',11,'change_jeocenio'),(43,'Can delete je ocenio',11,'delete_jeocenio'),(44,'Can view je ocenio',11,'view_jeocenio');
/*!40000 ALTER TABLE auth_permission ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS django_admin_log;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_admin_log (
  id int NOT NULL AUTO_INCREMENT,
  action_time datetime(6) NOT NULL,
  object_id longtext,
  object_repr varchar(200) NOT NULL,
  action_flag smallint unsigned NOT NULL,
  change_message longtext NOT NULL,
  content_type_id int DEFAULT NULL,
  user_id bigint NOT NULL,
  PRIMARY KEY (id),
  KEY django_admin_log_content_type_id_c4bce8eb_fk_django_co (content_type_id),
  KEY django_admin_log_user_id_c564eba6_fk_RegistrovanKorisnik_id (user_id),
  CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES django_content_type (id),
  CONSTRAINT django_admin_log_user_id_c564eba6_fk_RegistrovanKorisnik_id FOREIGN KEY (user_id) REFERENCES registrovankorisnik (id),
  CONSTRAINT django_admin_log_chk_1 CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES django_admin_log WRITE;
/*!40000 ALTER TABLE django_admin_log DISABLE KEYS */;
INSERT INTO django_admin_log VALUES (1,'2024-05-27 22:29:54.933401','1','moderator',1,'[{\"added\": {}}]',3,1),(2,'2024-05-27 22:31:49.617092','2','registrovanKorisnik',1,'[{\"added\": {}}]',3,1),(3,'2024-05-27 22:32:15.289235','1','admin',2,'[{\"changed\": {\"fields\": [\"Groups\", \"Profile picture\"]}}]',7,1),(4,'2024-05-27 22:32:22.101622','2','nikola123',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',7,1);
/*!40000 ALTER TABLE django_admin_log ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS django_content_type;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_content_type (
  id int NOT NULL AUTO_INCREMENT,
  app_label varchar(100) NOT NULL,
  model varchar(100) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY django_content_type_app_label_model_76bd3d3b_uniq (app_label,model)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES django_content_type WRITE;
/*!40000 ALTER TABLE django_content_type DISABLE KEYS */;
INSERT INTO django_content_type VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(8,'PSI_DUCK','informacijeporudzbine'),(11,'PSI_DUCK','jeocenio'),(6,'PSI_DUCK','karta'),(9,'PSI_DUCK','korpa'),(10,'PSI_DUCK','listazelja'),(7,'PSI_DUCK','registrovankorisnik'),(5,'sessions','session');
/*!40000 ALTER TABLE django_content_type ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS django_migrations;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_migrations (
  id bigint NOT NULL AUTO_INCREMENT,
  app varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  applied datetime(6) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES django_migrations WRITE;
/*!40000 ALTER TABLE django_migrations DISABLE KEYS */;
INSERT INTO django_migrations VALUES (1,'contenttypes','0001_initial','2024-05-27 22:10:58.333879'),(2,'contenttypes','0002_remove_content_type_name','2024-05-27 22:10:58.430040'),(3,'auth','0001_initial','2024-05-27 22:10:58.771918'),(4,'auth','0002_alter_permission_name_max_length','2024-05-27 22:10:58.863563'),(5,'auth','0003_alter_user_email_max_length','2024-05-27 22:10:58.873552'),(6,'auth','0004_alter_user_username_opts','2024-05-27 22:10:58.881573'),(7,'auth','0005_alter_user_last_login_null','2024-05-27 22:10:58.888885'),(8,'auth','0006_require_contenttypes_0002','2024-05-27 22:10:58.891936'),(9,'auth','0007_alter_validators_add_error_messages','2024-05-27 22:10:58.897984'),(10,'auth','0008_alter_user_username_max_length','2024-05-27 22:10:58.905177'),(11,'auth','0009_alter_user_last_name_max_length','2024-05-27 22:10:58.909177'),(12,'auth','0010_alter_group_name_max_length','2024-05-27 22:10:58.919059'),(13,'auth','0011_update_proxy_permissions','2024-05-27 22:10:58.924048'),(14,'auth','0012_alter_user_first_name_max_length','2024-05-27 22:10:58.927051'),(15,'PSI_DUCK','0001_initial','2024-05-27 22:11:00.086480'),(16,'admin','0001_initial','2024-05-27 22:11:00.249874'),(17,'admin','0002_logentry_remove_auto_add','2024-05-27 22:11:00.256980'),(18,'admin','0003_logentry_add_action_flag_choices','2024-05-27 22:11:00.262679'),(19,'sessions','0001_initial','2024-05-27 22:11:00.311855'),(20,'PSI_DUCK','0002_alter_korpa_brojartikala','2024-05-27 22:34:22.116925');
/*!40000 ALTER TABLE django_migrations ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS django_session;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_session (
  session_key varchar(40) NOT NULL,
  session_data longtext NOT NULL,
  expire_date datetime(6) NOT NULL,
  PRIMARY KEY (session_key),
  KEY django_session_expire_date_a5c62663 (expire_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES django_session WRITE;
/*!40000 ALTER TABLE django_session DISABLE KEYS */;
INSERT INTO django_session VALUES ('8xvmhness3jjyk8ir2ec7kgfmn4uhqlw','.eJxVjMsOwiAQRf-FtSEDlJdL934DGQaQqoGktCvjv2uTLnR7zzn3xQJuaw3byEuYEzszyU6_W0R65LaDdMd265x6W5c58l3hBx382lN-Xg7376DiqN9aWTDFOW9EKkXDlKTXEslnoeKkbBRgM2pFINBHMCaSkQBEpiRNVBx7fwDLozfJ:1sBj1c:1iry6cI8TroDuYaV2kFd4xADtbPVerZ83ncSXoX_FO0','2024-06-10 22:41:04.673473'),('xw4hiry74cyemme8bglpx1mq4h7iz1es','.eJxVjEEOwiAQRe_C2hCm7VB06b5nIMwMSNVAUtqV8e7apAvd_vfefykftjX7rcXFz6IuCtTpd6PAj1h2IPdQblVzLesyk94VfdCmpyrxeT3cv4McWv7WZ4GOiIzl3o4SBzTWBgeAJqGTZB1SisahY2DokRNBnzozoAuMYwT1_gDafTea:1sBikh:uE1xbuFyPVxDj9jgWOG4WLZYYI2JkWbsbK_wTyl2ITI','2024-06-10 22:23:35.266859');
/*!40000 ALTER TABLE django_session ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `informacijeporudzbine`
--

DROP TABLE IF EXISTS informacijeporudzbine;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE informacijeporudzbine (
  id bigint NOT NULL AUTO_INCREMENT,
  datum date NOT NULL,
  ime varchar(20) NOT NULL,
  prezime varchar(20) NOT NULL,
  adresa varchar(100) NOT NULL,
  grad varchar(20) NOT NULL,
  drzava varchar(20) NOT NULL,
  korisnik_id bigint NOT NULL,
  PRIMARY KEY (id),
  KEY InformacijePorudzbin_korisnik_id_3d0ed0a1_fk_Registrov (korisnik_id),
  CONSTRAINT InformacijePorudzbin_korisnik_id_3d0ed0a1_fk_Registrov FOREIGN KEY (korisnik_id) REFERENCES registrovankorisnik (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `informacijeporudzbine`
--

LOCK TABLES informacijeporudzbine WRITE;
/*!40000 ALTER TABLE informacijeporudzbine DISABLE KEYS */;
INSERT INTO informacijeporudzbine VALUES (1,'2024-05-28','','','Default Address','Default City','Default Country',2);
/*!40000 ALTER TABLE informacijeporudzbine ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jeocenio`
--

DROP TABLE IF EXISTS jeocenio;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE jeocenio (
  id bigint NOT NULL AUTO_INCREMENT,
  ocena int NOT NULL,
  karta_id bigint NOT NULL,
  korisnik_id bigint NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY jeOcenio_karta_id_korisnik_id_05fe90d1_uniq (karta_id,korisnik_id),
  KEY jeOcenio_korisnik_id_8eb34c7e_fk_RegistrovanKorisnik_id (korisnik_id),
  CONSTRAINT jeOcenio_karta_id_aef11a62_fk_Karta_id FOREIGN KEY (karta_id) REFERENCES karta (id),
  CONSTRAINT jeOcenio_korisnik_id_8eb34c7e_fk_RegistrovanKorisnik_id FOREIGN KEY (korisnik_id) REFERENCES registrovankorisnik (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jeocenio`
--

LOCK TABLES jeocenio WRITE;
/*!40000 ALTER TABLE jeocenio DISABLE KEYS */;
/*!40000 ALTER TABLE jeocenio ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `karta`
--

DROP TABLE IF EXISTS karta;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE karta (
  id bigint NOT NULL AUTO_INCREMENT,
  naziv varchar(20) NOT NULL,
  cena double NOT NULL,
  opis varchar(255) NOT NULL,
  brPrimeraka int NOT NULL,
  brLajkova int NOT NULL,
  brDislajkova int NOT NULL,
  slika varchar(100) DEFAULT NULL,
  popust int NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `karta`
--

LOCK TABLES karta WRITE;
/*!40000 ALTER TABLE karta DISABLE KEYS */;
INSERT INTO karta VALUES (1,'Pikachu',213,'Munjeviti pokemon',5,0,0,'imgs/pikachu_aYIqWog.png',0),(2,'Onix',70,'asdfasf',4,0,0,'imgs/onix.png',0);
/*!40000 ALTER TABLE karta ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `korpa`
--

DROP TABLE IF EXISTS korpa;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE korpa (
  id bigint NOT NULL AUTO_INCREMENT,
  brojArtikala int NOT NULL,
  karta_id bigint NOT NULL,
  porudzbina_id bigint NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY Korpa_porudzbina_id_karta_id_bedcbaad_uniq (porudzbina_id,karta_id),
  KEY Korpa_karta_id_36a2faca_fk_Karta_id (karta_id),
  CONSTRAINT Korpa_karta_id_36a2faca_fk_Karta_id FOREIGN KEY (karta_id) REFERENCES karta (id),
  CONSTRAINT Korpa_porudzbina_id_285661dd_fk_InformacijePorudzbine_id FOREIGN KEY (porudzbina_id) REFERENCES informacijeporudzbine (id)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `korpa`
--

LOCK TABLES korpa WRITE;
/*!40000 ALTER TABLE korpa DISABLE KEYS */;
INSERT INTO korpa VALUES (5,1,2,1),(6,2,1,1);
/*!40000 ALTER TABLE korpa ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `listazelja`
--

DROP TABLE IF EXISTS listazelja;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE listazelja (
  id bigint NOT NULL AUTO_INCREMENT,
  karta_id bigint NOT NULL,
  korisnik_id bigint NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY ListaZelja_karta_id_korisnik_id_f213f3ea_uniq (karta_id,korisnik_id),
  KEY ListaZelja_korisnik_id_8f8838d7_fk_RegistrovanKorisnik_id (korisnik_id),
  CONSTRAINT ListaZelja_karta_id_902bf50e_fk_Karta_id FOREIGN KEY (karta_id) REFERENCES karta (id),
  CONSTRAINT ListaZelja_korisnik_id_8f8838d7_fk_RegistrovanKorisnik_id FOREIGN KEY (korisnik_id) REFERENCES registrovankorisnik (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `listazelja`
--

LOCK TABLES listazelja WRITE;
/*!40000 ALTER TABLE listazelja DISABLE KEYS */;
/*!40000 ALTER TABLE listazelja ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registrovankorisnik`
--

DROP TABLE IF EXISTS registrovankorisnik;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE registrovankorisnik (
  id bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  last_login datetime(6) DEFAULT NULL,
  is_superuser tinyint(1) NOT NULL,
  username varchar(150) NOT NULL,
  first_name varchar(150) NOT NULL,
  last_name varchar(150) NOT NULL,
  email varchar(254) NOT NULL,
  is_staff tinyint(1) NOT NULL,
  is_active tinyint(1) NOT NULL,
  date_joined datetime(6) NOT NULL,
  slika varchar(100) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY username (username)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registrovankorisnik`
--

LOCK TABLES registrovankorisnik WRITE;
/*!40000 ALTER TABLE registrovankorisnik DISABLE KEYS */;
INSERT INTO registrovankorisnik VALUES (1,'pbkdf2_sha256$720000$vJvGYQDXvhP2gptBRFiXsV$S9ck70BKr6ieJljC2KOB0cglLR1t3EYCO+caD5/48ps=','2024-05-27 22:40:17.923353',1,'admin','','','',1,1,'2024-05-27 22:23:30.000000','imgs/logo_89np68g.png'),(2,'pbkdf2_sha256$720000$Ok9KdfAwI500ZtohvAIqlk$sKXSZg0N0HQJJ5Q7ZbwoGjHL/M/nJjW7X8Wx9P/2j6k=','2024-05-27 22:41:04.671473',0,'nikola123','','','',0,1,'2024-05-27 22:24:43.000000','imgs/logo_76kwdcY.png');
/*!40000 ALTER TABLE registrovankorisnik ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registrovankorisnik_groups`
--

DROP TABLE IF EXISTS registrovankorisnik_groups;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE registrovankorisnik_groups (
  id bigint NOT NULL AUTO_INCREMENT,
  registrovankorisnik_id bigint NOT NULL,
  group_id int NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY RegistrovanKorisnik_grou_registrovankorisnik_id_g_8790c4f8_uniq (registrovankorisnik_id,group_id),
  KEY RegistrovanKorisnik_groups_group_id_339a5b8d_fk_auth_group_id (group_id),
  CONSTRAINT RegistrovanKorisnik__registrovankorisnik__0cf45b23_fk_Registrov FOREIGN KEY (registrovankorisnik_id) REFERENCES registrovankorisnik (id),
  CONSTRAINT RegistrovanKorisnik_groups_group_id_339a5b8d_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group (id)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registrovankorisnik_groups`
--

LOCK TABLES registrovankorisnik_groups WRITE;
/*!40000 ALTER TABLE registrovankorisnik_groups DISABLE KEYS */;
INSERT INTO registrovankorisnik_groups VALUES (1,1,1),(2,2,2);
/*!40000 ALTER TABLE registrovankorisnik_groups ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registrovankorisnik_user_permissions`
--

DROP TABLE IF EXISTS registrovankorisnik_user_permissions;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE registrovankorisnik_user_permissions (
  id bigint NOT NULL AUTO_INCREMENT,
  registrovankorisnik_id bigint NOT NULL,
  permission_id int NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY RegistrovanKorisnik_user_registrovankorisnik_id_p_f162d7f4_uniq (registrovankorisnik_id,permission_id),
  KEY RegistrovanKorisnik__permission_id_d0adfcf4_fk_auth_perm (permission_id),
  CONSTRAINT RegistrovanKorisnik__permission_id_d0adfcf4_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES auth_permission (id),
  CONSTRAINT RegistrovanKorisnik__registrovankorisnik__f1ee191b_fk_Registrov FOREIGN KEY (registrovankorisnik_id) REFERENCES registrovankorisnik (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registrovankorisnik_user_permissions`
--

LOCK TABLES registrovankorisnik_user_permissions WRITE;
/*!40000 ALTER TABLE registrovankorisnik_user_permissions DISABLE KEYS */;
/*!40000 ALTER TABLE registrovankorisnik_user_permissions ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-28  1:04:42