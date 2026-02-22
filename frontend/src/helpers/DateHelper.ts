export const earlyThanToday = (stringDate?: string): boolean => {
  if (!stringDate) return true
  const date = new Date(stringDate)
  const today = new Date()

  return +date <= +today
}