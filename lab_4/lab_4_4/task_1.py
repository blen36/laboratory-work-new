import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima
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
#df['ISSUE_MONTH'] = df['ISSUE_DATE'].dt.month
df['ISSUE_YEAR'] = df['ISSUE_DATE'].dt.year
df['FLIGHT_MONTH'] = df['FLIGHT_DATE_LOC'].dt.month
df['FLIGHT_YEAR'] = df['FLIGHT_DATE_LOC'].dt.year

print('------------------После------------------')
print(df.isnull().sum())

print("\n=== ОПИСАТЕЛЬНЫЕ СТАТИСТИКИ ===")
print(df['REVENUE_AMOUNT'].describe())

# ---------------------- ГИСТОГРАММЫ И BAR ЧАРТЫ ----------------------
plt.figure(figsize=(15, 10))

# 1
plt.subplot(2, 3, 1)
plt.hist(df['REVENUE_AMOUNT'], bins=50, edgecolor='black', alpha=0.7)
plt.title('Распределение выручки')
plt.xlabel('Выручка')
plt.ylabel('Частота')

# 2
plt.subplot(2, 3, 2)
ax = df['PAX_TYPE'].value_counts().plot(kind='bar')
plt.title('Типы пассажиров')
add_bar_labels(ax)

# 3
plt.subplot(2, 3, 3)
ax = df['SALE_TYPE'].value_counts().plot(kind='bar', color='lightgreen')
plt.title('Способы покупки')
add_bar_labels(ax)

# 4
plt.subplot(2, 3, 4)
ax = df['ROUTE_FLIGHT_TYPE'].value_counts().plot(kind='bar', color='orange')
plt.title('Типы перелетов')
add_bar_labels(ax)

# 5
plt.subplot(2, 3, 5)
ax = df['FFP_FLAG'].value_counts().plot(kind='bar', color='pink')
plt.title('Программа лояльности')
add_bar_labels(ax)

# 6
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

# ---------------------- ПРОГНОЗ НА 6 МЕСЯЦЕВ ВПЕРЁД (SARIMAX без сезонности) ----------------------
print("\n=== ПРОГНОЗ SARIMAX (6 МЕСЯЦЕВ) ===")

df['YM'] = df['ISSUE_DATE'].dt.to_period('M')

monthly_rev = df.groupby('YM')['REVENUE_AMOUNT'].sum()
monthly_pax = df.groupby('YM')['REVENUE_AMOUNT'].count()

monthly_rev.index = monthly_rev.index.to_timestamp()
monthly_pax.index = monthly_pax.index.to_timestamp()

steps = 6
future_dates = pd.date_range(monthly_rev.index[-1] + pd.offsets.MonthBegin(1),
                             periods=steps, freq="MS")

# ----- МОДЕЛЬ ДЛЯ ВЫРУЧКИ (без сезонности)
model_rev = SARIMAX(monthly_rev,
                    order=(1,1,1),
                    seasonal_order=(0,0,0,0),
                    enforce_stationarity=False,
                    enforce_invertibility=False)

res_rev = model_rev.fit(disp=False)
rev_mean = res_rev.get_forecast(steps=steps).predicted_mean

# ----- МОДЕЛЬ ДЛЯ ПЕРЕЛЁТОВ (без сезонности)
model_pax = SARIMAX(monthly_pax,
                    order=(1,1,1),
                    seasonal_order=(0,0,0,0),
                    enforce_stationarity=False,
                    enforce_invertibility=False)

res_pax = model_pax.fit(disp=False)
pax_mean = res_pax.get_forecast(steps=steps).predicted_mean

# ----- ГРАФИКИ БЕЗ РОЗОВОГО ФОНА
plt.figure(figsize=(16, 6))

plt.subplot(1,2,1)
plt.plot(monthly_rev.index, monthly_rev.values, "o-", label="Фактическая выручка")
plt.plot(future_dates, rev_mean, "--", label="Прогноз")
plt.title("SARIMAX прогноз выручки на 6 месяцев")
plt.xlabel("Дата"); plt.ylabel("Выручка")
plt.legend()

plt.subplot(1,2,2)
plt.plot(monthly_pax.index, monthly_pax.values, "o-", label="Фактическое число перелётов")
plt.plot(future_dates, pax_mean, "--", label="Прогноз")
plt.title("SARIMAX прогноз числа перелётов на 6 месяцев")
plt.xlabel("Дата"); plt.ylabel("Количество перелётов")
plt.legend()

plt.tight_layout()
plt.show()




