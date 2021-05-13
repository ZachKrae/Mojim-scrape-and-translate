import requests
from bs4 import BeautifulSoup
import io
import re
import sys
from googletrans import Translator

response = requests.get(sys.argv[1])
soup = BeautifulSoup(response.content, "html.parser")

# scrape lyrics only
formatted_lyrics = soup.find("dl", {"class": "fsZx1"}).prettify()

# scrape song title
song_title = soup.find("dt", {"class": "fsZx2"}).next_sibling
song_title_text = re.sub("\n", "", song_title)

# remove html tags
final_lyrics = re.sub(" <br/>", "", formatted_lyrics)
final_lyrics2 = re.sub(" 更多更詳盡歌詞 在 ※ Mojim.com　魔鏡歌詞網\n\n", "", final_lyrics)
final_lyrics3 = re.sub(
    "\n\n\n\n <ol>\n  <li>\n  </li>\n </ol>\n</dl>", "", final_lyrics2)
final_lyrics4 = re.sub('\n ', '', final_lyrics3)
final_lyrics5 = re.sub('\n.*：.*', '', final_lyrics4)
final_lyrics6 = re.sub('<.*class=.*\n\n', '', final_lyrics5)

# translate
translator = Translator()
result = translator.translate(final_lyrics6, dest='en')
translated_title = translator.translate(song_title_text, dest='en')

# produce phonetic text of original lyrics
original = translator.translate(final_lyrics6, dest='zh-tw')

# write to document
with io.open("output.txt", "w", encoding="utf-8") as q:
    q.write('"' + translated_title.text.title() + '"' + "\n\n" +
            original.pronunciation + "\n\n—\n\n" + result.text + "\n\n—\n\n" + final_lyrics6)
