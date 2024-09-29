import { AxiosResponse } from 'axios'
import { authHttpClient } from 'src/api/AuthHttpClient'

class AuthService {
  static API_ENDPOINT = 'api/login'

  static async logIn (login: string, pass: string) {
    const postData = new URLSearchParams({
      username: login,
      password: pass
    })
    const response = await authHttpClient()
      .post(this.API_ENDPOINT, postData)
      .catch((err: unknown) => {
        return err
      })
    return response as AxiosResponse & {name: string}
  }
}

export { AuthService }
