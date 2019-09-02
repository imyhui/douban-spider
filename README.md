# 豆瓣电影爬虫

## 使用
- 创建s数据库
    - `db.sql` 
- 安装依赖
    - `pip install -r requirements.txt` 或 `pipenv install`
- 执行脚本
    - `python main.py`

## 思路
- 调用接口获取全部标签信息，加入标签队列
- 通过标签队列取出一个标签，爬取该标签下全部电影ID、标题等信息加入电影ID队列
- 电影ID队列取出电影ID，详情页抓取详情，加入存储队列
- 存储队列取出电影详情，存入MySQL

三个线程并发执行任务提高采集效率