import scrapy
class SpellSpider(scrapy.Spider):
    name = 'spell_spider'
    start_urls = ['https://dndtools.org/spells/spell-compendium--86/absorption--3798/']

    def parse(self, response):
        # Extracting information using XPath expressions
        spell_name = response.xpath('//h2[text()="Absorption"]').get()
        spell_level = response.xpath('//strong[text()="Level:"]/following-sibling::a/text()').get()
        components = response.xpath('//strong[text()="Components:"]/following-sibling::abbr/text()').get()
        casting_time = response.xpath('//strong[text()="Casting Time:"]/following-sibling::text()').get()
        spell_range = response.xpath('//strong[text()="Range:"]/following-sibling::text()').get()
        spell_target = response.xpath('//strong[text()="Target:"]/following-sibling::text()').get()
        spell_duration = response.xpath('//strong[text()="Duration:"]/following-sibling::text()').get()
        spell_description = '\n'.join(response.xpath('//div[@class="nice-textile"]/p/text()').getall())
        spell_item['source'] = response.xpath('//h2/following-sibling::br[1]/following-sibling::text()').get().strip()
        spell_item['url'] = response.url

        # Print or further process the extracted information
        print(f"Spell Name: {spell_name}")
        print(f"Spell Level: {spell_level}")
        print(f"Components: {components}")
        print(f"Casting Time: {casting_time}")
        print(f"Range: {spell_range}")
        print(f"Target: {spell_target}")
        print(f"Duration: {spell_duration}")
        print(f"Spell Description: {spell_description}")

    def parse(self, response):
        for quote in response.xpath("//strong"):
            yield {
                "author": quote.xpath('//*[text()="Casting Time:"]').get(),
                "text": quote.xpath("following-sibling::text()").get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

class SpellItem(scrapy.Item):
    spell_name = scrapy.Field()
    spell_level = scrapy.Field()
    components = scrapy.Field()
    casting_time = scrapy.Field()
    spell_range = scrapy.Field()
    spell_target = scrapy.Field()
    spell_duration = scrapy.Field()
    spell_description = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    saving_throw = scrapy.Field()
    spell_resistance = scrapy.Field()

class SpellSpider(scrapy.Spider):
    name = 'spell_spider'
    start_urls = [
        'https://dndtools.org/spells/spell-compendium--86/absorption--3798/',
        'https://dndtools.org/spells/spell-compendium--86/acid-storm--3803/'
    ]

    def parse(self, response):
        # Extracting information using XPath expressions
        spell_item = SpellItem()
        spell_item['spell_name'] = response.xpath('//h2/text()').get()
        spell_item['spell_level'] = response.xpath('//strong[text()="Level:"]/following-sibling::a/text()').get()
        spell_item['components'] = response.xpath('//strong[text()="Components:"]/following-sibling::abbr/text()').get()
        spell_item['casting_time'] = response.xpath('//strong[text()="Casting Time:"]/following-sibling::text()').get()
        spell_item['spell_range'] = response.xpath('//strong[text()="Range:"]/following-sibling::text()').get()
        spell_item['spell_target'] = response.xpath('//strong[text()="Target:"]/following-sibling::text()').get()
        spell_item['spell_duration'] = response.xpath('//strong[text()="Duration:"]/following-sibling::text()').get()
        spell_item['spell_description'] = '\n'.join(response.xpath('//div[@class="nice-textile"]/p/text()').getall())
        spell_item['source'] = response.xpath('//h2/following-sibling::br[1]/following-sibling::text()').get().strip()
        spell_item['url'] = response.url
        spell_item['saving_throw'] = response.xpath('//strong[contains(text(), "Saving Throw:")]/following-sibling::br/text()').get().strip()
        spell_item['spell_resistance'] = response.xpath('//strong[contains(text(), "Spell Resistance:")]/following-sibling::br/text()').get().strip()

        # Yield the item to be processed by the pipelines
        yield spell_item


