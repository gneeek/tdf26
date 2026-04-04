import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'

import StageDetails from '~/components/StageDetails.vue'

vi.mock('~/data/segments.json', () => ({
  default: [
    {
      segment: 1, km_start: 0, km_end: 7.1,
      towns: ['Malemort', 'Brive-la-Gaillarde'], climbs: [],
      min_elevation: 214, start_lat: 45.13, start_lng: 1.54,
    },
    {
      segment: 2, km_start: 7.1, km_end: 14.2,
      towns: [], climbs: ['Puy Boubou'],
      min_elevation: 172, start_lat: 45.08, start_lng: 1.56,
    },
  ],
}))

describe('StageDetails', () => {
  it('renders towns', () => {
    const wrapper = mount(StageDetails)
    expect(wrapper.text()).toContain('Malemort')
    expect(wrapper.text()).toContain('Brive-la-Gaillarde')
  })

  it('renders climbs', () => {
    const wrapper = mount(StageDetails)
    expect(wrapper.text()).toContain('Puy Boubou')
  })

  it('shows stage summary', () => {
    const wrapper = mount(StageDetails)
    expect(wrapper.text()).toContain('185 km')
    expect(wrapper.text()).toContain('9 climbs')
  })

  it('shows Towns and Climbs section headers', () => {
    const wrapper = mount(StageDetails)
    expect(wrapper.text()).toContain('Towns')
    expect(wrapper.text()).toContain('Climbs')
  })
})
