import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'

import StageDetails from '~/components/StageDetails.vue'

vi.mock('~/data/segments.json', () => ({
  default: [
    {
      segment: 1, km_start: 0, km_end: 7.1,
      elevation_gain: 100, elevation_loss: 50,
      towns: ['Malemort', 'Brive-la-Gaillarde'], climbs: [],
      min_elevation: 214, start_lat: 45.13, start_lng: 1.54,
    },
    {
      segment: 2, km_start: 7.1, km_end: 14.2,
      elevation_gain: 200, elevation_loss: 75,
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

  it('shows stage summary derived from segment data', () => {
    const wrapper = mount(StageDetails)
    expect(wrapper.text()).toContain('14 km')
    expect(wrapper.text()).toContain('1 climbs')
    expect(wrapper.text()).toContain('+300m elevation')
  })

  it('shows Towns and Climbs section headers', () => {
    const wrapper = mount(StageDetails)
    expect(wrapper.text()).toContain('Towns')
    expect(wrapper.text()).toContain('Climbs')
  })
})
