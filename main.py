from queue import Queue
from work import ThreadPool
from crawer import *
import os


def main():
    if not os.path.exists(today):
        os.makedirs(today)
        print("路径创建成功")
        pass
    get_stored()

    tag_queue = Queue(100)
    movie_queue = Queue(50000)
    db_queue = Queue(100000)

    tags = get_tags()
    for tag in tags:
        tag_queue.put((get_tag_movies, [tag, movie_queue, db_queue]))
    pool = ThreadPool(tag_queue, movie_queue, db_queue)
    pool.joinAll()
    print("----END----")


if __name__ == '__main__':
    main()
