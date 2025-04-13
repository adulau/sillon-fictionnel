#!/usr/bin/python
#
# Tooling for sillon-fictionnel.club
#
#  - Handle pages from a hugo repository (this could be used by other static
#  website having a large set of Markdown pages).
#  - Functionalities including dump all the markdown pages in a single page.
#  - Extract fields to build list or handle specific one like ISBN for the case
#  of the sillon-fictionnel.club
#
# Copyright (C) 2025 Alexandre Dulaunoy
#
# Licensed under AGPL version 3

import argparse
from os import walk
import re
from datetime import datetime, timedelta

# dateparser
import dateparser

# ISBN Obscure Library
from isbnlib import meta

SERVICE = "wiki"
host = "sillon-fictionnel.club"

content_path = "../content/post/"

g_footnote = 1


def get_article():
    articles = []
    for dirpath, dirnames, filenames in walk(content_path):
        for article in filenames:
            articles.append(f'{dirpath}{article}')
    return sorted(articles)


def extract_isbn(path=None):
    if path is None:
        return None
    f = open(path, 'r')
    for line in f.readlines():
        line = line.lower()
        if line.startswith("isbns"):
            isbns = (
                line.split("=")[1]
                .replace("[", "")
                .replace("]", "")
                .replace(" ", "")
                .replace("\"", "")
                .rstrip()
                .split(",")
            )
            return isbns
        elif line.startswith("isbn"):
            isbn = line.split("=")[1].replace(" ", "").replace("\"", "").rstrip()
            return [isbn]
    return False


def extract_title(path=None):
    if path is None:
        return None
    f = open(path, 'r')
    for line in f.readlines():
        if line.startswith("title"):
            title = line.split("=")[1].replace("\"", "").rstrip().lstrip()
            return title


def extract_date(path=None):
    if path is None:
        return None
    f = open(path, 'r')
    for line in f.readlines():
        if line.startswith("date"):
            date_post = line.split("=")[1].replace("\"", "").rstrip().lstrip()
            return dateparser.parse(date_post)


def extract_url(path=None):
    if path is None:
        return None
    ## Extract post url
    post_names = path.split(".")[-2].split("/")
    post_name = f'{post_names[2]}/{post_names[3]}'.lower()
    post_url = f'https://{host}/{post_name}'
    return post_url


def extract_author(path=None):
    if path is None:
        return None
    f = open(path, 'r')
    for line in f.readlines():
        if line.startswith("author"):
            author = line.split("=")[1].replace("\"", "").rstrip().lstrip()
            return author


def extract_content(path=None, image_rewrite=True):
    ## Footnote
    link = re.compile(r'[^(?<=\n)](\[\^([\d]+)\])')
    label = re.compile(r'(?<=\n)\[\^([\d]+)]:\s?(.*)')
    global g_footnote

    if path is None:
        return None

    f = open(path, 'r')
    i = 0
    content = ""
    for line in f.readlines():
        if image_rewrite:
            line = line.replace("/images", "./images")
        if line.startswith("+++"):
            i = i + 1
            next
        if i == 2:
            i = i + 1
            next
        elif i == 3:
            content = content + line
    ## bricolage to remplace footnote number with the global number for a single markdown document
    links = link.findall(content)
    labels = dict(
        label.findall(content)
    )  ## to keep if I want to create a book with footnotes only ;-)
    for link in links:
        g_footnote = g_footnote + 1
        c = content.replace(link[0], f'[^{g_footnote}]')
        content = c

    return content


parser = argparse.ArgumentParser(
    description="ISBN tooling for the famous Sillon Fictionnel"
)

parser.add_argument("-m", "--missing", action="store_true", help="Display missing ISBN")
parser.add_argument(
    "-l", "--lookup", action="store_true", help="Extract metadata from ISBN"
)
parser.add_argument(
    "-i",
    "--index",
    action="store_true",
    help="Generate index of all the pages in Markdown",
)
parser.add_argument(
    "-a",
    "--authors",
    action="store_true",
    help="Generate index of all the authors pages in Markdown",
)

parser.add_argument(
    "-d",
    "--dump",
    action="store_true",
    help="Dump all the content in a single markdown.",
)

parser.add_argument(
    "-t",
    "--time",
    action="store",
    help="Specify the number of days to filter. Integer value which is used as delta. Default is 31 days.",
    default=31,
)

args = parser.parse_args()

if args.missing:
    for article in get_article():
        isbn = extract_isbn(path=article)
        ## Missing ISBN
        if isbn is False:
            print(article)

if args.lookup:
    for article in get_article():
        isbn = extract_isbn(path=article)
        if not isbn:
            next
        else:
            for isbntolookup in isbn:
                print(article)
                print(meta(isbntolookup))
if args.index:
    i = []
    for article in get_article():
        title = extract_title(path=article)
        url = article.split('/', -1)[-1].split('.')[0]
        furl = f"/post/{url}"
        i.append((furl, title))
    s = sorted(i, key=lambda x: x[1].lower())
    for x in s:
        print(f"- [{x[1]}]({x[0]})")

if args.authors:
    i = {}
    for article in get_article():
        title = extract_title(path=article)
        authors = extract_author(path=article)
        url = article.split('/', -1)[-1].split('.')[0]
        furl = f"/post/{url}"
        final_link = f"[{title}]({furl})"
        if authors not in i:
            i[authors] = []
        i[authors].append(final_link)
    # print(i)
    for counter, author in enumerate(sorted(i)):
        print(f"\n## {author}")
        for page in i[author]:
            print(f"- {page}")


if args.dump:
    for article in get_article():
        # Skip if outside the date range
        postdate = extract_date(path=article)
        today = datetime.now()
        if postdate < today - timedelta(days=int(args.time)):
            continue

        title = extract_title(path=article)
        print(f"## {title}")
        url = extract_url(path=article)
        postdate_fr = postdate.strftime("%d %B %Y")
        print(
            f"Disponible sur le Sillon Fictionnel [{url}]({url}) en date du *{postdate_fr}*"
        )
        content = extract_content(path=article)
        print(f"{content}")
