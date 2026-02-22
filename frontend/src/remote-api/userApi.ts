import { RequestHelper } from './requestHelper'
import { LocalStorage } from './localStorage'
import { Response } from './response'
import { SignUpUserData, UserData } from './types'

export class UserApi {
  private helper: RequestHelper

  constructor() {
    this.helper = new RequestHelper()
  }

  private static baseUrl() {
    return "http://127.0.0.1/api/"
  }

  private static saveUserDataFromResponse(response: Response<UserData>): void {
    const data = response.data()
    if (!data) return

    const { user, token } = data
    LocalStorage.saveUserData(user, token)
  }

  signUpUser(
    hash: string,
    username: string,
    password: string,
    confirmationPassword: string
  ): Promise<Response<UserData> | undefined> {
    const body = {
      email: username,
      password,
      password_confirmation: confirmationPassword,
    }

    return this.helper
      .post<UserData>(UserApi.baseUrl() + 'register/' + hash, body)
      .then((response) => {
        if (response && response.isSuccessful())
          UserApi.saveUserDataFromResponse(response)
        return response
      })
  }

  signUpUserData(hash: string): Promise<Response<SignUpUserData> | undefined> {
    return this.helper.get<SignUpUserData>(
      UserApi.baseUrl() + 'registration_status/' + hash
    )
  }

  loginUser(
    username: string,
    password: string
  ): Promise<Response<UserData> | undefined> {
    const body = { username, password }
      debugger

    return this.helper
      .post<UserData>(UserApi.baseUrl() + 'login', body)
      .then((response) => {
        if (response && response.isSuccessful())
          UserApi.saveUserDataFromResponse(response)
        return response
      })
  }

  async logoutUser(): Promise<Response<UserData> | undefined> {
    const user = LocalStorage.fetchUser()
    if (!user) return Promise.reject()

    const body = { user_id: user.id }
    return this.helper
      .post<UserData>(UserApi.baseUrl() + 'logout', body)
      .then((response) => {
        if (response && response.isSuccessful()) LocalStorage.removeUserData()
        return response
      })
  }
}
