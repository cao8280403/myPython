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



    def get_window_size(self):
        value = self.cf.get("Window-Size", "size")
        return value


    def get_url(self):
        value = self.cf.get("Url-Num", "url_num")
        return value

    def get_pram(self):
        time_sleep = self.cf.get("Pram", "time_sleep")
        show_window = self.cf.get("Pram", "show_window")
        open_chrome_sec = self.cf.get("Pram", "open_chrome_sec")
        return [time_sleep,show_window,open_chrome_sec]


if __name__ == '__main__':
    test = ReadConfig()
    t = test.get_url()
    print(str(t))
