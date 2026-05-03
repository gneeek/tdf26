import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount, enableAutoUnmount } from '@vue/test-utils'
import { ref, computed } from 'vue'
import ImageLightbox from '~/components/ImageLightbox.vue'

enableAutoUnmount(afterEach)

const lightboxImage = ref<any>(null)
const siblings = ref<any[]>([])
const currentIndex = ref<number>(-1)
const closeSpy = vi.fn(() => { lightboxImage.value = null; siblings.value = []; currentIndex.value = -1 })
const nextSpy = vi.fn(() => {
  if (currentIndex.value < siblings.value.length - 1) {
    currentIndex.value += 1
    lightboxImage.value = siblings.value[currentIndex.value]
  }
})
const prevSpy = vi.fn(() => {
  if (currentIndex.value > 0) {
    currentIndex.value -= 1
    lightboxImage.value = siblings.value[currentIndex.value]
  }
})
const isOpen = computed(() => lightboxImage.value !== null)
const hasSiblings = computed(() => siblings.value.length > 1)
const hasPrev = computed(() => hasSiblings.value && currentIndex.value > 0)
const hasNext = computed(() => hasSiblings.value && currentIndex.value < siblings.value.length - 1)

vi.mock('~/composables/useImageLightbox', () => ({
  useImageLightbox: () => ({
    image: lightboxImage,
    siblings,
    currentIndex,
    isOpen,
    hasSiblings,
    hasPrev,
    hasNext,
    show: (img: any, list?: any[], idx?: number) => {
      lightboxImage.value = img
      if (list && typeof idx === 'number') {
        siblings.value = list
        currentIndex.value = idx
      } else {
        siblings.value = []
        currentIndex.value = -1
      }
    },
    close: closeSpy,
    next: nextSpy,
    prev: prevSpy,
  }),
}))

const A = { src: '/img/a.jpg', alt: 'A' }
const B = { src: '/img/b.jpg', alt: 'B' }
const C = { src: '/img/c.jpg', alt: 'C' }

describe('ImageLightbox', () => {
  beforeEach(() => {
    lightboxImage.value = null
    siblings.value = []
    currentIndex.value = -1
    closeSpy.mockClear()
    nextSpy.mockClear()
    prevSpy.mockClear()
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
  })

  it('does not close on non-Escape keydown', async () => {
    lightboxImage.value = { src: '/img/x.jpg', alt: 'X' }
    const wrapper = mount(ImageLightbox, { attachTo: document.body })
    await wrapper.vm.$nextTick()
    window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter' }))
    await wrapper.vm.$nextTick()
    expect(closeSpy).not.toHaveBeenCalled()
  })

  it('shows prev and next buttons when there are siblings', async () => {
    lightboxImage.value = A
    siblings.value = [A, B, C]
    currentIndex.value = 1
    const wrapper = mount(ImageLightbox)
    await wrapper.vm.$nextTick()
    expect(wrapper.find('button[aria-label="Previous image"]').exists()).toBe(true)
    expect(wrapper.find('button[aria-label="Next image"]').exists()).toBe(true)
  })

  it('hides prev and next buttons when there are no siblings', async () => {
    lightboxImage.value = A
    siblings.value = []
    currentIndex.value = -1
    const wrapper = mount(ImageLightbox)
    await wrapper.vm.$nextTick()
    expect(wrapper.find('button[aria-label="Previous image"]').exists()).toBe(false)
    expect(wrapper.find('button[aria-label="Next image"]').exists()).toBe(false)
  })

  it('disables prev button at the first image', async () => {
    lightboxImage.value = A
    siblings.value = [A, B, C]
    currentIndex.value = 0
    const wrapper = mount(ImageLightbox)
    await wrapper.vm.$nextTick()
    expect(wrapper.find('button[aria-label="Previous image"]').attributes('disabled')).toBeDefined()
    expect(wrapper.find('button[aria-label="Next image"]').attributes('disabled')).toBeUndefined()
  })

  it('disables next button at the last image', async () => {
    lightboxImage.value = C
    siblings.value = [A, B, C]
    currentIndex.value = 2
    const wrapper = mount(ImageLightbox)
    await wrapper.vm.$nextTick()
    expect(wrapper.find('button[aria-label="Previous image"]').attributes('disabled')).toBeUndefined()
    expect(wrapper.find('button[aria-label="Next image"]').attributes('disabled')).toBeDefined()
  })

  it('calls next() when next button is clicked', async () => {
    lightboxImage.value = A
    siblings.value = [A, B, C]
    currentIndex.value = 0
    const wrapper = mount(ImageLightbox)
    await wrapper.vm.$nextTick()
    await wrapper.find('button[aria-label="Next image"]').trigger('click')
    expect(nextSpy).toHaveBeenCalledTimes(1)
  })

  it('calls prev() when prev button is clicked', async () => {
    lightboxImage.value = B
    siblings.value = [A, B, C]
    currentIndex.value = 1
    const wrapper = mount(ImageLightbox)
    await wrapper.vm.$nextTick()
    await wrapper.find('button[aria-label="Previous image"]').trigger('click')
    expect(prevSpy).toHaveBeenCalledTimes(1)
  })

  it('navigates to the next image on ArrowRight keydown', async () => {
    lightboxImage.value = A
    siblings.value = [A, B, C]
    currentIndex.value = 0
    const wrapper = mount(ImageLightbox, { attachTo: document.body })
    await wrapper.vm.$nextTick()
    window.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight' }))
    await wrapper.vm.$nextTick()
    expect(nextSpy).toHaveBeenCalledTimes(1)
  })

  it('navigates to the previous image on ArrowLeft keydown', async () => {
    lightboxImage.value = B
    siblings.value = [A, B, C]
    currentIndex.value = 1
    const wrapper = mount(ImageLightbox, { attachTo: document.body })
    await wrapper.vm.$nextTick()
    window.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowLeft' }))
    await wrapper.vm.$nextTick()
    expect(prevSpy).toHaveBeenCalledTimes(1)
  })

  it('does not navigate past the end on ArrowRight at the last image', async () => {
    lightboxImage.value = C
    siblings.value = [A, B, C]
    currentIndex.value = 2
    const wrapper = mount(ImageLightbox, { attachTo: document.body })
    await wrapper.vm.$nextTick()
    window.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight' }))
    await wrapper.vm.$nextTick()
    expect(nextSpy).not.toHaveBeenCalled()
  })

  it('does not navigate before the start on ArrowLeft at the first image', async () => {
    lightboxImage.value = A
    siblings.value = [A, B, C]
    currentIndex.value = 0
    const wrapper = mount(ImageLightbox, { attachTo: document.body })
    await wrapper.vm.$nextTick()
    window.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowLeft' }))
    await wrapper.vm.$nextTick()
    expect(prevSpy).not.toHaveBeenCalled()
  })

  it('shows position indicator when there are siblings', async () => {
    lightboxImage.value = B
    siblings.value = [A, B, C]
    currentIndex.value = 1
    const wrapper = mount(ImageLightbox)
    await wrapper.vm.$nextTick()
    expect(wrapper.text()).toContain('2 / 3')
  })

  it('does not show position indicator with no siblings', async () => {
    lightboxImage.value = { src: '/img/x.jpg', alt: 'X' }
    siblings.value = []
    currentIndex.value = -1
    const wrapper = mount(ImageLightbox)
    await wrapper.vm.$nextTick()
    expect(wrapper.text()).not.toContain('/ 0')
    expect(wrapper.text()).not.toMatch(/\d+ \/ \d+/)
  })
})
