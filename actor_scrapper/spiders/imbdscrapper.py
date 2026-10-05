import scrapy

# Web scraped IMDB for Morgan Freeman and Eddie Murphy filmography
# Shawn Tribuce
# DS3500 Homework 4
# 03/11/2026

class ImdbScraperSpider(scrapy.Spider):
    name = "imdb" # The name to refer to in terminal when running the spider
    allowed_domains = ["www.imbd.com"] # Restrict the spider to only crawl pages from this domain
    start_urls = [
        "https://www.imdb.com/name/nm0000168/",
        "https://www.imdb.com/name/nm0000552/"
    ] # Starting URLs for the spider to begin crawling

    def parse(self, response):
        seed_actor = response.css("h1.sc-afe43def-1::text").get() # Get the seed actor's name from the page title
        for movie in response.css("li.ipc-metadata-list-summary-item"): # Loop through each movie in the filmography list
            url = movie.css("a.ipc-metadata-list-summary-item__t::attr(href)").get() # Get the URL of the movie page from the first column
            if url: # avoid empty rows
                yield scrapy.Request(
                    url=response.urljoin(url),
                    callback=self.parse_filmography,
                    cb_kwargs={"seed_actor": seed_actor} # Pass seed_actor to next function
                )

    def parse_filmography(self, response, seed_actor):
        movie_title = response.css("h1 span::text").get() # Get the movie title from the page title
        for cast in response.css("[data-testid='title-cast-item']"): # Loop through each cast member in the cast list on the movie page
            co_actor = cast.css("[data-testid='title-cast-item__actor']::text").get() # Get the co-actor's name from the cast list on the movie page
            if co_actor:
                yield {
                    "seed_actor": seed_actor,
                    "movie_title": movie_title,
                    "co_actor": co_actor,
                    "source": "imdb"
                }