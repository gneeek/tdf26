<template>
  <ClientOnly>
    <div ref="mapContainer" class="w-full h-[400px] rounded-lg overflow-hidden shadow-sm" />
    <template #fallback>
      <div class="w-full h-[400px] rounded-lg bg-gray-200 flex items-center justify-center text-gray-500">
        Loading map...
      </div>
    </template>
  </ClientOnly>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  segment: { type: Number, required: true },
  segments: { type: Array, default: () => [] },
  routeCoords: { type: Array, default: () => [] }
})

const mapContainer = ref(null)
let map = null

// Watch for the ref to become available (ClientOnly delays DOM rendering)
watch(mapContainer, async (el) => {
  if (!el || map) return

  const leafletModule = await import('leaflet')
  const L = leafletModule.default || leafletModule

  const segmentData = props.segments.find(s => s.segment === props.segment)
  if (!segmentData) return

  const center = [
    (segmentData.start_lat + segmentData.end_lat) / 2,
    (segmentData.start_lng + segmentData.end_lng) / 2
  ]

  map = L.map(el, {
    scrollWheelZoom: false
  }).setView(center, 12)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 18
  }).addTo(map)

  // Full route in light gray
  if (props.routeCoords.length > 0) {
    const fullRoute = props.routeCoords.map(c => [c[1], c[0]]) // [lng,lat] -> [lat,lng]
    L.polyline(fullRoute, {
      color: '#d1d5db',
      weight: 3,
      opacity: 0.6
    }).addTo(map)
  }

  // Current segment highlighted
  const segStart = segmentData.km_start
  const segEnd = segmentData.km_end
  const segCoords = getSegmentCoords(props.routeCoords, segStart, segEnd)

  if (segCoords.length > 1) {
    const segLine = L.polyline(segCoords.map(c => [c[1], c[0]]), {
      color: '#8B2500',
      weight: 5,
      opacity: 0.9
    }).addTo(map)
    map.fitBounds(segLine.getBounds(), { padding: [30, 30] })
  }

  // Start marker
  const startIcon = L.divIcon({
    html: '<div style="width:12px;height:12px;background:#16a34a;border-radius:50%;border:2px solid white;box-shadow:0 1px 3px rgba(0,0,0,0.3)"></div>',
    className: '',
    iconSize: [16, 16],
    iconAnchor: [8, 8]
  })
  L.marker([segmentData.start_lat, segmentData.start_lng], { icon: startIcon })
    .bindPopup(`<b>Start:</b> Km ${segmentData.km_start}`)
    .addTo(map)

  // End marker
  const endIcon = L.divIcon({
    html: '<div style="width:12px;height:12px;background:#dc2626;border-radius:50%;border:2px solid white;box-shadow:0 1px 3px rgba(0,0,0,0.3)"></div>',
    className: '',
    iconSize: [16, 16],
    iconAnchor: [8, 8]
  })
  L.marker([segmentData.end_lat, segmentData.end_lng], { icon: endIcon })
    .bindPopup(`<b>End:</b> Km ${segmentData.km_end}`)
    .addTo(map)
})

function getSegmentCoords(allCoords, kmStart, kmEnd) {
  if (!allCoords.length) return []

  const coords = []
  let cumDist = 0

  for (let i = 0; i < allCoords.length; i++) {
    if (i > 0) {
      const [lng1, lat1] = [allCoords[i - 1][0], allCoords[i - 1][1]]
      const [lng2, lat2] = [allCoords[i][0], allCoords[i][1]]
      cumDist += haversine(lat1, lng1, lat2, lng2)
    }
    const kmDist = cumDist / 1000
    if (kmDist >= kmStart && kmDist <= kmEnd) {
      coords.push(allCoords[i])
    }
    if (kmDist > kmEnd) break
  }
  return coords
}

function haversine(lat1, lon1, lat2, lon2) {
  const R = 6371000
  const toRad = d => d * Math.PI / 180
  const dLat = toRad(lat2 - lat1)
  const dLon = toRad(lon2 - lon1)
  const a = Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
}
</script>
