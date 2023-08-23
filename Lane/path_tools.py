import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString, Point
import osmnx  as ox
import networkx as nx
import matplotlib.pyplot as plt
import shapely.geometry
import geopandas as gpd
import time
import taxicab as tc

def get_shortest_route(orgnm, olon, olat, dstnm, dlon, dlat, G):
    routenm = orgnm+' -- '+dstnm
    print(routenm)
    origin = gpd.GeoDataFrame(columns = ['name', 'geometry'], crs = 4326, geometry = 'geometry')
    origin.at[0, 'geometry'] = Point(olon, olat)
    origin.at[0, 'name'] = orgnm
    destination = gpd.GeoDataFrame(columns = ['name', 'geometry'], crs = 4326, geometry = 'geometry')
    destination.at[0, 'geometry'] = Point(dlon, dlat)
    destination.at[0, 'name'] = dstnm
    
    origin_node_id = ox.nearest_nodes(G, origin.geometry.x, origin.geometry.y)
    destination_node_id = ox.nearest_nodes(G, destination.geometry.x, destination.geometry.y)
    
    route = ox.shortest_path(G, origin_node_id, destination_node_id)
    r = route[0]
    if r is None:
        orig = (olat, olon)
        dest = (dlat, dlon)
        route = tc.distance.shortest_path(G, orig, dest)
        r = route[1]

    nodes, edges = ox.graph_to_gdfs(G)
    route_nodes = nodes.loc[r]
    
    route_line = shapely.geometry.LineString(list(route_nodes.geometry.values))
    route_geom = gpd.GeoDataFrame({
        "geometry": [route_line],
        "osm_nodes": [r],
    })
    gdf=route_geom.set_crs(edges.crs, allow_override=True)
    
    gdf=gdf.to_crs(epsg=2914)
    gdf["length_km"] = gdf.length*0.3048/1000
    gdf["start"] = orgnm
    gdf["end"] = dstnm
    gdf["route"] = routenm
    
    return r, route_line, gdf