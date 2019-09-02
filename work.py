import threading
import time


class WorkThread(threading.Thread):
    # 创建同时启动线程
    def __init__(self, work_queue, name=""):
        threading.Thread.__init__(self)
        self.name = name
        self.work_queue = work_queue
        self.start()

    def run(self):
        no_task = 0
        while True:  # 除非确认队列中已经无任务，否则时刻保持线程在运行
            try:
                func, args = self.work_queue.get(
                    block=False)  # 如果队列空了，直接结束线程。根据是否还有任务
                if self.name == "数据存储":
                    print(
                        f"---------当前还有 {self.work_queue.qsize()} 条数据待插入数据库-------\n")
                elif self.name == "电影详情":
                    print(
                        f"---------当前还有 {self.work_queue.qsize()} 部电影待爬取-------\n")
                elif self.name == "电影ID":
                    print(
                        f"---------当前还有 {self.work_queue.qsize()} 种类型电影分类待爬取-------\n")
                try:
                    func(*args)
                except Exception as e:
                    print(f"bad execution: {e}\n")
                no_task = 0
                self.work_queue.task_done()
            except Exception as e:
                no_task = no_task + 1
                if no_task <= 120:
                    time.sleep(5)
                    continue
                else:
                    print(f"{self.name} 线程-{self.getName()}等待了120次仍无任务...立即退出\n")
                    break


class ThreadPool():
    def __init__(self, tag_queque, movie_queue, db_queue):
        # 初始化线程数 可配置
        self.tag_thread_num = 1
        self.movie_thread_num = 2
        self.db_thread_num = 4
        self.movie_queue = movie_queue
        self.tag_queque = tag_queque
        self.pool = []
        # 创建对应线程
        for i in range(self.tag_thread_num):
            self.pool.append(WorkThread(tag_queque, name="电影ID"))

        for i in range(self.movie_thread_num):
            self.pool.append(WorkThread(movie_queue, name="电影详情"))

        for i in range(self.db_thread_num):
            self.pool.append(WorkThread(db_queue, name="数据存储"))
        print("---------所有线程创建完毕---------")

    def joinAll(self):
        for thread in self.pool:
            if thread.isAlive():
                thread.join()
