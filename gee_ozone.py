import ee

# Authenticate once if not done already:
# ee.Authenticate()
ee.Initialize()

# Use the correct dataset
dataset = ee.ImageCollection('TOMS/MERGED') \
            .filterDate('2005-01-01', '2005-01-03')

ozone = dataset.select('ozone')

# Print some basic info
print('Number of images:', dataset.size().getInfo())
print('Band names:', ozone.first().bandNames().getInfo())

