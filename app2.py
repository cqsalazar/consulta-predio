import os
import folium
import sqlite3
import pandas as pd
import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap
from shapely import wkt
from shapely.geometry import Point

st.set_page_config(page_title='Consulta de Predios', layout='centered', page_icon="🔍")
st.subheader("Consulta Predial", divider='gray')

crs = 'EPSG:4326'
data_folder = 'data'

m = leafmap.Map(
    center=[3.4248559, -76.5188715],
    zoom=12,
    zoom_control=True,
    draw_control=False,
    scale_control=False,
    layers_control=True,
    fullscreen_control=False,
    measure_control=False,
    toolbar_control=False
)


@st.cache_data
def load_data(option, input):
   conexion1 = sqlite3.connect('Terrenos_Part1.db')
   conexion2 = sqlite3.connect('Terrenos_Part2.db')
   query1 = f"SELECT * FROM Terrenos_28032025_Part1_spatial WHERE {option} = '{input}'"
   query2 = f"SELECT * FROM Terrenos_28032025_Part2_spatial WHERE {option} = '{input}'"
   df1 = pd.read_sql_query(query1, conexion1)
   df1['geometry'] = df1['geometry'].apply(wkt.loads)
   df2 = pd.read_sql_query(query2, conexion2)
   df2['geometry'] = df2['geometry'].apply(wkt.loads)
   if df1.shape[0] > 0:
       gdf = gpd.GeoDataFrame(df1, geometry='geometry', crs='4326')
   elif df2.shape[0] > 0:
       gdf = gpd.GeoDataFrame(df2, geometry='geometry', crs='4326')
   conexion1.close()
   conexion2.close()
   return gdf


#    conexion = sqlite3.connect('consulta_predios.db')
#    query = f"SELECT * FROM Terrenos_28032025_spatial WHERE {option} = '{input}'"
#    df = pd.read_sql_query(query, conexion)
#    df['geometry'] = df['geometry'].apply(wkt.loads)
#    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs='4326')
#    conexion.close()
#    return gdf

# Cargue de información alfanumérica
@st.cache_data
def load_table(option, input):
    conexion = sqlite3.connect('export_alfanumerica.db')
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM export_predio_09032025 WHERE {option} = '{input}'")
    data = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    df = pd.DataFrame(data, columns=columns)
    gdf = gpd.GeoDataFrame(df)
    conexion.close()
    return gdf

m_streamlit = m.to_streamlit(800, 600)
