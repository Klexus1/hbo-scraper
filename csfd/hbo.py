import sys, getopt
from scrapy.crawler import CrawlerProcess
from spiders.hbo_spider import HboSpider
from scrapy.utils.project import get_project_settings

def main(argv):
    """

    :param argv: -u / --url, which is then passed to the hbo spider when initialized.
    """
    url = ''

    try:
        opts, args = getopt.getopt(argv, "hu:", ["url="])
    except getopt.GetoptError:
        print('Script accepts 1 required argument: -u <url> (--url <url>)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            sys.exit()
        elif opt in ("-u", "--url"):
            url = sys.argv[2]
            """
            if valid, spider initializes and outputs the entire data to the files folder and selected data to the console
            """
            process = CrawlerProcess(get_project_settings())

            process.crawl(HboSpider, url=str(url))
            process.start()


if __name__ == "__main__":
    main(sys.argv[1:])
