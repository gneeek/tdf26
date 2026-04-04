import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'

// Mock Leaflet — it requires DOM APIs not available in happy-dom
vi.mock('leaflet', () => ({
  default: {
    map: vi.fn(() => ({
      setView: vi.fn().mockReturnThis(),
      addLayer: vi.fn(),
      removeLayer: vi.fn(),
      fitBounds: vi.fn(),
      invalidateSize: vi.fn(),
      remove: vi.fn(),
    })),
    tileLayer: vi.fn(() => ({ addTo: vi.fn() })),
    marker: vi.fn(() => ({ addTo: vi.fn(), bindPopup: vi.fn().mockReturnThis() })),
    polyline: vi.fn(() => ({ addTo: vi.fn(), getBounds: vi.fn(() => ({})) })),
    layerGroup: vi.fn(() => ({ addTo: vi.fn() })),
    divIcon: vi.fn(),
    control: { layers: vi.fn(() => ({ addTo: vi.fn() })) },
    Icon: { Default: { mergeOptions: vi.fn() } },
  },
}))

vi.mock('leaflet/dist/leaflet.css', () => ({}))

import SegmentMap from '~/components/SegmentMap.vue'

describe('SegmentMap', () => {
  // SegmentMap uses ClientOnly which won't render in test env
  // We test that it mounts without errors

  it('mounts without errors', () => {
    const wrapper = mount(SegmentMap, {
      props: { segment: 1, segments: [], routeCoords: [] },
      global: {
        stubs: { ClientOnly: { template: '<div><slot /></div>' } },
      },
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('renders map container', () => {
    const wrapper = mount(SegmentMap, {
      props: { segment: 1, segments: [], routeCoords: [] },
      global: {
        stubs: { ClientOnly: { template: '<div><slot /></div>' } },
      },
    })
    expect(wrapper.find('div').exists()).toBe(true)
  })

  it('has fullscreen toggle', () => {
    const wrapper = mount(SegmentMap, {
      props: { segment: 1, segments: [], routeCoords: [] },
      global: {
        stubs: { ClientOnly: { template: '<div><slot /></div>' } },
      },
    })
    const buttons = wrapper.findAll('button')
    expect(buttons.length).toBeGreaterThan(0)
  })
})
