const units = require('./units.json')

export class UnitsReader {
  private readonly units: Units

  constructor() {
    this.units = units
  }

  unitDetails(unit: number): Unit {
    return this.units[unit]
  }

  listUnits(): string[] {
    return Object.keys(this.units)
  }
}

type Units = {
  [key: string]: Unit
}

type Unit = {
  exercises: string[]
  dueDate: string
}
