import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

app = dash.Dash(__name__)
server = app.server

url = 'https://github.com/jacky308082/nba-player-data-dash-plotly/blob/master/2012-18_playerBoxScore.csv'
df = pd.read_csv(url, parse_dates=['gmDate'])

def selected_columns(df):
	columns = ['gmDate', 'teamRslt', 'playDispNm', 'playMin', 'playPTS', 'playAST', 'playTO', 'playSTL', 'playBLK', 'playPF']
	new_df = df.loc[:, columns]
	return new_df

df = selected_columns(df)

def create_name_dict_list_of_player():
	"""
	建造dropdown裡面族值
	"""
	dictlist = []
	unique_list = df.playDispNm.unique()
	unique_list.sort()
	for title in unique_list:
		dictlist.append({'value': title, 'label': title})
	return dictlist

def create_dict_list_of_columns():
	"""
	根據數據的不同來建立圖表
	"""
	columns_dict = {
		'playPTS': 'Points', 
		'playAST': 'Assist', 
		'playTO': 'Turnover', 
		'playSTL': 'Steal', 
		'playBLK': 'Block', 
		'playPF': 'Personal Foul'
	}
	dictlist = []
	for column in columns_dict:
		dictlist.append({'value': column, 'label': columns_dict[column]})
	return dictlist


name_dictlist = create_name_dict_list_of_player()
column_dictlist = create_dict_list_of_columns()

app.layout = html.Div([
	html.Div([
		html.H1('Draw the NBA player data'),
		html.H2('Choose a player name'),
		dcc.Dropdown(
			id='player-dropdown',
			options=name_dictlist,
			multi=False,
			value=name_dictlist[0].get('value'),
			placeholder='Select a player'			
		),
		html.Br(),
		dcc.Dropdown(
			id='column-dropdown',
			options=column_dictlist,
			multi=False,
			value=column_dictlist[0].get('value'),
			placeholder='Select a data you what to understand'
		),
		html.Br(),
		html.H2('Choose a year'),
		dcc.Slider(
			id='year-slider',
			min=df.gmDate.dt.year.min(),
			max=df.gmDate.dt.year.max(),
			value=2012,
			marks={
				i: 'season {}~{}'.format(i, i+1) for i in range(2012, 2018)
			}
		),
		html.Br(),
		dcc.Graph(
			id='player-data-line'
		)
	])
])

@app.callback(Output('player-data-line', 'figure'), [Input('player-dropdown', 'value'),
													 Input('year-slider', 'value'),
													 Input('column-dropdown', 'value')])
def update_graph(selected_dropdown_value, selected_year, selected_column):
	start_date = '{}-10-01'.format(selected_year)
	end_date = '{}-04-30'.format(selected_year+1)
	player_df_filter = df[(df['playDispNm']==selected_dropdown_value) & ((df['gmDate'] > start_date) & (df['gmDate'] < end_date))].loc[:, ['gmDate', selected_column]]

	figure = {
		'data': [go.Scatter(
			x= player_df_filter['gmDate'],
			y= player_df_filter[selected_column],
			mode='lines')],
		'layout': go.Layout(
			xaxis={'title': 'Game Date'},
			yaxis={'title': 'Player {}'.format(selected_column)})
		}

	return figure

if __name__ == '__main__':
	app.run_server(debug=True)
