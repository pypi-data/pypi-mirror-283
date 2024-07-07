import logging
import re
import time
import urllib.parse
from datetime import datetime, timedelta
from typing import List

import parse
from bs4 import BeautifulSoup, ResultSet, Tag
from fastnumbers import fast_int
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


def load_page(func):
    def wrapper(self, product_url, *args, **kwargs):
        self.page_loader(product_url=product_url)
        return func(self, product_url, *args, **kwargs)

    return wrapper


################################################################
# GoogleShoppingScraper
################################################################
# [Abstract] GoogleShoppingScraper
class GoogleShoppingScraper:
    def __init__(self, driver: WebDriver, path: str):
        self.driver = driver
        self.path = path.strip("/") if path else path

        # cache
        self.cache_duration_hours = 1
        self.cache = dict()

    def get_url_info(self, product_url: str) -> str:
        PATTERN = "{schema}://{domain}/shopping/product/{product_id}/?{query}"
        PRD_PATTERN = "pid:{pid},rsk:{rsk}"

        p = parse.compile(PATTERN)
        parsed_url = p.parse(product_url)

        if not parsed_url:
            raise

        if self.path:
            scraping_url = "{schema}://{domain}/shopping/product/{product_id}/{path}/?{query}".format(
                **{**parsed_url.named, "path": self.path}
            )
        else:
            scraping_url = product_url

        url_info = {
            "product_id": parsed_url.named["product_id"],
            "product_url": product_url,
            "scraping_url": scraping_url,
        }

        # update query
        prd_pattern_compiler = parse.compile(PRD_PATTERN)
        params = urllib.parse.parse_qsl(parsed_url.named["query"])
        for key, value in params:
            if key == "prds":
                value = prd_pattern_compiler.parse(value)
                url_info.update(value.named)
            else:
                url_info.update({key: value})

        return url_info

    def page_loader(self, product_url: str) -> None:
        # get scraping url
        url_info = self.get_url_info(product_url)
        scraping_url = url_info["scraping_url"]

        now = datetime.now() - timedelta(hours=self.cache_duration_hours)
        if (product_url not in self.cache) or (self.cache[product_url]["updated"] < now):

            self.driver.get(scraping_url)
            self.page_loader_action()

            self.cache[product_url] = {
                "info": url_info,
                "soup": BeautifulSoup(self.driver.page_source, "html.parser"),
                "updated": datetime.now(),
            }

    def page_loader_action(self) -> None:
        pass


# ProductScraper
class ProductScraper(GoogleShoppingScraper):
    def __init__(self, driver: WebDriver):
        super().__init__(driver=driver, path=None)

    ################################
    # Methods you need to know
    ################################
    @load_page
    def __call__(self, product_url: str):
        # [PRODUCT CONTAINER]
        PRODUCT_DIV = ("div", {"class": "sg-product__dpdp-c"})

        product_div = self.cache[product_url]["soup"].find(*PRODUCT_DIV)

        # Placeholder
        product = dict()

        # Product Info
        PRODUCT_INFO_DIV = ("div", {"class": "YVQvvd"})
        PRODUCT_NAME = ("span", {"class": "BvQan sh-t__title-pdp sh-t__title translate-content"})
        PRODUCT_RATING = ("div", {"class": "UzThIf"})
        PRODUCT_TOTAL_REVIEWS = ("span", {"class": "HiT7Id"})

        product_info_div = product_div.find(*PRODUCT_INFO_DIV)
        product_name = product_info_div.find(*PRODUCT_NAME).get_text(strip=True)
        product_rating = product_info_div.find(*PRODUCT_RATING)["aria-label"]
        product_total_reviews = product_info_div.find(*PRODUCT_TOTAL_REVIEWS).span["aria-label"]

        product["product"] = {"name": product_name, "rating": product_rating, "total_reviews": product_total_reviews}

        # Product Properties
        PRODUCT_PROPS_DIV = ("div", {"class": "vqSBk"})
        PRODUCT_PROPS_SPAN = ("span",)
        PRODUCT_PROPS = ("li",)

        product_props_div = product_div.find(*PRODUCT_PROPS_DIV)
        for product_props_span in product_props_div.find_all(*PRODUCT_PROPS_SPAN, recursive=False):
            pass

        product_props = product_props_span.find_all(*PRODUCT_PROPS)
        product_props = {k: v.strip() for k, v in (prop.get_text().split(":") for prop in product_props)}

        product.update({"properties": product_props})

        # Product Detail
        PRODUCT_DETAIL_SECTION = ("section", {"class": "KS6Dwf"})
        PRODUCT_KEYWORD = ("span", {"class": "OA4wid"})
        PRODUCT_DESCRIPTION = ("span", {"class": "sh-ds__full-txt translate-content"})

        product_detail_section = product_div.find(*PRODUCT_DETAIL_SECTION)
        product_keyword = product_detail_section.find_all(*PRODUCT_KEYWORD)
        product_keyword = [span.get_text() for span in product_keyword]
        product_description = product_detail_section.find(*PRODUCT_DESCRIPTION).get_text()

        product.update({"detail": {"keyword": product_keyword, "description": product_description}})

        # [MEDIA VIEWER]
        # Product Images
        MEDIA_VIEWER_DIV = ("div", {"class": "sh-rso__overlay-inner sh-rso__media_viewer_overlay"})
        MEDIA_VIEWER_IMAGES = ("img", {"class": re.compile(r"\bsh-div__image\w*\b")})

        media_viewer_div = self.cache[product_url]["soup"].find(*MEDIA_VIEWER_DIV)
        media_viewer_images = media_viewer_div.find_all(*MEDIA_VIEWER_IMAGES)

        images = [img["src"] for img in media_viewer_images]

        product.update({"images": images})

        # Reviews
        # Reviews는 별도 페이지 추출 (/reviews)

        # Compare buying options
        # Compare buying options 별도 페이지 추출 (/offers)

        # Specification
        # Spacification은 별도 페이지 추출 (/specs)

        return product


# ReviewScraper
class ReviewScraper(GoogleShoppingScraper):
    def __init__(self, driver: WebDriver):
        super().__init__(driver=driver, path="reviews")

    ################################
    # Methods you need to know
    ################################
    @load_page
    def __call__(self, product_url: str, after: str = None) -> List[dict]:

        # Placeholder
        reviews = dict()

        # Product Info
        PRODUCT_INFO = ("div", {"class": "f0t7kf"})
        RATING = ("div", {"class": "UzThIf"})
        TOTAL_REVIEWS = ("span", {"class": "HiT7Id"})

        # Product
        product_info = self.cache[product_url]["soup"].find(*PRODUCT_INFO)
        product_name = product_info.a.get_text(strip=True)
        product_rating = product_info.find(*RATING)["aria-label"]
        product_total_reviews = product_info.find(*TOTAL_REVIEWS).span["aria-label"]

        reviews["product"] = {"name": product_name, "rating": product_rating, "total_reviews": product_total_reviews}

        # Favorable
        FAVORABLE = ("div", {"class": "bvrpZc"})
        CAT_NAME_DIV = ("div", {"class": "QlBp2c iQsAce"})
        CAT_VOTES_DIV = ("div", {"class": "kHy9we"})
        CAT_VOTE_COUNT = ("span", {"class": "ZaATJe"})

        favorable_div = self.cache[product_url]["soup"].find_all(*FAVORABLE)

        favorable = dict()
        for category_div in favorable_div:
            cat_name_div = category_div.find(*CAT_NAME_DIV)
            cat_name = cat_name_div.span.get_text()
            favorable[cat_name] = dict()

            cat_votes_div = category_div.find_all(*CAT_VOTES_DIV)
            for cat_vote_div in cat_votes_div:
                vote_name = cat_vote_div.span.get_text()
                vote_count = fast_int(cat_vote_div.find(*CAT_VOTE_COUNT).span.get_text())
                favorable[cat_name].update({vote_name: vote_count})

        reviews["favorable"] = favorable

        # Reviews
        EACH_REVIEW_SELECTORS = "#sh-rol__reviews-cont > div"

        review_divs = self.cache[product_url]["soup"].body.select(EACH_REVIEW_SELECTORS)
        all_reviews = list()
        for review_div in review_divs:
            try:
                review = self.review_parser(review_div)
                all_reviews.append(review)
            except Exception as ex:
                logger.warning(ex)
        if after:
            after_obj = datetime.strptime(after, "%Y-%m-%d")
            all_reviews = [r for r in reviews if r["date_obj"] >= after_obj]

        reviews["reviews"] = all_reviews

        return reviews

    ################################
    # Page Loader Action
    ################################
    def page_loader_action(self) -> None:
        MORE_REVIEWS_BUTTON_LOCATOR = (By.XPATH, '//*[@id="sh-fp__pagination-button-wrapper"]/button')

        while True:
            try:
                elem = WebDriverWait(self.driver, 2.0).until(
                    EC.presence_of_element_located(MORE_REVIEWS_BUTTON_LOCATOR)
                )
            except TimeoutException:
                break
            try:
                elem.click()
                time.sleep(0.5)
            except StaleElementReferenceException:
                continue

    ################################
    # Parser
    ################################
    @staticmethod
    def review_parser(review_div: Tag) -> dict:
        TITLE = ("div", {"class": re.compile(r"\b(P3O8Ne less-spaced|_-i2 less-spaced)\b")})
        RATING = ("div", {"class": re.compile(r"\b(UzThIf|_-lz)\b")})
        DATE = ("span", {"class": re.compile(r"\b(less-spaced ff3bE nMkOOb|less-spaced _-i8 _-i6)\b")})
        REVIEW_ID_PATTERN = re.compile(f"-full$")
        REVIEWER = ("div", {"class": re.compile(r"\b(sPPcBf|_-i3)\b")})  # _-i3
        REVIEWER_SEP = "·Review provided by"
        IMAGES_DIV = ("div", {"class": "gQVipb smsrl"})
        THUMBNAILS = ("img", {"class": "sg-review__review-image"})
        IMAGES = ("img", {"class": "sg-review__review-image-detail"})

        # title
        title = review_div.find(*TITLE)
        if title:
            title = title.get_text(strip=True)

        # rating
        rating = review_div.find(*RATING)
        rating = rating["aria-label"]

        # date
        date = review_div.find(*DATE).get_text(strip=True)
        date_obj = datetime.strptime(date, "%B %d, %Y")

        # comment
        comment = review_div.find(id=REVIEW_ID_PATTERN).get_text(strip=True)
        comment = comment.rstrip("Less")

        # reviewer
        reviewer = review_div.find(*REVIEWER).get_text(strip=True)
        reviewer, source = reviewer.split(REVIEWER_SEP)

        # results
        results = {
            "title": title,
            "rating": rating,
            "date": date,
            "date_obj": date_obj,
            "comment": comment,
            "reviewer": reviewer,
            "source": source,
        }

        # thumbnails & images
        divs = review_div.find_all("div")
        for div in divs:
            images_div = div.find(*IMAGES_DIV)
            if images_div:
                break
        else:
            return results

        thumbnails = images_div.find_all(*THUMBNAILS)
        images = images_div.find_all(*IMAGES)
        results.update({"thumbnails": [img["src"] for img in thumbnails], "images": [img["src"] for img in images]})

        return results


# OfferScraper
class OfferScraper(GoogleShoppingScraper):
    def __init__(self, driver: WebDriver):
        super().__init__(driver=driver, path="offers")

    @load_page
    def __call__(self, product_url):
        # Offers Container
        OFFERS_DIV = ("div", {"class": "dPIF2d"})

        soup = self.cache[product_url]["soup"]
        offers_div = soup.find(*OFFERS_DIV)

        # Placeholder
        offers = dict()

        # PRODUCT INFO
        PRODUCT_INFO_DIV = ("div", {"class": "lBRvsb"})
        PRODUCT_NAME = ("a", {"class": "BvQan sh-t__title sh-t__title-pdp translate-content"})
        PRODUCT_RATING = ("div", {"class": "UzThIf"})
        PRODUCT_TOTAL_REVIEWS = ("span", {"class": "HiT7Id"})

        product_info_div = offers_div.find(*PRODUCT_INFO_DIV)
        product_name = product_info_div.find(*PRODUCT_NAME).get_text(strip=True)
        product_rating = product_info_div.find(*PRODUCT_RATING)["aria-label"]
        product_total_reviews = product_info_div.find(*PRODUCT_TOTAL_REVIEWS).span["aria-label"]

        offers["product"] = {"name": product_name, "rating": product_rating, "total_reviews": product_total_reviews}

        # OFFERS TABLE
        OFFERS_TABLE = ("table", {"id": "sh-osd__online-sellers-grid"})
        offers_table = offers_div.find(*OFFERS_TABLE)

        # [TODO] parse this table!

        offers.update({"offers": offers_table})

        return offers


# SpecScraper
class SpecScraper(GoogleShoppingScraper):
    def __init__(self, driver: WebDriver):
        super().__init__(driver=driver, path="specs")

    @load_page
    def __call__(self, product_url: str) -> List[dict]:
        # [PRODUCT INFO CONTAINER]
        PRODUCT_INFO_DIV = ("div", {"class": "f0t7kf"})
        product_info_div = self.cache[product_url]["soup"].find(*PRODUCT_INFO_DIV)

        # Placeholder
        results = dict()

        # Product Info
        PRODUCT_NAME = ("a", {"class": "BvQan sh-t__title sh-t__title-pdp translate-content"})
        PRODUCT_RATING = ("div", {"class": "UzThIf"})
        PRODUCT_TOTAL_REVIEWS = ("span", {"class": "HiT7Id"})

        product_name = product_info_div.find(*PRODUCT_NAME).get_text(strip=True)
        product_rating = product_info_div.find(*PRODUCT_RATING)["aria-label"]
        product_total_reviews = product_info_div.find(*PRODUCT_TOTAL_REVIEWS).span["aria-label"]

        results["product"] = {"name": product_name, "rating": product_rating, "total_reviews": product_total_reviews}

        # Specification
        SPECS_TABLE = ("table", {"class": "O2pTHb"})
        specs_table = self.cache[product_url]["soup"].find(*SPECS_TABLE)

        specs = dict()
        for row in specs_table.find_all("tr"):
            if not row.attrs.get("class"):
                cat = row.td.get_text(strip=True)
                specs[cat] = dict()
                continue
            attr = row.find("div").get_text(strip=True)
            value = row.find("td", {"class": "AnDf0c"}).get_text(strip=True)
            specs[cat].update({attr: value})

        results.update({"specifications": specs})

        return results
