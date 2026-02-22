import {Path, Section} from "./types"
import { allKeys } from '../helpers/ObjectHelper'

const content = require('./content.json')

export class ContentReader {
  private readonly content: { [key: string]: Section }
  private readonly contentRootSections: string[]
  private readonly sectionsWithContent: string[]

  constructor() {
    this.content = content
    this.contentRootSections = Object.keys(content)
    this.sectionsWithContent = allKeys(content)
  }

  get rootSections(): string[] {
    return this.contentRootSections
  }

  rootSectionContent(section: string): Section {
    return content[section]
  }

  private previousSection(sectionPath: string) {
    const sectionPathIndex = this.sectionsWithContent.indexOf(sectionPath)
    return sectionPathIndex > 0
      ? this.sectionsWithContent[sectionPathIndex - 1]
      : undefined
  }

  private nextSection(sectionPath: string) {
    const sectionPathIndex = this.sectionsWithContent.indexOf(sectionPath)
    return sectionPathIndex < this.sectionsWithContent.length - 1
      ? this.sectionsWithContent[sectionPathIndex + 1]
      : undefined
  }

  filePathFrom(sectionPath: string): Path {
    const sectionParts = sectionPath.split('/')
    let sectionContent = this.content[sectionParts[0]]
    if (sectionParts.length > 1) {
      for (let i = 1; i < sectionParts.length; i++)
        sectionContent = sectionContent[sectionParts[i]]
    }
    const previous = this.previousSection(sectionPath)
    const next = this.nextSection(sectionPath)

    return {filePath: sectionContent && sectionContent.file, previous, next}
  }
}
