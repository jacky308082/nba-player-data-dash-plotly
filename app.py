import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc 				# dcc used in the html page
import dash_html_components as html 			# html can parse the html components
import plotly.graph_objs as go                  # plotly
import pandas as pd
import numpy as np

"""
Another version:

server = Flask(__name__)
app = Dash(__name__, server=server)
"""
# build dash object
app = dash.Dash(__name__)
# Use the server of flask to run
server = app.server

# read csv on the github
url = 'https://raw.githubusercontent.com/jacky308082/nba-player-data-dash-plotly/master/2012-18_playerBoxScore.csv'
df = pd.read_csv(url, parse_dates=['gmDate'])

def selected_columns(df):
	"""
	Choose the columns use in the dashboard
	"""
	columns = ['gmDate', 'teamRslt', 'playDispNm', 'playMin', 'playPTS', 'playAST', 'playTO', 'playSTL', 'playBLK', 'playPF']
	new_df = df.loc[:, columns]
	return new_df

df = selected_columns(df)

def create_name_dict_list_of_player():
	"""
	Build dropdown value and name
	This is will show in player-dropdown
	"""
	dictlist = []
	unique_list = df.playDispNm.unique()
	unique_list.sort()
	for title in unique_list:
		dictlist.append({'value': title, 'label': title})
	return dictlist

def create_dict_list_of_columns():
	"""
	Build the dashboard depend on the columns
	This will show in columns-dropdown
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

# Build the html page
app.layout = html.Div([
	html.Div([
		html.H1('Draw the NBA player data'),
		html.H2('Choose a player name'),
		dcc.Dropdown(
			id='player-dropdown', 											# Dropdown name (Used in the callback)
			options=name_dictlist, 											# The name that contains the value 
			multi=False, 													# Choose one in a time
			value=name_dictlist[0].get('value') 							# Value will show first
		),
		html.Br(),
		dcc.Dropdown(
			id='column-dropdown',
			options=column_dictlist,
			multi=False,
			value=column_dictlist[0].get('value'),
		),
		html.Br(),
		html.H2('Choose a year'),
		dcc.Slider( 														# The line from the begin to the end
			id='year-slider',
			min=df.gmDate.dt.year.min(), 									# Begin date
			max=df.gmDate.dt.year.max(), 									# End date
			value=2012, 													# value
			marks={
				i: 'season {}~{}'.format(i, i+1) for i in range(2012, 2018) # name will apear on the slider
			}
		),
		html.Br(),
		dcc.Graph(
			id='player-data-line'  											# Build the Graph by plotly
		)
	])
])

# Put the input and output in callback selector
# Output to the dcc.Graph
# Input contains value from the mulitiple functions
@app.callback(Output('player-data-line', 'figure'), [Input('player-dropdown', 'value'),
													 Input('year-slider', 'value'),
													 Input('column-dropdown', 'value')])
def update_graph(selected_dropdown_value, selected_year, selected_column):
	"""
	Base on the order of thw Input, Put names in the def function
	"""
	start_date = '{}-10-01'.format(selected_year)
	end_date = '{}-04-30'.format(selected_year+1)
	player_df_filter = df[(df['playDispNm']==selected_dropdown_value) & ((df['gmDate'] > start_date) & (df['gmDate'] < end_date))].loc[:, ['gmDate', selected_column]]

	# plot the figures (data, layout)
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
