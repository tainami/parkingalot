import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

api.interceptors.request.use((config)=>{
    const token = sessionStorage.getItem('token')

    if (token){
        config.headers.Authorization = `Bearer ${token}`
    }

    return config
})

api.interceptors.response.use(
    (resposta) => resposta,
    async (erro) => {
        const naoAutorizado = erro.response?.status === 401
        const ehLogin = erro.config?.url?.startsWith('/login')

        if (naoAutorizado && !ehLogin) {
            sessionStorage.removeItem('token')
            sessionStorage.removeItem('guarda')
            const { default: router } = await import('@/router')
            await router.push('/login')
        }

        return Promise.reject(erro)
    }
)

export default api
