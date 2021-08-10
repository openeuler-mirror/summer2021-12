drop schema if exists openeuler_faq;
create schema openeuler_faq;
use openeuler_faq;

-- c_answer_browse_type: table
CREATE TABLE `c_answer_browse_type`
(
    `id`   varchar(20) NOT NULL,
    `type` varchar(100) DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

insert into c_answer_browse_type (id, type)
values  ('1', '浏览'),
        ('2', '点赞'),
        ('3', '踩');

-- c_answer_level: table
CREATE TABLE `c_answer_level`
(
    `id`    varchar(20)  NOT NULL,
    `level` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

insert into c_answer_level (id, level)
values  ('1', 'std'),
        ('2', 'good'),
        ('3', 'deprecated'),
        ('4', 'undetermined');

-- c_answer_type: table
CREATE TABLE `c_answer_type`
(
    `id`   varchar(20)  NOT NULL,
    `type` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

insert into c_answer_type (id, type)
values  ('1', 'text'),
        ('2', 'video'),
        ('3', 'website');

-- c_question_browse_type: table
CREATE TABLE `c_question_browse_type`
(
    `id`   varchar(20) NOT NULL,
    `type` varchar(100) DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

insert into c_question_browse_type (id, type)
values  ('1', '满意'),
        ('2', '不满意');

-- c_user_role: table
CREATE TABLE `c_user_role`
(
    `id`   varchar(20)  NOT NULL,
    `type` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

insert into c_user_role (id, type)
values  ('1', '普通用户'),
        ('2', '审核员'),
        ('3', '管理员');

-- e_answer: table
CREATE TABLE `e_answer`
(
    `id`          varchar(20) NOT NULL,
    `type_id`     varchar(20)  DEFAULT NULL,
    `content`     varchar(200) DEFAULT NULL,
    `author_id`   varchar(20)  DEFAULT NULL,
    `question_id` varchar(20)  DEFAULT NULL,
    `level_id`    varchar(20)  DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `answer_c_answer_type_id_fk` (`type_id`),
    KEY `e_answer_e_user_id_fk` (`author_id`),
    KEY `e_answer_e_question_id_fk` (`question_id`),
    KEY `e_answer_c_answer_level_id_fk` (`level_id`),
    CONSTRAINT `answer_c_answer_type_id_fk` FOREIGN KEY (`type_id`) REFERENCES `c_answer_type` (`id`),
    CONSTRAINT `e_answer_c_answer_level_id_fk` FOREIGN KEY (`level_id`) REFERENCES `c_answer_level` (`id`),
    CONSTRAINT `e_answer_e_question_id_fk` FOREIGN KEY (`question_id`) REFERENCES `e_question` (`id`),
    CONSTRAINT `e_answer_e_user_id_fk` FOREIGN KEY (`author_id`) REFERENCES `e_user` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- No native definition for element: answer_c_answer_type_id_fk (index)

-- No native definition for element: e_answer_e_user_id_fk (index)

-- No native definition for element: e_answer_e_question_id_fk (index)

-- No native definition for element: e_answer_c_answer_level_id_fk (index)

-- e_answer_browse_log: table
CREATE TABLE `e_answer_browse_log`
(
    `id`        varchar(20) NOT NULL,
    `time`      datetime    DEFAULT NULL,
    `type_id`   varchar(20) DEFAULT NULL,
    `answer_id` varchar(20) DEFAULT NULL,
    `user_id`   varchar(20) DEFAULT NULL,
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

-- No native definition for element: e_answer_browse_log_c_answer_browse_type_id_fk (index)

-- No native definition for element: e_answer_browse_log_e_answer_id_fk (index)

-- No native definition for element: e_answer_browse_log_e_user_id_fk (index)

-- e_question: table
CREATE TABLE `e_question`
(
    `id`              varchar(20) NOT NULL,
    `std_description` varchar(250) DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `question_std_description_uindex` (`std_description`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- e_question_description: table
CREATE TABLE `e_question_description`
(
    `id`          varchar(20)  NOT NULL,
    `description` varchar(200) NOT NULL,
    `question_id` varchar(20) DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `question_description_question_id_fk` (`question_id`),
    CONSTRAINT `question_description_question_id_fk` FOREIGN KEY (`question_id`) REFERENCES `e_question` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- No native definition for element: question_description_question_id_fk (index)

-- e_questioning_log: table
CREATE TABLE `e_questioning_log`
(
    `id`                  varchar(20) NOT NULL,
    `type_id`             varchar(20)  DEFAULT NULL,
    `op_time`             datetime     DEFAULT NULL,
    `matched_question_id` varchar(20)  DEFAULT NULL,
    `user_id`             varchar(20)  DEFAULT NULL,
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

-- No native definition for element: e_question_browse_log_c_question__browse_type_id_fk (index)

-- No native definition for element: e_question_browse_log_e_question_id_fk (index)

-- No native definition for element: e_question_browse_log_e_user_id_fk (index)

-- e_request: table
CREATE TABLE `e_request`
(
    `id`          varchar(20) NOT NULL,
    `description` varchar(200) DEFAULT NULL,
    `author_id`   varchar(20)  DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `e_request_e_user_id_fk` (`author_id`),
    CONSTRAINT `e_request_e_user_id_fk` FOREIGN KEY (`author_id`) REFERENCES `e_user` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- No native definition for element: e_request_e_user_id_fk (index)

-- e_self_answer: table
CREATE TABLE `e_self_answer`
(
    `id`         varchar(20)  NOT NULL,
    `type_id`    varchar(20) DEFAULT NULL,
    `content`    varchar(200) NOT NULL,
    `author_id`  varchar(20) DEFAULT NULL,
    `request_id` varchar(20) DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `e_self_answer_c_answer_type_id_fk` (`type_id`),
    KEY `e_self_answer_e_request_id_fk` (`request_id`),
    KEY `e_self_answer_e_user_id_fk` (`author_id`),
    CONSTRAINT `e_self_answer_c_answer_type_id_fk` FOREIGN KEY (`type_id`) REFERENCES `c_answer_type` (`id`),
    CONSTRAINT `e_self_answer_e_request_id_fk` FOREIGN KEY (`request_id`) REFERENCES `e_request` (`id`),
    CONSTRAINT `e_self_answer_e_user_id_fk` FOREIGN KEY (`author_id`) REFERENCES `e_user` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- No native definition for element: e_self_answer_c_answer_type_id_fk (index)

-- No native definition for element: e_self_answer_e_user_id_fk (index)

-- No native definition for element: e_self_answer_e_request_id_fk (index)

-- e_tag: table
CREATE TABLE `e_tag`
(
    `id`   varchar(20) NOT NULL,
    `name` int         NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `tag_name_uindex` (`name`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- e_user: table
CREATE TABLE `e_user`
(
    `id`         varchar(20) NOT NULL,
    `gitee_id`   int          DEFAULT NULL,
    `username`   varchar(50)  DEFAULT NULL,
    `avatar_url` varchar(200) DEFAULT NULL,
    `email`      varchar(200) DEFAULT NULL,
    `role_id`    varchar(20)  DEFAULT NULL,
    `html_url`   varchar(200) DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `e_user_c_user_type_id_fk` (`role_id`),
    CONSTRAINT `e_user_c_user_type_id_fk` FOREIGN KEY (`role_id`) REFERENCES `c_user_role` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- No native definition for element: e_user_c_user_type_id_fk (index)

-- r_question_tagging: table
CREATE TABLE `r_question_tagging`
(
    `id`          varchar(20) NOT NULL,
    `question_id` varchar(20) DEFAULT NULL,
    `tag_id`      varchar(20) DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `r_tagging_question_id_fk` (`question_id`),
    KEY `r_tagging_tag_id_fk` (`tag_id`),
    CONSTRAINT `r_tagging_question_id_fk` FOREIGN KEY (`question_id`) REFERENCES `e_question` (`id`),
    CONSTRAINT `r_tagging_tag_id_fk` FOREIGN KEY (`tag_id`) REFERENCES `e_tag` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- No native definition for element: r_tagging_question_id_fk (index)

-- No native definition for element: r_tagging_tag_id_fk (index)

-- r_request_tagging: table
CREATE TABLE `r_request_tagging`
(
    `id`         varchar(20) NOT NULL,
    `tag_id`     varchar(20) NOT NULL,
    `request_id` varchar(20) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `r_request_tagging_e_request_id_fk` (`request_id`),
    KEY `r_request_tagging_e_tag_id_fk` (`tag_id`),
    CONSTRAINT `r_request_tagging_e_request_id_fk` FOREIGN KEY (`request_id`) REFERENCES `e_request` (`id`),
    CONSTRAINT `r_request_tagging_e_tag_id_fk` FOREIGN KEY (`tag_id`) REFERENCES `e_tag` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- No native definition for element: r_request_tagging_e_tag_id_fk (index)

-- No native definition for element: r_request_tagging_e_request_id_fk (index)

-- r_role_attaching: table
CREATE TABLE `r_role_attaching`
(
    `id`      varchar(20) NOT NULL,
    `user_id` varchar(20) DEFAULT NULL,
    `role_id` varchar(20) DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `r_role_attaching_c_user_role_id_fk` (`role_id`),
    KEY `r_role_attaching_e_user_id_fk` (`user_id`),
    CONSTRAINT `r_role_attaching_c_user_role_id_fk` FOREIGN KEY (`role_id`) REFERENCES `c_user_role` (`id`),
    CONSTRAINT `r_role_attaching_e_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `e_user` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- No native definition for element: r_role_attaching_e_user_id_fk (index)

-- No native definition for element: r_role_attaching_c_user_role_id_fk (index)

