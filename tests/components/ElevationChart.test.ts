import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'

import ElevationChart from '~/components/ElevationChart.vue'

// Mock Chart.js and vue-chartjs to avoid canvas rendering
vi.mock('vue-chartjs', () => ({
  Line: { template: '<canvas data-testid="chart" />', props: ['data', 'options', 'plugins'] },
}))

vi.mock('chart.js', () => ({
  Chart: { register: vi.fn() },
  CategoryScale: {},
  LinearScale: {},
  LineElement: {},
  PointElement: {},
  Filler: {},
  Tooltip: {},
}))

vi.mock('chartjs-plugin-zoom', () => ({ default: {} }))

const elevationData = {
  distance: [0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
  elevation: [200, 220, 250, 240, 260, 280, 270, 290],
  gradient: [0, 1.8, 2.7, -0.9, 1.8, 1.8, -0.9, 1.8],
  power_35kmh: [280, 300, 320, 260, 300, 300, 260, 300],
  summary: {
    avg_gradient: 2.5,
    max_gradient: 7.3,
    elevation_gain: 144,
    elevation_loss: 32,
  },
}

describe('ElevationChart', () => {
  it('renders chart when data is provided', () => {
    const wrapper = mount(ElevationChart, {
      props: { elevationData, segments: [], currentSegment: 1 },
    })
    expect(wrapper.find('[data-testid="chart"]').exists()).toBe(true)
  })

  it('shows placeholder when no data', () => {
    const wrapper = mount(ElevationChart, {
      props: { elevationData: null, segments: [], currentSegment: 1 },
    })
    expect(wrapper.find('[data-testid="chart"]').exists()).toBe(false)
    expect(wrapper.text()).toContain('Elevation')
  })

  it('has fullscreen toggle button', () => {
    const wrapper = mount(ElevationChart, {
      props: { elevationData, segments: [], currentSegment: 1 },
    })
    const buttons = wrapper.findAll('button')
    expect(buttons.length).toBeGreaterThan(0)
  })
})
