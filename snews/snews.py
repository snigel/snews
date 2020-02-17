#! /usr/bin/env python3

import locale
import json
from dialog import Dialog

def main():
    # This is almost always a good thing to do at the beginning of your programs.
    locale.setlocale(locale.LC_ALL, '')
    d = Dialog(dialog="dialog", autowidgetsize=True)
    d.set_background_title("snews")

    (_, snewspath) = d.fselect("/home/adam/snews/snews/spiders/", height=20, width=60)

    # Read json lines file
    data = []
    with open(snewspath) as f:
        for line in f:
            data.append(json.loads(line))


    # Build Category Tuple for Dialog Checklist
    categories = []
    for cat in data:
        categories.append(cat['category'])

    categoryTuple = []
    for cat in set(categories):
        categoryTuple.append((cat, "", 1))

    # Open Dialog Checklist

    text = "lorem ipsum"
    (_, filter) = d.checklist(text, choices=categoryTuple)

    # Build filtered list of articles for Dialog Menu
    filteredData = []
    for item in data:
        if item['category'] in filter:
            filteredData.append(item)

    # Sort articles by date
    sortedData = sorted(filteredData, key=lambda item: item['date'], reverse=True)

    pointer = 0
    articles = []
    for item in sortedData:
        articles.append((str(pointer), item['category'] + " : " + item['date'] + " : " + item['header']))
        pointer += 1

    while True:
        _, menu_pointer = d.menu(text, choices=articles)
        d.add_persistent_args(["--default-item", menu_pointer])
        d.set_background_title(sortedData[int(menu_pointer)]['header'])
        # Build text string to display
        item = sortedData[int(menu_pointer)]
        textstring = ""
        textstring += item['header']
        textstring += "\n"
        textstring += item['url']
        textstring += "\n"
        textstring += item['date'] + " - " + item['author']
        textstring += "\n\n"
        textstring += item['text']
        # Display the text string
        d.msgbox(textstring)

if __name__ == "__main__":
    main()
