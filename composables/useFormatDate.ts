export function useFormatDate() {
  function formatDate(dateStr: string | null | undefined): string {
    if (!dateStr) return ''
    return new Date(dateStr + 'T00:00:00').toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    })
  }

  return { formatDate }
}
