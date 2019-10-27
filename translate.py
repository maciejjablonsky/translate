#!/usr/bin/python3
import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("You need to enter a word you want to translate.\n")
    exit(1)

word = sys.argv[1]
for _word in sys.argv[2:]:
    word += " " + str(_word)

page = requests.get('https://www.diki.pl/slownik-angielskiego', params={'q': word})

soup = BeautifulSoup(page.content, 'html.parser')

a_tags = soup.select("ol.foreignToNativeMeanings > li > span.hw > a")
if len(a_tags) == 0:
    a_tags = soup.select("ol.nativeToForeignEntrySlices >li > span.hw > a")


def ordered_set(in_list):
    out_list = []
    added = set()
    for val in in_list:
        if val not in added:
            out_list.append(val)
            added.add(val)
    return out_list


translations = list(ordered_set([a_tag.get_text() for a_tag in a_tags]))

threshold = 4

translations = translations if len(translations) < threshold else translations[:threshold]
language = soup.select("#contentWrapper  div.dikiBackgroundBannerPlaceholder > div > a")[0]['name']

if language == 'pl-en':
    language = 'English'
elif language == 'en-pl':
    language = 'Polish'
print("In {0:s} '{1:s}' is:".format(language, word))
for i in range(0, len(translations)):
    print("{0:d}. {1:s}".format(i + 1, translations[i]))
