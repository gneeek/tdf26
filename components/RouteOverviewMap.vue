<template>
  <ClientOnly>
    <div
      ref="mapContainer"
      style="width:100%;height:500px"
      class="rounded-lg overflow-hidden shadow-sm"
    />
    <template #fallback>
      <div class="w-full h-[500px] rounded-lg bg-gray-200 flex items-center justify-center text-gray-500">
        Loading map...
      </div>
    </template>
  </ClientOnly>
</template>

<script setup>
import { ref, watch } from 'vue'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  segments: { type: Array, default: () => [] },
  routeCoords: { type: Array, default: () => [] },
  publishedSegments: { type: Array, default: () => [] }
})

const mapContainer = ref(null)
let mapInitialized = false

watch(mapContainer, async (el) => {
  if (!el || mapInitialized) return
  mapInitialized = true

  const leafletModule = await import('leaflet')
  const L = leafletModule.default || leafletModule

  const map = L.map(el, { scrollWheelZoom: false }).setView([45.35, 1.85], 10)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 18
  }).addTo(map)

  if (props.routeCoords.length < 2) return

  // Draw each segment, colored by published status
  const publishedSet = new Set(props.publishedSegments)
  let cumDist = 0
  let segIdx = 0
  let segCoords = []
  const segBounds = []

  for (let i = 0; i < props.routeCoords.length; i++) {
    if (i > 0) {
      const [lng1, lat1] = [props.routeCoords[i - 1][0], props.routeCoords[i - 1][1]]
      const [lng2, lat2] = [props.routeCoords[i][0], props.routeCoords[i][1]]
      cumDist += haversine(lat1, lng1, lat2, lng2)
    }

    const seg = props.segments[segIdx]
    if (!seg) break

    const kmDist = cumDist / 1000
    segCoords.push([props.routeCoords[i][1], props.routeCoords[i][0]])

    if (kmDist >= seg.km_end || i === props.routeCoords.length - 1) {
      const isPublished = publishedSet.has(seg.segment)
      const line = L.polyline(segCoords, {
        color: isPublished ? '#8B2500' : '#d1d5db',
        weight: isPublished ? 4 : 3,
        opacity: isPublished ? 0.9 : 0.5
      }).addTo(map)

      if (isPublished) {
        const title = seg.towns?.length ? seg.towns[0] : `Segment ${seg.segment}`
        line.bindPopup(`<b>Segment ${seg.segment}</b><br>${title}<br>Km ${seg.km_start}-${seg.km_end}`)
      }

      segBounds.push(...segCoords)
      segCoords = [segCoords[segCoords.length - 1]]
      segIdx++
    }
  }

  // Fit to route bounds
  if (segBounds.length > 1) {
    map.fitBounds(L.latLngBounds(segBounds), { padding: [20, 20] })
  }

  // Start and end markers
  const first = props.segments[0]
  const last = props.segments[props.segments.length - 1]
  if (first && last) {
    L.marker([first.start_lat, first.start_lng], {
      icon: L.divIcon({
        html: '<div style="background:#16a34a;color:white;font-size:10px;font-weight:bold;padding:2px 6px;border-radius:4px;white-space:nowrap;box-shadow:0 1px 3px rgba(0,0,0,0.3)">Malemort</div>',
        className: '',
        iconAnchor: [0, 12]
      })
    }).addTo(map)

    L.marker([last.end_lat, last.end_lng], {
      icon: L.divIcon({
        html: '<div style="background:#dc2626;color:white;font-size:10px;font-weight:bold;padding:2px 6px;border-radius:4px;white-space:nowrap;box-shadow:0 1px 3px rgba(0,0,0,0.3)">Ussel</div>',
        className: '',
        iconAnchor: [0, 12]
      })
    }).addTo(map)
  }
})

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
