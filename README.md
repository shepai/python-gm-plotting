# Google Maps plotting
This is a simple library for setting the background of a plot (e.g. of GPS
coordinates) to be a satellite image. An example of how to use the library is
[here](example.py).

## Set up
In order to use this library you need a Google API key (see instructions
[here](https://developers.google.com/maps/documentation/javascript/get-api-key)).

Once you have your API key, you can use it by setting the environment variable
``GOOGLE_MAPS_API_KEY`` to whatever its value is. Alternatively, you can just
pass the key to the ``APIClient`` constructor, though remember never to commit
private API keys to a public Git repo!
