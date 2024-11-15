import sqlite3
import scrapy
from scrapy.exceptions import DropItem
class DndSpellPipeline:
    def __init__(self):
        # Initialize the SQLite database connection
        self.conn = sqlite3.connect('dnd_spells.db')
        self.cursor = self.conn.cursor()

        # Create a table to store spell information
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS spells (
                title TEXT,
                level TEXT,
                components TEXT,
                casting_time TEXT,
                range TEXT,
                target TEXT,
                duration TEXT,
                saving_throw TEXT,
                spell_resistance TEXT,
                source TEXT,
                url TEXT,
                description TEXT
            )
        ''')
        self.conn.commit()

    def process_item(self, item, spider):
        # Convert the 'level' list to a string
        item['level'] = ', '.join(item['level'])

        # Insert the extracted information into the database
        self.cursor.execute('''
            INSERT INTO spells (title, level, components, casting_time, range, target, duration, saving_throw, spell_resistance, source, url, spell_description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (item['title'], ', '.join(item['level']), item['components'], item['casting_time'], item['range'],
              item['target'], item['duration'], item['saving_throw'], item['spell_resistance'], item['source'],
              item['url'], item['description']))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # Close the database connection when the spider is finished
        self.conn.close()

class DndSpellSpider(scrapy.Spider):
    name = 'dnd_spell'
    start_urls = [
        'https://dndtools.net/spells/complete-arcane--55/absorption--433/',
        # Add more URLs as needed
    ]

    custom_settings = {
        'ITEM_PIPELINES': {'spellitem.DndSpellPipeline': 1},
    }

    def parse(self, response):
        item = {}
        item['title'] = response.xpath('//h2/text()').get().strip()
        levels = response.xpath('//strong[contains(text(), "Level:")]/following-sibling::a/text()').getall()
        item['level'] = [level.strip().replace(",", "") for level in levels]
        item['components'] = ','.join(response.xpath('//strong[contains(text(), "Components:")]/following-sibling::abbr/@title').getall())
        item['casting_time'] = response.xpath('//strong[contains(text(), "Casting Time:")]/following-sibling::text()').get(default='').strip()
        item['range'] = response.xpath('//strong[contains(text(), "Range:")]/following-sibling::text()').get(default='').strip()
        item['target'] = response.xpath('//strong[contains(text(), "Target:")]/following-sibling::text()').get(default='').strip()
        item['duration'] = response.xpath('//strong[contains(text(), "Duration:")]/following-sibling::text()').get(default='').strip()
        item['saving_throw'] = response.xpath('//strong[contains(text(), "Saving Throw:")]/following-sibling::text()').get(default='').strip()
        item['spell_resistance'] = response.xpath('//strong[contains(text(), "Spell Resistance:")]/following-sibling::text()').get(default='').strip()
        item['source'] = response.xpath('//h2/following-sibling::br[1]/following-sibling::text()').get(default='').strip()
        item['url'] = response.url
        item['description'] = '\n'.join(response.xpath('//div[@class="nice-textile"]/p/text()').getall())
        print("Parsed item:", item)  # Add this line for debugging
        yield item

    def process_item(self, item, spider):
        # Convert the 'level' list to a string
        item['level'] = ', '.join(item['level'])

        # Insert the extracted information into the database
        sql = '''
            INSERT INTO spells (title, level, components, casting_time, range, target, duration, saving_throw, spell_resistance, source, url, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        values = (item['title'], ', '.join(item['level']), item['components'], item['casting_time'], item['range'],
                  item['target'], item['duration'], item['saving_throw'], item['spell_resistance'], item['source'],
                  item['url'], item['description'])
        print("SQL Statement:", sql)
        print("Values:", values)

        self.cursor.execute(sql, values)
        self.conn.commit()
        return item
