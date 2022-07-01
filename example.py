import json

import matplotlib.pyplot as plt

import gm_plotting

# Create API client using key from environment variable
client = gm_plotting.APIClient()

# Plot some example coordinates
with open('example_gps_coords.json', 'r') as f:
    gps_coords = json.load(f)

# We have to convert the GPS coordinates to Mercator coordinates
mlat, mlon = gm_plotting.gps_to_merc(gps_coords['lat'], gps_coords['lon'])
plt.plot(mlon, mlat)

# Add the background
client.add_satellite_image_background(plt.gca())

plt.show()
