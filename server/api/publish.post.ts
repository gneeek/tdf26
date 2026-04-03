import { execSync } from 'child_process'
import { resolve } from 'path'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { skipDeploy = true, dryRun = false } = body

  const projectDir = resolve('.')
  const venvPython = resolve('processing/.venv/bin/python')
  const logs: string[] = []

  function run(label: string, cmd: string) {
    logs.push(`--- ${label} ---`)
    try {
      const output = execSync(cmd, {
        cwd: projectDir,
        timeout: 120000,
        encoding: 'utf8',
        env: { ...process.env, PATH: process.env.PATH }
      })
      logs.push(output.trim())
      logs.push(`✓ ${label} complete`)
    } catch (err: any) {
      logs.push(`✗ ${label} failed: ${err.message}`)
      throw createError({ statusCode: 500, message: `${label} failed`, data: { logs } })
    }
  }

  // Step 1: Rider stats
  run('Rider Stats', `${venvPython} processing/rider_stats.py --daily-log data/riders/daily-log.json --rider-config data/riders/rider-config.json --output data/riders/stats.json`)

  // Step 2: Build
  run('Build Site', 'npx nuxt generate')

  // Step 3: Deploy
  if (skipDeploy || dryRun) {
    logs.push('--- Deploy ---')
    logs.push(dryRun ? '(dry run - skipped)' : '(skip deploy - skipped)')
  } else {
    const target = process.env.DEPLOY_TARGET
    if (target) {
      run('Deploy', `scp -r .output/public/* ${target}`)
    } else {
      logs.push('--- Deploy ---')
      logs.push('No DEPLOY_TARGET set, skipped')
    }
  }

  return { success: true, logs }
})
