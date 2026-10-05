import scrapy

# Web scraped Wikipedia for Morgan Freeman and Eddie Murphy's filmography
# Shawn Tribuce
# DS3500 Homework 4
# 03/11/2026


class WikipediaScraperSpider(scrapy.Spider):
    name = "wikipedia" # The name to refer to in terminal when running the spider
    allowed_domains = ["en.wikipedia.org"] # Setting a boundry for the spider to crawl
    start_urls = [
        "https://en.wikipedia.org/wiki/Eddie_Murphy_filmography", # Eddie Murphy's webpage
        "https://en.wikipedia.org/wiki/Morgan_Freeman_on_screen_and_stage" # Morgan Freeman Webpage
    ]

    def parse(self, response):
        if "Eddie" in response.url: # Get the seed actor's name from the page title
            seed_actor = "Eddie Murphy"
        else:
            seed_actor = "Morgan Freeman"

        for movie in response.css("table.plainrowheaders tr"): # Loop through each movie in the filmography list
            url = movie.css("td i a::attr(href)").get() # Get the URL of the movie page from the first column
            movie_title = movie.css("td i a::attr(title)").get() # Get the movie title
            if url: # avoid empty rows
                yield scrapy.Request(
                    url=response.urljoin(url),
                    callback=self.parse_filmography,
                    cb_kwargs={"seed_actor": seed_actor, "movie_title": movie_title} # Pass seed_actor to next function
                )

    def parse_filmography(self, response, seed_actor, movie_title):
        for castmember in response.css("div.mw-content-ltr.mw-parser-output ul li"): # Loop through each cast member in the cast list on the movie page
            co_actor = castmember.css("a::attr(title)").get() # Get the co-actor's name from the cast list on the movie page
            if co_actor:
                yield {
                    "seed_actor": seed_actor,
                    "movie_title": movie_title,
                    "co_actor": co_actor,
                    "source": "wikipedia"
                }