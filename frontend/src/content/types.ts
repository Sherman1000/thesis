export type Section = {
  title: string
  isPrivate: boolean
  file?: string
  [key: string]: any
  date?: string //YYYY-MM-DD
}

export type Path = {
  filePath?: string
  previous?: string
  next?: string
}