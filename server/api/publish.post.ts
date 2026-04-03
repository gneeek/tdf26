import { execSync } from 'child_process'
import { resolve } from 'path'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { steps = ['stats'] } = body

  const projectDir = resolve('.')
  const venvPython = resolve('processing/.venv/bin/python')
  const logs: string[] = []

  function run(label: string, cmd: string) {
    logs.push(`--- ${label} ---`)
    try {
      const output = execSync(cmd, {
        cwd: projectDir,
        timeout: 60000,
        encoding: 'utf8',
        shell: '/bin/bash'
      })
      if (output.trim()) logs.push(output.trim())
      logs.push(`✓ ${label} complete`)
    } catch (err: any) {
      const stderr = err.stderr ? err.stderr.trim() : ''
      logs.push(stderr || err.message)
      logs.push(`✗ ${label} failed`)
      throw createError({ statusCode: 500, message: `${label} failed`, data: { logs } })
    }
  }

  if (steps.includes('stats')) {
    run('Rider Stats', `${venvPython} processing/rider_stats.py --daily-log data/riders/daily-log.json --rider-config data/riders/rider-config.json --output data/riders/stats.json`)
  }

  if (steps.includes('weather')) {
    const apiKey = process.env.OPENWEATHERMAP_API_KEY
    if (apiKey) {
      run('Weather', `${venvPython} processing/weather.py --entry current --api-key ${apiKey} --segments-json data/segments.json --entries-dir content/entries`)
    } else {
      logs.push('--- Weather ---')
      logs.push('No OPENWEATHERMAP_API_KEY set, skipped')
    }
  }

  logs.push('')
  logs.push('To build and deploy, run from the terminal:')
  logs.push('  ./scripts/publish.sh --skip-deploy   # build only')
  logs.push('  ./scripts/publish.sh                 # build + deploy')

  return { success: true, logs }
})
