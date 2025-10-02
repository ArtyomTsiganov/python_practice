import asyncio
import collections
import re
import urllib.parse
from html.parser import HTMLParser

import aiohttp


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


async def get_content(name):
    headers = {"User-Agent": "MyWikibot"}
    link = "https://ru.wikipedia.org/wiki/"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(link + format_links(name)) as response:
            return await response.text()



def extract_content(page):
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
    page = urllib.parse.unquote(page)
    reg = r"href=[\'\"]/wiki/((?![\d\w]*?:)(?![\d\w]*?#).*?)[\'\"]"
    regex = re.compile(reg, re.IGNORECASE)
    links = regex.findall(page, begin, end)
    return set(links)


def format_links(link: str):
    return link.capitalize()


async def get_links(name):
    content = await get_content(name)
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


async def get_courotine(name, start, finish, visited, all_links, result):
    links = await get_links(format_links(name))

    if len(result) > 0:
        return

    for lnk in links:
        if lnk not in visited:
            all_links.append(lnk)
            visited[lnk] = name
        if lnk == finish:
            result.append(get_chain(start, finish, visited))

async def find_chain(start, finish):
    all_links = collections.deque()
    all_links.append(start)
    visited = {start: start}
    if start.lower() == finish.lower():
        return [start]

    result = []
    tasks = []
    while len(result) == 0 and (len(tasks) > 0 or len(visited) == 1):
        if len(all_links) > 0:
            name = all_links.pop()
            tasks.append(asyncio.create_task(get_courotine(name, start, finish, visited, all_links, result)))
            continue

        for i in range(len(tasks) - 1, 0, -1):
            if tasks[i].done():
                tasks.pop(i)
        await asyncio.sleep(1)


    return result[0] if len(result) > 0 else None


def main(*args):
    return asyncio.run(find_chain(args[0], "Философия"))


if __name__ == "__main__":
    main("Наука")
