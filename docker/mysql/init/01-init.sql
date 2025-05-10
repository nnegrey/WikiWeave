CREATE DATABASE IF NOT EXISTS wikiweave;
USE wikiweave;

CREATE TABLE `page` (
  `page_id` int unsigned NOT NULL AUTO_INCREMENT,
  `page_namespace` int NOT NULL DEFAULT '0',
  `page_title` varbinary(255) NOT NULL DEFAULT '',
  `page_is_redirect` tinyint unsigned NOT NULL DEFAULT '0',
  `page_random` double unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`page_id`),
  UNIQUE KEY `page_name_title` (`page_namespace`,`page_title`),
  KEY `page_random` (`page_random`)
) ENGINE=InnoDB DEFAULT CHARSET=binary ROW_FORMAT=COMPRESSED;

CREATE TABLE `pagelinks` (
  `pl_from` int unsigned NOT NULL DEFAULT '0',
  `pl_target_id` bigint unsigned NOT NULL,
  PRIMARY KEY (`pl_from`,`pl_target_id`),
  KEY `pl_target_id` (`pl_target_id`,`pl_from`)
) ENGINE=InnoDB DEFAULT CHARSET=binary ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8;

CREATE TABLE `linktarget` (
  `lt_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `lt_namespace` int NOT NULL,
  `lt_title` varbinary(255) NOT NULL,
  PRIMARY KEY (`lt_id`),
  UNIQUE KEY `lt_namespace_title` (`lt_namespace`,`lt_title`)
) ENGINE=InnoDB DEFAULT CHARSET=binary;

CREATE TABLE `page_embeddings` (
  `title` varchar(255) DEFAULT NULL,
  `content` text,
  `embedding` json DEFAULT NULL,
  KEY `idx_title` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;