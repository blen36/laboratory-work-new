import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

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

df['ISSUE_MONTH'] = df['ISSUE_DATE'].dt.month
df['ISSUE_YEAR'] = df['ISSUE_DATE'].dt.year
df['FLIGHT_MONTH'] = df['FLIGHT_DATE_LOC'].dt.month
df['FLIGHT_YEAR'] = df['FLIGHT_DATE_LOC'].dt.year

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

# ---------------------- АНАЛИЗ ПАССАЖИРОВ ----------------------
print("\n=== АНАЛИЗ ПАССАЖИРОВ ===")
revenue_by_pax = df.groupby('PAX_TYPE')['REVENUE_AMOUNT'].agg(['mean', 'count', 'sum'])
revenue_by_ffp = df.groupby('FFP_FLAG')['REVENUE_AMOUNT'].agg(['mean', 'count', 'sum'])

print("Типы пассажиров:\n", revenue_by_pax)
print(f"\nТип пассажира с максимальной выручкой: {revenue_by_pax['sum'].idxmax()} = {revenue_by_pax['sum'].max():.0f}")

print("\nПрограмма лояльности:\n", revenue_by_ffp)
print(f"\nFFP-группа с максимальной выручкой: {revenue_by_ffp['sum'].idxmax()} = {revenue_by_ffp['sum'].max():.0f}")

plt.figure(figsize=(15, 5))

plt.subplot(1, 2, 1)
ax = revenue_by_pax['mean'].plot(kind='bar')
plt.title('Средняя выручка по типам пассажиров')
add_bar_labels(ax)

plt.subplot(1, 2, 2)
ax = revenue_by_ffp['mean'].plot(kind='bar')
plt.title('Средняя выручка: программа лояльности')
add_bar_labels(ax)

plt.tight_layout()
plt.show()

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

# ---------------------- ПРОГНОЗ ПРОДАЖ И ПЕРЕЛЁТОВ ----------------------

print("\n=== ПРОГНОЗ ПРОДАЖ И ПЕРЕЛЁТОВ ===")

# ===== 1. Агрегация по месяцам =====
monthly = df.groupby(pd.Grouper(key='ISSUE_DATE', freq='M')).agg({
    'REVENUE_AMOUNT': 'sum',
    'FLIGHT_DATE_LOC': 'count'
}).rename(columns={'FLIGHT_DATE_LOC': 'FLIGHTS'}).reset_index()

# Нормальная нумерация месяцев для регрессии
monthly['MONTH_NUM'] = range(len(monthly))

# ===== 2. Модели =====
X = monthly[['MONTH_NUM']]
y_sales = monthly['REVENUE_AMOUNT']
y_flights = monthly['FLIGHTS']

model_sales = LinearRegression().fit(X, y_sales)
model_flights = LinearRegression().fit(X, y_flights)

# ===== 3. Прогноз на 3 будущих месяца =====
future_periods = 3
last_month_num = monthly['MONTH_NUM'].iloc[-1]

future_nums = list(range(last_month_num + 1, last_month_num + 1 + future_periods))

future_dates = pd.date_range(
    start=monthly['ISSUE_DATE'].iloc[-1] + pd.DateOffset(months=1),
    periods=future_periods,
    freq='M'
)

future_df = pd.DataFrame({
    'ISSUE_DATE': future_dates,
    'MONTH_NUM': future_nums
})

# Прогнозы
future_df['PRED_SALES'] = model_sales.predict(future_df[['MONTH_NUM']])
future_df['PRED_FLIGHTS'] = model_flights.predict(future_df[['MONTH_NUM']])

# ===== 4. Вывод прогноза в консоль =====
print("\nПрогноз на следующие 3 месяца:")
print(future_df[['ISSUE_DATE', 'PRED_SALES', 'PRED_FLIGHTS']])

# ===== 5. Объединяем факт + прогноз для графика =====
plot_df = pd.concat([
    monthly[['ISSUE_DATE', 'REVENUE_AMOUNT', 'FLIGHTS']],
    future_df.rename(columns={
        'PRED_SALES': 'REVENUE_AMOUNT',
        'PRED_FLIGHTS': 'FLIGHTS'
    })[['ISSUE_DATE', 'REVENUE_AMOUNT', 'FLIGHTS']]
], ignore_index=True)

# Отметим где прогноз
is_future = [False] * len(monthly) + [True] * len(future_df)

# ===== 6. График прогноза =====
plt.figure(figsize=(14, 6))

# ---- выручка ----
plt.subplot(1, 2, 1)
plt.plot(monthly['ISSUE_DATE'], monthly['REVENUE_AMOUNT'], label='Факт', color='blue')
plt.plot(future_df['ISSUE_DATE'], future_df['PRED_SALES'], 'o--', label='Прогноз', color='gold')
plt.title('Прогноз выручки на 3 месяца')
plt.legend()

# ---- перелёты ----
plt.subplot(1, 2, 2)
plt.plot(monthly['ISSUE_DATE'], monthly['FLIGHTS'], label='Факт', color='green')
plt.plot(future_df['ISSUE_DATE'], future_df['PRED_FLIGHTS'], 'o--', label='Прогноз', color='orange')
plt.title('Прогноз количества перелётов на 3 месяца')
plt.legend()

plt.tight_layout()
plt.show()

