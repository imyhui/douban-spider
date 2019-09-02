CREATE TABLE `movies` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `douban_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '豆瓣ID',
  `title` varchar(100) NOT NULL DEFAULT '' COMMENT '电影名',
  `cover` varchar(255) NOT NULL DEFAULT '' COMMENT '背景图',
  `score` float NOT NULL DEFAULT '5.0' COMMENT '评分',
  `year` int(10) unsigned NOT NULL DEFAULT '2018' COMMENT '上映年份',
  `summary` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '剧情简介',
  `director` varchar(100) NOT NULL DEFAULT '' COMMENT '导演',
  `screenwriter` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '编剧',
  `mainactors` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '主演',
  `tags` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '制片国家',
  `countries` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '制片国家',
  `languages` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '语言',
  `release_time` varchar(200) NOT NULL DEFAULT '' COMMENT '上映日期',
  `length` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '片长',
  `imdb_url` varchar(255) NOT NULL DEFAULT '' COMMENT 'IMDb链接',
  `othername` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '又名',
  `evaluation_nums` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '评价数',
  `shortcom_nums` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '短评数字',
  `comment_nums` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '影评数',
  PRIMARY KEY (`id`),
  KEY `idx_db_id` (`douban_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='电影表';

CREATE TABLE `tags` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `movie_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '电影ID',
  `tag_name` varchar(20) NOT NULL DEFAULT '' COMMENT '标签名',
  PRIMARY KEY (`id`),
  KEY `idx_movie_id` (`movie_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='标签表';

CREATE TABLE `screenwriters` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `movie_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '电影ID',
  `screenwriter_name` varchar(50) NOT NULL DEFAULT '' COMMENT '编剧名',
  PRIMARY KEY (`id`),
  KEY `idx_movie_id` (`movie_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='编剧表';

CREATE TABLE `mainactors` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `movie_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '电影ID',
  `mainactor_name` varchar(50) NOT NULL DEFAULT '' COMMENT '主演名',
  PRIMARY KEY (`id`),
  KEY `idx_movie_id` (`movie_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='主演表';