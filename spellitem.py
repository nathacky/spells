import sqlite3
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
                effect TEXT,
                area TEXT,
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
       # item['level'] = ', '.join(item['level'])

        # Insert the extracted information into the database
        sql = '''
            INSERT INTO spells (title, level, components, casting_time, range, target, effect, area, duration, saving_throw, spell_resistance, source, url, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        values = (item['title'],
                  item['level'],
                  item['components'],
                  item['casting_time'],
                  item['range'],
                  item['target'],
                  item['effect'],
                  item['area'],
                  item['duration'],
                  item['saving_throw'],
                  item['spell_resistance'],
                  item['source'],
                  item['url'],
                  item['description'])

        self.cursor.execute(sql, values)
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # Close the database connection when the spider is finished
        self.conn.close()