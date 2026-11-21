<script setup lang="ts">
import {ref} from 'vue'
import { useRouter } from 'vue-router';
import api from '@/services/api'

const router = useRouter()

const cpf = ref('')
const nome = ref('')
const novaSenha = ref('')
const confirmarSenha = ref('')

const mensagemErro = ref('')
const mensagemSucesso = ref('')
const carregando = ref(false)

function validarCPF(event : Event) {
    const input = event.target as HTMLInputElement
    let valor = input.value.replace(/\D/g, '').slice(0,11)

    valor = valor.replace(/(\d{3})(\d)/, '$1.$2')
    valor = valor.replace(/(\d{3})(\d)/, '$1.$2')
    valor = valor.replace(/(\d{3})(\d{1,2})$/, '$1-$2')

    cpf.value = valor
}

async function redefinirSenha(){
    mensagemErro.value = ''
    mensagemSucesso.value = ''

    if (!cpf.value || !nome.value.trim() || !novaSenha.value || !confirmarSenha.value){
        mensagemErro.value = 'Preencha todos os campos.'
        return
    }
    if (novaSenha.value !== confirmarSenha.value){
        mensagemErro.value = 'As senhas não coincidem.'
        return
    }
    if(novaSenha.value.length <8){
        mensagemErro.value = 'A senha deve ter pelo menos 8 caracteres'
        return
    }

    carregando.value = true

    try{
        const resposta = await api.post('/login/redefinir-senha',{
            cpf_guarda: cpf.value.replace(/\D/g, ''),
            nome_guarda: nome.value,
            nova_senha: novaSenha.value,
            confirmar_senha: confirmarSenha.value
        })

        mensagemSucesso.value = resposta.data.message

        setTimeout(()=>{
            router.push('/login')
        }, 2000)
    }
    catch(erro:any){
        mensagemErro.value = erro.response?.data?.error ||
        'Não foi possível redefinir a senha'
    }
    finally{
        carregando.value = false
    }
}

</script>

<template>
    <div class="reset-container">
        <div class="reset-card">
            <h1>Redefinir senha</h1>
            <p>Informe seus dados para cadastrar uma nova senha.</p>

            <form @submit.prevent="redefinirSenha">
                <label for="cpf">CPF</label>
                <input
                    id="cpf"
                    type="text"
                    :value="cpf"
                    @input="validarCPF"
                    maxlength="14"
                    placeholder="000.000.000-00"
                />

                <label for="nome">Nome Completo</label>
                <input
                    id="nome"
                    v-model="nome"
                    type="text"
                    placeholder="Digite seu nome completo"
                />

                <label for="novaSenha">Nova senha</label>
                <input
                    id="novaSenha"
                    v-model="novaSenha"
                    type="password"
                    placeholder="Digite sua nova senha"
                />
                <label for="confirmarSenha">Confirmar senha</label>
                <input  
                    id="confirmarSenha"
                    v-model = "confirmarSenha"
                    type="password"
                    placeholder="Confirme sua nova senha"
                />

                <p v-if="mensagemErro" class="mensagem-erro">
                    {{ mensagemErro }}
                </p>

                <p v-if="mensagemSucesso" class="mensagem-sucesso">
                    {{ mensagemSucesso }}
                </p>

                <button type="submit" :disabled="carregando">
                    {{ carregando ? 'Redefinindo...' : 'Redefinir senha' }}
                </button>

                <button
                    type="button"
                    class="voltar-button"
                    @click="router.push('/login')"
                >
                    Voltar para o login
                </button>
            </form>
        </div>
    </div>


</template>

<style scoped>
.reset-container{
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
    box-sizing: border-box;
    background-color: var(--color-bg);
}

.reset-card{
    width: 100%;
    max-width: 400px;
    padding: 32px;
    box-sizing: border-box;
    border-radius: 14px;
    background-color: var(--color-surface);
}

.reset-card button:hover{
    background-color: var(--color-primary-hover);
}

.reset-card .voltar-button:hover{
    background-color: #b7d9e8;
}

.reset-card h1{
    color: var(--color-text);
    font-size: 24px;
}

.reset-card p{
    color: var(--color-text-muted);
    font-size: 14px;
}

.reset-card form{
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.reset-card label{
    color: var(--color-text);
    font-size: 14px;
    font-weight: 500;
}

.reset-card input{
    width: 100%;
    height: var(--control-height);
    padding: 0 12px;
    box-sizing: border-box;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    font-family: var(--font-family);
}

.reset-card input:focus{
    outline: 1px solid var(--color-primary);
}

.reset-card button{
    min-height: var(--control-height);
    border: none;
    border-radius: var(--radius-md);
    background-color: var(--color-primary);
    color: var(--color-surface);
    font-family: var(--font-family);
    cursor: pointer;
}

.reset-card button:disabled{
    opacity: 0.6;
    cursor: not-allowed;
}

.reset-card .voltar-button{
    background-color: transparent;
    color: var(--color-primary);
}

.mensagem-erro{
    color: var(--color-error) !important; 
}

.mensagem-sucesso{
    color:#15803D !important;
}
</style>