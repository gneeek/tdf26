<template>
  <div class="p-4 bg-amber-100 rounded-lg text-sm text-stone-700">
    <p class="font-semibold text-stone-800 mb-2">The Race</p>
    <p>
      Four riders are virtually cycling from the comfort of their homes. Starting in April,
      each logs daily kilometres from their own rides, and we track their progress along the
      185km Stage 9 parcours. Each day, up to 2km counts toward their position on the route -
      but unused cap rolls over, rewarding rest days followed by big efforts. Four jerseys are
      contested:
      <JerseyIcon type="yellow" size="xs" class="inline-block mx-0.5" /> yellow for the race leader,
      <JerseyIcon type="green" size="xs" class="inline-block mx-0.5" /> green for sprint points,
      <JerseyIcon type="polkaDot" size="xs" class="inline-block mx-0.5" /> polka dot for climbing points,
      and the
      <JerseyIcon type="red" size="xs" class="inline-block mx-0.5" /> lanterne rouge for last place.
    </p>
    <NuxtLink to="/rules" class="inline-block mt-2 text-correze-red hover:underline font-medium">
      Full competition rules
    </NuxtLink>
  </div>
</template>
