# Mapa de Riesgo de Inundación por Parroquia - Cantón Guayaquil

Este proyecto es una aplicación web desarrollada con **Flask** y **Folium** que muestra un mapa interactivo con los niveles de riesgo de inundación por parroquia en el cantón Guayaquil.  

El mapa incluye:
- Tooltip con parroquia, cantón y provincia.
- Popup con nivel de riesgo y probabilidad.
- Colores diferenciados según nivel de riesgo.
- Leyenda explicativa.
- Resaltado en azul del borde de la parroquia al pasar el cursor.
- Título con fondo azul en la parte superior.

---

## Requisitos

- Python 3.9 o superior
- Flask
- Folium

Instalación de dependencias:

```bash
pip install flask folium
```

## Ejecución local
1. Clona este repositorio:
git clone https://github.com/tuusuario/nombre-del-repo.git
cd nombre-del-repo

2. Asegúrate de tener los archivos:
- app.py
- data/riesgo_parroquias_final.csv
- parroquias_normalizadas.geojson

3. Ejecuta la aplicación:
python app.py

4. Abre en tu navegador:
http://127.0.0.1:5000


## Despliegue en PythonAnywhere
- Sube los archivos del proyecto (app.py, data/, geojson) a tu cuenta de PythonAnywhere.
- Configura una Web App con Flask.
- Edita la ruta del archivo principal para que apunte a app.py.
- Recuerda que en el plan gratuito debes entrar al menos una vez al mes y hacer clic en “Run until 1 month from today” para mantener activa la aplicación.


## Emparejamiento entre datos geográficos y predicciones
El proyecto combina dos fuentes de información:
- Datos geográficos (GeoJSON):
Contiene los polígonos de las parroquias con atributos básicos como nombre de parroquia, cantón y provincia.
- Predicciones (CSV):
Incluye las categorías de riesgo de inundación y la probabilidad asociada a cada parroquia.

🔹 Proceso de emparejamiento
- Se normaliza el nombre de la parroquia en ambos archivos (mayúsculas, sin espacios extra).
- Por cada feature del GeoJSON, se busca la parroquia correspondiente en el CSV.
- Se añaden al GeoJSON las propiedades:
- CANTON
- PROVINCIA
- RIESGO (categoría: Alto, Medio, Bajo, Sin datos)
- PROBABILIDAD (valor numérico de la predicción)

🔹 Resultado
- El mapa muestra cada parroquia con un color según su nivel de riesgo.
- Al pasar el cursor, se despliega un tooltip con parroquia, cantón y provincia.
- Al hacer clic, aparece un popup con la predicción de riesgo y la probabilidad.
- De esta forma, los datos geográficos (ubicación y límites de parroquias) quedan vinculados directamente con las predicciones de riesgo de inundación.
  

## Flujo de datos y emparejamiento
CSV (riesgo_parroquias_final.csv)
    └── Contiene nivel de riesgo y probabilidad por parroquia
          ↓
GeoJSON (parroquias_normalizadas.geojson)
    └── Contiene polígonos y nombres de parroquias
          ↓
Emparejamiento en app.py
    └── Se normalizan nombres y se añaden propiedades:
        - Cantón
        - Provincia
        - Riesgo
        - Probabilidad
          ↓
Mapa interactivo (Flask + Folium)
    └── Visualización:
        - Colores según riesgo
        - Tooltip con parroquia, cantón y provincia
        - Popup con riesgo y probabilidad
        - Resaltado azul en borde al pasar el cursor
        - Leyenda y título con fondo azul


## Estructura del proyecto
├── app.py                          # Aplicación principal Flask
├── data/
│   └── riesgo_parroquias_final.csv # Datos de riesgo por parroquia
├── parroquias_normalizadas.geojson # Datos geográficos de parroquias
├── requirements.txt                # Dependencias del proyecto
└── README.md                       # Documentación del proyecto


## Notas
- Los datos de riesgo se cargan desde el archivo CSV y se integran al GeoJSON.
- El mapa ajusta automáticamente el zoom a la zona de estudio.
- Puedes personalizar colores, título y estilo de la leyenda en app.py.



