Little scripts to crawl the content of teufelsturm.de and create offline usable HTML.

# usage

1. `scrapy crawl teufelsturm`
   - raw html and images contained in **./output/**
2. `python ./src/convert.py`
   - converted html page contained in **./converted/** 
3. open **./converted/index.html** in a browser