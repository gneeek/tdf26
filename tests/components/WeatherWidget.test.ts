import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import WeatherWidget from '~/components/WeatherWidget.vue'

describe('WeatherWidget', () => {
  const weather = {
    fetchedAt: '2026-04-04',
    current: {
      temp: 18,
      conditions: 'Partly cloudy',
      wind: '12 km/h SW',
    },
    forecast: 'Warm and dry through the weekend',
  }

  it('renders weather data', () => {
    const wrapper = mount(WeatherWidget, { props: { weather } })
    expect(wrapper.text()).toContain('18')
    expect(wrapper.text()).toContain('°C')
    expect(wrapper.text()).toContain('Partly cloudy')
    expect(wrapper.text()).toContain('12 km/h SW')
  })

  it('shows forecast when present', () => {
    const wrapper = mount(WeatherWidget, { props: { weather } })
    expect(wrapper.text()).toContain('Warm and dry through the weekend')
  })

  it('renders nothing when weather is null', () => {
    const wrapper = mount(WeatherWidget, { props: { weather: null } })
    expect(wrapper.text()).toBe('')
  })

  it('renders nothing when weather prop is missing', () => {
    const wrapper = mount(WeatherWidget)
    expect(wrapper.text()).toBe('')
  })

  it('handles weather without forecast', () => {
    const noForecast = { ...weather, forecast: null }
    const wrapper = mount(WeatherWidget, { props: { weather: noForecast } })
    expect(wrapper.text()).toContain('18')
    expect(wrapper.text()).not.toContain('Warm and dry')
  })

  it('shows fetchedAt date', () => {
    const wrapper = mount(WeatherWidget, { props: { weather } })
    expect(wrapper.text()).toContain('April 4, 2026')
  })
})
