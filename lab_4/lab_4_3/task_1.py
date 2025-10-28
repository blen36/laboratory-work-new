import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

fake = Faker('ru_RU')
np.random.seed(42)

CURRENT_YEAR = datetime.now().year
YEARS = list(range(CURRENT_YEAR - 4, CURRENT_YEAR + 1))
SUBJECTS = ['Математика', 'Русский язык', 'Физика', 'Химия', 'Биология', 'История', 'Обществознание']
FORMS = ['Бюджет', 'Платно', 'Целевое']
SPECIALTIES = ['Прикладная информатика', 'Прикладная математика', 'Ядерная физика', 'Химия', 'Лечебное дело',
               'Экономика', 'Юриспруденция', 'Радиофизика']
SPECIALTIES_SUBJECT = {
    'Прикладная информатика': ['Математика', 'Физика', 'Русский язык'],
    'Прикладная математика': ['Математика', 'Физика', 'Русский язык'],
    'Ядерная физика': ['Математика', 'Физика', 'Русский язык'],
    'Химия': ['Химия', 'Математика', 'Русский язык'],
    'Лечебное дело': ['Биология', 'Химия', 'Русский язык'],
    'Экономика': ['Математика', 'Обществознание', 'Русский язык'],
    'Юриспруденция': ['История', 'Обществознание', 'Русский язык'],
    'Радиофизика': ['Математика', 'Физика', 'Русский язык']
}

data = []
for year in YEARS:
    student_count = np.random.randint(800, 1200)

    for _ in range(student_count):
        specialty = random.choice(SPECIALTIES)
        study_form = random.choice(FORMS)
        subjects = SPECIALTIES_SUBJECT[specialty]

        if study_form == 'Бюджет':
            subject_scores = {subject: np.random.randint(75, 100) for subject in subjects}
            certificate_score = np.random.uniform(8.5, 10.0)
        elif study_form == 'Платно':
            subject_scores = {subject: np.random.randint(50, 80) for subject in subjects}
            certificate_score = np.random.uniform(6.0, 8.0)
        else:
            subject_scores = {subject: np.random.randint(50, 70) for subject in subjects}
            certificate_score = np.random.uniform(5.0, 8.0)

        total_score = sum(subject_scores.values()) + certificate_score * 10

        student_data = {
            'ФИО': fake.name(),
            'Год_поступления': year,
            'Форма_обучения': study_form,
            'Специальность': specialty,
            'Средний_балл_аттестата': round(certificate_score, 2),
            'Общий_балл': round(total_score, 2),
            'Адрес_регистрации': fake.address().replace('\n', ', '),
            'Телефон': fake.phone_number()
        }

        for i, subject in enumerate(subject_scores, 1):
            student_data[f"Предмет_{i}"] = subject
            student_data[f"Балл_{i}"] = subject_scores[subject]

        data.append(student_data)

df = pd.DataFrame(data)
print(f"Сгенерировано {len(df)} записей")

sns.set_theme(style = "whitegrid")

# Подготовка данных для предметов
subject_long_data = []
for year in YEARS:
    year_data = df[df['Год_поступления'] == year]
    for i in range(1, 4):
        for _, row in year_data.iterrows():
            subject_long_data.append({
                'Год': year,
                'Предмет': row[f'Предмет_{i}'],
                'Балл': row[f'Балл_{i}']
            })
subject_df = pd.DataFrame(subject_long_data)

# Создание фигуры с сеткой 3x2
fig, axes = plt.subplots(3, 2, figsize = (22, 20), dpi = 100, constrained_layout = True)
fig.suptitle('Анализ вступительной кампании за 5 лет', fontsize = 18, fontweight = 'bold')

# 1) Динамика среднего балла ЦТ по предметам
subject_year_avg = subject_df.groupby(['Год', 'Предмет'], as_index = False)['Балл'].mean()
sns.barplot(data = subject_year_avg, x = 'Год', y = 'Балл', hue = 'Предмет', ax = axes[0, 0])
axes[0, 0].set_title('Динамика среднего балла ЦТ по предметам', fontsize = 14)
axes[0, 0].set_ylabel('Средний балл', fontsize = 12)
axes[0, 0].set_xlabel('Год', fontsize = 12)
axes[0, 0].tick_params(axis = 'x', labelsize = 10)
axes[0, 0].tick_params(axis = 'y', labelsize = 10)
axes[0, 0].legend(bbox_to_anchor = (1.02, 1), loc = 'upper left', fontsize = 9)

# 2) Динамика проходного балла по специальностям
passing_data = []
for specialty in SPECIALTIES:
    specialty_data = df[df['Специальность'] == specialty]

    # Правильный расчет проходного балла с учетом 3 предметов и среднего балла аттестата
    passing_scores = specialty_data.groupby('Год_поступления').apply(
        lambda x: x.nsmallest(1, 'Общий_балл')['Общий_балл'].iloc[0] if len(x) > 0 else 0
    ).reset_index()
    passing_scores.columns = ['Год_поступления', 'Общий_балл']
    passing_scores['Специальность'] = specialty
    passing_data.append(passing_scores)

passing_df = pd.concat(passing_data)
heatmap_passing = passing_df.pivot_table(values = 'Общий_балл',
                                         index = 'Специальность',
                                         columns = 'Год_поступления',
                                         aggfunc = 'mean')
sns.heatmap(heatmap_passing, annot = True, cmap = 'RdYlGn_r', fmt = '.1f',
            ax = axes[0, 1], cbar_kws = {'label': 'Проходной балл'})
axes[0, 1].set_title('Динамика проходного балла по специальностям', fontsize = 14)
axes[0, 1].set_xlabel('Год', fontsize = 12)
axes[0, 1].set_ylabel('Специальность', fontsize = 12)

# 3) Динамика среднего балла аттестата
certificate_avg = df.groupby('Год_поступления')['Средний_балл_аттестата'].mean().reset_index()
sns.barplot(data = certificate_avg, x = 'Год_поступления', y = 'Средний_балл_аттестата',
            ax = axes[1, 0], palette = 'Reds_r')
axes[1, 0].set_title('Динамика среднего балла аттестата', fontsize = 14)
axes[1, 0].set_xlabel('Год', fontsize = 12)
axes[1, 0].set_ylabel('Средний балл', fontsize = 12)

# 4) Количество поступивших по специальностям
specialty_counts = df['Специальность'].value_counts().reset_index()
specialty_counts.columns = ['Специальность', 'Количество']
sns.barplot(data = specialty_counts, x = 'Специальность', y = 'Количество', ax = axes[1, 1])
axes[1, 1].set_title('Количество поступивших по специальностям', fontsize = 14)
axes[1, 1].set_xlabel('Специальность', fontsize = 12)
axes[1, 1].set_ylabel('Количество студентов', fontsize = 12)
plt.setp(axes[1, 1].xaxis.get_majorticklabels(), rotation = 35, ha = 'right', fontsize = 9)
axes[1, 1].tick_params(axis = 'y', labelsize = 10)

# 5) Распределение по формам обучения
form_counts = df['Форма_обучения'].value_counts()
ax_pie = axes[2, 0]
ax_pie.pie(form_counts.values, labels = form_counts.index, autopct = '%1.1f%%',
           startangle = 90, colors = ['#ff9999', '#66b3ff', '#99ff99'])
ax_pie.set_title('Распределение по формам обучения', fontsize = 14)
ax_pie.axis('equal')

# Скрываем шестую пустую ячейку
axes[2, 1].set_visible(False)

plt.show()