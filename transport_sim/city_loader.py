import osmnx as ox
import folium
import numpy as np

tram_coords_lookup = {
    "Bournemouth Pier": (50.7167, -1.8760),
    "Boscombe": (50.7261, -1.8417),
    "Winton": (50.7360, -1.8813),
    "Lansdowne": (50.7236, -1.8641),
    "Southbourne": (50.7220, -1.8160),
    "Poole Station": (50.7174, -1.9835),
    "Parkstone": (50.7232, -1.9500),
    "Canford Cliffs": (50.7122, -1.9256),
    "Hamworthy": (50.7146, -2.0055),
    "Central Station": (50.9078, -1.4137),
    "Portswood": (50.9300, -1.3881),
    "Highfield": (50.9361, -1.3974),
    "Woolston": (50.8992, -1.3783),
    "Ocean Village": (50.8953, -1.3882)
}

def add_tramline_to_map(m, start_name, end_name):
    if start_name in tram_coords_lookup and end_name in tram_coords_lookup:
        coords = [tram_coords_lookup[start_name], tram_coords_lookup[end_name]]
        folium.PolyLine(coords, color="red", weight=4).add_to(m)
        folium.Marker(coords[0], tooltip="Start", icon=folium.Icon(color="green")).add_to(m)
        folium.Marker(coords[1], tooltip="End", icon=folium.Icon(color="blue")).add_to(m)

def load_city(city_name="Bournemouth, UK"):
    # Step 1: Download and simplify graph
    G = ox.graph_from_place(city_name, network_type="walk", simplify=True)

    # Step 2: Project it to ensure lat/lon are assigned properly
    G_proj = ox.project_graph(G, to_crs="EPSG:4326")

    # Step 3: Convert to undirected *after* projection
    G_undirected = G_proj.to_undirected()

    # Step 4: Ensure all nodes have x/y (some nodes get stripped during simplification)
    for node, data in G_undirected.nodes(data=True):
        if "x" not in data or "y" not in data:
            geom = data.get("geometry", None)
            if geom:
                data["x"] = geom.x
                data["y"] = geom.y

    return G_undirected

def get_hub_node(G, location_name="Bournemouth Station"):
    coords = ox.geocoder.geocode(location_name)
    node = ox.distance.nearest_nodes(G, coords[1], coords[0])
    return node

# def export_access_map(G, hub_node, access_distances, out_path, tramline_nodes=None):
#     import numpy as np
#     import folium
#
#     # Get graph centroid for initial map position
#     xs = [data["x"] for _, data in G.nodes(data=True) if "x" in data]
#     ys = [data["y"] for _, data in G.nodes(data=True) if "y" in data]
#     m = folium.Map(location=[np.mean(ys), np.mean(xs)], zoom_start=13)
#
#     # Add legend manually using a FloatImage or HTML overlay
#     legend_html = '''
#      <div style="position: fixed;
#                  bottom: 30px; left: 30px; width: 200px; height: 110px;
#                  background-color: white; z-index:9999; font-size:14px;
#                  border:2px solid grey; padding: 10px;">
#      <b>Legend</b><br>
#      ● <span style="color:blue">Agent (active)</span><br>
#      ● <span style="color:red">Hub Station</span><br>
#      <hr style="margin: 5px 0">
#      <span style="border-left: 4px dashed orange; padding-left: 5px;">Tramline</span>
#      </div>
#      '''
#     m.get_root().html.add_child(folium.Element(legend_html))
#
#     # Add agent points with distance popup
#     for node, dist in access_distances.items():
#         if node in G:
#             x, y = G.nodes[node]["x"], G.nodes[node]["y"]
#             folium.CircleMarker(
#                 location=[y, x],
#                 radius=5,
#                 color="blue",
#                 fill=True,
#                 fill_opacity=0.7,
#                 popup=f"Distance: {dist:.1f} m",
#             ).add_to(m)
#
#     # Add hub marker
#     hub_x, hub_y = G.nodes[hub_node]["x"], G.nodes[hub_node]["y"]
#     folium.Marker(
#         location=[hub_y, hub_x],
#         icon=folium.Icon(color="red", icon="train", prefix="fa"),
#         popup="Hub",
#     ).add_to(m)
#
#     # Optional tramline overlay
#     if tramline_nodes:
#         n1, n2 = tramline_nodes
#         if n1 in G and n2 in G:
#             x1, y1 = G.nodes[n1]["x"], G.nodes[n1]["y"]
#             x2, y2 = G.nodes[n2]["x"], G.nodes[n2]["y"]
#
#             folium.PolyLine(
#                 [(y1, x1), (y2, x2)],
#                 color="orange",
#                 weight=4,
#                 dash_array="5, 5",
#                 tooltip="🚋 Proposed Tramline",
#             ).add_to(m)
#
#     m.save(out_path)

def export_access_map(G, hub, distances, out_path, tramline_nodes=None, tramline_names=None):
    import folium
    from folium.plugins import MarkerCluster

    m = folium.Map(location=[50.72, -1.88], zoom_start=13)
    mc = MarkerCluster().add_to(m)

    for node, dist in distances.items():
        x, y = G.nodes[node]["x"], G.nodes[node]["y"]
        folium.CircleMarker(location=[y, x], radius=4,
                            color="blue", fill=True, fill_opacity=0.6,
                            popup=f"Node {node}, Dist: {dist:.0f}m").add_to(mc)

    # Add tramline by name
    if tramline_names:
        from city_loader import add_tramline_to_map
        add_tramline_to_map(m, tramline_names[0], tramline_names[1])

    m.save(out_path)




