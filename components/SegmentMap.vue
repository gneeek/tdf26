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
        class="absolute top-2 right-2 z-[1000] w-8 h-8 flex items-center justify-center rounded border text-lg font-bold cursor-pointer transition-colors shadow"
        :class="isFullscreen ? 'bg-red-600 text-white border-red-600 hover:bg-red-700' : 'bg-white text-stone-600 border-stone-300 hover:bg-stone-100'"
        :title="isFullscreen ? 'Exit fullscreen' : 'Fullscreen'"
        @click="toggleFullscreen"
      >
        {{ isFullscreen ? '✕' : '⛶' }}
      </button>
    </div>
    <template #fallback>
      <div class="w-full h-[400px] rounded-lg bg-stone-200 flex items-center justify-center text-stone-500">
        Loading map...
      </div>
    </template>
  </ClientOnly>
</template>

<script setup>
import { ref, watch, nextTick, onUnmounted } from 'vue'
import 'leaflet/dist/leaflet.css'
import attractionsData from '~/data/attractions.json'
import townsDetailData from '~/data/towns-detail.json'

const props = defineProps({
  segment: { type: Number, required: true },
  segments: { type: Array, default: () => [] },
  routeCoords: { type: Array, default: () => [] },
  townCoords: { type: Object, default: () => ({}) },
  riderStats: { type: Object, default: null },
  riderConfig: { type: Object, default: null }
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

  // Towns and climbs markers overlay using real coordinates
  const poiGroup = L.layerGroup()
  const townCoordsData = props.townCoords || {}
  const placed = new Set()

  for (const seg of props.segments) {
    if (seg.towns?.length) {
      for (const town of seg.towns) {
        if (placed.has(town)) continue
        placed.add(town)
        const coords = townCoordsData[town]
        const lat = coords?.lat || (seg.start_lat + seg.end_lat) / 2
        const lng = coords?.lng || (seg.start_lng + seg.end_lng) / 2
        const townIcon = L.divIcon({
          html: '<div style="font-size:22px;filter:drop-shadow(0 1px 2px rgba(0,0,0,0.4))">🏘️</div>',
          className: '',
          iconSize: [26, 26],
          iconAnchor: [13, 13]
        })
        const detail = townsDetailData.find(t => t.name === town)
        let popupHtml = `<b>${town}</b>`
        if (detail) {
          if (detail.population) popupHtml += `<br><span style="font-size:12px;color:#666">Pop. ${detail.population.toLocaleString()}</span>`
          if (detail.description) popupHtml += `<br><span style="font-size:12px;color:#666">${detail.description}</span>`
        }
        popupHtml += `<br><span style="font-size:11px;color:#8B2500">Segment ${seg.segment} (km ${seg.km_start}-${seg.km_end})</span>`
        L.marker([lat, lng], { icon: townIcon })
          .bindTooltip(town, { direction: 'top', offset: [0, -10] })
          .bindPopup(popupHtml)
          .addTo(poiGroup)
      }
    }
    if (seg.climbs?.length) {
      for (const climb of seg.climbs) {
        if (placed.has(climb)) continue
        placed.add(climb)
        const coords = townCoordsData[climb]
        const lat = coords?.lat || (seg.start_lat + seg.end_lat) / 2
        const lng = coords?.lng || (seg.start_lng + seg.end_lng) / 2
        const climbIcon = L.divIcon({
          html: '<div style="font-size:22px;filter:drop-shadow(0 1px 2px rgba(0,0,0,0.4))">⛰️</div>',
          className: '',
          iconSize: [26, 26],
          iconAnchor: [13, 13]
        })
        L.marker([lat, lng], { icon: climbIcon })
          .bindTooltip(climb, { direction: 'top', offset: [0, -10] })
          .bindPopup(`<b>${climb}</b><br>Segment ${seg.segment}`)
          .addTo(poiGroup)
      }
    }
  }

  // --- Layer control ---
  const baseLayers = {
    'Street': osm,
    'Topographic': topo,
    'Cycling': cyclOSM,
    'Satellite': satellite
  }
  // Rider progress layer
  const riderGroup = L.layerGroup()
  if (props.riderStats?.riders && props.riderConfig?.riders && props.routeCoords.length > 1) {
    // Build cumulative distance lookup from route coords
    const cumDists = [0]
    for (let i = 1; i < props.routeCoords.length; i++) {
      const [lng1, lat1] = [props.routeCoords[i - 1][0], props.routeCoords[i - 1][1]]
      const [lng2, lat2] = [props.routeCoords[i][0], props.routeCoords[i][1]]
      cumDists.push(cumDists[i - 1] + haversine(lat1, lng1, lat2, lng2))
    }
    // Calculate positions and group riders at same distance for offset
    const riderPositions = []
    for (const rider of props.riderConfig.riders) {
      const stats = props.riderStats.riders[rider.id]
      if (!stats || !stats.totalDistanceCapped) continue

      const targetMeters = stats.totalDistanceCapped * 1000
      let coordIdx = 0
      for (let i = 0; i < cumDists.length; i++) {
        if (cumDists[i] >= targetMeters) {
          coordIdx = i
          break
        }
        coordIdx = i
      }
      riderPositions.push({ rider, stats, coordIdx })
    }

    // Group by coordIdx to detect overlaps
    const groups = {}
    for (const rp of riderPositions) {
      const key = rp.coordIdx
      if (!groups[key]) groups[key] = []
      groups[key].push(rp)
    }

    for (const key of Object.keys(groups)) {
      const group = groups[key]
      const coordIdx = parseInt(key)
      const coord = props.routeCoords[coordIdx]

      // Calculate perpendicular direction to route at this point
      const prevIdx = Math.max(0, coordIdx - 1)
      const nextIdx = Math.min(props.routeCoords.length - 1, coordIdx + 1)
      const dx = props.routeCoords[nextIdx][0] - props.routeCoords[prevIdx][0]
      const dy = props.routeCoords[nextIdx][1] - props.routeCoords[prevIdx][1]
      // Perpendicular: rotate 90 degrees
      const len = Math.sqrt(dx * dx + dy * dy) || 1
      const perpLng = -dy / len
      const perpLat = dx / len

      const spread = 0.001 // ~100m offset between riders
      const offset0 = -(group.length - 1) / 2

      for (let i = 0; i < group.length; i++) {
        const { rider, stats: rStats } = group[i]
        const offsetAmount = (offset0 + i) * spread
        const lat = coord[1] + perpLat * offsetAmount
        const lng = coord[0] + perpLng * offsetAmount

        const riderIcon = L.divIcon({
          html: `<div style="font-size:20px;filter:drop-shadow(0 1px 2px rgba(0,0,0,0.4));background:${rider.color};border-radius:50%;width:28px;height:28px;display:flex;align-items:center;justify-content:center;border:2px solid white">🚴</div>`,
          className: '',
          iconSize: [28, 28],
          iconAnchor: [14, 14]
        })
        L.marker([lat, lng], { icon: riderIcon, zIndexOffset: i * 10 })
          .bindTooltip(rider.name, { direction: 'top', offset: [0, -12], permanent: false })
          .bindPopup(`<b style="color:${rider.color}">${rider.name}</b><br>${rStats.totalDistanceCapped} km of ${props.riderConfig.totalDistance} km`)
          .addTo(riderGroup)
      }
    }
  }

  // Attractions layer
  const attractionsGroup = L.layerGroup()
  const categoryEmoji = {
    food: '🍷', cheese: '🧀', market: '🛒', castle: '🏰', church: '⛪', abbey: '⛪',
    museum: '🏛️', nature: '🌿', bridge: '🌉', archaeology: '🏺',
    memorial: '🕯️', industrial: '🏭', craft: '🔨',
  }

  // Filter attractions by proximity to current segment
  for (const poi of attractionsData) {
    // For overview, show all. For segments, show nearby ones.
    if (!isOverview) {
      const seg = props.segments.find(s => s.segment === props.segment)
      if (seg) {
        const midLat = (seg.start_lat + seg.end_lat) / 2
        const midLng = (seg.start_lng + seg.end_lng) / 2
        const dist = Math.sqrt((poi.lat - midLat) ** 2 + (poi.lng - midLng) ** 2)
        if (dist > 0.15) continue // ~15km radius
      }
    }

    const emoji = categoryEmoji[poi.category] || '📍'
    const poiIcon = L.divIcon({
      html: `<div style="font-size:18px;filter:drop-shadow(0 1px 2px rgba(0,0,0,0.3))">${emoji}</div>`,
      className: '',
      iconSize: [22, 22],
      iconAnchor: [11, 11]
    })

    // Find nearest segment for entry link
    let nearestSeg = null
    let nearestDist = Infinity
    for (const seg of props.segments) {
      const midLat = (seg.start_lat + seg.end_lat) / 2
      const midLng = (seg.start_lng + seg.end_lng) / 2
      const d = Math.sqrt((poi.lat - midLat) ** 2 + (poi.lng - midLng) ** 2)
      if (d < nearestDist) { nearestDist = d; nearestSeg = seg }
    }

    let popupHtml = `<b>${poi.name}</b><br><span style="font-size:12px;color:#666">${poi.description}</span>`
    if (nearestSeg) {
      popupHtml += `<br><span style="font-size:11px;color:#8B2500">Segment ${nearestSeg.segment} (km ${nearestSeg.km_start}-${nearestSeg.km_end})</span>`
    }
    if (poi.link) {
      popupHtml += `<br><a href="${poi.link}" target="_blank" rel="noopener" style="font-size:12px">More info</a>`
    }

    L.marker([poi.lat, poi.lng], { icon: poiIcon })
      .bindTooltip(poi.name, { direction: 'top', offset: [0, -8] })
      .bindPopup(popupHtml)
      .addTo(attractionsGroup)
  }

  const overlays = {
    'Cycle Routes': cycleRoutes,
    'Hillshade': hillshade,
    'Towns & Climbs': poiGroup,
    'Attractions': attractionsGroup,
    'Rider Progress': riderGroup
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
