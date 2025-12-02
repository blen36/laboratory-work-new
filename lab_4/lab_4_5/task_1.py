import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

df = pd.read_excel("lab_4_part_5.xlsx", skiprows=1, usecols="B:J")

print("Размер данных:", df.shape)
print("Колонки:", df.columns.tolist(), '\n')

total_sales = df["Продажи"].sum()
total_cost = df["Себестоимость"].sum()
total_profit = total_sales - total_cost
avg_price = total_sales / df["Количество"].sum()

print(f"Общие продажи: {total_sales:,.0f} руб.")
print(f"Общая себестоимость: {total_cost:,.0f} руб.")
print(f"Общая прибыль: {total_profit:,.0f} руб.")
print(f"Средняя цена: {avg_price:,.2f} руб.\n")

df["Год-мес"] = df["Год-мес"].astype(str)
df["Год"] = df["Год-мес"].str[:4].astype(int)
df["Месяц"] = df["Год-мес"].str[-2:].astype(int)
df = df[df["Месяц"] <= 12]

df["Период"] = pd.to_datetime(df["Год"].astype(str) + "-" + df["Месяц"].astype(str).str.zfill(2))

# --- Динамика продаж по месяцам ---
sales_by_month = df.groupby("Период")[["Продажи", "Себестоимость"]].sum().reset_index()

plt.figure()
sns.lineplot(data=sales_by_month, x="Период", y="Продажи", label="Продажи")
sns.lineplot(data=sales_by_month, x="Период", y="Себестоимость", label="Себестоимость")
plt.title("Динамика продаж и себестоимости по месяцам")
plt.xlabel("Период")
plt.ylabel("Сумма, руб.")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- Продажи по видам товара ---
sales_by_product = (
    df.groupby("товар")[["Количество", "Продажи", "Себестоимость"]]
    .sum()
    .sort_values("Продажи", ascending=False)
)

plt.figure()
sns.barplot(x=sales_by_product.index, y="Продажи", data=sales_by_product)
plt.title("Продажи по видам товара")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- Продажи по точкам реализации ---
sales_by_store = (
    df.groupby("точка")[["Продажи", "Количество"]]
    .sum()
    .sort_values("Продажи", ascending=False)
)

plt.figure()
sns.barplot(x=sales_by_store.index, y="Продажи", data=sales_by_store)
plt.title("Продажи по точкам реализации")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- Средняя цена по товарам ---
df["Средняя_цена"] = df["Продажи"] / df["Количество"]
avg_price_by_product = df.groupby("товар")["Средняя_цена"].mean().reset_index()

plt.figure()
sns.barplot(data=avg_price_by_product, x="товар", y="Средняя_цена")
plt.title("Средняя цена по видам товара")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- Динамика общего товарооборота ---
df["Дата"] = pd.to_datetime(df["Дата"])
turnover_by_date = df.groupby("Дата")["Продажи"].sum().reset_index()

plt.figure()
sns.lineplot(data=turnover_by_date, x="Дата", y="Продажи", label="Продажи")
plt.title("Общий товарооборот во времени")
plt.tight_layout()
plt.show()

# --- Прогноз продаж по каждому виду товара ---
plt.figure(figsize = (14, 8))

for product, group in df.groupby("товар"):
    monthly_sales = group.groupby("Период")["Продажи"].sum().reset_index()

    if len(monthly_sales) > 1:
        x = np.arange(len(monthly_sales))
        y = monthly_sales["Продажи"].values

        # Линейный тренд
        coeffs = np.polyfit(x, y, 1)
        trend = np.poly1d(coeffs)

        # Прогноз на 3 месяца вперед
        last_date = monthly_sales["Период"].max()
        future_dates = pd.date_range(
            start = last_date + pd.DateOffset(months = 1),
            periods = 3,
            freq = 'MS'
        )

        # Значения прогноза
        forecast_x = np.arange(len(monthly_sales), len(monthly_sales) + 3)
        forecast_y = trend(forecast_x)

        # Рисуем линии
        plt.plot(monthly_sales["Период"], y, 'o-', label = f"{product} (факт)", markersize = 4)
        plt.plot(monthly_sales["Период"], trend(x), '--', alpha = 0.5, label = f"{product} (тренд)")
        plt.plot(future_dates, forecast_y, 's:', label = f"{product} (прогноз)", markersize = 6)

plt.xticks(rotation = 45)
plt.title("Прогноз продаж по видам товара на 3 месяца", fontsize = 14)
plt.xlabel("Период")
plt.ylabel("Продажи, руб.")
plt.grid(True, alpha = 0.3)

# Уменьшаем легенду и выносим справа
plt.legend(loc = 'center left', bbox_to_anchor = (1, 0.5), fontsize = 9)
plt.subplots_adjust(right = 0.75)  # Место для легенды
plt.show()
