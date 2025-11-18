import requests
import csv
from bs4 import BeautifulSoup
import time
import os
import re

def load_page(country_name, cache_dir="cache"):
    filename = os.path.join(cache_dir, country_name + ".html")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    if os.path.exists(filename):
        print(f"Загружено из кэша: {country_name}")
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()

    print(f"Скачиваем страницу: {country_name}")
    url = f"https://en.wikipedia.org/wiki/{country_name.replace(' ', '_')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    html = response.text
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    time.sleep(1)
    return html


def parse_page(html):
    soup = BeautifulSoup(html, "lxml")
    info_table = soup.find("table", class_="infobox")
    if not info_table:
        return None, None, None

    capital = None
    area = None
    population = None

    for row in info_table.find_all("tr"):
        header = row.find("th")
        if not header:
            continue

        header_text = header.get_text(strip=True)

        # --- CAPITAL ---
        if "Capital" in header_text and not capital:
            td = header.find_next("td")
            if td:
                a = td.find("a")
                if a:
                    capital = a.get_text(strip=True)
                else:
                    capital = td.get_text(strip=True).split('[')[0].split('\n')[0]

        # --- AREA ---
        elif ("Area" in header_text or "• Total" in header_text) and not area:
            td = header.find_next("td")
            if td:
                area_text = td.get_text(" ", strip=True)

                area_match = re.search(r'([\d.,]+)\s*km', area_text)

                if area_match:
                    raw = area_match.group(1).replace(",", "")
                    area = raw
                    if "." in area:
                        area = area.split(".")[0]

        # --- POPULATION ---
        elif "Population" in header_text and not population:
            td = header.find_next("td")
            if td:
                pop_text = td.get_text(" ", strip=True)

                pop_match = re.search(r'([\d,]+)', pop_text)
                if pop_match:
                    population = pop_match.group(1).replace(",", "")

    return capital, area, population


def main():
    try:
        with open("countries.txt", "r", encoding="utf-8") as f:
            countries = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Файл countries.txt не найден!")
        return

    results = []
    for country in countries:
        html = load_page(country)
        if not html:
            continue

        capital, area, population = parse_page(html)

        print(f"  Найдено: {capital}, {area} км², {population} чел.")

        results.append({
            "country": country,
            "city": capital,
            "area": area,
            "population": population
        })

    with open("countries_data.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["country", "city", "area", "population"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Готово! Сохранено {len(results)} стран")


if __name__ == "__main__":
    main()
