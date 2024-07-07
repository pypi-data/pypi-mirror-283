# Google Scraper

---

## Installation

호스트 머신에 구글 크롬이 설치되어 있어야 함. [리눅스에 구글 크롬 설치하기.](https://support.google.com/chrome/a/answer/9025903?hl=en)

크롬이 설치되어 있으면, (이 패키지는 퍼블리 PyPI에 업로드 하지 않아서, 우리 GitLab으로부터 설치해야 합니다!)

```bash
pip install git+http://gitlab.cjcj.io/food-360/data-collector/google-scraper.git
```



## Google Shopping 사용하기

```python
from google_scraper.connect import webdriver_maker
from google_scraper.shopping import ReviewScraper, ProductScraper, OfferScraper, SpecScraper

TEST_PRODUCT_URL = 'https://www.google.com/shopping/product/15835715455185603972/?q=Bibigo&gl=us&num=50&hl=en&prds=pid:768232301723508999,rsk:PC_4302309345052043859'

driver = webdriver_maker()

# 제품 상세페이지 Scraper
product_scraper = ProductScraper(driver)
product_info = product_scraper(product_url=TEST_PRODUCT_URL)

# 리뷰 페이지 Scraper
review_scraper = ReviewScraper(driver)
reviews = review_scraper(product_url=TEST_PRODUCT_URL)

# 제품사양 페이지 Scraper
spec_scraper = SpecScraper(driver)
specification = spec_scraper(product_url=TEST_PRODUCT_URL)

# 제품 판매 정보 Scraper (미완성)
offer_scraper = OfferScraper(driver)
offers = offer_scraper(product_url=TEST_PRODUCT_URL)
```

