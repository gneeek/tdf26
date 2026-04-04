import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'

import PublishSchedule from '~/components/PublishSchedule.vue'

vi.mock('~/data/segments.json', () => ({
  default: [
    { segment: 1, towns: ['Malemort'], climbs: [] },
    { segment: 2, towns: [], climbs: [] },
  ],
}))

describe('PublishSchedule', () => {
  it('renders schedule title', () => {
    const wrapper = mount(PublishSchedule)
    expect(wrapper.text()).toContain('Publish Schedule')
  })

  it('shows segment numbers', () => {
    const wrapper = mount(PublishSchedule)
    expect(wrapper.text()).toContain('1')
    expect(wrapper.text()).toContain('2')
  })

  it('generates publish dates', () => {
    const wrapper = mount(PublishSchedule)
    // First entry should be April 5
    expect(wrapper.text()).toContain('Apr')
  })
})
