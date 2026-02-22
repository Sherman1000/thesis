import { User } from './types'

export class LocalStorage {
  private static loggedUserKey = 'logged_user_id'
  private static loggedUserTokenKey = 'logged_user_token'

  static saveUserData(user: User, token: string): void {
    localStorage.setItem(this.loggedUserKey, JSON.stringify(user))
    localStorage.setItem(this.loggedUserTokenKey, token)
  }

  static hasUserData(): boolean {
    const user = this.fetchUser()
    const token = this.fetchUserToken()
    return !!user && !!user.id && !!user.name && !!token
  }

  static removeUserData(): void {
    localStorage.removeItem(this.loggedUserKey)
    localStorage.removeItem(this.loggedUserTokenKey)
  }

  static fetchUser(): User | null {
    const item = localStorage.getItem(this.loggedUserKey)
    return !!item ? JSON.parse(item) : item
  }

  static isTeacher(): boolean {
    const user = this.fetchUser()
    return user ? user.is_teacher : false
  }

  static fetchUserId(): string {
    const user = this.fetchUser()
    return user ? user.id : ''
  }

  static fetchUserToken(): string | null {
    return localStorage.getItem(this.loggedUserTokenKey)
  }
}
