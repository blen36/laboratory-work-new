import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

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

def nice_bar_plot(x, y, title, rotation=45, cmap_name="viridis"):
    labels = list(x)
    values = list(y)
    n = len(values)
    if n == 0:
        print("Нет данных для графика:", title)
        return

    palette = sns.color_palette(cmap_name, n_colors=n)
    indices = np.arange(n)

    fig, ax = plt.subplots()
    bars = ax.bar(indices, values, color=palette)

    ax.set_xticks(indices)
    ax.set_xticklabels(labels, rotation=rotation)
    ax.set_title(title)
    ax.set_ylabel("Сумма, руб.")

    for rect, val in zip(bars, values):
        height = rect.get_height()
        ax.annotate(f"{height:,.0f}",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 6),
                    textcoords='offset points',
                    ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.show()

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

sales_by_product = (
    df.groupby("товар")[["Количество", "Продажи", "Себестоимость"]]
    .sum()
    .sort_values("Продажи", ascending=False)
).reset_index()

nice_bar_plot(sales_by_product["товар"], sales_by_product["Продажи"], title="Продажи по видам товара", cmap_name="viridis")

sales_by_store = (
    df.groupby("точка")[["Продажи", "Количество"]]
    .sum()
    .sort_values("Продажи", ascending=False)
).reset_index()

nice_bar_plot(sales_by_store["точка"], sales_by_store["Продажи"], title="Продажи по точкам реализации", cmap_name="magma")

df["Средняя_цена"] = df["Продажи"] / df["Количество"]
avg_price_by_product = df.groupby("товар")["Средняя_цена"].mean().reset_index().sort_values("Средняя_цена", ascending=False)

nice_bar_plot(avg_price_by_product["товар"], avg_price_by_product["Средняя_цена"], title="Средняя цена по видам товара", cmap_name="coolwarm")

df["Дата"] = pd.to_datetime(df["Дата"])
turnover_by_date = df.groupby("Дата")["Продажи"].sum().reset_index()

plt.figure()
sns.lineplot(data=turnover_by_date, x="Дата", y="Продажи", linewidth=2, marker='o', color="#6F4E7C")
plt.title("Общий товарооборот во времени")
plt.tight_layout()
plt.show()

plt.figure(figsize = (14, 8))

products = df["товар"].unique()
colors = plt.cm.tab20(np.linspace(0, 1, len(products)))

for idx, product in enumerate(products):
    group = df[df["товар"] == product]
    monthly_sales = group.groupby("Период")["Продажи"].sum().reset_index().sort_values("Период")

    if len(monthly_sales) > 2:
        x = np.arange(len(monthly_sales))
        y = monthly_sales["Продажи"].values

        weights = np.exp(np.linspace(0, 1, len(x)))
        coeffs = np.polyfit(x, y, 1, w = weights)
        trend = np.poly1d(coeffs)

        residuals = y - trend(x)
        std_residual = np.std(residuals)

        last_date = monthly_sales["Период"].max()
        future_dates = pd.date_range(
            start = last_date + pd.DateOffset(months = 1),
            periods = 3,
            freq = 'MS'
        )

        forecast_x = np.arange(len(monthly_sales), len(monthly_sales) + 3)
        forecast_y = trend(forecast_x)

        noise = np.random.normal(0, std_residual * 0.7, 3)
        forecast_y = np.maximum(forecast_y + noise, 0)

        last_value = y[-1]
        forecast_y = (forecast_y * 0.7) + (last_value * 0.3)

        color = colors[idx]
        plt.plot(monthly_sales["Период"], y, 'o-',
                 label = f"{product} (факт)",
                 markersize = 5,
                 linewidth = 2,
                 color = color)

        plt.plot([last_date, future_dates[0]],
                 [last_value, forecast_y[0]],
                 '--', alpha = 0.7, color = color)

        plt.plot(future_dates, forecast_y, 's--',
                 label = f"{product} (прогноз)",
                 markersize = 7,
                 linewidth = 2,
                 color = color,
                 alpha = 0.8)


plt.xticks(rotation = 45)
plt.title("Прогноз продаж по видам товара на 3 месяца", fontsize = 14, fontweight = 'bold')
plt.xlabel("Период", fontsize = 12)
plt.ylabel("Продажи, руб.", fontsize = 12)
plt.grid(True, alpha = 0.3)

last_overall_date = df["Период"].max()
plt.axvline(x = last_overall_date, color = 'gray', linestyle = '--', alpha = 0.5, linewidth = 1)
plt.text(last_overall_date, plt.ylim()[1] * 0.95, "Начало прогноза",
         ha = 'right', va = 'top', fontsize = 9, color = 'gray', rotation = 90)

plt.legend(loc = 'center left', bbox_to_anchor = (1, 0.5), fontsize = 9)
plt.subplots_adjust(right = 0.75)
plt.tight_layout()
plt.show()

top_products = df.groupby("товар")["Продажи"].sum().nlargest(4).index.tolist()

plt.figure(figsize = (14, 8))

colors = plt.cm.Set2(np.linspace(0, 1, len(top_products)))

for idx, product in enumerate(top_products):
    group = df[df["товар"] == product]
    monthly_sales = group.groupby("Период")["Продажи"].sum().reset_index().sort_values("Период")

    if len(monthly_sales) > 2:
        x = np.arange(len(monthly_sales))
        y = monthly_sales["Продажи"].values

        weights = np.exp(np.linspace(0, 1, len(x)))
        coeffs = np.polyfit(x, y, 1, w = weights)
        trend = np.poly1d(coeffs)

        residuals = y - trend(x)
        std_residual = np.std(residuals)

        last_date = monthly_sales["Период"].max()
        future_dates = pd.date_range(
            start = last_date + pd.DateOffset(months = 1),
            periods = 3,
            freq = 'MS'
        )

        forecast_x = np.arange(len(monthly_sales), len(monthly_sales) + 3)
        forecast_y = trend(forecast_x)

        noise = np.random.normal(0, std_residual * 0.7, 3)
        forecast_y = np.maximum(forecast_y + noise, 0)

        last_value = y[-1]
        forecast_y = (forecast_y * 0.7) + (last_value * 0.3)
        color = colors[idx]

        plt.plot(monthly_sales["Период"], y, 'o-',
                 label = f"{product} (факт)",
                 markersize = 6,
                 linewidth = 2.5,
                 color = color)

        plt.plot([last_date, future_dates[0]],
                 [last_value, forecast_y[0]],
                 '--', alpha = 0.7, color = color, linewidth = 2)

        plt.plot(future_dates, forecast_y, 's--',
                 label = f"{product} (прогноз)",
                 markersize = 8,
                 linewidth = 2,
                 color = color,
                 alpha = 0.9,
                 markeredgewidth = 1.5)

        plt.fill_between(future_dates,
                         forecast_y - std_residual * 0.5,
                         forecast_y + std_residual * 0.5,
                         alpha = 0.2,
                         color = color)

        for i, (date, value) in enumerate(zip(future_dates, forecast_y)):
            plt.annotate(f"{value:,.0f}",
                         xy = (date, value),
                         xytext = (0, 12),
                         textcoords = 'offset points',
                         ha = 'center',
                         va = 'bottom',
                         fontsize = 10,
                         fontweight = 'bold',
                         color = color,
                         bbox = dict(boxstyle = "round,pad=0.3",
                                     facecolor = "white",
                                     edgecolor = color,
                                     alpha = 0.8))

plt.xticks(rotation = 45)
plt.title("Прогноз продаж для 4 ключевых товаров на 3 месяца",
          fontsize = 16, fontweight = 'bold', pad = 20)
plt.xlabel("Период", fontsize = 13)
plt.ylabel("Продажи, руб.", fontsize = 13)
plt.grid(True, alpha = 0.3)

last_overall_date = df["Период"].max()
plt.axvline(x = last_overall_date, color = 'gray', linestyle = '--', alpha = 0.7, linewidth = 2)
plt.text(last_overall_date, plt.ylim()[1] * 0.95, "Начало прогноза",
         ha = 'right', va = 'top', fontsize = 10, color = 'gray',
         rotation = 90, fontweight = 'bold')

plt.legend(loc = 'upper left', fontsize = 11, framealpha = 0.9, shadow = True)

plt.tight_layout()
plt.show()