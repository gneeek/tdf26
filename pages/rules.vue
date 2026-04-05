<template>
  <article class="max-w-3xl mx-auto">
    <header class="mb-8">
      <h1 class="text-4xl font-serif font-semibold text-stone-900 tracking-wide">Competition Rules</h1>
      <p class="text-xl text-stone-500 mt-2 font-serif">How four riders race 185km from home</p>
    </header>

    <div class="prose md:prose-lg max-w-none font-serif">
      <h2>The Race</h2>
      <p>
        Four riders - Justin, Marian, Nan, and Wally - are each cycling the 185km Stage 9 route
        from Malemort to Ussel. Not on the road in France, but on their bikes at home, logging
        daily kilometres from April through July 2026.
      </p>
      <p>
        Every kilometre they ride at home moves them a little further along the route. The rider
        who covers the full 185km first wins. But there's a catch.
      </p>

      <h2>The Daily Cap</h2>
      <p>
        Each day, a maximum of <strong>2 kilometres</strong> counts toward your progress on the route.
        Ride 20km on a Saturday? Only 2km are credited. This keeps the race tight and rewards
        consistency over single big efforts.
      </p>
      <p>
        But unused cap rolls over. If you don't ride on Monday, Tuesday's cap becomes 4km. Take three
        days off and you have 8km of cap to burn. The carry-over rewards riders who bank rest days and
        then put in a big effort.
      </p>

      <h2>The Jerseys</h2>
      <div class="not-prose grid grid-cols-1 sm:grid-cols-2 gap-4 my-6">
        <div class="bg-white rounded-lg shadow-sm p-4 border-l-4 border-yellow-400">
          <div class="flex items-center gap-2 mb-2">
            <JerseyIcon type="yellow" size="md" />
            <span class="font-bold text-stone-800">Yellow Jersey</span>
          </div>
          <p class="text-sm text-stone-600">Race leader. Highest total capped distance. Tiebreaker: highest actual distance ridden.</p>
        </div>
        <div class="bg-white rounded-lg shadow-sm p-4 border-l-4 border-green-500">
          <div class="flex items-center gap-2 mb-2">
            <JerseyIcon type="green" size="md" />
            <span class="font-bold text-stone-800">Green Jersey</span>
          </div>
          <p class="text-sm text-stone-600">Sprint leader. Most sprint points accumulated at intermediate sprint locations along the route.</p>
        </div>
        <div class="bg-white rounded-lg shadow-sm p-4 border-l-4 border-red-500">
          <div class="flex items-center gap-2 mb-2">
            <JerseyIcon type="polkaDot" size="md" />
            <span class="font-bold text-stone-800">Polka Dot Jersey</span>
          </div>
          <p class="text-sm text-stone-600">Climbing leader. Most climbing points earned at the summits of the route's categorized climbs.</p>
        </div>
        <div class="bg-white rounded-lg shadow-sm p-4 border-l-4 border-red-800">
          <div class="flex items-center gap-2 mb-2">
            <JerseyIcon type="red" size="md" />
            <span class="font-bold text-stone-800">Lanterne Rouge</span>
          </div>
          <p class="text-sm text-stone-600">Last place by capped distance. In Tour tradition, a badge of honour - the rider who refuses to abandon.</p>
        </div>
      </div>

      <h2>Sprint Points</h2>
      <p>
        Five intermediate sprints are placed along the route, mostly in flat or rolling terrain near towns.
        When a rider's cumulative progress passes a sprint location, they "contest" the sprint.
        The first rider to reach each sprint gets the most points, with decreasing points for 2nd, 3rd, and 4th.
      </p>
      <div class="overflow-x-auto">
      <table>
        <thead>
          <tr>
            <th>Location</th>
            <th>Km</th>
            <th>1st</th>
            <th>2nd</th>
            <th>3rd</th>
            <th>4th</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sprint in sprints" :key="sprint.name">
            <td>{{ sprint.name }}</td>
            <td>{{ sprint.km }}</td>
            <td>{{ sprint.points[0] }}</td>
            <td>{{ sprint.points[1] }}</td>
            <td>{{ sprint.points[2] }}</td>
            <td>{{ sprint.points[3] }}</td>
          </tr>
        </tbody>
      </table>
      </div>

      <h2>Climbing Points</h2>
      <p>
        Ten categorized climbs dot the route, from the gentle Cote de Malemort near the start to the
        fearsome Suc au May at 7.7%. Higher-category climbs award more points. The first rider over
        each summit claims the biggest prize.
      </p>
      <div class="overflow-x-auto">
      <table>
        <thead>
          <tr>
            <th>Climb</th>
            <th>Km</th>
            <th>Cat</th>
            <th>1st</th>
            <th>2nd</th>
            <th>3rd</th>
            <th>4th</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="climb in climbs" :key="climb.name">
            <td>{{ climb.name }}</td>
            <td>{{ climb.km }}</td>
            <td>{{ climb.category }}</td>
            <td>{{ climb.points[0] }}</td>
            <td>{{ climb.points[1] }}</td>
            <td>{{ climb.points[2] || '-' }}</td>
            <td>{{ climb.points[3] || '-' }}</td>
          </tr>
        </tbody>
      </table>
      </div>

      <h2>Tiebreaking</h2>
      <p>
        When two or more riders reach a point location on the same day, ties are broken randomly.
        For the yellow jersey, ties in capped distance are broken by total actual distance ridden.
      </p>

      <h2>Timing</h2>
      <p>
        Rider distances are logged daily from the start of publication (April 2026) through to the
        stage race day on Sunday, July 12. Standings are updated with each blog entry, published
        twice weekly on Sundays and Wednesdays.
      </p>
    </div>
  </article>
</template>

<script setup>
import pointsConfig from '~/data/competition/points-config.json'

const sprints = pointsConfig.sprints
const climbs = pointsConfig.climbs
</script>
