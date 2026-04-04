import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ImageGallery from '~/components/ImageGallery.vue'

describe('ImageGallery', () => {
  it('renders images when provided', () => {
    const images = [
      { src: '/img/photo1.jpg', alt: 'Photo one', attribution: 'Author A, CC BY 4.0' },
      { src: '/img/photo2.jpg', alt: 'Photo two', attribution: 'Author B, CC BY-SA 4.0' },
    ]
    const wrapper = mount(ImageGallery, { props: { images } })
    const imgs = wrapper.findAll('img')
    expect(imgs).toHaveLength(2)
    expect(imgs[0].attributes('alt')).toBe('Photo one')
    expect(imgs[1].attributes('alt')).toBe('Photo two')
  })

  it('shows attribution text', () => {
    const images = [
      { src: '/img/test.jpg', alt: 'Test', attribution: 'John Doe, CC BY 4.0' },
    ]
    const wrapper = mount(ImageGallery, { props: { images } })
    expect(wrapper.text()).toContain('John Doe')
  })

  it('renders nothing when images array is empty', () => {
    const wrapper = mount(ImageGallery, { props: { images: [] } })
    expect(wrapper.find('img').exists()).toBe(false)
  })

  it('renders nothing when images prop is missing', () => {
    const wrapper = mount(ImageGallery)
    expect(wrapper.find('img').exists()).toBe(false)
  })

  it('uses lazy loading on images', () => {
    const images = [{ src: '/img/test.jpg', alt: 'Test', attribution: '' }]
    const wrapper = mount(ImageGallery, { props: { images } })
    expect(wrapper.find('img').attributes('loading')).toBe('lazy')
  })

  it('strips HTML from attribution', () => {
    const images = [
      { src: '/img/test.jpg', alt: 'Test', attribution: '<a href="http://example.com">Author</a>' },
    ]
    const wrapper = mount(ImageGallery, { props: { images } })
    const figcaption = wrapper.find('figcaption')
    expect(figcaption.text()).toContain('Author')
  })
})
