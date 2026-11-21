<script setup lang="ts">
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import api from '@/services/api'

const router = useRouter()

const cpf = ref('')
const senha = ref('')
const mensagemErro = ref('')
const carregando = ref(false)

function validarCPF(event:Event){
    const input = event.target as HTMLInputElement
    let valor = input.value.replace(/\D/g,'')

    valor = valor.replace(/(\d{3})(\d)/, '$1.$2')
    valor = valor.replace(/(\d{3})(\d)/, '$1.$2')
    valor = valor.replace(/(\d{3})(\d{1,2})$/, '$1-$2')

    cpf.value = valor
    
}

const erroCPF = ref('')
const erroSenha = ref('')

async function fazerLogin(){
    console.log('Função fazer login')
    mensagemErro.value = ''

    erroCPF.value = ''
    erroSenha.value = ''

    if (!cpf.value.trim()){
        erroCPF.value = 'Preencha este campo.'
    }

    if (!senha.value.trim()){
        erroSenha.value = 'Preencha este campo'
    }

    if (erroCPF.value || erroSenha.value){
        return
    }

    carregando.value = true

    try{
        const resposta = await api.post('/login/', {
            cpf_guarda: cpf.value.replace(/\D/g,''),
            senha: senha.value
        })

        sessionStorage.setItem('token', resposta.data.token)
        sessionStorage.setItem('guarda', JSON.stringify(resposta.data.guarda))

        await router.push('/')
    }

    catch (erro: any){
        if(erro.response){
            mensagemErro.value = erro.response.data.error || 'Erro ao realizar  login.'
        }
        else{
            mensagemErro.value = 'Não foi possível conectar ao servidor.'
        }
        
    }
    finally{
            carregando.value = false
        }
}

</script>

<template>
    <div class="screen-layout">
    <div class="screen-content">
        <div class="screen-elements">
            <div class="login-logo-icon">P</div>
            <h1 class="screen-title">ParkingALot</h1>
            <p class="screen-subtitle">Controle de entrada e saída do estacionamento</p>
        </div>
        <div class="login-container">
            <div class="login-content">
                <h2 class="login-container-title">Entrar como guarda</h2>
                <form 
                    class="login-form" 
                    @submit.prevent="fazerLogin">
                    <div class="input-group">
                        <label for="cpf">CPF</label>
                        <input
                            type="text" 
                            id="cpf" 
                            name="cpf" 
                            placeholder="000.000.000-00"
                            maxlength="14"
                            inputmode="numeric"
                            v-model="cpf"
                            @input="validarCPF"
                            :class="{'input-invalid': erroCPF}"
                        />
                        <p v-if="erroCPF" class="input-error">
                            {{ erroCPF }}
                        </p>
                    </div>
                    <div class="input-group">
                        <label for="password">Senha</label>
                        <input
                            type="password" 
                            id="password" 
                            name="password" 
                            placeholder="Digite sua senha"
                            v-model="senha"
                            :class="{'input-invalid': erroSenha}"
                        />
                        <p v-if="erroSenha" class="input-error">
                            {{ erroSenha }}
                        </p>
                    </div>
                    <p v-if="mensagemErro" class="login-error">
                        {{ mensagemErro }}
                    </p>
                    <button
                        type="submit" 
                        class="login-button"
                        :disabled="carregando"
                    >
                        {{ carregando ? 'Entrando...' : 'Entrar' }}
                    </button>
                </form>
                <p class="login-container-subtitle">
                Acesso restrito aos guardas. Esqueceu a senha? 
                <a href="#">Redefinir senha</a></p>
            </div>
        </div>

    </div>
    </div>
</template>

<style scoped>

.screen-layout {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    width: 100%;
    background-color: var(--color-bg);
}
.screen-content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    width: 100%;
}

.screen-elements h1{  
    font-size: 45px;
    font-weight: 700;
    margin-bottom: 16px;
}

.screen-elements {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: min(50%, 600px);
    color: var(--color-surface);
    margin-bottom: 10px;
}

.login-logo-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 60px;
    height: 60px;
    border-radius: var(--radius-md);
    background-color: var(--color-primary);
    color: var(--color-surface);
    font-size: 30px;
    font-weight: 700;
}

.screen-title {
    font-size: clamp(32px, 4vw, 48px);
    font-weight: 700;
    margin-bottom: 16px;
    color: var(--color-text);
}

.screen-subtitle {
    font-size: 15px;
    font-weight: 400;
    color: var(--color-text-muted);
}

.login-container {
    display: flex;
    justify-content: flex-start;
    align-items: stretch;
    border-radius: 14px;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
    border: 1px solid #ccc;
    width: min(450px, 90%);
    min-height: 300px;
    padding: 12px 20px 20px;
    background-color: var(--color-bg);
}  

.login-content{
    width: 100%;
}

.login-container-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 24px;
    align-self: self-start;
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.input-group {
    display: flex;
    flex-direction: column;
}

.input-group input:focus{
    outline: none;
    border: 1px solid var(--color-primary);
}

.input-group label {
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 4px;
}

.input-group input {
    padding: 8px 12px;
    border: 1px solid #bfc5ca;
    border-radius: var(--radius-md);
    font-size: 14px;
}

.login-button {
    padding: 10px 16px;
    background-color: var(--color-primary);
    color: var(--color-surface);
    border: none;
    border-radius: var(--radius-md);
    width: min(45%, 180px);
    align-self: center;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition:
        background-color 0.2s ease,
        transform 0.15s ease;
}

.login-button:hover {
    background-color: var(--color-primary-hover);
}

.login-button:active{
    transform: scale(1.05);
}

.login-container-subtitle {
    font-size: 12px;
    font-weight: 400;
    margin-top: 22px;
    text-align: center;
}

.login-container-subtitle a {
    color: var(--color-primary);
    text-decoration: none;
    transition: text-decoration 0.2s ease;
}

.login-container-subtitle a:hover{
    text-decoration: underline;
}

.login-error{
    color: #DC2626;
    font-size: 13px;
    text-align: center;
}

.login-button:disabled{
    opacity: 0.7;
    cursor: not-allowed;
}

.input-error{
    color: #DC2626;
    font-size: 12px;
    margin-top: 4px;
}

.input-invalid{
    border: 1px solid #DC2626 !important
}

</style>