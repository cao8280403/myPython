import configparser
import os


class ReadConfig:
    """定义一个读取配置文件的类"""

    def __init__(self, filepath=None):
        if filepath:
            configpath = filepath
        else:
            # root_dir = os.path.dirname(os.path.abspath('.'))
            root_dir = os.path.abspath('.')
            configpath = os.path.join(root_dir, "config.ini")
        self.cf = configparser.ConfigParser()
        self.cf.read(configpath, encoding="utf-8-sig")

    def get_db(self, param):
        value = self.cf.get("Mysql-Database", param)
        return value

    def get_window_size(self):
        value = self.cf.get("Window-Size", "size")
        return value

    def get_keyword(self):
        value = self.cf.get("Keyword", "words")
        return value

    def get_site(self):
        value = self.cf.get("Site", "site")
        return value

    def get_url(self):
        value = self.cf.get("Url", "url")
        return value

    def get_pram(self):
        pram1 = self.cf.get("Pram", "pram1")
        pram2 = self.cf.get("Pram", "pram2")
        time_sleep = self.cf.get("Pram", "time_sleep")
        show_window = self.cf.get("Pram", "show_window")
        return [pram1, pram2,time_sleep,show_window]


if __name__ == '__main__':
    test = ReadConfig()
    t = test.get_db("host")
    print(test.get_window_size())
