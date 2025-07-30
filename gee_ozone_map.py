import ee
import geemap
import ipywidgets as widgets

# Initialize Earth Engine
ee.Initialize()

# Create Map
Map = geemap.Map(center=[20, 0], zoom=2)

# Define continents with geometry (example polygons simplified)
continents = {
    'Africa': ee.Geometry.Polygon([
        [[-17.7, 37.1], [51.2, 37.1], [51.2, -35.1], [-17.7, -35.1], [-17.7, 37.1]]
    ]),
    'Asia': ee.Geometry.Polygon([
        [[26.0, 81.0], [169.0, 81.0], [169.0, -11.0], [26.0, -11.0], [26.0, 81.0]]
    ]),
    # Add other continents similarly...
}

# Load ozone dataset (make sure this dataset is accessible)
dataset = ee.ImageCollection('NASA/OMI/Aura_O3_Daily').select('O3_column_number_density')

def add_continent_layer(cont_name, geom):
    # Filter the dataset by date or keep as is
    ozone_image = dataset.mean()  # Average over all time for demo

    # Calculate mean ozone over the continent
    mean_dict = ozone_image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geom,
        scale=10000,
        maxPixels=1e9
    )
    mean_val = mean_dict.get('O3_column_number_density').getInfo()

    # Get centroid coordinates for marker
    center = geom.centroid().coordinates().getInfo()

    # Add the continent polygon
    Map.addLayer(geom, {}, cont_name)

    # Create popup widget with HTML
    popup_widget = widgets.HTML(f"<b>{cont_name}</b><br>Avg Ozone: {mean_val:.7f} mol/m²")

    # Add marker with popup widget
    Map.add_marker(location=[center[1], center[0]], popup=popup_widget, icon_color='blue')

# Add each continent
for name, geometry in continents.items():
    add_continent_layer(name, geometry)

# Show map
Map

