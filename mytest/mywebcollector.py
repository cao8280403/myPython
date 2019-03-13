# coding=utf-8
import webcollector


class NewsCrawler(webcollector.RamCrawler):
    def __init__(self):
        super().__init__(auto_detect=True)
        self.num_threads = 10
        self.add_seed("https://github.blog/")
        self.add_regex("+https://github.blog/[0-9]+.*")
        self.add_regex("-.*#.*")  # do not detect urls that contain "#"

    def visit(self, page, detected):
        if page.match_url("https://github.blog/[0-9]+.*"):
            title = page.select("h1.lh-condensed")[0].text.strip()
            content = page.select("div.markdown-body")[0].text.replace("\n", " ").strip()
            print("\nURL: ", page.url)
            print("TITLE: ", title)
            print("CONTENT: ", content[:100], "...")


crawler = NewsCrawler()
crawler.start(10)
