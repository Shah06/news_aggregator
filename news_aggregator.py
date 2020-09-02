import feedparser
import time
from datetime import datetime

# timezone adjustment (currently 12 hours)
TZ_ADJUST = -28800

# output file
OUTPUT_FILE = "output.html"

# open from sources
SOURCES_FILE = "sources.txt"
sources = [line.rstrip('\n') for line in open(SOURCES_FILE)]

articles_arr = [] # should be an array of tuples (timestamp, link)
html_content = "<!DOCTYPE html><html><body><h1>NEWS</h1><h3>Updated: "+str(datetime.now())+"</h3><ol>"

for source in sources:
   
    source_parsed = feedparser.parse(source)
    for entry in source_parsed.entries:
        #entry_string_formatted = (str(entry.title) + "\n" + str(entry.link) + "\n")
        entry_date = entry.published_parsed # date as a standard 9-tuple
        timestamp = time.mktime(entry_date) + TZ_ADJUST
        dt_obj = datetime.fromtimestamp(timestamp)
        date_str = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
        #html_formatted_link = "<li><a target=\"_blank\" href=\"" + entry.link + "\"a>" + entry.title + "</a>. Pub: " + entry.published + "</li>"
        html_formatted_link = "<li>" + entry.description + " <em>" + date_str + "</em></li>"
        articles_arr.append( (timestamp, html_formatted_link) ) # tuple that can be used to sort by date
        #html_links.append(html_formatted_link)

# sort the articles by date
articles_arr.sort(key=(lambda a : a[0]), reverse=True)

for article in articles_arr:
    html_content += article[1]

html_content += ("</ol></body></html>")

out = open(OUTPUT_FILE, "w")
out.write(html_content)
