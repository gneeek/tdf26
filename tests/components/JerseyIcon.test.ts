import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import JerseyIcon from '~/components/JerseyIcon.vue'

describe('JerseyIcon', () => {
  it('renders yellow jersey with correct fill and stroke', () => {
    const wrapper = mount(JerseyIcon, { props: { type: 'yellow' } })
    const path = wrapper.find('path')
    expect(path.attributes('fill')).toBe('#FFD100')
    expect(path.attributes('stroke')).toBe('#B8960A')
  })

  it('renders green jersey with correct fill and stroke', () => {
    const wrapper = mount(JerseyIcon, { props: { type: 'green' } })
    const path = wrapper.find('path')
    expect(path.attributes('fill')).toBe('#22C55E')
    expect(path.attributes('stroke')).toBe('#16A34A')
  })

  it('renders polka dot jersey with white fill and red stroke', () => {
    const wrapper = mount(JerseyIcon, { props: { type: 'polkaDot' } })
    const path = wrapper.find('path')
    expect(path.attributes('fill')).toBe('white')
    expect(path.attributes('stroke')).toBe('#DC2626')
  })

  it('renders red jersey with correct fill and stroke', () => {
    const wrapper = mount(JerseyIcon, { props: { type: 'red' } })
    const path = wrapper.find('path')
    expect(path.attributes('fill')).toBe('#DC2626')
    expect(path.attributes('stroke')).toBe('#991B1B')
  })

  it('renders polka dots only for polkaDot type', () => {
    const polka = mount(JerseyIcon, { props: { type: 'polkaDot' } })
    expect(polka.findAll('circle').length).toBe(5)

    const yellow = mount(JerseyIcon, { props: { type: 'yellow' } })
    expect(yellow.findAll('circle').length).toBe(0)
  })

  it('uses fallback fill and stroke for unknown type', () => {
    const wrapper = mount(JerseyIcon, { props: { type: 'unknown' } })
    const path = wrapper.find('path')
    expect(path.attributes('fill')).toBe('#999')
    expect(path.attributes('stroke')).toBe('#666')
  })

  it('defaults to sm size class', () => {
    const wrapper = mount(JerseyIcon, { props: { type: 'yellow' } })
    const svg = wrapper.find('svg')
    expect(svg.classes()).toContain('w-5')
    expect(svg.classes()).toContain('h-5')
  })

  it('applies xs size class', () => {
    const wrapper = mount(JerseyIcon, { props: { type: 'yellow', size: 'xs' } })
    const svg = wrapper.find('svg')
    expect(svg.classes()).toContain('w-4')
    expect(svg.classes()).toContain('h-4')
  })

  it('applies lg size class', () => {
    const wrapper = mount(JerseyIcon, { props: { type: 'yellow', size: 'lg' } })
    const svg = wrapper.find('svg')
    expect(svg.classes()).toContain('w-8')
    expect(svg.classes()).toContain('h-8')
  })

  it('sets title attribute on svg', () => {
    const wrapper = mount(JerseyIcon, { props: { type: 'yellow', title: 'Race leader' } })
    expect(wrapper.find('svg').attributes('title')).toBe('Race leader')
  })
})
