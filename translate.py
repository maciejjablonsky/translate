#!/usr/bin/python3
import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("You need to enter a word you want to translate.\n")
    exit(1)

expression = sys.argv[1]
for word in sys.argv[2:]:
    expression += " " + str(word)

page = requests.get('https://www.diki.pl/slownik-angielskiego', params={'q': expression})
soup = BeautifulSoup(page.content, 'html.parser')
language = soup.select("#contentWrapper  div.dikiBackgroundBannerPlaceholder > div > a")[0]['name']

# checks if there is simple translation of the phrase in data base
if len(soup.select('ul.wordByWordTranslation')) != 0:
    print("There is no such phrase in diki.pl data base.")
    exit(2)

if language == 'en-pl':
    language = 'English'
    tags_with_translation = soup.select("ol.foreignToNativeMeanings > li > span.hw > a")
    tags_with_translation += soup.select("span.hiddenNotForChildrenMeaning a.plainLink")

else:
    language = 'Polish'
    tags_with_translation = soup.select("ol.nativeToForeignEntrySlices >li > span.hw  a.plainLink")


def ordered_set(in_list):
    out_list = []
    added = set()
    for val in in_list:
        if val not in added:
            out_list.append(val)
            added.add(val)
    return out_list


translations = list(ordered_set([tag.get_text() for tag in tags_with_translation]))

threshold = 100

translations = translations if len(translations) < threshold else translations[:threshold]

print("In {0:s} '{1:s}' means:".format(language, expression))
for i in range(0, len(translations)):
    print("{0:d}. {1:s}".format(i + 1, translations[i]))
