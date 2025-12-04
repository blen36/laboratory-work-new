import requests
import csv
from bs4 import BeautifulSoup
import time
import os
import re
import sys


def load_page(country_name, cache_dir = "cache"):
    filename = os.path.join(cache_dir, country_name + ".html")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    if os.path.exists(filename):
        print(f"Загружено из кэша: {country_name}")
        with open(filename, "r", encoding = "utf-8") as f:
            return f.read()

    print(f"Скачиваем страницу: {country_name}")
    url = f"https://en.wikipedia.org/wiki/{country_name.replace(' ', '_')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    }

    response = requests.get(url, headers = headers)
    response.raise_for_status()
    html = response.text
    with open(filename, "w", encoding = "utf-8") as f:
        f.write(html)
    time.sleep(1)
    return html


def parse_page(html):
    soup = BeautifulSoup(html, "lxml")
    info_table = soup.find("table", class_ = "infobox")
    if not info_table:
        return None, None, None

    capital = None
    area = None
    population = None

    for row in info_table.find_all("tr"):
        header = row.find("th")
        if not header:
            continue

        header_text = header.get_text(strip = True)

        if "Capital" in header_text and not capital:
            td = header.find_next("td")
            if td:
                a = td.find("a")
                if a:
                    capital = a.get_text(strip = True)
                else:
                    capital = td.get_text(strip = True).split('[')[0].split('\n')[0]

        elif ("Area" in header_text or "• Total" in header_text) and not area:
            td = header.find_next("td")
            if td:
                area_text = td.get_text(" ", strip = True)

                area_match = re.search(r'([\d.,]+)\s*km', area_text)

                if area_match:
                    raw = area_match.group(1).replace(",", "")
                    area = raw
                    if "." in area:
                        area = area.split(".")[0]

        elif "Population" in header_text and not population:
            td = header.find_next("td")
            if td:
                pop_text = td.get_text(" ", strip = True)

                pop_match = re.search(r'([\d,]+)', pop_text)
                if pop_match:
                    population = pop_match.group(1).replace(",", "")

    return capital, area, population


def choose_files():
    while True:
        print("\n" + "=" * 50)
        print("ВЫБОР ФАЙЛОВ:")
        print("1 - Использовать готовый файл countries.txt")
        print("2 - Создать новый файл и вписать страны")
        print("=" * 50)

        choice = input("Выберите вариант (1 или 2): ").strip()

        if choice == "1":
            input_file = "countries.txt"
            output_file = "countries_data.csv"

            if not os.path.exists(input_file):
                print(f"Файл {input_file} не найден!")
                print("Создайте файл countries.txt со списком стран или выберите вариант 2")
                continue

            print(f"Используется готовый файл: {input_file}")
            print(f"Результат будет сохранен в: {output_file}")
            return input_file, output_file

        elif choice == "2":
            input_file = input("Введите имя нового файла (например: my_countries.txt): ").strip()
            if not input_file:
                print("Имя файла не может быть пустым!")
                continue

            output_file = input("Введите имя для CSV файла с результатами (например: my_results.csv): ").strip()
            if not output_file:
                print("Имя выходного файла не может быть пустым!")
                continue

            print(f"\nВводите названия стран для файла '{input_file}'")
            print("Вводите по одной стране, пустая строка - завершение ввода")

            countries = []
            count = 1
            while True:
                country = input(f"Страна {count}: ").strip()
                if not country:
                    break
                countries.append(country)
                count += 1

            if not countries:
                print("Не введено ни одной страны!")
                continue

            try:
                with open(input_file, "w", encoding = "utf-8") as f:
                    for country in countries:
                        f.write(country + "\n")
                print(f"Файл создан: {input_file}")
                print(f"Сохранено стран: {len(countries)}")
                print(f"Результат будет сохранен в: {output_file}")
                return input_file, output_file

            except Exception as e:
                print(f"Ошибка при создании файла {input_file}: {e}")
                continue

        else:
            print("Неверный выбор! Введите 1 или 2")


def main():
    input_file, output_file = choose_files()

    if not os.path.exists(input_file):
        print(f"Файл {input_file} не найден!")
        print("Создайте файл со списком стран или выберите другой файл.")
        return

    try:
        with open(input_file, "r", encoding = "utf-8") as f:
            countries = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Ошибка при чтении файла {input_file}: {e}")
        return

    if not countries:
        print(f"Файл {input_file} пуст!")
        return

    print(f"\nНайдено стран для обработки: {len(countries)}")

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

    try:
        with open(output_file, "w", encoding = "utf-8", newline = "") as f:
            writer = csv.DictWriter(f, fieldnames = ["country", "city", "area", "population"])
            writer.writeheader()
            writer.writerows(results)

        print(f"\nГотово! Сохранено {len(results)} стран в файл: {output_file}")

    except Exception as e:
        print(f"Ошибка при сохранении в файл {output_file}: {e}")


if __name__ == "__main__":
    main()