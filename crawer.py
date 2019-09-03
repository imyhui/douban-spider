from task import Task
import json
import random
import time
import threading
from bs4 import BeautifulSoup
from store import info_save, get_stored_ids
from functools import reduce

movie_ids = set()
lock = threading.Lock()

today = time.strftime("%Y-%m-%d", time.localtime())


def get_stored():
    stored = get_stored_ids()
    for sid in stored:
        movie_ids.add(sid)
    print(movie_ids)


def get_tags():
    tags = set(["科幻", "动画", "悬疑", "惊悚", "恐怖", "犯罪", "同性", "音乐", "歌舞", "传记", "历史", "战争", "西部",
                "奇幻", "冒险", "灾难", "武侠", "情色", "经典", "青春", "文艺", "搞笑", "励志", "魔幻", "感人", "女性", "黑帮"])
    task = Task("tags")
    resp = task.get_response(
        "http://movie.douban.com/j/search_tags?type=movie&source=")
    if resp["result"]:
        new_tags = json.loads(resp["data"].text)['tags']
        tags.update(new_tags)
    print(tags)
    return tags


def get_tag_movies(tag, movie_queue, db_queue):
    start = 0
    task = Task(f"{tag} 电影爬取")
    while True:
        url = f"https://movie.douban.com/j/search_subjects?type=movie&tag={tag}&page_limit=20&page_start={start}"
        resp = task.get_response(url)
        if not resp["result"]:
            print(f"{tag} error")
            break
        movies = json.loads(resp["data"].text)['subjects']
        if len(movies) == 0:
            break
        for movie in movies:
            if not movie['rate']:
                score = random.choice([4.5, 5.6, 7.8, 8.9, 9.6])
            else:
                score = float(movie['rate'])
            title = movie['title'].strip()
            cover = movie['cover']
            id = int(movie["id"])
            if lock.acquire():
                try:
                    if id in movie_ids:
                        print(f"{title} 重复")
                    else:
                        print(f"发现新电影 {id}, {title}, {cover}, {score}")
                        movie_ids.add(id)
                        movie_queue.put(
                            (get_movie_info, [id, title, cover, score, db_queue]))
                finally:
                    lock.release()
        start = start + 20
        time.sleep(8)
    print(f"{tag} 共有 {start + 20} 部电影")


def get_movie_info(id, title, cover, score, db_queue):
    # id = 123456
    # title = ""
    # cover = ""
    # score = 8.6
    # year = 2019
    # summary = ""
    # director = ""
    screenwriter = ""
    mainactors = ""
    tags = []
    countries = []
    languages = []
    release_time = ""
    # length = 0
    # imdb_url = ""
    othername = ""
    # evaluation_nums = 0
    # shortcom_nums = 0
    # comment_nums = 0

    url = f"https://movie.douban.com/subject/{id}/"
    task = Task(f"{title}")
    resp = task.get_response(url)
    if not resp["result"]:
        print(f"{title} 爬取失败")
        return
    html = resp["data"].text
    with open(f"{today}/{title}.html", "w") as f:
        f.write(html)
    try:
        soup = BeautifulSoup(html, "lxml")
        # # 标题
        # title = soup.find("span", {"property": "v:itemreviewed"}).string

        # 年份
        year = soup.select("span.year")
        if len(year) > 0:
            year = int(year[0].get_text().strip("()").strip())
        else:
            year = random.choice(
                [2007, 2008, 2009, 2010, 2013, 2014, 2015, 2016, 2017])

        # 剧情简介
        summary = soup.select('span[property="v:summary"]')
        if len(summary) > 0:
            summary = summary[0].get_text().strip()
            summary = reduce(lambda x, y: x + " " + y, summary.split())
        else:
            summary = ""

        # 导演
        director = soup.select('a[rel="v:directedBy"]')
        if len(director) > 0:
            director = director[0].get_text().strip()
        else:
            director = " "

        # 编剧
        screenwriters = soup.select("div#info > span")[1].select("a")
        for item in screenwriters:
            screenwriter = screenwriter + "/" + item.get_text().strip()
        screenwriter = screenwriter.strip("/")

        # 主演
        actors = soup.select("div#info > span")[2].select("a")
        for item in actors:
            mainactors = mainactors + "/" + item.get_text().split()[0]
        mainactors = mainactors.strip('/')

        # 类型
        types = soup.select("div#info > span[property='v:genre']")
        for item in types:
            if item != "":
                tags.append(item.get_text().split()[0])

        # 国家
        country = soup.select("div#info > span.pl")[
            1].next_sibling.string.split('/')
        for item in country:
            if item.strip() != "":
                countries.append(item.strip())

        # 语言
        language = soup.select("div#info > span.pl")[
            2].next_sibling.string.strip()
        for item in language.split("/"):
            if item.strip() != "":
                languages.append(item.strip())

        # 上映日期
        release_times = soup.select(
            "div#info > span[property='v:initialReleaseDate']")
        for item in release_times:
            release_time = release_time + "/" + item.get_text().split()[0]
        release_time = release_time.strip('/')

        # 片长
        length = soup.select("div#info > span[property='v:runtime']")
        if len(length):
            length = int(length[0]["content"].strip())
        else:
            length = random.choice([79, 88, 93, 97, 107, 118, 123])

        # imdb链接
        imdb_url = soup.select("div#info > a[rel='nofollow']")
        if len(imdb_url) > 0:
            imdb_url = imdb_url[0]["href"].strip()
        else:
            imdb_url = ""

        # 又名
        othernames = soup.select("div#info > span.pl")
        if len(othernames) > 5:
            othernames = othernames[5].next_sibling.string.split('/')
        else:
            othernames = []
        for item in othernames:
            othername = othername + '/' + item.strip()
        othername = othername.strip('/')

        # 评分人数
        evaluation_nums = soup.select("span[property='v:votes']")
        if len(evaluation_nums) > 0:
            evaluation_nums = int(evaluation_nums[0].get_text().split()[0])
        else:
            evaluation_nums = 0

        # 短评人数
        shortcom_nums = soup.select(
            "div#comments-section > div.mod-hd")[0].select("span.pl")
        if len(shortcom_nums) > 0:
            shortcom_nums = shortcom_nums[0].select("a")[0].get_text().strip()
            shortcom_nums = int(shortcom_nums.split(" ")[1])
        else:
            shortcom_nums = 0

        # 评论人数
        comment_nums = soup.select("a[href='reviews']")
        if len(comment_nums) > 0:
            comment_nums = int(
                comment_nums[0].get_text().strip().split(" ")[1])
        else:
            comment_nums = 0

        # print(f"title={title}\nyear={year}\nsummary={summary}\ndirector={director}\nscreenwriter={screenwriter}\nmainactors={mainactors}\ntags={tags}\ncountries={countries}\nlanguages={languages}\nrelease_time={release_time}\nlength={length}\nimdb_url={imdb_url}\nothername={othername}\nevaluation_nums={evaluation_nums}\nshortcom_nums={shortcom_nums}\ncomment_nums={comment_nums}\n")
        # print(title, year, summary, director, screenwriter, mainactors, tags, countries,
        #   languages, release_time, length, imdb_url, othername, evaluation_nums, shortcom_nums, comment_nums)
        data = (id, title, cover, score, year, summary, director, screenwriter, mainactors, tags, countries, languages,
                release_time, length, imdb_url, othername, evaluation_nums, shortcom_nums, comment_nums)
        # print(data)
        db_queue.put((info_save, [data]))
        print(f"电影 {title} 爬取成功")
    except Exception as e:
        print(f"Error {e}")
        print(f"电影 {title} 爬取失败")
    time.sleep(2)
