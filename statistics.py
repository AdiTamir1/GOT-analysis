import pandas
excel_data_df = pandas.read_excel('./processed_data/output.xlsx')
names = []
episodes = []
seasons = []

for id in excel_data_df['id']:
    splitted_name = id.split('_', 2)
    season = splitted_name[0]
    episode = splitted_name[1]
    name = splitted_name[2]
    names.append(name)
    episodes.append(episode)
    seasons.append(season)

excel_data_df['Name'] = names
excel_data_df['Episode'] = episodes
excel_data_df['Season'] = seasons

name_col_data = excel_data_df["Name"]
name_col_data_with_char = name_col_data.str.contains('tyrion|cersei|snow|daenerys')

filtred_data = excel_data_df[name_col_data_with_char]
filtred_data.to_excel('./processed_data/newoutput.xlsx')

my_data = pandas.read_excel('./processed_data/newoutput.xlsx')
my_data = my_data.itertuples()

avg = {}
for row in my_data:
    avg[row.Season] = avg.get(row.Season,{})
    avg[row.Season][row.Name] = avg[row.Season].get(row.Name, {})
    avg[row.Season][row.Name]['sentiment_sum'] = avg[row.Season][row.Name].get('sentiment_sum', 0)
    avg[row.Season][row.Name]['count'] = avg[row.Season][row.Name].get('count', 0)
    avg[row.Season][row.Name]['sentiment_sum'] += row.sentiment
    avg[row.Season][row.Name]['count'] += 1

new_avg = {}
for season_name, season_dict in avg.items():
    parser_season_name = int(season_name.replace('Season ', ''))
    new_avg[parser_season_name] = new_avg.get(parser_season_name, {})
    for char_name, char_dict in season_dict.items():
        new_avg[parser_season_name][char_name] = char_dict['sentiment_sum'] / char_dict['count']


avaragedata = pandas.DataFrame.from_dict(new_avg, orient="index")
avaragedata.to_excel("avaragedata.xlsx")

import numpy
import seaborn
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

data = pandas.read_excel('avaragedata.xlsx')
fig = plt.figure()
graph = fig.add_subplot(1,1,1)

X = data.iloc[:, 0].values.reshape(-1, 1)
Y1 = data.iloc[:,1].values.reshape(-1, 1)
Y2 = data.iloc[:,2].values.reshape(-1, 1)
Y3 = data.iloc[:,3].values.reshape(-1, 1)
Y4 = data.iloc[:,4].values.reshape(-1, 1)

jon_snow = plt.scatter(X, Y1, color='royalblue', marker='*')
cersei_lannister = plt.scatter(X, Y2, color='gold', marker='^')
tyrion_lannister = plt.scatter(X, Y3, color='fuchsia', marker='o')
daenerys_targaryen = plt.scatter(X, Y4, color='red', marker='x')

graph.legend([jon_snow,cersei_lannister,tyrion_lannister,daenerys_targaryen],['Jon Snow','Cersei Lannister','Tyrion Lannister','Daenerys Targaryen'])
graph.set_xlabel('Seasons')
graph.set_ylabel('Average Of Sentiments')
avg_of_avg = []

for zipped_item in zip(Y1, Y2, Y3, Y4):
    zipped_sum = 0
    for char_sentiment_avg in zipped_item:
        zipped_sum += char_sentiment_avg[0]

    avg_of_avg.append([zipped_sum / len(zipped_item)])

linear_regressor = LinearRegression()
linear_regressor.fit(X, avg_of_avg)
Y_pred = linear_regressor.predict(X)
plt.plot(X, Y_pred, color='black')
plt.show()
