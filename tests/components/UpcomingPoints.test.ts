import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'

import UpcomingPoints from '~/components/UpcomingPoints.vue'

vi.mock('~/data/competition/points-config.json', () => ({
  default: {
    sprints: [
      { name: 'Sprint - Turenne', segment: 3, km: 17, points: [20, 17, 15, 13] },
      { name: 'Sprint - Brive', segment: 1, km: 3, points: [5, 3, 2, 1] },
    ],
    climbs: [
      { name: 'Puy Boubou', segment: 3, km: 19, category: 4, points: [3, 2, 1, 0] },
      { name: 'Suc au May', segment: 15, km: 105, category: 1, points: [10, 8, 6, 4] },
      { name: 'Col HC', segment: 3, km: 21, category: 'HC', points: [20, 15, 10, 5] },
    ],
  },
}))

describe('UpcomingPoints', () => {
  it('renders nothing when next segment has no points', () => {
    const wrapper = mount(UpcomingPoints, { props: { segment: 5 } })
    expect(wrapper.find('div').exists()).toBe(false)
  })

  it('renders sprint points for next segment', () => {
    const wrapper = mount(UpcomingPoints, { props: { segment: 2 } })
    expect(wrapper.text()).toContain('Sprint')
    expect(wrapper.text()).toContain('Sprint - Turenne')
    expect(wrapper.text()).toContain('km 17')
  })

  it('renders climbing points with category formatting', () => {
    const wrapper = mount(UpcomingPoints, { props: { segment: 2 } })
    expect(wrapper.text()).toContain('Cat 4')
    expect(wrapper.text()).toContain('Puy Boubou')
  })

  it('formats HC category correctly', () => {
    const wrapper = mount(UpcomingPoints, { props: { segment: 2 } })
    expect(wrapper.text()).toContain('HC')
    expect(wrapper.text()).toContain('Col HC')
  })

  it('sorts points by km', () => {
    const wrapper = mount(UpcomingPoints, { props: { segment: 2 } })
    const text = wrapper.text()
    const turenne = text.indexOf('Turenne')
    const boubou = text.indexOf('Puy Boubou')
    const hc = text.indexOf('Col HC')
    expect(turenne).toBeLessThan(boubou)
    expect(boubou).toBeLessThan(hc)
  })

  it('filters to next segment only', () => {
    const wrapper = mount(UpcomingPoints, { props: { segment: 2 } })
    expect(wrapper.text()).not.toContain('Suc au May')
    expect(wrapper.text()).not.toContain('Sprint - Brive')
  })

  it('shows points values excluding zeros', () => {
    const wrapper = mount(UpcomingPoints, { props: { segment: 2 } })
    expect(wrapper.text()).toContain('20/17/15/13 pts')
    expect(wrapper.text()).toContain('3/2/1 pts')
  })

  it('shows Coming Up Next heading', () => {
    const wrapper = mount(UpcomingPoints, { props: { segment: 2 } })
    expect(wrapper.text()).toContain('Coming Up Next')
  })
})
