import {Section} from "../content/types"
import {earlyThanToday} from "./DateHelper"

export const allKeys = (obj: Section, parentKey: string = '', array: string[] = []) => {
  for (let key in obj) {
    if (key === 'title' || key === 'file' || key === 'date') continue
    if (obj[key].date && !earlyThanToday(obj[key].date)) continue
    if (obj[key].file) {
      const item = parentKey ? `${parentKey}/${key}` : key
      array.push(item)
    } else {
      const updatedParentKey = parentKey ? `${parentKey}/${key}` : key
      allKeys(obj[key], updatedParentKey, array)
    }
  }

  return array
}
