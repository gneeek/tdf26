interface LightboxImage {
  src: string
  alt?: string
  caption?: string
  author?: string
  authorUrl?: string
  license?: string
  licenseUrl?: string
  sourceUrl?: string
  attribution?: string
}

export function useImageLightbox() {
  const image = useState<LightboxImage | null>('lightbox-image', () => null)
  const siblings = useState<LightboxImage[]>('lightbox-siblings', () => [])
  const currentIndex = useState<number>('lightbox-index', () => -1)

  const isOpen = computed(() => image.value !== null)
  const hasSiblings = computed(() => siblings.value.length > 1)
  const hasPrev = computed(() => hasSiblings.value && currentIndex.value > 0)
  const hasNext = computed(() => hasSiblings.value && currentIndex.value < siblings.value.length - 1)

  function show(payload: LightboxImage, siblingList?: LightboxImage[], index?: number) {
    image.value = payload
    if (siblingList && typeof index === 'number' && index >= 0) {
      siblings.value = siblingList
      currentIndex.value = index
    } else {
      siblings.value = []
      currentIndex.value = -1
    }
  }

  function close() {
    image.value = null
    siblings.value = []
    currentIndex.value = -1
  }

  function next() {
    if (!hasNext.value) return
    currentIndex.value += 1
    image.value = siblings.value[currentIndex.value]
  }

  function prev() {
    if (!hasPrev.value) return
    currentIndex.value -= 1
    image.value = siblings.value[currentIndex.value]
  }

  return { image, siblings, currentIndex, isOpen, hasSiblings, hasPrev, hasNext, show, close, next, prev }
}
