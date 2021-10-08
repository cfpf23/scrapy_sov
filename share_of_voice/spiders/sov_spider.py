import scrapy
import pandas as pd
import json
import datetime
import scrapy_splash
from scraper_interpreter.content_scraper import ContentBot

# from apteka_melissa_pl.scraper_interpreter.content_scraper import ContentBot

# from scrapy_sov.sov_bayer.apteka_melissa_pl.apteka_melissa_pl.scraper_interpreter.content_scraper import ContentBot
# docker run -p 8050:8050 scrapinghub/splash

root_dir = r'C:\Users\c.ferrao\Documents\Projects\sov_bayer_scrapper'.replace('\\', '/')
cloud_root = r'C:\Users\c.ferrao\Pathfinder23\Business Intelligence Team - 05. SOV_Tracking'.replace('\\', '/')
json_root = f'{root_dir}/e_retailers_library'

ua_mobile = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) ' \
            'Version/11.0 Mobile/15A372 Safari/604.1 '
ua_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 ' \
             'Safari/537.36 '
"""
run docker: docker run -p 8050:8050 scrapinghub/splash
task = 'products' or 'banners.
apteka = 'melissa', 'doz' or 'gemini'
json_name = 'apteka-melissa_pl', 'doz_pl' or 'aptekagemini_pl'
"""
task = 'products'


# apteka = 'gemini'
# json_name = 'aptekagemini_pl'


def open_json(file):
    with open(file) as json_file:
        json_output = json.load(json_file)
    return json_output


def expand_number(refresh_number):
    return ','.join([str(n) for n in range(1, int(refresh_number) + 1)])


class Sov(scrapy.Spider, ContentBot):
    """
    TODO work on this issue with the connectors from a json file
    """

    name = f'{task}_sov'

    path_library = 'e_retailer_library'

    splash_script = """
            function main(splash)
              splash:go(splash.args.url)
              splash:wait(0.5)
              local site_depth = 0
              local scroll_to = splash:jsfunc("window.scrollTo")
              while site_depth < 3000 do
                site_depth = site_depth + 500
                scroll_to(0, site_depth)
                splash:wait(0.2)
              end
              splash:set_viewport_full()
              local html = splash:html()
              return html
            end
    """

    def find_my_json(self, link):
        e_retailers = {
            'doz': {"engine": "Scrapy", "request": "scrapy_splash", "setup": False},
            'apteka-melissa': {"engine": "Scrapy", "request": "scrapy_splash", "setup": False},
            'aptekagemini': {"engine": "Scrapy", "request": "scrapy_splash", "setup": False},
            'shop-apotheke': {"engine": "Scrapy", "request": "scrapy_splash", "setup": False},
            'mediaworld': {"engine": "Scrapy", "request": "scrapy_splash", "setup": False},
            'kruidvat': {"engine": "Scrapy", "request": "scrapy", "setup": False},
            'bol': {"engine": "Scrapy", "request": "scrapy_splash", "setup": False},
            'allegro': {"engine": "Scrapy", "request": "scrapy_splash", "setup": True}
            # 'allegro': {"engine": "Scrapy", "additional_scrapping": False}, UNDONE
        }
        markets = ['es', 'co.uk', 'fr', 'de', 'it', 'pl', 'nl', 'com', 'br', 'se']
        for e_r, value in e_retailers.items():
            if len(link.split(f'www.{e_r}')) > 1:
                for m in markets:
                    if len(link.split(f'www.{e_r}.{m}')) > 1:
                        m = m.split('.')[-1]
                        file = f'{self.path_library}/{e_r}_{m}.json'
                        instructions = {"file": file}
                        for k, v in value.items():
                            instructions[k] = v
                        return instructions

    def request_manager(self, url, instructions, platform, cb_kwargs):
        if platform == 'mobile':
            ua = ua_mobile
        else:
            ua = ua_desktop
        if instructions['request'] == 'scrapy_splash':
            return scrapy_splash.SplashRequest(url=url,
                                               dont_filter=False,
                                               callback=self.parse,
                                               headers={'User-Agent': ua},
                                               cb_kwargs=cb_kwargs,
                                               endpoint="execute",
                                               args={'lua_source': self.splash_script,
                                                     'wait': 0.5,
                                                     "proxy": "http://host.docker.internal:8888"})
        else:
            return scrapy.Request(url=url,
                                  dont_filter=False,
                                  callback=self.parse,
                                  headers={'User-Agent': ua_mobile},
                                  cb_kwargs=cb_kwargs)

    def start_requests(self):
        sov_bayer_pages = pd.read_excel(f'{cloud_root}/input/template_test.xlsx', sheet_name='PAGES')
        # apteka = 'doz'
        # json_name = 'doz_pl'
        # task = 'products'

        # melissa_filtered = sov_bayer_pages[sov_bayer_pages['E_RETAILER'] == apteka]
        for column in ['E_RETAILER', 'PAGE_TYPE', 'KEYWORD', 'URL', 'PROJECT', 'SCRAP_TYPE', 'REFRESH',
                       'REFRESH_BANNERS',
                       'REFRESH_PRODUCTS']:
            sov_bayer_pages[column] = sov_bayer_pages[column].apply(lambda x: str(x).strip())
        sov_bayer_pages['REFRESH'] = sov_bayer_pages['REFRESH'].apply(expand_number)
        sov_bayer_pages = sov_bayer_pages.assign(REFRESH=sov_bayer_pages['REFRESH'].str.split(',')).explode(
            'REFRESH').reset_index()
        for index, row in sov_bayer_pages.iterrows():
            json_file = self.find_my_json(link=row['URL'])
            row_data = {'page_type': row['PAGE_TYPE'],
                        'scrap_type': row['SCRAP_TYPE'],
                        'refresh_number': row['REFRESH'],
                        'keyword': row['KEYWORD'],
                        'json_file': json_file,
                        'e_retailer': row['E_RETAILER'],
                        'task': task}
            if json_file['setup']:
                yield self.request_manager(url=row['URL'], instructions=json_file, platform=row['SCRAP_TYPE'], cb_kwargs=row_data)
                # if row['SCRAP_TYPE'] == 'mobile':
                #     # url=row['URL']
                #     # url='file:///C:/Users/c.ferrao/AppData/Local/Temp/tmpq_7e2jb_.html' homepage DOZ
                #     # url='file:///C:/Users/c.ferrao/AppData/Local/Temp/tmpny6tb8h1.html' search DOZ
                #     # url='file:///C:/Users/c.ferrao/AppData/Local/Temp/tmpsh5j7zez.html' category DOZ !
                #     # url='file:///C:/Users/c.ferrao/AppData/Local/Temp/tmp23x78g2y.html' product DOZ
                #
                #     # url='file:///C:/Users/c.ferrao/AppData/Local/Temp/tmpnyso3nzl.html' category gemini
                #     # url='file:///C:/Users/c.ferrao/AppData/Local/Temp/tmp280b_erw.html' homepage gemini
                #
                #     # url = 'file:///C:/Users/c.ferrao/AppData/Local/Temp/tmpq1c2f44n.html' gemini homepage
                #     yield scrapy.Request(url=row['URL'],
                #                          dont_filter=False,
                #                          callback=self.parse,
                #                          headers={'User-Agent': ua_mobile},
                #                          cb_kwargs=row_data)
                #     # if row['REFRESH_BANNERS'] == 'no':
                #     # yield scrapy_splash.SplashRequest(url=row['URL'],
                #     #                                   dont_filter=False,
                #     #                                   callback=self.parse,
                #     #                                   headers={'User-Agent': ua_mobile},
                #     #                                   cb_kwargs=row_data,
                #     #                                   endpoint="execute",
                #     #                                   args={'lua_source': self.splash_script,
                #     #                                         'wait': 0.5,
                #     #                                         "proxy": "http://host.docker.internal:8888"})
                # else:
                #     yield scrapy.Request(url=row['URL'],
                #                          dont_filter=False,
                #                          callback=self.parse,
                #                          headers={'User-Agent': ua_desktop},
                #                          cb_kwargs=row_data)
                #     # yield scrapy_splash.SplashRequest(url=row['URL'],
                #     #                                   dont_filter=False,
                #     #                                   callback=self.parse,
                #     #                                   headers={'User-Agent': ua_desktop},
                #     #                                   cb_kwargs=row_data,
                #     #                                   endpoint="execute",
                #     #                                   args={'lua_source': self.splash_script,
                #     #                                         'wait': 0.5,
                #     #                                         "proxy": "http://host.docker.internal:8888"})

    custom_settings = {
        "FEEDS": {f"{task}_sov.csv": {"format": "csv"}},
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
        "LOG_FILE": f"log_sov_{task}.txt",
    }

    # @staticmethod
    # def product_card_scraper(instructions, response, scrap_type, refresh_number, keyword):
    #     page_type = instructions['page_type']
    #
    #     instructions = instructions['json_instructions']['product_card']
    #     n = 1
    #
    #     product_card_instance = ContentBot()
    #
    #     item_data = {}
    #
    #     item_data.update({"description": 'product_main_product_page',
    #                       "order": n,
    #                       "e_retailer": "melissa",
    #                       "project": "Bayer",
    #                       "page_link": response.url,
    #                       "page_type": page_type,
    #                       'scrap_type': scrap_type,
    #                       'refresh_number': refresh_number,
    #                       'keyword': keyword,
    #                       "date": datetime.date.today()})
    #
    #     item_data.update(product_card_instance.get_content(content_instructions=instructions,
    #                                                        response=response))
    #
    #     print('worked!', item_data)
    #
    #     yield item_data

    def parse(self, response, page_type, scrap_type, refresh_number, keyword, json_file, task, e_retailer):
        # print(response.text)
        # html_file = open('page_text.html', 'w')
        # html_file.write(response.body.decode("utf-8"))
        # print('json_file', json_file)

        e_retailer_instructions = open_json(json_file['file'])
        page_type = page_type.strip().replace(' ', '_').lower()
        instructions = {'json_instructions': e_retailer_instructions,
                        'page_type': page_type}

        if (page_type == 'product_page') and (task == 'products'):
            page_type = instructions['page_type']

            instructions = instructions['json_instructions']['product_card']
            n = 1
            # print('instructions', instructions)

            product_card_instance = ContentBot()

            item_data = {}

            item_data.update({"description": 'product_main_product_page',
                              "order": n,
                              "e_retailer": e_retailer,
                              "project": "Bayer",
                              "page_link": response.url,
                              "page_type": page_type,
                              'scrap_type': scrap_type,
                              'refresh_number': refresh_number,
                              'keyword': keyword,
                              "date": datetime.date.today()})

            item_data.update(product_card_instance.get_content(content_instructions=instructions,
                                                               response=response))

            # print('worked!', item_data)
            yield item_data
        else:
            page_type = instructions['page_type']
            if task == 'products':
                instructions = instructions['json_instructions']['listing'][0]['containers']
            else:
                instructions = instructions['json_instructions']['listing'][0]['banners']
                # print('instructions_banners', instructions)

            items_page_type = []
            for product_container in instructions:
                if product_container['page_type'] == page_type:
                    product_container_instructions = {}
                    product_container_instructions.update({
                        'container_instructions': {product_container['name']: {
                            'name': product_container['name'],
                            'functions': [
                                product_container['locate']
                            ]}},
                        'field_instructions': product_container['fields']})
                    items_page_type.append(product_container_instructions)

            listings_instance = ContentBot()
            for item in items_page_type:
                n = 1
                product_frames_found = listings_instance.get_content(
                    content_instructions=item['container_instructions'],
                    response=response)
                for web_element in [element for element in product_frames_found.values()][0]:
                    item_data = {}
                    description = [k for k in item['container_instructions']][0]
                    print(f'Processing - {description} - {e_retailer}')

                    item_data.update({"order": n,
                                      "e_retailer": e_retailer,
                                      "project": "Bayer",
                                      "page_link": response.url,
                                      "page_type": page_type,
                                      'scrap_type': scrap_type,
                                      'refresh_number': refresh_number,
                                      'keyword': keyword,
                                      "date": datetime.date.today()})
                    item_data.update(listings_instance.get_content(content_instructions=item['field_instructions'],
                                                                   response=web_element))
                    item_data.update({"description": [k for k in item['container_instructions'].keys()][0]})
                    n = n + 1
                    yield item_data
