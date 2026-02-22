import {ApiResponse} from "./types"

export class BuildResponse {
  newFrom<T>(status: number, jsonResponse: ApiResponse<T>): Response<T> {
    if (status >= 400 && status <= 599) {
      const response = {success: false}
      return new Response(response);
    } else {
      return new Response(jsonResponse);
    }
  }
}

export class Response<T> {
  private apiResponse: ApiResponse<T>;

  constructor(apiResponse: ApiResponse<T>) {
    this.apiResponse = apiResponse;
  }

  isSuccessful() {
    return this.apiResponse.success;
  }

  data() {
    return this.apiResponse.data;
  }

  errors() {
    return this.apiResponse.errors;
  }

  message(): string {
    return (this.isSuccessful()) ? 'OK' : this.errors() || 'Ocurrió un error';
  }
}

