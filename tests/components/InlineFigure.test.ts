import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import InlineFigure from '~/components/content/InlineFigure.vue'

const showSpy = vi.fn()
vi.mock('~/composables/useImageLightbox', () => ({
  useImageLightbox: () => ({ show: showSpy, close: vi.fn(), image: { value: null }, isOpen: { value: false } }),
}))

describe('InlineFigure', () => {
  beforeEach(() => {
    showSpy.mockClear()
  })

  it('renders the image with src and alt', () => {
    const wrapper = mount(InlineFigure, { props: { src: '/img/x.jpg', alt: 'X' } })
    const img = wrapper.find('img')
    expect(img.attributes('src')).toBe('/img/x.jpg')
    expect(img.attributes('alt')).toBe('X')
    expect(img.attributes('loading')).toBe('lazy')
  })

  it('renders caption and attribution', () => {
    const wrapper = mount(InlineFigure, {
      props: {
        src: '/img/x.jpg',
        alt: 'X',
        caption: 'A nice caption',
        author: 'Jane',
        license: 'CC BY 4.0',
      },
    })
    expect(wrapper.text()).toContain('A nice caption')
    expect(wrapper.text()).toContain('Jane')
    expect(wrapper.text()).toContain('CC BY 4.0')
  })

  it('does not wrap the image in a target="_blank" anchor', () => {
    const wrapper = mount(InlineFigure, { props: { src: '/img/x.jpg', alt: 'X' } })
    const imgWrapper = wrapper.find('img').element.parentElement
    expect(imgWrapper?.tagName).not.toBe('A')
    expect(imgWrapper?.getAttribute('target')).toBeNull()
  })

  it('opens the lightbox with the full image payload on click', async () => {
    const wrapper = mount(InlineFigure, {
      props: {
        src: '/img/x.jpg',
        alt: 'X',
        caption: 'cap',
        author: 'Jane',
        authorUrl: 'https://example.com/jane',
        license: 'CC BY 4.0',
        licenseUrl: 'https://creativecommons.org/licenses/by/4.0',
        sourceUrl: 'https://example.com/source',
      },
    })
    await wrapper.find('button').trigger('click')
    expect(showSpy).toHaveBeenCalledTimes(1)
    expect(showSpy).toHaveBeenCalledWith({
      src: '/img/x.jpg',
      alt: 'X',
      caption: 'cap',
      author: 'Jane',
      authorUrl: 'https://example.com/jane',
      license: 'CC BY 4.0',
      licenseUrl: 'https://creativecommons.org/licenses/by/4.0',
      sourceUrl: 'https://example.com/source',
    })
  })
})
