import scrapy
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import read
from spellitem import DndSpellPipeline  # Import the pipeline

class DndSpellSpider(scrapy.Spider):
    name = 'dnd_spell'
    start_urls = [
        'https://dndtools.net/spells/complete-arcane--55/absorption--433/',
        # Add more URLs as needed
    ]
    custom_settings = {
        'ITEM_PIPELINES': {'spellitem.DndSpellPipeline': 1},
    }

    '''def start_requests(self):
        # Authenticate with Google Sheets
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        gc = gspread.authorize(credentials)

        # Open the spreadsheet and select the worksheet
        spreadsheet = gc.open("all spells")
        worksheet = spreadsheet.worksheet("Sheet1")

        # Extract URLs from the first column of the worksheet
        urls = worksheet.col_values(1)

        # Send requests for each URL
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)'''

    def parse(self, response):
        item = {}
        item['title'] = response.xpath('(//h2)[2]/text()').get().strip()
        levels = response.xpath('//strong[contains(text(), "Level:")]/following-sibling::a/text()').getall()
        item['level'] = ", ".join(levels)
        item['components'] = ','.join(response.xpath('//strong[contains(text(), "Components:")]/following-sibling::abbr/text()').getall())
        item['casting_time'] = response.xpath('//strong[contains(text(), "Casting Time:")]/following-sibling::text()').get(default='').strip()
        item['range'] = response.xpath('//strong[contains(text(), "Range:")]/following-sibling::text()').get(default='').strip()
        item['target'] = response.xpath('//strong[contains(text(), "Target:")]/following-sibling::text()').get(default='').strip()
        item['effect'] = response.xpath('//strong[contains(text(), "Effect:")]/following-sibling::text()').get(default='').strip()
        item['area'] = response.xpath('//strong[contains(text(), "Area:")]/following-sibling::text()').get(default='').strip()
        item['duration'] = response.xpath('//strong[contains(text(), "Duration:")]/following-sibling::text()').get(default='').strip()
        item['saving_throw'] = response.xpath('//strong[contains(text(), "Saving Throw:")]/following-sibling::text()').get(default='').strip()
        item['spell_resistance'] = response.xpath('//strong[contains(text(), "Spell Resistance:")]/following-sibling::text()').get(default='').strip()
        item['source'] = response.xpath('//h2/following-sibling::br[1]/following-sibling::text()').get(default='').strip()
        item['url'] = response.url
        item['description'] = '\n'.join(response.xpath('//div[@class="nice-textile"]/p/text()').getall())
        # print("Parsed item:", item)  # Add this line for debugging
        yield item