from dash import Dash, html
from dash.dependencies import Input, Output
import dash_leaflet as dl
import geopandas as gpd
import json

mexico_shape=gpd.read_parquet('data/mexico_shape.parquet')
estados_shape=gpd.read_parquet('data/estados_shape.parquet')
municipios_shape=gpd.read_parquet('data/municipios_shape.parquet')

tile_url='https://stamen-tiles-{s}.a.ssl.fastly.net/toner-background/{z}/{x}/{y}{r}.png'

app=Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1(children='MEXICO TREEMAP'),
        html.Div([
            dl.Map(children=[
                dl.TileLayer(url=tile_url),
                dl.GeoJSON(
                    click_feature=None,
                    zoomToBoundsOnClick=False,
                    id='shapes'),
                html.Button('↩', id='btn', n_clicks=0, className='btn')],
                id='map',
                center=[23.634501, -102.552784],
                zoom=5,
                zoomControl=False,
                doubleClickZoom=False,
                dragging=False,
                scrollWheelZoom=False,
                preferCanvas=True)],
            id='map_div', className='map_div')],
        className='main_div')],
    className='container')

@app.callback(Output('shapes', 'data'),
              Output('shapes', 'zoomToBoundsOnClick'),
              Input('shapes', 'click_feature'))
def shape_clicked(feature):
    if feature is not None:
        if feature['properties']['SHP_TYPE']==0:
            return json.loads(estados_shape.to_json()), True
        else:
            return json.loads(municipios_shape[municipios_shape['CVEGEO']==feature['properties']['CVEGEO']].to_json()), True
    else:
        return json.loads(mexico_shape.to_json()), False

@app.callback(
    Output('shapes', 'click_feature'),
    Output('map', 'center'),
    Output('map', 'zoom'),
    Input('btn', 'n_clicks'))
def displayClick(btn):
    return None, [23.634501, -102.552784], 5

if __name__ == '__main__':
    app.run_server(debug=True)                   