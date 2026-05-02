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
  const isOpen = computed(() => image.value !== null)

  function show(payload: LightboxImage) {
    image.value = payload
  }

  function close() {
    image.value = null
  }

  return { image, isOpen, show, close }
}
