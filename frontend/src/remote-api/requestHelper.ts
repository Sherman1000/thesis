import {BuildResponse, Response} from './response';
import {LocalStorage} from './localStorage';
import {ApiResponse} from "./types"

export class RequestHelper {
  post<T>(url: string, body: object|FormData): Promise<Response<T> | undefined> {
    return RequestHelper.makeRequest<T>(url, 'POST', body)
      .then(response => response && new BuildResponse().newFrom(response[0], response[1]))
  }

  get<T>(url: string): Promise<Response<T> | undefined> {
    return RequestHelper.makeRequest<T>(url, 'GET')
      .then(response => response && new BuildResponse().newFrom(response[0], response[1]))
  }

  private static async makeRequest<T>(path: string, method: string, body?: object|FormData): Promise<[number, ApiResponse<T>] | undefined> {
    const options: RequestInit = {method: method, headers: {}};

    const token = LocalStorage.fetchUserToken();
    if (token) {
      // @ts-ignore
      options.headers.Authorization = 'Token ' + token;
    }
    if (body) {
      if (!(body instanceof FormData)) {
        // @ts-ignore
        options.headers['Content-Type'] = 'application/json'
      }
      options.body = body instanceof FormData ? body : JSON.stringify(body);
    }

    return fetch(path, options)
      .then(async response => [response.status, await response.json()])
  }
}
