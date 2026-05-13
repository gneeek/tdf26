---
segment: 99
title: "Unbalanced MDC fixture"
publishDate: 2000-01-01
images: []
imagesOptional: true
draft: false
---

# Unbalanced fixture

This entry opens an MDC block and never closes it. Nuxt Content would render
the remainder of the entry as block content, producing a broken page.

::inline-figure{src="/img/a.jpg" alt="A" author="Test" license="CC BY-SA 4.0"}

The next paragraph is intended as body text, not as MDC content, but no `::`
ever closes the block above.
