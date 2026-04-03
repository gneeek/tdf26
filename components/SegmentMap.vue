<template>
  <ClientOnly>
    <div
      class="relative rounded-lg overflow-hidden shadow-sm"
      :class="isFullscreen ? 'z-50 rounded-none' : ''"
      :style="isFullscreen ? 'position:fixed;top:0;left:0;width:100vw;height:100vh' : ''"
    >
      <div
        ref="mapContainer"
        :style="isFullscreen ? 'width:100%;height:100%' : 'width:100%;height:400px'"
      />
      <button
        @click="toggleFullscreen"
        class="absolute top-2 right-2 z-[1000] w-8 h-8 flex items-center justify-center rounded border text-lg font-bold cursor-pointer transition-colors shadow"
        :class="isFullscreen ? 'bg-red-600 text-white border-red-600 hover:bg-red-700' : 'bg-white text-gray-600 border-gray-300 hover:bg-gray-100'"
        :title="isFullscreen ? 'Exit fullscreen' : 'Fullscreen'"
      >
        {{ isFullscreen ? '✕' : '⛶' }}
      </button>
    </div>
    <template #fallback>
      <div class="w-full h-[400px] rounded-lg bg-gray-200 flex items-center justify-center text-gray-500">
        Loading map...
      </div>
    </template>
  </ClientOnly>
</template>

<script setup>
import { ref, watch, nextTick, onUnmounted } from 'vue'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  segment: { type: Number, required: true },
  segments: { type: Array, default: () => [] },
  routeCoords: { type: Array, default: () => [] }
})

const mapContainer = ref(null)
const isFullscreen = ref(false)
let map = null
let mapInitialized = false

function resizeMap() {
  nextTick(() => {
    setTimeout(() => { if (map) map.invalidateSize() }, 100)
  })
}

function toggleFullscreen() {
  isFullscreen.value = !isFullscreen.value
  resizeMap()
}

function onKeydown(e) {
  if (e.key === 'Escape' && isFullscreen.value) {
    isFullscreen.value = false
    resizeMap()
  }
}

if (typeof window !== 'undefined') {
  window.addEventListener('keydown', onKeydown)
  onUnmounted(() => window.removeEventListener('keydown', onKeydown))
}

async function initMap(el) {
  if (mapInitialized || !el) return
  mapInitialized = true

  const leafletModule = await import('leaflet')
  const L = leafletModule.default || leafletModule

  const segmentData = props.segments.find(s => s.segment === props.segment)
  const isOverview = props.segment === 0

  if (!segmentData && !isOverview) return

  const center = segmentData
    ? [(segmentData.start_lat + segmentData.end_lat) / 2, (segmentData.start_lng + segmentData.end_lng) / 2]
    : [45.35, 1.85]

  map = L.map(el, {
    scrollWheelZoom: false
  }).setView(center, isOverview ? 10 : 12)

  // --- Base layers ---
  const osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 18
  })

  const topo = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
    maxZoom: 17
  })

  const cyclOSM = L.tileLayer('https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.cyclosm.org">CyclOSM</a> &amp; OSM contributors',
    maxZoom: 18
  })

  const satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: '&copy; Esri, Maxar, Earthstar Geographics',
    maxZoom: 18
  })

  // Default base layer
  osm.addTo(map)

  // --- Overlay layers ---
  const cycleRoutes = L.tileLayer('https://tile.waymarkedtrails.org/cycling/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://waymarkedtrails.org">Waymarked Trails</a>',
    maxZoom: 18,
    opacity: 0.7
  })

  const hillshade = L.tileLayer('https://tiles.wmflabs.org/hillshading/{z}/{x}/{y}.png', {
    attribution: 'Hillshade &copy; SRTM',
    maxZoom: 17,
    opacity: 0.4
  })

  // Towns and climbs markers overlay
  const poiGroup = L.layerGroup()
  const allSegments = props.segments
  for (const seg of allSegments) {
    // Town markers
    if (seg.towns?.length) {
      const midLat = (seg.start_lat + seg.end_lat) / 2
      const midLng = (seg.start_lng + seg.end_lng) / 2
      const townIcon = L.divIcon({
        html: '<div style="width:8px;height:8px;background:#2563eb;border-radius:50%;border:1px solid white;box-shadow:0 1px 2px rgba(0,0,0,0.3)"></div>',
        className: '',
        iconSize: [10, 10],
        iconAnchor: [5, 5]
      })
      L.marker([midLat, midLng], { icon: townIcon })
        .bindPopup(`<b>${seg.towns.join(', ')}</b><br>Segment ${seg.segment}`)
        .addTo(poiGroup)
    }
    // Climb markers
    if (seg.climbs?.length) {
      const midLat = (seg.start_lat + seg.end_lat) / 2
      const midLng = (seg.start_lng + seg.end_lng) / 2
      const climbIcon = L.divIcon({
        html: '<div style="width:0;height:0;border-left:6px solid transparent;border-right:6px solid transparent;border-bottom:10px solid #dc2626;filter:drop-shadow(0 1px 1px rgba(0,0,0,0.3))"></div>',
        className: '',
        iconSize: [12, 10],
        iconAnchor: [6, 10]
      })
      L.marker([midLat, midLng], { icon: climbIcon })
        .bindPopup(`<b>${seg.climbs.join(', ')}</b><br>Segment ${seg.segment}`)
        .addTo(poiGroup)
    }
  }

  // --- Layer control ---
  const baseLayers = {
    'Street': osm,
    'Topographic': topo,
    'Cycling': cyclOSM,
    'Satellite': satellite
  }
  const overlays = {
    'Cycle Routes': cycleRoutes,
    'Hillshade': hillshade,
    'Towns & Climbs': poiGroup
  }
  L.control.layers(baseLayers, overlays, { position: 'topleft' }).addTo(map)

  // Full route
  if (props.routeCoords.length > 0) {
    const fullRoute = props.routeCoords.map(c => [c[1], c[0]])
    const routeLine = L.polyline(fullRoute, {
      color: isOverview ? '#8B2500' : '#d1d5db',
      weight: isOverview ? 4 : 3,
      opacity: isOverview ? 0.9 : 0.6
    }).addTo(map)

    if (isOverview) {
      map.fitBounds(routeLine.getBounds(), { padding: [30, 30] })

      const first = props.segments[0]
      const last = props.segments[props.segments.length - 1]
      if (first) {
        L.marker([first.start_lat, first.start_lng], {
          icon: L.divIcon({
            html: '<div style="background:#16a34a;color:white;font-size:10px;font-weight:bold;padding:2px 6px;border-radius:4px;white-space:nowrap;box-shadow:0 1px 3px rgba(0,0,0,0.3)">Malemort</div>',
            className: '', iconAnchor: [0, 12]
          })
        }).addTo(map)
      }
      if (last) {
        L.marker([last.end_lat, last.end_lng], {
          icon: L.divIcon({
            html: '<div style="background:#dc2626;color:white;font-size:10px;font-weight:bold;padding:2px 6px;border-radius:4px;white-space:nowrap;box-shadow:0 1px 3px rgba(0,0,0,0.3)">Ussel</div>',
            className: '', iconAnchor: [0, 12]
          })
        }).addTo(map)
      }
    }
  }

  // Current segment highlighted (not in overview mode)
  if (!isOverview && segmentData) {
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

    const startIcon = L.divIcon({
      html: '<div style="width:12px;height:12px;background:#16a34a;border-radius:50%;border:2px solid white;box-shadow:0 1px 3px rgba(0,0,0,0.3)"></div>',
      className: '', iconSize: [16, 16], iconAnchor: [8, 8]
    })
    L.marker([segmentData.start_lat, segmentData.start_lng], { icon: startIcon })
      .bindPopup(`<b>Start:</b> Km ${segmentData.km_start}`)
      .addTo(map)

    const endIcon = L.divIcon({
      html: '<div style="width:12px;height:12px;background:#dc2626;border-radius:50%;border:2px solid white;box-shadow:0 1px 3px rgba(0,0,0,0.3)"></div>',
      className: '', iconSize: [16, 16], iconAnchor: [8, 8]
    })
    L.marker([segmentData.end_lat, segmentData.end_lng], { icon: endIcon })
      .bindPopup(`<b>End:</b> Km ${segmentData.km_end}`)
      .addTo(map)
  }
}

// Watch for the ref to become available (ClientOnly delays DOM rendering)
watch(mapContainer, (el) => {
  if (el) initMap(el)
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
