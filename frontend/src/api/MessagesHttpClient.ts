import axios from 'axios'

const messageHttpClient = () => {
  const baseUrl = `https://${process.env.API}/`

  return axios.create({ baseURL: baseUrl })
}

export { messageHttpClient }
