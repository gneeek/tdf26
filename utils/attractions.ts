// Single source of truth for the category-to-emoji mapping used by the
// nearby-attractions UI. Three components previously kept their own copies
// (NearbyAttractions.vue, SegmentMap.vue, pages/admin/images.vue) and drifted:
// 'geology' and 'heritage' POIs in attractions.json fell through to the 📍
// fallback because the maps had not been updated when those categories were
// introduced. tests/utils/attraction-categories.test.ts asserts every category
// declared in data/attractions.json has an entry here.
export const CATEGORY_EMOJI: Record<string, string> = {
  abbey: '⛪',
  archaeology: '🏺',
  bridge: '🌉',
  castle: '🏰',
  cheese: '🧀',
  church: '⛪',
  craft: '🔨',
  food: '🍷',
  geology: '🪨',
  heritage: '⚜️',
  industrial: '🏭',
  market: '🛒',
  memorial: '🕯️',
  museum: '🏛️',
  nature: '🌿',
}

export const FALLBACK_EMOJI = '📍'

export function emojiFor(category: string): string {
  return CATEGORY_EMOJI[category] ?? FALLBACK_EMOJI
}
