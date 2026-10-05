import scrapy

# Web scraped Letterboxd for Morgan Freeman and Eddie Murphy filmography
# Shawn Tribuce
# DS3500 Homework 4
# 03/11/2026


class LetterboxdScraperSpider(scrapy.Spider):
    name = "letterboxd"
    allowed_domains = ["letterboxd.com"]  # no https:// in allowed_domains
    start_urls = [
        "https://letterboxd.com/actor/morgan-freeman/",
        "https://letterboxd.com/actor/eddie-murphy/"
    ]

    def parse(self, response):
        seed_actor = response.css("h1.title-1::text").get()
        for movie in response.css("li.tooltip.griditem"):
            url = movie.css("div.film-poster a::attr(href)").get()
            if url:
                yield scrapy.Request(
                    url=response.urljoin(url),
                    callback=self.parse_filmography,
                    cb_kwargs={"seed_actor": seed_actor}
                )

    def parse_filmography(self, response, seed_actor):
        movie_title = response.css("h1.headline-1::text").get()
        for cast in response.css("div.cast-list a.text-slug"):
            co_actor = cast.css("::text").get()
            if co_actor:
                yield {
                    "seed_actor": seed_actor,
                    "movie_title": movie_title,
                    "co_actor": co_actor,
                    "source": "letterboxd"
                }