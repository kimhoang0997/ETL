#!/usr/bin/env python3
import argparse
import urllib.request, urllib.parse, urllib.error
from lxml import etree
from slugify import slugify
import ssl
import os

def preprocess():
    parser = argparse.ArgumentParser()
    parser.add_argument('download', type=str, help='folder to save all of downloaded zip')
    return parser.parse_args()

def main():
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE


    args = preprocess()
    url = 'https://data.worldbank.org/indicator'
    response = urllib.request.urlopen(url, context=ctx)#.read()
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    sections= tree.xpath('//section')

    for section in sections:
        # Create folder to contain material from web
        section_id = section.xpath('./h3/@id')[0]
        print(section_id)

        os.makedirs(args.download, exist_ok=True)

        # Down material from web
        links = section.xpath('.//ul/li/a/@href')
        names = section.xpath('.//ul/li/a/text()')
        root = 'https://data.worldbank.org'

        for index, link in enumerate(links):
            try:
                newurl = root + str(link)
                newresponse = urllib.request.urlopen(str(newurl), context=ctx)
                tree = etree.parse(newresponse, htmlparser)
                downs = tree.xpath('//aside/div//div/div//p/a')
                down = downs[0].xpath('./@href')
                filename = slugify(names[index]) +'.zip'
                print(filename)
                filepath = os.path.join(args.download, filename)
                urllib.request.urlretrieve(str(down[0]), filepath)
            except Exception as error:
                print(error)

if __name__ == "__main__":
    main()