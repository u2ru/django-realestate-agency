document.addEventListener('DOMContentLoaded', function () {
  const mapContainer = document.getElementById('map-admin')
  if (!mapContainer) {
    console.error('Map container not found')
    return
  }

  // Find the hidden input by looking for the closest coordinates-widget div
  const widgetContainer = mapContainer.closest('.coordinates-widget')
  if (!widgetContainer) {
    console.error('Coordinates widget container not found')
    return
  }

  const coordinatesInput = widgetContainer.querySelector('input[type="hidden"]')
  if (!coordinatesInput) {
    console.error('Coordinates input not found')
    return
  }

  const coordinatesDisplay = document.getElementById('coordinates-display')
  if (!coordinatesDisplay) {
    console.error('Coordinates display element not found')
    return
  }

  console.log('All elements found, initializing map...')

  // Initialize map
  mapboxgl.accessToken =
    'pk.eyJ1IjoibHVrYWRhdGFjeSIsImEiOiJjbWFtZWs5c3EwZzV5MnBzNGVzdXk0cXNiIn0.tfUSq0hYimUnpRBZCHvJKg'
  const map = new mapboxgl.Map({
    container: 'map-admin',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [41.636237224128195, 41.65211072506244],
    zoom: 14,
    interactive: true,
  })

  // Initialize marker
  let marker = null

  // Wait for the map to load before adding events
  map.on('load', function () {
    console.log('Map loaded')

    // Set initial coordinates if they exist
    if (coordinatesInput.value) {
      try {
        const coords = JSON.parse(coordinatesInput.value)
        if (coords.lat && coords.lng) {
          map.setCenter([coords.lng, coords.lat])
          addMarker(coords.lng, coords.lat)
          updateCoordinatesDisplay(coords.lng, coords.lat)
        }
      } catch (e) {
        console.error('Error parsing coordinates:', e)
      }
    }

    // Add click event to map
    map.on('click', function (e) {
      console.log('Map clicked:', e.lngLat)
      const coordinates = e.lngLat
      addMarker(coordinates.lng, coordinates.lat)
      updateCoordinates(coordinates.lng, coordinates.lat)
    })

    // Add drag end event to marker
    map.on('dragend', function (e) {
      console.log('Map dragged:', e.lngLat)
      const coordinates = e.lngLat
      addMarker(coordinates.lng, coordinates.lat)
      updateCoordinates(coordinates.lng, coordinates.lat)
    })
  })

  function addMarker(lng, lat) {
    if (marker) {
      marker.remove()
    }
    marker = new mapboxgl.Marker({
      draggable: true,
    })
      .setLngLat([lng, lat])
      .addTo(map)

    // Add drag end event to marker
    marker.on('dragend', function () {
      const coordinates = marker.getLngLat()
      console.log('Marker dragged:', coordinates)
      updateCoordinates(coordinates.lng, coordinates.lat)
    })
  }

  function updateCoordinates(lng, lat) {
    const coordinates = {
      lng: lng,
      lat: lat,
    }
    coordinatesInput.value = JSON.stringify(coordinates)
    updateCoordinatesDisplay(lng, lat)
  }

  function updateCoordinatesDisplay(lng, lat) {
    coordinatesDisplay.textContent = `Selected coordinates: ${lat.toFixed(
      6
    )}, ${lng.toFixed(6)}`
  }
})
