import sqlite3
con = sqlite3.connect("spelldata.db")
cur = con.cursor()
cur.execute("CREATE TABLE spells(name, school, source, url, level, components, casting time, range, area, target, effect, duration, saving throw, spell resistance)")
res = cur.execute("SELECT name FROM sqlite_master")
res.fetchone()