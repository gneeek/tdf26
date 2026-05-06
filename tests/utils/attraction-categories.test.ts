import { describe, it, expect } from 'vitest'

import attractionsData from '~/data/attractions.json'
import { CATEGORY_EMOJI } from '~/utils/attractions'

// Drift detector. CATEGORY_EMOJI must cover every category declared in
// attractions.json. The same drift had already happened twice before #474:
// 'geology' and 'heritage' POIs were added to attractions.json without
// updating the three component-side categoryEmoji maps, so those POIs fell
// through to the 📍 fallback. Failing here means a new attraction category
// has landed without an emoji entry — either add the entry or change the
// POI's category.
describe('CATEGORY_EMOJI vs attractions.json categories', () => {
  const declared = new Set<string>(attractionsData.map(p => p.category))

  it('contains every category declared in attractions.json', () => {
    for (const category of declared) {
      expect(CATEGORY_EMOJI[category], `missing emoji for category "${category}"`).toBeDefined()
    }
  })
})
