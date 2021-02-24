import os
import json
import scrapy
from pprint import pprint
import logging

class HboSpider(scrapy.Spider):
    logging.getLogger("scrapy").propagate = False
    name = "hbo"
    """initializes the spider with the url that was passed as the argument."""
    def __init__(self, url= None):
        self.url = url

    def start_requests(self):
        if self.url:
            urls = [
                self.url,
            ]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):

        page_name = response.url.split("/")[-2]
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, f"files/{page_name}.json")

        """
        Creates a file with corresponding filename.
        Writes the obtained dictionary the file for future use.
        Saves to the spiders/files dir.
        """
        with open(filename, "w+", encoding="utf-8") as f:
            json.dump(self.get_relevant_data(response), f, indent=4, ensure_ascii=False)

        """
        Opens the file and selects some of the relevant data. 
        This can be extended reduced by picking desired keys from the dict (eg in the file) and extending the "data" dict. 
        """
        with open(filename, "r", encoding="utf-8") as scraped:
            text = json.load(scraped)

            data = {}
            data["name"] = text["name"]
            data["description"] = text["description"]
            data["url"] = text["url"]
            data["countryOfOrigin"] = text["countryOfOrigin"]["name"]
            data["aggregateRating"] = text["aggregateRating"]
            data["dateCreated"] = text["dateCreated"]
            data["image"] = text["image"][0]["url"]
            data["type"] = text["@type"]
            data["subtitleLanguage"] = text["subtitleLanguage"]
            data["seasons"] = [season["name"] for season in text["containsSeason"]]

            for season in text["containsSeason"]:
                if "episode" in season.keys():
                    name = season["name"]
                    data[f"{name} episodes"] = [episode["episodeNumber"] for episode in season["episode"]]
            pprint(data)

    def get_relevant_data(self, response) -> str:
        """
        :param response: response returned by the spider after dispatching a request to the given url.
        :return: returns a json dictionary.
        """
        the_dictionary = response.xpath("//body//script[1]/text()").extract()[0]
        return json.loads(the_dictionary)



