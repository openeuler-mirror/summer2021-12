
INSERT INTO e_user(id, gitee_id, username, avatar_url, email, html_url)
VALUES ('1', 820, 'cctxg', 'gntbb', 'nlfoz', 'tkkth'),
       ('10', 982, 'kueeb', 'rjtkv', 'xkhtf', 'hfaht'),
       ('2', 599, 'isnrb', 'ixhpq', 'tmkdl', 'enggw'),
       ('3', 975, 'pnkyg', 'tkmik', 'lpjol', 'wrupl'),
       ('4', 616, 'nofsm', 'jiuxe', 'seolw', 'mdcfc'),
       ('5', 735, 'hbhlb', 'xgwsj', 'vzbsg', 'bvuzt'),
       ('6', 370, 'gczza', 'zbvdb', 'nvepk', 'tisis'),
       ('7', 275, 'cvkyn', 'ghylf', 'wfvvz', 'ftiym'),
       ('8', 483, 'lfxow', 'esdfb', 'qdvil', 'vimld'),
       ('9', 725, 'powbe', 'lshkm', 'wflph', 'ptcki');


INSERT INTO e_request(id, description, author_id, reviewer_id, time, review_status, comment)
VALUES ('1', 'wgmzn', '4', '8', '2003-01-16 13:58:21', '1', 'dkrdd'),
       ('10', 'ouqub', '6', '7', '1996-12-08 15:25:03', '2', 'oyfve'),
       ('2', 'ybnkp', '5', '9', '2021-01-22 18:12:36', '1', 'sqvap'),
       ('3', 'ufgtd', '9', '1', '1989-10-13 14:46:10', '1', 'algnb'),
       ('4', 'arzef', '8', '10', '2000-02-08 15:53:01', '3', 'uxbpe'),
       ('5', 'jpqpx', '8', '4', '1992-08-18 06:12:53', '2', 'heeki'),
       ('6', 'yugkv', '5', '2', '2003-10-21 21:41:17', '2', 'qnymr'),
       ('7', 'ffvwc', '9', '4', '1976-07-29 06:07:50', '1', 'lyvas'),
       ('8', 'qvodm', '2', '6', '1990-12-18 15:37:57', '1', 'qosfr'),
       ('9', 'kduqz', '4', '5', '1979-09-09 04:27:31', '2', 'daxyy');

INSERT INTO e_self_answer(id, type_id, summary, content, request_id, comment, review_status)
VALUES ('1', '2', 'fngey', 'ycpyu', '9', 'zvrfk', '1'),
       ('10', '2', 'dvlkt', 'qryyp', '6', 'nnkpv', '1'),
       ('2', '2', 'reaqi', 'nuiex', '5', 'rgwmz', '1'),
       ('3', '1', 'cjfme', 'lfzxm', '7', 'gomgm', '1'),
       ('4', '2', 'rjsbt', 'qmvlv', '8', 'rdweb', '1'),
       ('5', '3', 'vujsi', 'hiteq', '4', 'lcfgj', '1'),
       ('6', '2', 'wjbma', 'mmmmf', '2', 'scvlv', '1'),
       ('7', '2', 'luxkg', 'qygex', '9', 'tgunn', '1'),
       ('8', '3', 'vbvtw', 'bwtuw', '6', 'dbpkg', '1'),
       ('9', '1', 'boevh', 'tsmbp', '5', 'psoyi', '1');

INSERT INTO e_question(id, std_description)
VALUES ('5', 'afjlj'),
       ('7', 'cpeux'),
       ('4', 'dpgvm'),
       ('2', 'gjdce'),
       ('9', 'kklzu'),
       ('1', 'kpyuq'),
       ('3', 'nhtsw'),
       ('8', 'qabgr'),
       ('6', 'slsxp'),
       ('10', 'zkugt');

INSERT INTO e_answer(id, type_id, summary, content, author_id, question_id, level_id, comment, reviewer_id)
VALUES ('1', '2', 'qosnl', 'wgjix', '2', '8', '4', 'yyomd', '2'),
       ('10', '2', 'jzgfp', 'ryqba', '5', '3', '3', 'fxscn', '2'),
       ('2', '1', 'gsmsn', 'bwbfq', '2', '2', '3', 'htshp', '2'),
       ('3', '2', 'unxyx', 'fzmnv', '8', '7', '1', 'cdyzm', '2'),
       ('4', '2', 'twidt', 'ifevk', '8', '2', '5', 'pvgkv', '2'),
       ('5', '2', 'pchbd', 'wgyve', '6', '8', '5', 'mnrgk', '2'),
       ('6', '2', 'ghrvn', 'dfolb', '7', '6', '4', 'ockhc', '2'),
       ('7', '3', 'vokws', 'oswsu', '10', '7', '5', 'cxbtp', '2'),
       ('8', '2', 'wrcsz', 'mltom', '10', '6', '2', 'hbmqv', '2'),
       ('9', '3', 'zioyc', 'tongh', '1', '1', '2', 'esvcg', '2');

INSERT INTO e_question_description(id, description, question_id)
VALUES ('1', 'tgpqi', '9'),
       ('10', 'golfx', '8'),
       ('2', 'glstt', '8'),
       ('3', 'htcgf', '2'),
       ('4', 'nqugi', '5'),
       ('5', 'byqij', '5'),
       ('6', 'jsevf', '7'),
       ('7', 'hrqdr', '4'),
       ('8', 'kktnb', '4'),
       ('9', 'robnk', '2');

INSERT INTO e_tag(id, tag_name)
VALUES ('2', 'fefui'),
       ('7', 'gjqvb'),
       ('8', 'hmdwz'),
       ('9', 'kolnn'),
       ('4', 'oubvu'),
       ('5', 'roykw'),
       ('10', 'ttftp'),
       ('1', 'vqnab'),
       ('6', 'vvwyg'),
       ('3', 'ylymr');

INSERT INTO e_answer_browse_log(id, time, type_id, answer_id, user_id)
VALUES ('1', '1996-08-28 09:39:25', '2', '6', '5'),
       ('10', '1983-09-05 15:54:54', '1', '5', '3'),
       ('2', '1999-12-13 00:08:05', '2', '7', '5'),
       ('3', '1975-06-03 02:11:59', '3', '3', '2'),
       ('4', '1987-05-12 11:11:42', '2', '5', '9'),
       ('5', '1972-03-04 04:42:12', '1', '6', '1'),
       ('6', '1990-08-26 18:32:45', '1', '4', '3'),
       ('7', '2003-08-28 00:53:45', '2', '8', '6'),
       ('8', '1979-08-30 16:39:08', '2', '7', '6'),
       ('9', '1996-07-12 00:41:58', '3', '9', '9');

INSERT INTO e_questioning_log(id, type_id, op_time, matched_question_id, user_id, user_question)
VALUES ('1', '2', '2003-01-12 10:37:47', '5', '6', 'gwkzb'),
       ('10', '2', '1973-06-30 21:44:00', '1', '8', 'ojvci'),
       ('2', '1', '1982-11-01 09:08:11', '6', '7', 'ndkwu'),
       ('3', '1', '2003-07-13 09:55:40', '6', '7', 'vflec'),
       ('4', '1', '2007-09-16 06:23:51', '3', '7', 'uiefe'),
       ('5', '1', '1976-08-24 07:11:14', '3', '5', 'eizeb'),
       ('6', '2', '1993-12-22 23:14:57', '6', '6', 'bfodt'),
       ('7', '2', '2006-07-03 01:25:51', '8', '4', 'hegbl'),
       ('8', '1', '2018-04-18 19:49:38', '6', '2', 'hehxi'),
       ('9', '1', '2018-08-03 23:36:16', '9', '2', 'hunaz');

INSERT INTO r_question_tagging(id, question_id, tag_id)
VALUES ('1', '8', '4'),
       ('10', '6', '2'),
       ('2', '4', '1'),
       ('3', '6', '3'),
       ('4', '1', '9'),
       ('5', '7', '9'),
       ('6', '6', '3'),
       ('7', '2', '10'),
       ('8', '3', '5'),
       ('9', '3', '10');

INSERT INTO r_request_tagging(id, tag_id, request_id)
VALUES ('1', '6', '2'),
       ('10', '2', '3'),
       ('2', '9', '4'),
       ('3', '4', '6'),
       ('4', '5', '9'),
       ('5', '3', '2'),
       ('6', '6', '8'),
       ('7', '4', '6'),
       ('8', '3', '9'),
       ('9', '4', '5');

INSERT INTO r_role_attaching(id, user_id, role_id)
VALUES ('1', '6', '2'),
       ('10', '4', '3'),
       ('2', '3', '2'),
       ('3', '9', '3'),
       ('4', '5', '3'),
       ('5', '8', '2'),
       ('6', '3', '1'),
       ('7', '7', '2'),
       ('8', '2', '2'),
       ('9', '1', '3');

