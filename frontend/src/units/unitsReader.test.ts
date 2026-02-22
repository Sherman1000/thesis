import {UnitsReader} from "./unitsReader"

describe('Units reader', () => {
  let reader: UnitsReader

  beforeAll(() => {
    reader = new UnitsReader()
  })

  test('lists all exercises per unit', () => {
    expect(reader.unitDetails(1).exercises).toEqual(["rebotes.py", "hipoteca.py", "esfera.py", "geringoso.py"])
    expect(reader.unitDetails(2).exercises).toEqual([
      "buscar_precios.py",
      "costo_camion.py",
      "camion_commandline.py",
      "diccionario_geringoso.py",
      "informe.py"
    ])
    expect(reader.unitDetails(3).exercises).toEqual([
      "solucion_de_errores.py",
      "informe.py",
      "tabla_informe.py",
      "tablamult.py",
      "arboles.py"
    ])
    expect(reader.unitDetails(4).exercises).toEqual(["busqueda_en_listas.py", "invlista.py", "propaga.py", "arboles.py"])
    expect(reader.unitDetails(5).exercises).toEqual([
      "generala.py",
      "termometro.py",
      "plotear_temperaturas.py",
      "figuritas.py",
      "arboles.py"
    ])
    expect(reader.unitDetails(6).exercises).toEqual([
      "fileparse.py",
      "informe_funciones.py",
      "costo_camion.py",
      "bbin.py",
      "plot_bbin_vs_bsec.py"
    ])
    expect(reader.unitDetails(7).exercises).toEqual([
      "fileparse.py",
      "informe_final.py",
      "documentacion.py",
      "random_walk.py"
    ])
    expect(reader.unitDetails(8).exercises).toEqual([
      "vida.py",
      "listar_imgs.py",
      "arbolado_parques_veredas.py",
      "mareas_a_mano.py"
    ])
    expect(reader.unitDetails(9).exercises).toEqual([
      "informe_final.py",
      "lote.py",
      "torre_control.py",
      "canguros_buenos.py",
      "NDVI.py"
    ])
  })

  test('lists all units', () => {
    expect(reader.listUnits()).toEqual(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
  })
})