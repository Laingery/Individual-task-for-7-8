# Индивидуальное задание для практики 7-8
import pandas as pd

dataframe_comp = pd.read_csv('data/competition_1.csv', sep=";", decimal=',')
print(dataframe_comp.dtypes)
print(dataframe_comp.head(3))

# 1.1) среднее значение и медиану бега на 100 метров (мин, сек) по каждой
# возрастной группе (год рождения есть) по девочкам и мальчикам;
print('-' * 15, '1.1)', '-' * 15)
print(
    dataframe_comp.groupby(["Год рождения", "Пол"])[["Бег 1000 метров, мин. и сек."]
    ].agg(['mean', 'median'])
)
print('-' * 15, '1.2)', '-' * 15)


# 1.2) определить победителей (фамилии и имена детей) в каждой возрастной группе
#  по мальчикам и по девочкам (3 первых места) по каждому виду. Учесть,
#  что победителей может быть больше 3-х, так как результаты могут совпадать;

# если можно элегантный прошу направить в нужном направлении, а пока извините ГОВНОКОД)))
def win_list(year, gender, discipline, top_n=3):
    v = dataframe_comp[(dataframe_comp["Год рождения"] == year)
                       & (dataframe_comp["Пол"] == gender)][discipline].sort_values(
        ascending=(discipline != 'Прыжок в длину с места, см ')).unique()[top_n - 1]
    # print(v)
    x = dataframe_comp[(dataframe_comp["Год рождения"] == year)
                       & (dataframe_comp["Пол"] == gender)
                       & (dataframe_comp[discipline] <= v if (discipline != 'Прыжок в длину с места, см ') else
                          dataframe_comp[discipline] >= v)
                       ][["Фамилия", "Имя", "Год рождения", discipline]].sort_values(by=discipline, ascending=(
            discipline != 'Прыжок в длину с места, см ')).reset_index(drop=True)
    return x


print(win_list(1999, "ж", "Бег 1000 метров, мин. и сек."), '\n')
print(win_list(1999, "ж", "Бег 30 метров, сек."), '\n')
print(win_list(1999, "ж", "Прыжок в длину с места, см "), '\n')
# for i in pd.unique(dataframe_comp["Год рождения"].sort_values(ascending=False).unique()):
#   print(f'\n{i} год.')
#   print(f' мальчики.')
#   print(win_list(i ,"м","Бег 1000 метров, мин. и сек.").head(-1))
#   print(f'\n девочки.')
#   print(win_list(i ,"ж","Бег 1000 метров, мин. и сек.").head(-1))

# win_list(1996 ,"ж","Прыжок в длину с места, см ",5)

print('-' * 15, '1.3)', '-' * 15)
# 1.3) определить в каждой возрастной группе девочек,
# которые по трём видам (по всем) испытаний входят в ТОП5;

m_year = 1999


# print(win_list(m_year ,"ж","Бег 1000 метров, мин. и сек.",5),'\n')
# print(win_list(m_year ,"ж","Бег 30 метров, сек.",5),'\n')
# print(win_list(m_year ,"ж","Прыжок в длину с места, см ",5),'\n')

def get_best_list(year):
    best_list = win_list(year, "ж", "Бег 1000 метров, мин. и сек.", 5)
    best_list = best_list.merge(win_list(year, "ж", "Бег 30 метров, сек.", 5), how='inner',
                                on=['Фамилия', 'Имя', 'Год рождения'])
    best_list = best_list.merge(win_list(year, "ж", "Прыжок в длину с места, см ", 5), how='inner',
                                on=['Фамилия', 'Имя', 'Год рождения'])
    return best_list


bl = get_best_list(m_year)
print(bl.head(bl.shape[0]))

print('-' * 15, '1.4)', '-' * 15)
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def data_grapgGenderMean(discipl):
    p = dataframe_comp[(dataframe_comp["Пол"] == 'ж')].groupby(["Год рождения"])[[discipl]].mean()
    p["м"] = dataframe_comp[(dataframe_comp["Пол"] == 'м')].groupby(["Год рождения"])[[discipl]].mean()
    p = p.reset_index().rename(columns={discipl: 'ж'})
    return p


fig = plt.figure(figsize=(20, 4))

discipline, data_figure, position = ['Бег 1000 метров, мин. и сек.', 'Бег 30 метров, сек.',
                                     'Прыжок в длину с места, см '], [], []

for i in range(len(discipline)):
    position.append(fig.add_subplot(1, 3, i + 1))  # контейнер
    data_figure.append(data_grapgGenderMean(discipline[i]))  # данные

    position[i].set(title=discipline[i], xlabel='Год рождения', ylabel='Усреднённый показатель')
    position[i].xaxis.set_major_locator(ticker.MultipleLocator(1))

    position[i].plot(data_figure[i]["Год рождения"], data_figure[i]["ж"], '-*')  # в отресовка первой фигуры
    position[i].plot(data_figure[i]["Год рождения"], data_figure[i]["м"], '-x')  # в отресовка второй фигуры
    plt.legend(["ж", "м"], fontsize=10, loc="lower right")  # параметры легенды
    plt.grid(True)
plt.subplots_adjust(wspace=0.4)
# plt.show()

fig_2 = plt.figure(figsize=(20, 4))
old_caunt = len(position)

for i in range(len(discipline)):
    position.append(fig_2.add_subplot(1, 3, i + 1))  # контейнер

    position[i + old_caunt].set(xlabel='Год рождения', ylabel='Единицы измерения')
    position[i + old_caunt].xaxis.set_major_locator(ticker.MultipleLocator(1))

    position[i + old_caunt].scatter(dataframe_comp[(dataframe_comp["Пол"] == "ж")]["Год рождения"],
                                    dataframe_comp[(dataframe_comp["Пол"] == "ж")][discipline[i]], color='orange',
                                    alpha=0.2)

    position[i + old_caunt].scatter(dataframe_comp[(dataframe_comp["Пол"] == "м")]["Год рождения"],
                                    dataframe_comp[(dataframe_comp["Пол"] == "м")][discipline[i]], color='blue',
                                    alpha=0.1)
    plt.legend(["ж", "м"], fontsize=10, loc="lower center")  # параметры легенды
    plt.subplots_adjust(wspace=0.4)
plt.show()

print('-' * 15, '1.5)', '-' * 15)

import seaborn as sns

plt.figure(figsize=(10, 6))
sns.violinplot(x="Год рождения", y="Бег 1000 метров, мин. и сек.", data=dataframe_comp, hue="Пол", split=True,
               palette=['green', 'orange'])
plt.grid(True)

plt.figure(figsize=(10, 5))
sns.violinplot(x="Год рождения", y="Бег 30 метров, сек.", data=dataframe_comp, hue="Пол", split=True,
               palette=['green', 'orange'])
plt.grid(True)

plt.figure(figsize=(10, 5))
sns.violinplot(x="Год рождения", y="Прыжок в длину с места, см ", data=dataframe_comp, hue="Пол", split=True,
               palette=['green', 'orange'])
plt.grid(True)

plt.figure(figsize=(10, 6))
sns.violinplot(x="Пол", y="Год рождения", data=dataframe_comp, palette=['green', 'orange'])
plt.grid(True)
plt.show()
