import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11


# ------------------------------------------
# Функция для подписей столбцов
# ------------------------------------------
def add_bar_labels_ax(ax):
    for p in ax.patches:
        value = p.get_height()
        try:
            v = float(value)
        except Exception:
            continue
        ax.annotate(f"{v:,.0f}",
                    (p.get_x() + p.get_width() / 2, v),
                    ha='center', va='bottom', fontsize=9,
                    xytext=(0, 6), textcoords='offset points')


# ------------------------------------------
# Утилита: красивый barplot через matplotlib + seaborn palette
# ------------------------------------------
def nice_bar_plot(x, y, title, rotation=45, cmap_name="viridis"):
    """
    x : list-like (labels)
    y : list-like (values)
    """
    labels = list(x)
    values = list(y)
    n = len(values)
    if n == 0:
        print("Нет данных для графика:", title)
        return

    # получить палитру
    palette = sns.color_palette(cmap_name, n_colors=n)
    indices = np.arange(n)

    fig, ax = plt.subplots()
    bars = ax.bar(indices, values, color=palette)

    ax.set_xticks(indices)
    ax.set_xticklabels(labels, rotation=rotation)
    ax.set_title(title)
    ax.set_ylabel("Сумма, руб.")

    # подписи значений
    for rect, val in zip(bars, values):
        height = rect.get_height()
        ax.annotate(f"{height:,.0f}",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 6),
                    textcoords='offset points',
                    ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.show()


# ------------------------------------------
# Загрузка данных
# ------------------------------------------
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


# ------------------------------------------
# Подготовка дат (исправлено: .str.zfill)
# ------------------------------------------
df["Год-мес"] = df["Год-мес"].astype(str)
df["Год"] = df["Год-мес"].str[:4].astype(int)
df["Месяц"] = df["Год-мес"].str[-2:].astype(int)
df = df[df["Месяц"] <= 12]

df["Период"] = pd.to_datetime(df["Год"].astype(str) + "-" + df["Месяц"].astype(str).str.zfill(2))


# ------------------------------------------
# Динамика продаж по месяцам
# ------------------------------------------
sales_by_month = df.groupby("Период")[["Продажи", "Себестоимость"]].sum().reset_index()

plt.figure()
sns.lineplot(data=sales_by_month, x="Период", y="Продажи", label="Продажи", linewidth=2, marker='o', color="#0B84A5")
sns.lineplot(data=sales_by_month, x="Период", y="Себестоимость", label="Себестоимость", linewidth=2, marker='o', color="#F6C85F")
plt.title("Динамика продаж и себестоимости по месяцам")
plt.xlabel("Период")
plt.ylabel("Сумма, руб.")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ------------------------------------------
# Продажи по видам товара (без предупреждений)
# ------------------------------------------
sales_by_product = (
    df.groupby("товар")[["Количество", "Продажи", "Себестоимость"]]
    .sum()
    .sort_values("Продажи", ascending=False)
).reset_index()

nice_bar_plot(sales_by_product["товар"], sales_by_product["Продажи"], title="Продажи по видам товара", cmap_name="viridis")


# ------------------------------------------
# Продажи по точкам реализации (без предупреждений)
# ------------------------------------------
sales_by_store = (
    df.groupby("точка")[["Продажи", "Количество"]]
    .sum()
    .sort_values("Продажи", ascending=False)
).reset_index()

nice_bar_plot(sales_by_store["точка"], sales_by_store["Продажи"], title="Продажи по точкам реализации", cmap_name="magma")


# ------------------------------------------
# Средняя цена по товарам (без предупреждений)
# ------------------------------------------
df["Средняя_цена"] = df["Продажи"] / df["Количество"]
avg_price_by_product = df.groupby("товар")["Средняя_цена"].mean().reset_index().sort_values("Средняя_цена", ascending=False)

nice_bar_plot(avg_price_by_product["товар"], avg_price_by_product["Средняя_цена"], title="Средняя цена по видам товара", cmap_name="coolwarm")


# ------------------------------------------
# Динамика общего товарооборота
# ------------------------------------------
df["Дата"] = pd.to_datetime(df["Дата"])
turnover_by_date = df.groupby("Дата")["Продажи"].sum().reset_index()

plt.figure()
sns.lineplot(data=turnover_by_date, x="Дата", y="Продажи", linewidth=2, marker='o', color="#6F4E7C")
plt.title("Общий товарооборот во времени")
plt.tight_layout()
plt.show()


# ------------------------------------------
# Прогноз продаж по видам товара (3 месяца)
# ------------------------------------------
plt.figure(figsize=(14, 8))

for product, group in df.groupby("товар"):
    monthly_sales = group.groupby("Период")["Продажи"].sum().reset_index().sort_values("Период")

    if len(monthly_sales) > 1:
        x = np.arange(len(monthly_sales))
        y = monthly_sales["Продажи"].values

        # Линейный тренд
        coeffs = np.polyfit(x, y, 1)
        trend = np.poly1d(coeffs)

        # Прогноз на 3 месяца
        last_date = monthly_sales["Период"].max()
        future_dates = pd.date_range(
            start=last_date + pd.DateOffset(months=1),
            periods=3,
            freq='MS'
        )

        forecast_x = np.arange(len(monthly_sales), len(monthly_sales) + 3)
        forecast_y = trend(forecast_x)

        plt.plot(monthly_sales["Период"], y, 'o-', label=f"{product} (факт)", markersize=4)
        plt.plot(monthly_sales["Период"], trend(x), '--', alpha=0.5, label=f"{product} (тренд)")
        plt.plot(future_dates, forecast_y, 's--', label=f"{product} (прогноз)", markersize=6)

plt.xticks(rotation=45)
plt.title("Прогноз продаж по видам товара на 3 месяца")
plt.xlabel("Период")
plt.ylabel("Продажи, руб.")
plt.grid(True, alpha=0.3)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=9)
plt.subplots_adjust(right=0.75)
plt.show()
