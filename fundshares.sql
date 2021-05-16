/*
 Navicat Premium Data Transfer

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 80015
 Source Host           : localhost:3306
 Source Schema         : fund

 Target Server Type    : MySQL
 Target Server Version : 80015
 File Encoding         : 65001

 Date: 04/02/2021 17:07:47
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for fundshares
-- ----------------------------
DROP TABLE IF EXISTS `fundshares`;
CREATE TABLE `fundshares`  (
  `fundSharesId` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '股票代码',
  `fundSharesName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '股票名称',
  `fundSharesMoney` double(255, 2) NULL DEFAULT NULL COMMENT '金额（万元）',
  UNIQUE INDEX `unique`(`fundSharesId`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of fundshares
-- ----------------------------
INSERT INTO `fundshares` VALUES ('1', '1', 2.00);

SET FOREIGN_KEY_CHECKS = 1;
