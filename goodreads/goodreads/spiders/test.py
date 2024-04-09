import scrapy
import csv
import re


class Goodreads(scrapy.Spider):
    name = "test"
    shelves = []
    with open('shelves.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for shelf in csv_reader:
            shelves.append(shelf[0])
    file.close()
    start_urls = []
    for shelf in shelves:
        for page in range(1, 100):
            url = "https://www.goodreads.com" + shelf + "?page=" + str(page)
            start_urls.append(url)

    def parse(self, response, **kwargs):
        # scrape on goodreads.com using desire genre type or keyword
        # and save the titles and authors in a csv file
        ratinglist = []
        titles = response.xpath("//a[@class='bookTitle']/span[@itemprop='name']/text()").extract()
        authors = response.xpath("//a[@class='authorName']/span[@itemprop='name']/text()").extract()
        ratings = response.xpath("//span[@class='minirating']/text()").extract()
        for rating in ratings:
            for stars in re.findall("[0-5][.][0-9][0-9]", rating):
                ratinglist.append(stars)
        with open("books.csv", mode='a', newline="", encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            for i in range(len(titles)):
                csv_writer.writerow([titles[i], authors[i], ratinglist[i]])
        file.close()
