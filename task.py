import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    # "Accept-Encoding": "gzip, deflate, br",
    "Host": "movie.douban.com",
    "Referer": "https://movie.douban.com",
    "Connection": "keep-alive"
}


class Task():
    def __init__(self, name):
        self.name = name
        self.session = requests.Session()
        # todo faker headers
        self.session.headers.update(headers)
        print("任务 " + self.name + " 已创建")

    def get_response(self, url):
        # todo max fail time
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                return {"result": True, "data": response}
        except Exception as e:
            print(f"Error {e}")
        return {"result": False, "data": None}
