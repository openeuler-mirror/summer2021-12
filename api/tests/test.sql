drop database if exists openeuler_faq;
create database openeuler_faq;
use openeuler_faq;

CREATE TABLE `c_review_status`
(
    `id`   varchar(32)  NOT NULL,
    `type` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`id`)
);

INSERT INTO `c_review_status`
VALUES ('1', 'waiting'),
       ('2', 'allowed'),
       ('3', 'denied'),
       ('4', 'withdrawn');

CREATE TABLE `c_answer_browse_type`
(
    `id`   varchar(32) NOT NULL,
    `type` varchar(100) DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

insert into c_answer_browse_type (id, type)
values ('1', 'browser'),
       ('2', 'like'),
       ('3', 'dislike');

CREATE TABLE `c_answer_level`
(
    `id`    varchar(32)  NOT NULL,
    `level` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

insert into c_answer_level (id, level)
values ('1', 'std'),
       ('2', 'good'),
       ('3', 'deprecated'),
       ('4', 'undetermined'),
       ('5', 'denied');

CREATE TABLE `c_answer_type`
(
    `id`   varchar(32)  NOT NULL,
    `type_name` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

insert into c_answer_type (id, type_name)
values ('1', 'text'),
       ('2', 'video'),
       ('3', 'website');

CREATE TABLE `c_question_browse_type`
(
    `id`   varchar(32) NOT NULL,
    `type` varchar(100) DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

insert into c_question_browse_type (id, type)
values ('1', 'like'),
       ('2', 'dislike');

CREATE TABLE `c_user_role`
(
    `id`   varchar(32)  NOT NULL,
    `type` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

insert into c_user_role (id, type)
values ('1', 'user'),
       ('2', 'reviewer'),
       ('3', 'admin');


CREATE TABLE `e_user`
(
    `id`         varchar(32) NOT NULL,
    `gitee_id`   int          DEFAULT NULL,
    `username`   varchar(50)  DEFAULT NULL,
    `avatar_url` varchar(200) DEFAULT NULL,
    `email`      varchar(200) DEFAULT NULL,
    `html_url`   varchar(200) DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;



DROP TABLE IF EXISTS e_request;
CREATE TABLE `e_request`
(
    `id`            varchar(32) NOT NULL,
    `description`   varchar(200) DEFAULT NULL,
    `author_id`     varchar(32)  DEFAULT NULL,
    `reviewer_id`   varchar(32)  default null,
    `time`          datetime     DEFAULT NULL,
    `review_status` varchar(32) NOT NULL,
    `comment`       varchar(200) DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `e_request_e_user_id_fk` (`author_id`),
    KEY `e_request_e_user_id_fk2` (`reviewer_id`),
    KEY `e_request_c_review_status_id_fk` (`review_status`),
    CONSTRAINT `e_request_c_review_status_id_fk` FOREIGN KEY (`review_status`) REFERENCES `c_review_status` (`id`),
    CONSTRAINT `e_request_e_user_id_fk` FOREIGN KEY (`author_id`) REFERENCES `e_user` (`id`),
    constraint `e_request_e_user_id_fk2` foreign key (`reviewer_id`) references `e_user` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE `e_self_answer`
(
    `id`         varchar(32)  NOT NULL,
    `type_id`    varchar(32)  DEFAULT NULL,
    `summary`    varchar(200) DEFAULT NULL,
    `content`    varchar(200) NOT NULL,
    `request_id` varchar(32)  DEFAULT NULL,
    `review_status` varchar(32) DEFAULT NULL,
    `comment`    VARCHAR(200) DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `e_self_answer_c_answer_type_id_fk` (`type_id`),
    KEY `e_self_answer_e_request_id_fk` (`request_id`),
    KEY `e_self_answer_c_review_status_id_fk` (`review_status`),
    CONSTRAINT `e_self_answer_c_review_status_id_fk` FOREIGN KEY (`review_status`) REFERENCES `c_review_status` (`id`),
    CONSTRAINT `e_self_answer_c_answer_type_id_fk` FOREIGN KEY (`type_id`) REFERENCES `c_answer_type` (`id`),
    CONSTRAINT `e_self_answer_e_request_id_fk` FOREIGN KEY (`request_id`) REFERENCES `e_request` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE `e_question`
(
    `id`              varchar(32) NOT NULL,
    `std_description` varchar(250) DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `question_std_description_uindex` (`std_description`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE `e_answer`
(
    `id`          varchar(32) NOT NULL,
    `type_id`     varchar(32)  DEFAULT NULL,
    `summary`     varchar(200) DEFAULT NULL,
    `content`     varchar(200) DEFAULT NULL,
    `author_id`   varchar(32)  DEFAULT NULL,
    `question_id` varchar(32)  DEFAULT NULL,
    `level_id`    varchar(32)  DEFAULT NULL,
    `reviewer_id` varchar(32) DEFAULT NULL,
    `comment`     VARCHAR(200) DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `answer_c_answer_type_id_fk` (`type_id`),
    KEY `e_answer_e_user_id_fk` (`author_id`),
    KEY `e_answer_e_question_id_fk` (`question_id`),
    KEY `e_answer_c_answer_level_id_fk` (`level_id`),
    KEY `e_answer_e_user_id_fk2` (`reviewer_id`),
    constraint `e_answer_e_user_id_fk2` foreign key (`reviewer_id`) references `e_user` (`id`),
    CONSTRAINT `answer_c_answer_type_id_fk` FOREIGN KEY (`type_id`) REFERENCES `c_answer_type` (`id`),
    CONSTRAINT `e_answer_c_answer_level_id_fk` FOREIGN KEY (`level_id`) REFERENCES `c_answer_level` (`id`),
    CONSTRAINT `e_answer_e_question_id_fk` FOREIGN KEY (`question_id`) REFERENCES `e_question` (`id`),
    CONSTRAINT `e_answer_e_user_id_fk` FOREIGN KEY (`author_id`) REFERENCES `e_user` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE `e_question_description`
(
    `id`          varchar(32)  NOT NULL,
    `description` varchar(200) NOT NULL,
    `question_id` varchar(32) DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `question_description_question_id_fk` (`question_id`),
    CONSTRAINT `question_description_question_id_fk` FOREIGN KEY (`question_id`) REFERENCES `e_question` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE `e_tag`
(
    `id`     varchar(32)  NOT NULL,
    `tag_name` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `tag_name_uindex` (tag_name)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;


CREATE TABLE `e_answer_browse_log`
(
    `id`        varchar(32) NOT NULL,
    `time`      datetime    DEFAULT NULL,
    `type_id`   varchar(32) DEFAULT NULL,
    `answer_id` varchar(32) DEFAULT NULL,
    `user_id`   varchar(32) DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `e_answer_browse_log_e_answer_id_fk` (`answer_id`),
    KEY `e_answer_browse_log_e_user_id_fk` (`user_id`),
    KEY `e_answer_browse_log_c_answer_browse_type_id_fk` (`type_id`),
    CONSTRAINT `e_answer_browse_log_c_answer_browse_type_id_fk` FOREIGN KEY (`type_id`) REFERENCES `c_answer_browse_type` (`id`),
    CONSTRAINT `e_answer_browse_log_e_answer_id_fk` FOREIGN KEY (`answer_id`) REFERENCES `e_answer` (`id`),
    CONSTRAINT `e_answer_browse_log_e_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `e_user` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE `e_questioning_log`
(
    `id`                  varchar(32) NOT NULL,
    `type_id`             varchar(32)  DEFAULT NULL,
    `op_time`             datetime     DEFAULT NULL,
    `matched_question_id` varchar(32)  DEFAULT NULL,
    `user_id`             varchar(32)  DEFAULT NULL,
    `user_question`       varchar(100) DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `e_question_browse_log_c_question__browse_type_id_fk` (`type_id`),
    KEY `e_question_browse_log_e_question_id_fk` (`matched_question_id`),
    KEY `e_question_browse_log_e_user_id_fk` (`user_id`),
    CONSTRAINT `e_question_browse_log_c_question__browse_type_id_fk` FOREIGN KEY (`type_id`) REFERENCES `c_question_browse_type` (`id`),
    CONSTRAINT `e_question_browse_log_e_question_id_fk` FOREIGN KEY (`matched_question_id`) REFERENCES `e_question` (`id`),
    CONSTRAINT `e_question_browse_log_e_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `e_user` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;


CREATE TABLE `r_question_tagging`
(
    `id`          varchar(32) NOT NULL,
    `question_id` varchar(32) DEFAULT NULL,
    `tag_id`      varchar(32) DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `r_tagging_question_id_fk` (`question_id`),
    KEY `r_tagging_tag_id_fk` (`tag_id`),
    CONSTRAINT `r_tagging_question_id_fk` FOREIGN KEY (`question_id`) REFERENCES `e_question` (`id`),
    CONSTRAINT `r_tagging_tag_id_fk` FOREIGN KEY (`tag_id`) REFERENCES `e_tag` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE `r_request_tagging`
(
    `id`         varchar(32) NOT NULL,
    `tag_id`     varchar(32) NOT NULL,
    `request_id` varchar(32) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `r_request_tagging_e_request_id_fk` (`request_id`),
    KEY `r_request_tagging_e_tag_id_fk` (`tag_id`),
    CONSTRAINT `r_request_tagging_e_request_id_fk` FOREIGN KEY (`request_id`) REFERENCES `e_request` (`id`),
    CONSTRAINT `r_request_tagging_e_tag_id_fk` FOREIGN KEY (`tag_id`) REFERENCES `e_tag` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE `r_role_attaching`
(
    `id`      varchar(32) NOT NULL,
    `user_id` varchar(32) DEFAULT NULL,
    `role_id` varchar(32) DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `r_role_attaching_c_user_role_id_fk` (`role_id`),
    KEY `r_role_attaching_e_user_id_fk` (`user_id`),
    CONSTRAINT `r_role_attaching_c_user_role_id_fk` FOREIGN KEY (`role_id`) REFERENCES `c_user_role` (`id`),
    CONSTRAINT `r_role_attaching_e_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `e_user` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

INSERT INTO e_user(id, gitee_id, username, avatar_url, email, html_url)
VALUES ('1', 820, 'admin', 'gntbb', 'nlfoz', 'tkkth'),
       ('2', 599, 'reviewer_yy', 'ixhpq', 'youngyee620@gmail.com', 'enggw'),
       ('3', 975, 'reviewer_tt', 'tkmik', 'youngyee620@gmail.com', 'wrupl'),
       ('4', 616, 'Tim', 'jiuxe', 'seolw', 'mdcfc'),
       ('5', 735, 'bob', 'xgwsj', 'vzbsg', 'bvuzt');

INSERT INTO e_tag(id, tag_name)
VALUES ('2', 'linux'),
       ('7', 'windows'),
       ('8', 'centos'),
       ('9', 'faq'),
       ('4', 'openEuler');

INSERT INTO r_role_attaching(id, user_id, role_id)
VALUES ('1', '1', '1'),
       ('2', '2', '1'),
       ('3', '3', '1'),
       ('4', '4', '1'),
       ('5', '5', '1'),
       ('6', '2', '2'),
       ('7', '3', '2'),
       ('8', '1', '3');

