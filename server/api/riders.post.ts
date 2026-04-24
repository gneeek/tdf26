import { readFileSync, writeFileSync } from 'fs'
import { resolve } from 'path'
import { execSync } from 'child_process'

function runPython(scriptPath: string, args: string[]) {
  const venvPython = resolve('processing/.venv/bin/python')
  const cmd = [venvPython, scriptPath, ...args].map(s => JSON.stringify(s)).join(' ')
  try {
    execSync(cmd, { stdio: ['ignore', 'pipe', 'pipe'] })
  } catch (err: unknown) {
    const e = err as { stderr?: Buffer | string; message?: string }
    const stderr = e.stderr ? e.stderr.toString().trim() : ''
    const scriptName = scriptPath.split('/').pop() ?? scriptPath
    throw createError({
      statusCode: 500,
      message: `${scriptName} failed: ${stderr || e.message || 'unknown error'}`,
    })
  }
}

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { date, distances } = body

  if (!date || !distances) {
    throw createError({ statusCode: 400, message: 'Missing date or distances' })
  }

  const logPath = resolve('data/riders/daily-log.json')
  const configPath = resolve('data/riders/rider-config.json')
  const statsPath = resolve('data/riders/stats.json')
  const pointsConfigPath = resolve('data/competition/points-config.json')
  const pointsPath = resolve('data/riders/points.json')

  const log = JSON.parse(readFileSync(logPath, 'utf8'))
  log.entries = log.entries.filter((e: { date: string }) => e.date !== date)
  log.entries.push({ date, distances })
  log.entries.sort((a: { date: string }, b: { date: string }) => a.date.localeCompare(b.date))
  writeFileSync(logPath, JSON.stringify(log, null, 2))

  runPython(resolve('processing/rider_stats.py'), [
    '--daily-log', logPath,
    '--rider-config', configPath,
    '--output', statsPath,
  ])
  runPython(resolve('processing/calculate_points.py'), [
    '--daily-log', logPath,
    '--rider-config', configPath,
    '--points-config', pointsConfigPath,
    '--output', pointsPath,
  ])

  const stats = JSON.parse(readFileSync(statsPath, 'utf8'))
  return { success: true, stats }
})
