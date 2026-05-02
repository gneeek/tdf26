import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { ref, computed } from 'vue'
import ImageLightbox from '~/components/ImageLightbox.vue'

const lightboxImage = ref<any>(null)
const closeSpy = vi.fn(() => { lightboxImage.value = null })
const isOpen = computed(() => lightboxImage.value !== null)

vi.mock('~/composables/useImageLightbox', () => ({
  useImageLightbox: () => ({
    image: lightboxImage,
    isOpen,
    show: (img: any) => { lightboxImage.value = img },
    close: closeSpy,
  }),
}))

describe('ImageLightbox', () => {
  beforeEach(() => {
    lightboxImage.value = null
    closeSpy.mockClear()
  })

  it('renders nothing when no image is open', () => {
    const wrapper = mount(ImageLightbox)
    expect(wrapper.find('[role="dialog"]').exists()).toBe(false)
  })

  it('renders the image and attribution when open', async () => {
    lightboxImage.value = {
      src: '/img/x.jpg',
      alt: 'Test',
      caption: 'A caption',
      author: 'Jane',
      license: 'CC BY 4.0',
    }
    const wrapper = mount(ImageLightbox)
    await wrapper.vm.$nextTick()
    expect(wrapper.find('[role="dialog"]').exists()).toBe(true)
    expect(wrapper.find('img').attributes('src')).toBe('/img/x.jpg')
    expect(wrapper.text()).toContain('A caption')
    expect(wrapper.text()).toContain('Jane')
    expect(wrapper.text()).toContain('CC BY 4.0')
  })

  it('closes when the close button is clicked', async () => {
    lightboxImage.value = { src: '/img/x.jpg', alt: 'X' }
    const wrapper = mount(ImageLightbox)
    await wrapper.vm.$nextTick()
    await wrapper.find('button[aria-label="Close image viewer"]').trigger('click')
    expect(closeSpy).toHaveBeenCalledTimes(1)
  })

  it('closes when the backdrop is clicked', async () => {
    lightboxImage.value = { src: '/img/x.jpg', alt: 'X' }
    const wrapper = mount(ImageLightbox)
    await wrapper.vm.$nextTick()
    await wrapper.find('[role="dialog"]').trigger('click.self')
    expect(closeSpy).toHaveBeenCalledTimes(1)
  })

  it('closes on Escape keydown', async () => {
    lightboxImage.value = { src: '/img/x.jpg', alt: 'X' }
    const wrapper = mount(ImageLightbox, { attachTo: document.body })
    await wrapper.vm.$nextTick()
    window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }))
    await wrapper.vm.$nextTick()
    expect(closeSpy).toHaveBeenCalledTimes(1)
    wrapper.unmount()
  })

  it('does not close on non-Escape keydown', async () => {
    lightboxImage.value = { src: '/img/x.jpg', alt: 'X' }
    const wrapper = mount(ImageLightbox, { attachTo: document.body })
    await wrapper.vm.$nextTick()
    window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter' }))
    await wrapper.vm.$nextTick()
    expect(closeSpy).not.toHaveBeenCalled()
    wrapper.unmount()
  })
})
