"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Martina Svobodova
email: Svobodova.Martina14@gmail.com
"""

from requests import get
from bs4 import BeautifulSoup
import sys
import csv

baseUrl = "https://www.volby.cz/pls/ps2017nss/"

def getPageHtml(url):
    print("Opening " + url)
    response = get(url)

    return BeautifulSoup(response.text, features="html.parser")

def getHeaders(link):
    html = getPageHtml(link)
    firstCountyLink = baseUrl + html.select_one("td.cislo > a")["href"]
    html = getPageHtml(firstCountyLink)
    detinfo = html.select("table tr td.overflow_name")
    headers = ["code", "location", "registered", "envelops", "valid"]
    for party in detinfo:
        headers.append(party.get_text(strip=True))
    return headers

def writeToCsv(filename, rows):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def getCountyResults(relativeLink):
    url = baseUrl + relativeLink
    html = getPageHtml(url)

    table = html.find_all("table")[0]
    cells = table.find_all(["td"])  # data only, no headers
    detinfo = html.select("table tr td.overflow_name")

    #we need columns 3,4 and 7 probably
    cell_text = [cell.get_text(strip=True).replace('\xa0', '') 
                 for cell in cells[3:5] + [cells[7]]]
    for group in detinfo:
        cell_text += [group.find_next_sibling("td").get_text(strip=True)]
    return cell_text

def getData(url):
    html = getPageHtml(url)
    table = html.find("table")

    rows = []
    for row in table.find_all("tr"):
        cells = row.find_all(["td"]) 
        cell_text = [cell.get_text(strip=True) for cell in cells[0:2]]
        if cell_text != []:
            detailsLink = cells[0].a["href"]
            details = getCountyResults(detailsLink)
            rows.append(cell_text + details)
    return rows

def getInputParams(args):
    if len(args) != 3:
        print("Usage: python baby3.py <url> <filename.csv>")
        sys.exit(1)
    return args[1], args[2]

def main():
    url, filename = getInputParams(sys.argv)

    print(f"Parameter 1: {url}")
    print(f"Parameter 2: {filename}")

    rows = []
    partyheader = getHeaders(url)
    rows.append(partyheader)
    
    # Loop through rows and extract text
    rows += getData(url)

    # Save to CSV
    writeToCsv(filename, rows)

    print(f"Saved table to {filename}")

if __name__ == "__main__":
    main()

