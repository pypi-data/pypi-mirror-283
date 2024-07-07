# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
import re
from typing import Iterable, Union
import time
import datetime


import colemen_utils as c
import ramanager.settings as _settings
import ramanager.settings.types as _t

# from ra.Post import Post


@dataclass
class Database:

    db=None
    ra=None
    db_path:str=None

    def __init__(
        self,
        ra_manager:_t.main_type
        ):
        self.ra = ra_manager
        self.db_path = "ra_manager.db"
        self.create_database()


    def create_database(self):

        if c.file.exists(self.db_path) is False:
            self.db = c.db.DatabaseManager()
            self.db.connect(DB_PATH=self.db_path)
            create_database(self.db)
            return
        self.db = c.db.DatabaseManager()
        self.db.connect(DB_PATH=self.db_path)

    def get_last_id(self):
        result = self.db.execute_single_statement("SELECT last_insert_rowid() as last_id")
        return self.db.fetchall()[0]['last_id']

    def select_fetchall(self,sql):
        self.db.run(sql)
        return self.db.fetchall()

    def select_fetchone(self,sql):
        self.db.run(sql)
        result = self.db.fetchall()

        if len(result) > 0:
            return result[0]
        return None

    def prep_update_assigns(self,data):
        # print(f"data:")
        # print(data)
        assign_list = []
        for k,v in data.items():
            if v in ["__NO_VALUE__"]:
                continue

            if v is None:
                val = f"{k}=NULL"
                assign_list.append(val)
                continue

            if isinstance(v,(str)):
                val = f"{k}='{v}'"
                assign_list.append(val)
                continue

            val = f"{k}={v}"
            assign_list.append(val)

        if len(assign_list) == 0:
            return False
        return ','.join(assign_list)








# def create_database(db):
#     print(f"create_database")

#     sql = [
#     """DROP TABLE IF EXISTS `sleep_minutes`;
#     DROP TABLE IF EXISTS `post_activities`;
#     DROP TABLE IF EXISTS `message_terms`;
#     DROP TABLE IF EXISTS `sleep`;
#     DROP TABLE IF EXISTS `post_keywords`;
#     DROP TABLE IF EXISTS `heart_rate`;
#     DROP TABLE IF EXISTS `activities`;
#     DROP TABLE IF EXISTS `posts`;
#     DROP TABLE IF EXISTS `keywords`;
#     DROP TABLE IF EXISTS `categories`;
#     """,
#     """CREATE TABLE IF NOT EXISTS `posts`
#     (
#     `post_id` integer PRIMARY KEY,
#     `message`          TEXT NOT NULL,
#     `start_time`       int NULL DEFAULT NULL,
#     `end_time`         int NULL DEFAULT NULL,
#     `score`            int NULL DEFAULT NULL,
#     `timestamp_string` TEXT NOT NULL,
#     `content_hash`     TEXT NOT NULL
#     );
#     """,
#     """CREATE TABLE IF NOT EXISTS `keywords`
#     (
#     `keyword_id` integer PRIMARY KEY,
#     `value`      TEXT NOT NULL ,
#     `synonyms`   varchar(1000) NULL
#     );""",
#     """CREATE TABLE IF NOT EXISTS `categories`
#     (
#     `category_id` integer PRIMARY KEY,
#     `name`        TEXT NOT NULL ,
#     `description` TEXT NULL ,
#     `importance`  int NOT NULL

#     );""",
#     """CREATE TABLE IF NOT EXISTS `sleep`
#     (
#     `sleep_id`      int PRIMARY KEY,
#     `post_id`       integer NOT NULL ,
#     `efficiency`    int NULL ,
#     `date_of_sleep` TEXT NULL ,
#     `fitbit_log_id` integer NULL ,
#     FOREIGN KEY (`post_id`) REFERENCES `posts` (`post_id`)
#     );""",
#     """CREATE TABLE IF NOT EXISTS `post_keywords`
#     (
#     `post_keyword_id` integer PRIMARY KEY,
#     `post_id`         integer NOT NULL ,
#     `keyword_id`      integer NOT NULL ,

#     FOREIGN KEY (`post_id`) REFERENCES `posts` (`post_id`),
#     FOREIGN KEY (`keyword_id`) REFERENCES `keywords` (`keyword_id`)
#     );""",
#     """CREATE TABLE IF NOT EXISTS `heart_rate`
#     (
#     `heart_rate_id` integer PRIMARY KEY,
#     `post_id`       integer NOT NULL ,
#     `rate`          int NOT NULL ,
#     `timestamp`     int NOT NULL ,

#     FOREIGN KEY (`post_id`) REFERENCES `posts` (`post_id`)
#     );""",
#     """CREATE TABLE IF NOT EXISTS `activities`
#     (
#     `activity_id` integer PRIMARY KEY,
#     `category_id` integer NOT NULL ,
#     `name`        TEXT NOT NULL ,
#     `description` TEXT NULL ,
#     `positive`    tinyint NULL DEFAULT -1 ,
#     `importance`  int NULL ,
#     FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`)
#     );""",
#     """CREATE TABLE IF NOT EXISTS `sleep_minutes`
#     (
#     `sleep_minute_id` integer PRIMARY KEY ,
#     `sleep_id`        int NOT NULL ,
#     `timestamp`       int NOT NULL ,
#     `level`           TEXT NOT NULL ,
#     FOREIGN KEY (`sleep_id`) REFERENCES `sleep` (`sleep_id`)
#     );""",
#     """CREATE TABLE IF NOT EXISTS `post_activities`
#     (
#     `post_activity_id` integer PRIMARY KEY,
#     `activity_id`      integer NOT NULL ,
#     `post_id`          integer NOT NULL ,
#     FOREIGN KEY (`post_id`) REFERENCES `posts` (`post_id`),
#     FOREIGN KEY (`activity_id`) REFERENCES `activities` (`activity_id`)
#     );""",
#     """CREATE TABLE IF NOT EXISTS `message_terms`
#     (
#     `message_term_id` integer PRIMARY KEY,
#     `exrex`           tinyint NULL DEFAULT -1 ,
#     `activity_id`     integer NOT NULL ,
#     `base`            TEXT NOT NULL ,
#     `whole_word`      tinyint NULL DEFAULT -1 ,
#     `case_sensitive`  tinyint NULL DEFAULT 1 ,
#     `regex`           tinyint NULL DEFAULT -1 ,
#     FOREIGN KEY (`activity_id`) REFERENCES `activities` (`activity_id`)
#     );
#     """,
#     """CREATE TABLE IF NOT EXISTS `activity_keywords`
#     (
#     `activity_keyword_id` integer PRIMARY KEY,
#     `activity_id`         bigint NOT NULL ,
#     `keyword_id`          bigint NOT NULL ,
#     FOREIGN KEY (`activity_id`) REFERENCES `activities` (`activity_id`),
#     FOREIGN KEY (`keyword_id`) REFERENCES `keywords` (`keyword_id`)
#     );

#     """
#     ]


#     for x in sql:
#         db.run(x)