from dataclasses import dataclass



@dataclass
class Spell:
    name: str
    level: str
    components: str
    casting_time: str
    spell_range: str
    target: str
    effect: str
    area: str
    duration: str
    saving_throw: str
    spell_resistance: str
    source: str
    url: str
    description: str


class DerScraper:
    def parse_url(self, url: str) -> Spell:
        s = Spell()
        raise NotImplementedError
    
class DummyScraper(DerScraper):
    def parse_url(self, url: str) -> Spell:
        s = Spell()
        s.name = "Fireball"
        s.area = "big"
        s.spell_range = "short"
        s.description = "u gonna get hurt bro"
        return s

class DasSpreadsheet:
    def __init__(self, scraper: DerScraper):
        self.scraper = scraper
        # verbindung herstellen
        raise NotImplementedError

    def parse_line(self, linenumber: int):
        #get url
        #Scraper.parse_url()
        #wieder ins spreadsheet schreiben
        raise NotImplementedError
    
    def parse_all(self):
        raise NotImplementedError
 