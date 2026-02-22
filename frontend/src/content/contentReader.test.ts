import { ContentReader } from './contentReader'

describe('Content reader', () => {
  let reader: ContentReader

  beforeAll(() => {
    reader = new ContentReader()
  })

  test('lists all root sections', () => {
    expect(reader.rootSections).toEqual(['inicio', 'about', 'units'])
  })

  test('returns content of root section', () => {
    expect(reader.rootSectionContent('inicio')).toEqual({
      title: 'Inicio',
      file: '/content/index.md',
    })
  })

  test('returns md file from root path', () => {
    expect(reader.filePathFrom('inicio')).toEqual('/content/index.md')
  })

  test('returns md file from two levels path', () => {
    expect(reader.filePathFrom('about/condiciones')).toEqual('/content/sobre-el-curso/Cursada.md')
  })

  test('returns md file from two three path', () => {
    expect(reader.filePathFrom('units/estructuras-y-funciones/resumen')).toEqual('/content/unidades/02_Estructuras_y_Funciones/00_Resumen.md')
  })
})
