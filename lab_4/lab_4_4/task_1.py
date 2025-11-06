import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

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

df['ISSUE_MONTH'] = df['ISSUE_DATE'].dt.month
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
df['PAX_TYPE'].value_counts().plot(kind='bar', color='skyblue')
plt.title('Типы пассажиров')

plt.subplot(2, 3, 3)
df['SALE_TYPE'].value_counts().plot(kind='bar', color='lightgreen')
plt.title('Способы покупки')

plt.subplot(2, 3, 4)
df['ROUTE_FLIGHT_TYPE'].value_counts().plot(kind='bar', color='orange')
plt.title('Типы перелетов')

plt.subplot(2, 3, 5)
df['FFP_FLAG'].value_counts().plot(kind='bar', color='pink')
plt.title('Программа лояльности')

plt.subplot(2, 3, 6)
df['FOP_TYPE_CODE'].value_counts().head(10).plot(kind='bar', color='purple')
plt.title('Топ-10 методов оплаты')

plt.tight_layout()
plt.show()

print("\n=== АНАЛИЗ АЭРОПОРТОВ ===")

top_origins = df['ORIG_CITY_CODE'].value_counts().head(10)
top_destinations = df['DEST_CITY_CODE'].value_counts().head(10)
print("Топ-10 городов отправления:\n", top_origins)
print("\nТоп-10 городов назначения:\n", top_destinations)

revenue_by_origin = df.groupby('ORIG_CITY_CODE')['REVENUE_AMOUNT'].sum().sort_values(ascending=False).head(10)
revenue_by_dest = df.groupby('DEST_CITY_CODE')['REVENUE_AMOUNT'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
revenue_by_origin.plot(kind='bar', color='teal')
plt.title('Выручка по аэропортам отправления')
plt.xticks(rotation=45)
plt.subplot(1, 2, 2)
revenue_by_dest.plot(kind='bar', color='coral')
plt.title('Выручка по аэропортам назначения')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\n=== АНАЛИЗ СЕЗОННОСТИ ===")
monthly_sales = df.groupby('ISSUE_MONTH')['REVENUE_AMOUNT'].sum()
monthly_flights = df.groupby('FLIGHT_MONTH')['REVENUE_AMOUNT'].count()

plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
monthly_sales.plot(marker='o', color='blue')
plt.title('Выручка по месяцам продаж')
plt.subplot(1, 2, 2)
monthly_flights.plot(marker='o', color='red')
plt.title('Количество перелетов по месяцам')
plt.tight_layout()
plt.show()

print("\n=== АНАЛИЗ ПАССАЖИРОВ ===")
revenue_by_pax = df.groupby('PAX_TYPE')['REVENUE_AMOUNT'].agg(['mean', 'count', 'sum'])
revenue_by_ffp = df.groupby('FFP_FLAG')['REVENUE_AMOUNT'].agg(['mean', 'count', 'sum'])
print("Типы пассажиров:\n", revenue_by_pax)
print("\nПрограмма лояльности:\n", revenue_by_ffp)

plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
revenue_by_pax['mean'].plot(kind='bar', color=['blue', 'green', 'red'])
plt.title('Средняя выручка по типам пассажиров')
plt.subplot(1, 2, 2)
revenue_by_ffp['mean'].plot(kind='bar', color=['purple', 'orange'])
plt.title('Средняя выручка: программа лояльности')
plt.tight_layout()
plt.show()

print("\n=== АНАЛИЗ СПОСОБОВ ОПЛАТЫ ===")
payment_stats = df.groupby('FOP_TYPE_CODE')['REVENUE_AMOUNT'].agg(['mean', 'count', 'sum']).sort_values('sum', ascending=False)
payment_pax_cross = pd.crosstab(df['FOP_TYPE_CODE'], df['PAX_TYPE'], normalize='index') * 100

plt.figure(figsize=(15, 8))
plt.subplot(2, 2, 1)
payment_stats.head(8)['sum'].plot(kind='bar', color='lightblue')
plt.title('Суммарная выручка по методам оплаты')
plt.subplot(2, 2, 2)
payment_stats.head(8)['mean'].plot(kind='bar', color='lightcoral')
plt.title('Средняя выручка по методам оплаты')
plt.subplot(2, 2, 3)
payment_stats.head(8)['count'].plot(kind='bar', color='lightgreen')
plt.title('Количество транзакций')
plt.subplot(2, 2, 4)
sns.heatmap(payment_pax_cross.head(8), annot=True, cmap='YlOrRd', fmt='.1f')
plt.title('Методы оплаты по типам пассажиров (%)')
plt.tight_layout()
plt.show()

print("\n=== ПРОГНОЗ ПРОДАЖ И ПЕРЕЛЁТОВ ===")

monthly = df.groupby(pd.Grouper(key='ISSUE_DATE', freq='M')).agg({
    'REVENUE_AMOUNT': 'sum',
    'FLIGHT_DATE_LOC': 'count'
}).rename(columns={'FLIGHT_DATE_LOC': 'FLIGHTS'}).reset_index()

monthly['MONTH_NUM'] = range(len(monthly))

X = monthly[['MONTH_NUM']]
y_sales = monthly['REVENUE_AMOUNT']
y_flights = monthly['FLIGHTS']

model_sales = LinearRegression().fit(X, y_sales)
model_flights = LinearRegression().fit(X, y_flights)

monthly['PRED_SALES'] = model_sales.predict(X)
monthly['PRED_FLIGHTS'] = model_flights.predict(X)

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(monthly['ISSUE_DATE'], monthly['REVENUE_AMOUNT'], label='Факт', color='blue')
plt.plot(monthly['ISSUE_DATE'], monthly['PRED_SALES'], label='Прогноз', color='red')
plt.title('Прогноз выручки по месяцам')
plt.legend()
plt.subplot(1, 2, 2)
plt.plot(monthly['ISSUE_DATE'], monthly['FLIGHTS'], label='Факт', color='green')
plt.plot(monthly['ISSUE_DATE'], monthly['PRED_FLIGHTS'], label='Прогноз', color='orange')
plt.title('Прогноз количества перелётов по месяцам')
plt.legend()
plt.tight_layout()
plt.show()
