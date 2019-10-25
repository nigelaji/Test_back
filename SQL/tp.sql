-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'tp_user_role'
-- 用户角色关联表
-- ---

DROP TABLE IF EXISTS `tp_user_role`;

CREATE TABLE `tp_user_role` (
  `id` INTEGER NULL DEFAULT NULL,
  `user_code` VARCHAR(20) NULL,
  `role_id` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) COMMENT '用户角色关联表';

-- ---
-- Table 'tp_user'
-- 测试平台用户表
-- ---

DROP TABLE IF EXISTS `tp_user`;

CREATE TABLE `tp_user` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `user_name` VARCHAR(20) NULL,
  `user_code` VARCHAR(20) NULL,
  `password` VARCHAR(20) NOT NULL,
  `email` VARCHAR(20) NOT NULL COMMENT '邮箱不为空',
  `phone` VARCHAR(11) NULL DEFAULT NULL,
  `create_time` DATETIME NULL,
  `update_time` DATETIME NULL DEFAULT NULL,
  `status` CHAR(1) NULL DEFAULT '"1"' COMMENT '是否删除，1是正常，0是被删除',
  `locked` CHAR(1) NULL DEFAULT '"1"' COMMENT '是否被锁定，1是正常，0是被锁定',
  `locked_date` DATETIME NULL DEFAULT NULL COMMENT '锁定时间',
  `unlocked_date` DATETIME NULL DEFAULT NULL COMMENT '解锁时间',
  `login_fail` INTEGER NULL DEFAULT 0 COMMENT '登录失败次数',
  PRIMARY KEY (`id`, `user_code`)
) COMMENT '测试平台用户表';

-- ---
-- Table 'tp_role'
-- 测试平台角色表
-- ---

DROP TABLE IF EXISTS `tp_role`;

CREATE TABLE `tp_role` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `role_name` VARCHAR(20) NOT NULL COMMENT '角色名称',
  `introduction` VARCHAR(200) NULL DEFAULT NULL COMMENT '角色介绍',
  PRIMARY KEY (`id`)
) COMMENT '测试平台角色表';

-- ---
-- Table 'tp_menu'
-- 菜单表
-- ---

DROP TABLE IF EXISTS `tp_menu`;

CREATE TABLE `tp_menu` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `menu_name` INTEGER NULL DEFAULT NULL,
  `menu_url` VARCHAR NULL DEFAULT NULL,
  `icon_class` VARCHAR(30) NULL DEFAULT NULL,
  `status` CHAR NULL DEFAULT '"1"',
  `parent_menu_id` INTEGER NULL DEFAULT NULL COMMENT '父菜单id',
  PRIMARY KEY (`id`)
) COMMENT '菜单表';

-- ---
-- Table 'tp_role_menu'
-- 角色菜单关联表
-- ---

DROP TABLE IF EXISTS `tp_role_menu`;

CREATE TABLE `tp_role_menu` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `role_id` INTEGER NULL,
  `menu_id` INTEGER NULL,
  PRIMARY KEY (`id`)
) COMMENT '角色菜单关联表';

-- ---
-- Foreign Keys
-- ---

ALTER TABLE `tp_user_role` ADD FOREIGN KEY (user_code) REFERENCES `tp_user` (`user_code`);
ALTER TABLE `tp_user_role` ADD FOREIGN KEY (role_id) REFERENCES `tp_role` (`id`);
ALTER TABLE `tp_role_menu` ADD FOREIGN KEY (role_id) REFERENCES `tp_user_role` (`id`);
ALTER TABLE `tp_role_menu` ADD FOREIGN KEY (menu_id) REFERENCES `tp_menu` (`id`);

-- ---
-- Table Properties
-- ---

-- ALTER TABLE `tp_user_role` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `tp_user` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `tp_role` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `tp_menu` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `tp_role_menu` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `tp_user_role` (`id`,`user_code`,`role_id`) VALUES
-- ('','','');
-- INSERT INTO `tp_user` (`id`,`user_name`,`user_code`,`password`,`email`,`phone`,`create_time`,`update_time`,`status`,`locked`,`locked_date`,`unlocked_date`,`login_fail`) VALUES
-- ('','','','','','','','','','','','','');
-- INSERT INTO `tp_role` (`id`,`role_name`,`introduction`) VALUES
-- ('','','');
-- INSERT INTO `tp_menu` (`id`,`menu_name`,`menu_url`,`icon_class`,`status`,`parent_menu_id`) VALUES
-- ('','','','','','');
-- INSERT INTO `tp_role_menu` (`id`,`role_id`,`menu_id`) VALUES
-- ('','','');