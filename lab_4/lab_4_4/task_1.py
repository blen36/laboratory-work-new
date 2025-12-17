import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing

plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def add_bar_labels(ax):
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{height:.0f}',
                    (p.get_x() + p.get_width() / 2, height),
                    ha='center', va='bottom', fontsize=8, rotation=0)

print("=== ЗАГРУЗКА ДАННЫХ ===")
df = pd.read_excel('s7_data_sample_rev4_50k.xlsx', sheet_name=0)

print(f"Размер данных: {df.shape}")
print("\nПервые 5 строк:")
print(df.head())
print("\nИнформация о данных:")
print(df.info())
print("\nПропущенные значения:")
print(df.isnull().sum())

print("\n=== ОБРАБОТКА ДАННЫХ ===")

df['ISSUE_DATE'] = pd.to_datetime(df['ISSUE_DATE'], errors='coerce')
df['FLIGHT_DATE_LOC'] = pd.to_datetime(df['FLIGHT_DATE_LOC'], errors='coerce')
df['FFP_FLAG'] = df['FFP_FLAG'].fillna('NO_FFP')
ORIG_CITY_CODE_mode = df['ORIG_CITY_CODE'].mode()
df['ORIG_CITY_CODE'].fillna(ORIG_CITY_CODE_mode, inplace=True)
df['ISSUE_YEAR'] = df['ISSUE_DATE'].dt.year
df['FLIGHT_MONTH'] = df['FLIGHT_DATE_LOC'].dt.month
df['FLIGHT_YEAR'] = df['FLIGHT_DATE_LOC'].dt.year

print("\n=== ОПИСАТЕЛЬНЫЕ СТАТИСТИКИ ===")
print(df['REVENUE_AMOUNT'].describe())

plt.figure(figsize=(15, 10))

plt.subplot(2, 3, 1)
plt.hist(df['REVENUE_AMOUNT'], bins=50, edgecolor='black', alpha=0.7)
plt.title('Распределение выручки')
plt.xlabel('Выручка')
plt.ylabel('Частота')

plt.subplot(2, 3, 2)
ax = df['PAX_TYPE'].value_counts().plot(kind='bar')
plt.title('Типы пассажиров')
add_bar_labels(ax)

plt.subplot(2, 3, 3)
ax = df['SALE_TYPE'].value_counts().plot(kind='bar', color='lightgreen')
plt.title('Способы покупки')
add_bar_labels(ax)

plt.subplot(2, 3, 4)
ax = df['ROUTE_FLIGHT_TYPE'].value_counts().plot(kind='bar', color='orange')
plt.title('Типы перелетов')
add_bar_labels(ax)

plt.subplot(2, 3, 5)
ax = df['FFP_FLAG'].value_counts().plot(kind='bar', color='pink')
plt.title('Программа лояльности')
add_bar_labels(ax)

plt.subplot(2, 3, 6)
ax = df['FOP_TYPE_CODE'].value_counts().head(10).plot(kind='bar', color='purple')
plt.title('Топ-10 методов оплаты')
add_bar_labels(ax)

plt.tight_layout()
plt.show()

# ---------------------- АНАЛИЗ АЭРОПОРТОВ ----------------------
print("\n=== АНАЛИЗ АЭРОПОРТОВ ===")

top_origins = df['ORIG_CITY_CODE'].value_counts().head(10)
top_destinations = df['DEST_CITY_CODE'].value_counts().head(10)

print("Топ-10 городов отправления:\n", top_origins)
print(f"\nСамый востребованный город отправления: {top_origins.idxmax()} ({top_origins.max()} перелётов)")

print("\nТоп-10 городов назначения:\n", top_destinations)
print(f"\nСамый востребованный город назначения: {top_destinations.idxmax()} ({top_destinations.max()} перелётов)")

revenue_by_origin = df.groupby('ORIG_CITY_CODE')['REVENUE_AMOUNT'].sum().sort_values(ascending=False).head(10)
revenue_by_dest = df.groupby('DEST_CITY_CODE')['REVENUE_AMOUNT'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(15, 5))

plt.subplot(1, 2, 1)
ax = revenue_by_origin.plot(kind='bar', color='teal')
plt.title('Выручка по аэропортам отправления')
plt.xticks(rotation=45)
add_bar_labels(ax)

plt.subplot(1, 2, 2)
ax = revenue_by_dest.plot(kind='bar', color='coral')
plt.title('Выручка по аэропортам назначения')
plt.xticks(rotation=45)
add_bar_labels(ax)

plt.tight_layout()
plt.show()

print(f"\nМаксимальная выручка по аэропорту отправления: {revenue_by_origin.idxmax()} = {revenue_by_origin.max():.0f}")
print(f"Максимальная выручка по аэропорту назначения: {revenue_by_dest.idxmax()} = {revenue_by_dest.max():.0f}")

# ---------------------- АНАЛИЗ СЕЗОННОСТИ ----------------------
print("\n=== АНАЛИЗ СЕЗОННОСТИ ===")

df['ISSUE_MONTH'] = df['ISSUE_DATE'].dt.month
df['ISSUE_YEAR'] = df['ISSUE_DATE'].dt.year
df['FLIGHT_MONTH'] = df['FLIGHT_DATE_LOC'].dt.month
df['FLIGHT_YEAR'] = df['FLIGHT_DATE_LOC'].dt.year

monthly_sales = df.groupby('ISSUE_MONTH')['REVENUE_AMOUNT'].sum()
monthly_flights = df.groupby('FLIGHT_MONTH')['REVENUE_AMOUNT'].count()

plt.figure(figsize=(15, 5))

plt.subplot(1, 2, 1)
monthly_sales.plot(marker='o')
plt.title('Выручка по месяцам продаж')

plt.subplot(1, 2, 2)
monthly_flights.plot(marker='o')
plt.title('Количество перелетов по месяцам')

plt.tight_layout()
plt.show()

print("\nМаксимальная выручка по месяцам:", monthly_sales.idxmax(), "=", monthly_sales.max())
print("Максимальное число перелётов по месяцам:", monthly_flights.idxmax(), "=", monthly_flights.max())

# ---------------------- МЕТОДЫ ОПЛАТЫ ----------------------
print("\n=== АНАЛИЗ СПОСОБОВ ОПЛАТЫ ===")

payment_stats = df.groupby('FOP_TYPE_CODE')['REVENUE_AMOUNT'].agg(['mean', 'count', 'sum']).sort_values('sum', ascending=False)
payment_pax_cross = pd.crosstab(df['FOP_TYPE_CODE'], df['PAX_TYPE'], normalize='index') * 100

print("\nМетод оплаты с максимальной выручкой:", payment_stats['sum'].idxmax(),
      "=", payment_stats['sum'].max())

plt.figure(figsize=(15, 8))

plt.subplot(2, 2, 1)
ax = payment_stats.head(8)['sum'].plot(kind='bar', color='lightblue')
plt.title('Суммарная выручка по методам оплаты')
add_bar_labels(ax)

plt.subplot(2, 2, 2)
ax = payment_stats.head(8)['mean'].plot(kind='bar', color='lightcoral')
plt.title('Средняя выручка по методам оплаты')
add_bar_labels(ax)

plt.subplot(2, 2, 3)
ax = payment_stats.head(8)['count'].plot(kind='bar', color='lightgreen')
plt.title('Количество транзакций по методам оплаты')
add_bar_labels(ax)

plt.subplot(2, 2, 4)
sns.heatmap(payment_pax_cross.head(8), annot=True, cmap='YlOrRd', fmt='.1f')
plt.title('Методы оплаты по типам пассажиров (%)')

plt.tight_layout()
plt.show()

# ---------------------- ПРОГНОЗИРОВАНИЕ НА 6 МЕСЯЦЕВ ----------------------

print("\n=== ПРОГНОЗИРОВАНИЕ НА 6 МЕСЯЦЕВ ===")

df_issue_date = df.copy()
df_issue_date['ISSUE_DATE'] = pd.to_datetime(df_issue_date['ISSUE_DATE'])

if 'TICKET_NUMBER' in df_issue_date.columns:
    daily_sales = df_issue_date.groupby('ISSUE_DATE').agg({
        'REVENUE_AMOUNT': 'sum',
        'TICKET_NUMBER': 'count'
    }).rename(columns = {'TICKET_NUMBER': 'TICKET_COUNT'})
else:
    daily_sales = df_issue_date.groupby('ISSUE_DATE').agg({
        'REVENUE_AMOUNT': 'sum'
    })
    daily_sales['TICKET_COUNT'] = df_issue_date.groupby('ISSUE_DATE').size()

daily_sales = daily_sales.asfreq('D')
daily_sales['REVENUE_AMOUNT'] = daily_sales['REVENUE_AMOUNT'].fillna(0)
daily_sales['TICKET_COUNT'] = daily_sales['TICKET_COUNT'].fillna(0)

monthly_data = daily_sales.resample('M').agg({
    'REVENUE_AMOUNT': 'sum',
    'TICKET_COUNT': 'sum'
})

print(f"Доступные данные за период: {monthly_data.index.min()} - {monthly_data.index.max()}")
print(f"Количество месяцев в данных: {len(monthly_data)}")

if len(monthly_data) < 12:
    print("ВНИМАНИЕ: Недостаточно данных для сезонного прогноза!")
    X = np.arange(len(monthly_data)).reshape(-1, 1)
    y_revenue = monthly_data['REVENUE_AMOUNT'].values
    y_tickets = monthly_data['TICKET_COUNT'].values

    model_revenue = LinearRegression()
    model_tickets = LinearRegression()

    model_revenue.fit(X, y_revenue)
    model_tickets.fit(X, y_tickets)

    future_months = np.arange(len(monthly_data), len(monthly_data) + 6).reshape(-1, 1)
    revenue_forecast = model_revenue.predict(future_months)
    tickets_forecast = model_tickets.predict(future_months)

    last_date = monthly_data.index[-1]
    forecast_dates = [last_date + pd.DateOffset(months = i + 1) for i in range(6)]

else:
    try:
        model_revenue = SARIMAX(monthly_data['REVENUE_AMOUNT'],
                                order = (1, 1, 1),
                                seasonal_order = (1, 1, 1, 12),
                                enforce_stationarity = False,
                                enforce_invertibility = False)

        revenue_fit = model_revenue.fit(disp = False)
        revenue_forecast = revenue_fit.forecast(steps = 6)

        model_tickets = SARIMAX(monthly_data['TICKET_COUNT'],
                                order = (1, 1, 1),
                                seasonal_order = (1, 1, 1, 12),
                                enforce_stationarity = False,
                                enforce_invertibility = False)

        tickets_fit = model_tickets.fit(disp = False)
        tickets_forecast = tickets_fit.forecast(steps = 6)

        last_date = monthly_data.index[-1]
        forecast_dates = pd.date_range(start = last_date + pd.DateOffset(months = 1),
                                       periods = 6, freq = 'M')

    except Exception as e:
        print(f"Ошибка в SARIMA: {e}. Используем Holt-Winters")

        model_revenue = ExponentialSmoothing(monthly_data['REVENUE_AMOUNT'],
                                             seasonal = 'add',
                                             seasonal_periods = 12).fit()
        model_tickets = ExponentialSmoothing(monthly_data['TICKET_COUNT'],
                                             seasonal = 'add',
                                             seasonal_periods = 12).fit()

        revenue_forecast = model_revenue.forecast(6)
        tickets_forecast = model_tickets.forecast(6)

        last_date = monthly_data.index[-1]
        forecast_dates = pd.date_range(start = last_date + pd.DateOffset(months = 1),
                                       periods = 6, freq = 'M')

forecast_df = pd.DataFrame({
    'Date': forecast_dates,
    'REVENUE_AMOUNT': revenue_forecast,
    'TICKET_COUNT': tickets_forecast
})
forecast_df.set_index('Date', inplace = True)

full_data_revenue = pd.concat([monthly_data[['REVENUE_AMOUNT']],
                               forecast_df[['REVENUE_AMOUNT']]], axis = 0)
full_data_revenue['Type'] = ['Факт'] * len(monthly_data) + ['Прогноз'] * len(forecast_df)

full_data_tickets = pd.concat([monthly_data[['TICKET_COUNT']],
                               forecast_df[['TICKET_COUNT']]], axis = 0)
full_data_tickets['Type'] = ['Факт'] * len(monthly_data) + ['Прогноз'] * len(forecast_df)

fig, axes = plt.subplots(2, 1, figsize = (15, 12))

ax1 = axes[0]
actual_revenue = full_data_revenue[full_data_revenue['Type'] == 'Факт']
ax1.plot(actual_revenue.index, actual_revenue['REVENUE_AMOUNT'],
         'b-', linewidth = 2, marker = 'o', markersize = 5, label = 'Фактические данные')

forecast_revenue = full_data_revenue[full_data_revenue['Type'] == 'Прогноз']
ax1.plot(forecast_revenue.index, forecast_revenue['REVENUE_AMOUNT'],
         'r--', linewidth = 2, marker = 's', markersize = 5, label = 'Прогноз')

split_date = forecast_df.index[0]
ax1.axvline(x = split_date, color = 'gray', linestyle = '--', alpha = 0.7)

ax1.fill_between(forecast_revenue.index,
                 forecast_revenue['REVENUE_AMOUNT'] * 0.8,
                 forecast_revenue['REVENUE_AMOUNT'] * 1.2,
                 alpha = 0.2, color = 'red', label = 'Доверительный интервал (±20%)')

ax1.set_title('ПРОГНОЗ ОБЪЕМОВ ПРОДАЖ БИЛЕТОВ НА 6 МЕСЯЦЕВ', fontsize = 14, fontweight = 'bold')
ax1.set_xlabel('Дата')
ax1.set_ylabel('Выручка (руб.)')
ax1.legend()
ax1.grid(True, alpha = 0.3)
ax1.tick_params(axis = 'x', rotation = 45)

for i, (idx, row) in enumerate(forecast_revenue.iterrows()):
    ax1.annotate(f'{row["REVENUE_AMOUNT"]:,.0f}'.replace(',', ' '),
                 (idx, row["REVENUE_AMOUNT"]),
                 textcoords = "offset points",
                 xytext = (0, 10),
                 ha = 'center',
                 fontsize = 9,
                 bbox = dict(boxstyle = "round,pad=0.3", facecolor = "yellow", alpha = 0.7))

ax2 = axes[1]
actual_tickets = full_data_tickets[full_data_tickets['Type'] == 'Факт']
ax2.plot(actual_tickets.index, actual_tickets['TICKET_COUNT'],
         'g-', linewidth = 2, marker = 'o', markersize = 5, label = 'Фактические данные')

forecast_tickets = full_data_tickets[full_data_tickets['Type'] == 'Прогноз']
ax2.plot(forecast_tickets.index, forecast_tickets['TICKET_COUNT'],
         'orange', linestyle = '--', linewidth = 2, marker = 's', markersize = 5, label = 'Прогноз')

ax2.axvline(x = split_date, color = 'gray', linestyle = '--', alpha = 0.7)

ax2.fill_between(forecast_tickets.index,
                 forecast_tickets['TICKET_COUNT'] * 0.8,
                 forecast_tickets['TICKET_COUNT'] * 1.2,
                 alpha = 0.2, color = 'orange', label = 'Доверительный интервал (±20%)')

ax2.set_title('ПРОГНОЗ КОЛИЧЕСТВА ПЕРЕЛЕТОВ НА 6 МЕСЯЦЕВ', fontsize = 14, fontweight = 'bold')
ax2.set_xlabel('Дата')
ax2.set_ylabel('Количество билетов')
ax2.legend()
ax2.grid(True, alpha = 0.3)
ax2.tick_params(axis = 'x', rotation = 45)

for i, (idx, row) in enumerate(forecast_tickets.iterrows()):
    ax2.annotate(f'{row["TICKET_COUNT"]:,.0f}'.replace(',', ' '),
                 (idx, row["TICKET_COUNT"]),
                 textcoords = "offset points",
                 xytext = (0, 10),
                 ha = 'center',
                 fontsize = 9,
                 bbox = dict(boxstyle = "round,pad=0.3", facecolor = "lightgreen", alpha = 0.7))

plt.tight_layout()
plt.show()

print("\n=== СТАТИСТИКА ПРОГНОЗА ===")
print("\nПрогноз выручки на следующие 6 месяцев:")
for date, value in zip(forecast_df.index, forecast_df['REVENUE_AMOUNT']):
    print(f"  {date.strftime('%Y-%m')}: {value:,.0f} руб.".replace(',', ' '))

print(f"\nСуммарная прогнозируемая выручка: {forecast_df['REVENUE_AMOUNT'].sum():,.0f} руб.".replace(',', ' '))
print(f"Среднемесячная прогнозируемая выручка: {forecast_df['REVENUE_AMOUNT'].mean():,.0f} руб.".replace(',', ' '))

print("\nПрогноз количества перелетов на следующие 6 месяцев:")
for date, value in zip(forecast_df.index, forecast_df['TICKET_COUNT']):
    print(f"  {date.strftime('%Y-%m')}: {value:,.0f} билетов".replace(',', ' '))

print(f"\nСуммарное прогнозируемое количество перелетов: {forecast_df['TICKET_COUNT'].sum():,.0f} билетов".replace(',',
                                                                                                                   ' '))
print(f"Среднемесячное прогнозируемое количество перелетов: {forecast_df['TICKET_COUNT'].mean():,.0f} билетов".replace(
    ',', ' '))
print("\n=== ПРОГНОЗИРОВАНИЕ ЗАВЕРШЕНО ===")