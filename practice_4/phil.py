#!/usr/bin/env python3
from collections import deque
import re
import urllib.parse
from random import shuffle
from html.parser import HTMLParser

try:
    import httpx
except ModuleNotFoundError:
    import pip

    pip.main(['install', '--quiet', 'httpx'])
    import httpx


# РґР»СЏ РѕР±СЂР°С‰РµРЅРёСЏ Рє РІРµР±-СЃС‚СЂР°РЅРёС†Рµ РјРѕР¶РЅРѕ
# РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ РїСЂРёРјРµСЂС‹ https://www.python-httpx.org

class MyHTMLParser(HTMLParser):
    def __init__(self, search_attr):
        super().__init__()
        self.start_pos = (0, 1)
        self.finish_pos = (1, 1)
        self.search_attr = search_attr
        self.in_content = False
        self.tag_a = ""
        self.deep = 0

    def handle_starttag(self, tag, attrs):
        if self.search_attr in attrs:
            self.start_pos = self.getpos()
            self.in_content = True
            self.tag_a = tag

        if self.tag_a == tag and self.in_content:
            self.deep += 1

    def handle_endtag(self, tag):
        if self.tag_a == tag and self.in_content:
            self.deep -= 1

        if self.deep == 0 and self.in_content:
            self.finish_pos = self.getpos()
            self.in_content = False

    def handle_data(self, data):
        pass

    def get_positions(self):
        return self.start_pos, self.finish_pos


def get_content(name):
    """
    Р¤СѓРЅРєС†РёСЏ РІРѕР·РІСЂР°С‰Р°РµС‚ СЃРѕРґРµСЂР¶РёРјРѕРµ РІРёРєРё-СЃС‚СЂР°РЅРёС†С‹ name РёР· СЂСѓСЃСЃРєРѕР№ Р’РёРєРёРїРµРґРёРё.
    Р’ СЃР»СѓС‡Р°Рµ РѕС€РёР±РєРё Р·Р°РіСЂСѓР·РєРё РёР»Рё РѕС‚СЃСѓС‚СЃС‚РІРёСЏ СЃС‚СЂР°РЅРёС†С‹ РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ None.
    """
    link = "https://ru.wikipedia.org/wiki/"
    page = httpx.get(link + format_links(name)).text
    return urllib.parse.unquote(page)


def extract_content(page):
    """
    Р¤СѓРЅРєС†РёСЏ РїСЂРёРЅРёРјР°РµС‚ РЅР° РІС…РѕРґ СЃРѕРґРµСЂР¶РёРјРѕРµ СЃС‚СЂР°РЅРёС†С‹ Рё РІРѕР·РІСЂР°С‰Р°РµС‚ 2-СЌР»РµРјРµРЅС‚РЅС‹Р№
    tuple, РїРµСЂРІС‹Р№ СЌР»РµРјРµРЅС‚ РєРѕС‚РѕСЂРѕРіРѕ вЂ” РЅРѕРјРµСЂ РїРѕР·РёС†РёРё, СЃ РєРѕС‚РѕСЂРѕР№ РЅР°С‡РёРЅР°РµС‚СЃСЏ
    СЃРѕРґРµСЂР¶РёРјРѕРµ СЃС‚Р°С‚СЊРё, РІС‚РѕСЂРѕР№ СЌР»РµРјРµРЅС‚ вЂ” РЅРѕРјРµСЂ РїРѕР·РёС†РёРё, РЅР° РєРѕС‚РѕСЂРѕРј Р·Р°РєР°РЅС‡РёРІР°РµС‚СЃСЏ
    СЃРѕРґРµСЂР¶РёРјРѕРµ СЃС‚Р°С‚СЊРё.
    Р•СЃР»Рё СЃРѕРґРµСЂР¶РёРјРѕРµ РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚, РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ (0, 0).
    """
    attr = ("id", "mw-content-text")
    parser = MyHTMLParser(attr)
    parser.feed(page)
    start_line, finish_line = parser.get_positions()
    pref_lens = [0] + list(map(lambda x: len(x), page.split("\n")))
    for i in range(1, len(pref_lens)):
        pref_lens[i] += pref_lens[i - 1]
    start_pos = pref_lens[start_line[0]] + start_line[1] - 1
    finish_pos = pref_lens[finish_line[0] - 1] + finish_line[1] - 1
    return start_pos, finish_pos


def extract_links(page, begin, end):
    """
    Р¤СѓРЅРєС†РёСЏ РїСЂРёРЅРёРјР°РµС‚ РЅР° РІС…РѕРґ СЃРѕРґРµСЂР¶РёРјРѕРµ СЃС‚СЂР°РЅРёС†С‹ Рё РЅР°С‡Р°Р»Рѕ Рё РєРѕРЅРµС† РёРЅС‚РµСЂРІР°Р»Р°,
    Р·Р°РґР°СЋС‰РµРіРѕ РїРѕР·РёС†РёСЋ СЃРѕРґРµСЂР¶РёРјРѕРіРѕ СЃС‚Р°С‚СЊРё РЅР° СЃС‚СЂР°РЅРёС†Рµ Рё РІРѕР·РІСЂР°С‰Р°РµС‚ РІСЃРµ РёРјРµСЋС‰РёРµСЃСЏ
    СЃСЃС‹Р»РєРё РЅР° РґСЂСѓРіРёРµ РІРёРєРё-СЃС‚СЂР°РЅРёС†С‹ Р±РµР· РїРѕРІС‚РѕСЂРµРЅРёР№ Рё СЃ СѓС‡С‘С‚РѕРј СЂРµРіРёСЃС‚СЂР°.
    """
    # С‚РµСЃС‚С‹ РЅР° СЃР°Р№С‚Рµ,
    page = urllib.parse.unquote(page)
    reg = r"href=[\'\"]/wiki/((?![\d\w]*?:)(?![\d\w]*?#).*?)[\'\"]"
    regex = re.compile(reg, re.IGNORECASE)
    links = regex.findall(page, begin, end)
    return set(links)


def format_links(link: str):
    return link.capitalize()


def get_links(name):
    content = get_content(name)
    start, finish = extract_content(content)
    return extract_links(content, start, finish)


def get_chain(start, finish, visited):
    way = list()
    while finish != start:
        way.append(finish)
        finish = visited[finish]
    way.append(start)
    way.reverse()
    return way


def find_chain(start, finish):
    """
    Р¤СѓРЅРєС†РёСЏ РїСЂРёРЅРёРјР°РµС‚ РЅР° РІС…РѕРґ РЅР°Р·РІР°РЅРёРµ РЅР°С‡Р°Р»СЊРЅРѕР№ Рё РєРѕРЅРµС‡РЅРѕР№ СЃС‚Р°С‚СЊРё Рё РІРѕР·РІСЂР°С‰Р°РµС‚
    СЃРїРёСЃРѕРє РїРµСЂРµС…РѕРґРѕРІ, РїРѕР·РІРѕР»СЏСЋС‰РёР№ РґРѕР±СЂР°С‚СЊСЃСЏ РёР· РЅР°С‡Р°Р»СЊРЅРѕР№ СЃС‚Р°С‚СЊРё РІ РєРѕРЅРµС‡РЅСѓСЋ.
    РџРµСЂРІС‹Рј СЌР»РµРјРµРЅС‚РѕРј СЂРµР·СѓР»СЊС‚Р°С‚Р° РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ start, РїРѕСЃР»РµРґРЅРёРј вЂ” finish.
    Р•СЃР»Рё РїРѕСЃС‚СЂРѕРёС‚СЊ РїРµСЂРµС…РѕРґС‹ РЅРµРІРѕР·РјРѕР¶РЅРѕ, РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ None.
    """
    all_links = list()
    all_links.append(start)
    visited = {start: start}
    if start.lower() == finish.lower():
        return [start]
    while len(all_links) > 0:
        shuffle(all_links)
        name = all_links.pop()
        links = get_links(format_links(name))
        for lnk in links:
            if lnk not in visited:
                all_links.append(lnk)
                visited[lnk] = name
            if lnk == finish:
                return get_chain(start, finish, visited)
    return None


def main(*args):
    return find_chain(args[0], "Философия")



if __name__ == "__main__":
    main("Наука")