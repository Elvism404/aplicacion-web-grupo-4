from flask import Flask, render_template_string
import folium
import json
import csv

app = Flask(__name__)

@app.route('/')
def index():
    # Diccionarios para riesgo, probabilidad, cantón y provincia
    riesgo_dict = {}
    prob_dict = {}
    canton_dict = {}
    provincia_dict = {}

    # Leer CSV y normalizar parroquia a mayúsculas
    with open("/home/elvism456/PROYECTO_WEB/data/riesgo_parroquias_final.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            parroquia = row["parroquia"].strip().upper()
            riesgo_dict[parroquia] = row["nivel_riesgo"]
            prob_dict[parroquia] = row["prob_riesgo"]
            canton_dict[parroquia] = row["canton"]
            provincia_dict[parroquia] = row["provincia"]

    # Cargar GeoJSON
    with open("/home/elvism456/PROYECTO_WEB/parroquias_normalizadas.geojson", encoding="utf-8") as f:
        geojson_data = json.load(f)

    # Inyectar datos del CSV en las propiedades del GeoJSON
    for feature in geojson_data["features"]:
        parroquia = feature["properties"]["PARROQUIA"].strip().upper()
        feature["properties"]["CANTON"] = canton_dict.get(parroquia, "N/A")
        feature["properties"]["PROVINCIA"] = provincia_dict.get(parroquia, "N/A")
        feature["properties"]["RIESGO"] = riesgo_dict.get(parroquia, "Sin datos")
        feature["properties"]["PROBABILIDAD"] = prob_dict.get(parroquia, "N/A")

    # Crear mapa
    m = folium.Map()

    # Función de estilo según nivel de riesgo
    def style_function(feature):
        nivel = feature['properties']['RIESGO']
        if nivel == "Alto":
            color = "red"
        elif nivel == "Medio":
            color = "orange"
        elif nivel == "Bajo":
            color = "green"
        else:
            color = "gray"
        return {
            'fillColor': color,
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6,
        }

    # Añadir capa GeoJSON con tooltip, popup y highlight (solo borde azul)
    geo_layer = folium.GeoJson(
        geojson_data,
        style_function=style_function,
        highlight_function=lambda feature: {
            'fillColor': style_function(feature)['fillColor'],  # mantiene el color original
            'color': 'blue',   # borde azul
            'weight': 3,
            'fillOpacity': 0.6
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['PARROQUIA', 'CANTON', 'PROVINCIA'],
            aliases=['Parroquia:', 'Cantón:', 'Provincia:'],
            localize=True
        ),
        popup=folium.GeoJsonPopup(
            fields=['RIESGO', 'PROBABILIDAD'],
            aliases=['Riesgo:', 'Probabilidad:'],
            localize=True,
            labels=True,
            style="background-color: white;"
        )
    )
    geo_layer.add_to(m)

    # Ajustar automáticamente el zoom a la extensión del GeoJSON
    m.fit_bounds(geo_layer.get_bounds())

    # Título con fondo sombreado arriba del mapa
    title_html = """
            <div style="
             background-color:#007BFF;  /* azul */
             color:white;               /* texto blanco para contraste */
             text-align:center;
             font-size:20px;
             font-weight:bold;
             padding:10px;
             margin-bottom:10px;
         ">
         Mapa de Riesgo de Inundación por Parroquia - Cantón Guayaquil
         </div>
         """
    m.get_root().html.add_child(folium.Element(title_html))

    # Leyenda debajo de los botones de zoom
    legend_html = """
     <div style="
         position: fixed;
         top: 70px; left: 10px;
         width: 240px; height: 160px;
         border:2px solid grey;
         z-index:9999;
         font-size:14px;
         background-color:white;
         padding:8px;
     ">
     <b style="font-size:15px;">Nivel de Riesgo de Inundación</b><br>
     <span style="background:red; width:25px; height:25px; display:inline-block;"></span> Alto<br>
     <span style="background:orange; width:25px; height:25px; display:inline-block;"></span> Medio<br>
     <span style="background:green; width:25px; height:25px; display:inline-block;"></span> Bajo<br>
     <span style="background:gray; width:25px; height:25px; display:inline-block;"></span> Sin datos
     </div>
     """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Exportar mapa a HTML
    map_html = m._repr_html_()

    return render_template_string("""
    <html>
    <head>
        <title>Mapa de Riesgo</title>
    </head>
    <body>
        {{ map_html|safe }}
    </body>
    </html>
    """, map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)