import { readFileSync, writeFileSync } from 'fs'
import { resolve } from 'path'
import { execSync } from 'child_process'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { date, distances } = body

  if (!date || !distances) {
    throw createError({ statusCode: 400, message: 'Missing date or distances' })
  }

  const logPath = resolve('data/riders/daily-log.json')
  const configPath = resolve('data/riders/rider-config.json')
  const statsPath = resolve('data/riders/stats.json')

  // Read current log
  const log = JSON.parse(readFileSync(logPath, 'utf8'))

  // Remove existing entry for this date if it exists
  log.entries = log.entries.filter((e: any) => e.date !== date)

  // Add new entry
  log.entries.push({ date, distances })
  log.entries.sort((a: any, b: any) => a.date.localeCompare(b.date))

  // Write updated log
  writeFileSync(logPath, JSON.stringify(log, null, 2))

  // Regenerate stats
  try {
    const venvPython = resolve('processing/.venv/bin/python')
    const statsScript = resolve('processing/rider_stats.py')
    execSync(`${venvPython} ${statsScript} --daily-log ${logPath} --rider-config ${configPath} --output ${statsPath}`)
  } catch (err: any) {
    console.error('Stats regeneration failed:', err.message)
  }

  // Read and return updated stats
  const stats = JSON.parse(readFileSync(statsPath, 'utf8'))
  return { success: true, stats }
})
