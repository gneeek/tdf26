import { readFileSync } from 'fs'
import { resolve } from 'path'

export default defineEventHandler(() => {
  const logPath = resolve('data/riders/daily-log.json')
  const configPath = resolve('data/riders/rider-config.json')
  const statsPath = resolve('data/riders/stats.json')

  const log = JSON.parse(readFileSync(logPath, 'utf8'))
  const config = JSON.parse(readFileSync(configPath, 'utf8'))

  let stats = { riders: {} }
  try {
    stats = JSON.parse(readFileSync(statsPath, 'utf8'))
  } catch {}

  return { log, config, stats }
})
