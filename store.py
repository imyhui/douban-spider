import pymysql


def info_save(data):
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="douban", charset="utf8")
    douban_id, title, cover, score, year, summary, director, screenwriter, mainactors, tags, countries, languages, release_time, length, imdb_url, othername, evaluation_nums, shortcom_nums, comment_nums = data
    cur = db.cursor()
    sql_movie = f"""
    insert into `douban`.`movies` (
                `douban_id`,
                `title`,
                `cover`,
                `score`,
                `year`,
                `summary`,
                `director`,
                `screenwriter`,
                `mainactors`,
                `tags`,
                `countries`,
                `languages`,
                `release_time`,
                `length`,
                `imdb_url`,
                `othername`,
                `evaluation_nums`,
                `shortcom_nums`,
                `comment_nums`) values ({douban_id}, '{pymysql.escape_string(
        title)}', '{cover}', {score}, {year}, '{pymysql.escape_string(summary)}', '{pymysql.escape_string(
        director)}', '{pymysql.escape_string(screenwriter)}','{pymysql.escape_string(mainactors)}', 
                '{"/".join(tags)}', '{"/".join(countries)}', '{"/".join(
        languages)}', '{release_time}', {length}, '{imdb_url}', '{pymysql.escape_string(
        othername)}',{evaluation_nums}, {shortcom_nums}, {comment_nums});"""
    try:
        db.begin()
        cur.execute(sql_movie)
        if len(tags):
            add_tags = []
            for tag in tags:
                add_tags.append((douban_id, pymysql.escape_string(tag)))
            cur.executemany('insert into `douban`.`tags` (`movie_id`,`tag_name`) value(%s,%s)',
                            add_tags)
        if screenwriter != "":
            add_wrs = []
            screenwriter = screenwriter.split("/")
            for sn_writer in screenwriter:
                add_wrs.append((douban_id, pymysql.escape_string(sn_writer)))
            cur.executemany('insert into `douban`.`screenwriters` (`movie_id`,`screenwriter_name`) value(%s,%s)',
                            add_wrs)
        if mainactors != "":
            add_macs = []
            mainactors = mainactors.split("/")
            for main_ac in mainactors:
                add_macs.append((douban_id, pymysql.escape_string(main_ac)))
            cur.executemany('insert into `douban`.`mainactors` (`movie_id`,`mainactor_name`) value(%s,%s)',
                            add_macs)
        db.commit()
        print(f"电影 {title} 插入成功")
    except Exception as e:
        db.rollback()
        print(f"电影 {title} 插入出错")
        print(f"db error {e}")
    finally:
        cur.close()
        db.close()
