import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import PowerStats from '~/components/PowerStats.vue'

describe('PowerStats', () => {
  const elevationData = {
    summary: {
      avg_gradient: 3.2,
      max_gradient: 8.5,
      avg_climb_gradient: 4.6,
      avg_descent_gradient: -2.1,
      max_climb_gradient: 8.5,
      max_descent_gradient: -5.3,
      elevation_gain: 245,
      elevation_loss: 120,
      avg_power_30kmh: 220,
      avg_power_35kmh: 310,
      avg_power_40kmh: 420,
      avg_power_50kmh: 700,
      estimated_time_30kmh: '14:12',
      estimated_time_35kmh: '12:10',
      estimated_time_40kmh: '10:39',
      estimated_time_50kmh: '8:31',
    },
  }

  it('displays gradient stats', () => {
    const wrapper = mount(PowerStats, { props: { elevationData } })
    expect(wrapper.text()).toContain('4.6')
    expect(wrapper.text()).toContain('8.5')
    expect(wrapper.text()).toContain('-2.1')
    expect(wrapper.text()).toContain('-5.3')
  })

  it('displays elevation gain and loss', () => {
    const wrapper = mount(PowerStats, { props: { elevationData } })
    expect(wrapper.text()).toContain('245')
    expect(wrapper.text()).toContain('120')
  })

  it('displays power at 35km/h', () => {
    const wrapper = mount(PowerStats, { props: { elevationData } })
    expect(wrapper.text()).toContain('310')
  })

  it('displays estimated times', () => {
    const wrapper = mount(PowerStats, { props: { elevationData } })
    expect(wrapper.text()).toContain('14:12')
    expect(wrapper.text()).toContain('12:10')
    expect(wrapper.text()).toContain('10:39')
    expect(wrapper.text()).toContain('8:31')
  })

  it('renders nothing when elevationData is null', () => {
    const wrapper = mount(PowerStats, { props: { elevationData: null } })
    expect(wrapper.text()).toBe('')
  })

  it('shows reference rider spec', () => {
    const wrapper = mount(PowerStats, { props: { elevationData } })
    expect(wrapper.text()).toContain('70kg')
  })
})
