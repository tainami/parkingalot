<script setup lang="ts">
import {ref, computed, onMounted} from 'vue'
import api from '@/services/api'
import CrudLayout from '@/components/CrudLayout.vue';
import BaseButton from '@/components/BaseButton.vue';
import BaseField from '@/components/BaseField.vue';
import DataTable from '@/components/DataTable.vue';

interface Guarda {
    cpf_guarda: string,
    nome_guarda: string,
    turno: string
}

interface GuardaTabela {
    Nome: string,
    CPF: string,
    Turno: string,
    cpfCompleto: string
}

const columns = ['Nome', 'CPF', 'Turno']

const rows = ref<GuardaTabela[]>([])

const busca = ref('')
const nome = ref('')
const cpf = ref('')
const senha = ref('')
const turno = ref('')

const modalExclusao = ref(false)
const guardaSelecionado = ref<GuardaTabela | null>(null)

const modoEdicao = ref(false)
const cpfOriginal = ref('')

const mensagem = ref('')
const carregando = ref(false)

const linhasFiltradas = computed (()=>{

    const termo = busca.value
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')

    const cpfBusca = busca.value.replace(/\D/g, '')

    return rows.value.filter(guarda => {
        const nome = guarda.Nome
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')

        const turno = guarda.Turno
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
        
        return (
            nome.includes(termo) ||
            turno.includes(termo) ||
            (cpfBusca.length > 0 && guarda.cpfCompleto.includes(cpfBusca))
        )}
    )
})

function formatarCPF(valor: string){
    return valor.replace(
         /^(\d{3})(\d{3})(\d{3})(\d{2})$/,
        '$1.$2.$3-$4'
    )
}

function bloquearNumero(event:KeyboardEvent){
    if(/^[0-9]$/.test(event.key)){
        event.preventDefault()
    }
}

function bloquearLetra(event:KeyboardEvent){
    if(event.key.length === 1 && !/[0-9]/.test(event.key)){
        event.preventDefault()
    }
}

function bloquearColagemNumero(event: ClipboardEvent){
    const texto = event.clipboardData?.getData('text') || ''

    if(/[0-9]/.test(texto)){
        event.preventDefault()
    }
}


async function listarGuardas(){
    try{
        const resposta = await api.get<Guarda[]>('/guardas/')

        rows.value = resposta.data.map(guarda => ({
            Nome: guarda.nome_guarda,
            CPF: esconderCPF(guarda.cpf_guarda),
            Turno: guarda.turno,
            cpfCompleto: guarda.cpf_guarda
        }))
    }
    catch (erro){
        console.error('Erro ao listar guardas:', erro)
        mensagem.value = 'Não foi possível carregar os guardas'
    }
}

async function cadastrar(){

    if (modoEdicao.value){
        await atualizarGuarda()
        return
    }
    mensagem.value = ''

    const cpfNumerico = cpf.value.replace(/\D/g, '')

    if (!nome.value.trim() || !cpfNumerico || !senha.value || !turno.value){
        mensagem.value = 'Preencha todos os campos.'
        return
    }
    if (cpfNumerico.length !== 11){
        mensagem.value = 'O CPF deve conter 11 dígitos.'
        return
    }
    if (senha.value.length < 8){
        mensagem.value = 'A senha deve conter pelo menos 8 caracteres'
        return
    }

    carregando.value = true

    try{
        await api.post('/guardas/', {
            cpf_guarda: cpfNumerico,
            nome_guarda: nome.value,
            turno: turno.value,
            senha: senha.value
        })

        mensagem.value = 'Guarda cadastrado com sucesso'

        limparFormulario()
        await listarGuardas()
    }
    catch (erro: any){
        console.error('Erro ao cadastrar guarda:', erro)

        mensagem.value =
            erro.response?.data?.error || 'Não foi possível cadastrar o guarda.'
    }
    finally {
        carregando.value = false
    }
}

function validarCPF(valor:string){
    const cpfNumerico = valor.replace(/\D/g, '').slice(0, 11)

    let cpfFormatado = cpfNumerico

    if(cpfNumerico.length > 3){
        cpfFormatado = cpfNumerico.slice(0, 3) + '.' + cpfNumerico.slice(3)
    }

    if(cpfNumerico.length > 6){
        cpfFormatado = cpfNumerico.slice(0, 3) + '.' +
            cpfNumerico.slice(3, 6) + '.' +
            cpfNumerico.slice(6)
    }

    if(cpfNumerico.length > 9){
        cpfFormatado = cpfNumerico.slice(0, 3) + '.' +
            cpfNumerico.slice(3, 6) + '.' +
            cpfNumerico.slice(6, 9) + '-' +
            cpfNumerico.slice(9)
    }

    cpf.value = cpfFormatado
}

function esconderCPF(valor:string){
    const cpfNumerico = valor.replace(/\D/g, '')

    return `***.${cpfNumerico.slice(3, 6)}.***-${cpfNumerico.slice(9, 11)}`
}

function limparFormulario(){
    nome.value = ''
    cpf.value = ''
    senha.value = ''
    turno.value = ''
    mensagem.value = ''

    modoEdicao.value = false
    cpfOriginal.value = ''
    
}

onMounted(()=>{
    listarGuardas()
})

function editarGuarda(guarda: GuardaTabela){

    mensagem.value = ''

    modoEdicao.value = true
    cpfOriginal.value = guarda.cpfCompleto

    nome.value = guarda.Nome
    cpf.value = formatarCPF(guarda.cpfCompleto)
    turno.value = guarda.Turno.toLowerCase()

    mensagem.value = 'Editando os dados do guarda'
}

async function atualizarGuarda(){
    if(!nome.value.trim() || !turno.value){
        mensagem.value = 'Preencha todos os campos'
        return
    }
    carregando.value = true
    try{
        await api.put(`/guardas/${cpfOriginal.value}`,{
            nome_guarda: nome.value,
            turno: turno.value
        })
        mensagem.value = 'Guarda atualizado com sucesso'

        limparFormulario()
        await listarGuardas()
    }
    catch (erro:any){
        console.error('Erro ao atualizar guarda:', erro)
        mensagem.value = 
            erro.response?.data?.error || 'Não foi possível atualizar o guarda'
    }
    finally{
        carregando.value = false
    }
}

function excluirGuarda(guarda:GuardaTabela){
    guardaSelecionado.value = guarda
    modalExclusao.value = true
}

function cancelarExclusao(){
    modalExclusao.value = false
    guardaSelecionado.value = null
}

async function confirmarExclusao(){
    if(!guardaSelecionado.value) return

    carregando.value = true

    try{
        await api.delete(`/guardas/${guardaSelecionado.value.cpfCompleto}`)

        mensagem.value = 'Guarda excluído com sucesso'

        cancelarExclusao()
        await listarGuardas()
    }
    catch(erro:any){
        console.error('Erro ao excluir guarda:', erro)

        mensagem.value = 
         erro.response?.data?.error || 'Não foi possível excluir o guarda'

        cancelarExclusao()
    }
    finally{
        carregando.value = false
    }
}

</script>

<template>
    <CrudLayout
        v-model:busca="busca"
        titulo="Guardas"
        subtitulo="Usuários com acesso ao sistema. Entrada via CPF e senha"
        :titulo-formulario="modoEdicao ? 'Editar guarda' : 'Novo guarda'"
        placeholder-busca="Nome ou CPF"
    >
        <template #tabela>
            <DataTable
                :columns="columns"
                :rows="linhasFiltradas"
                :mostrarExcluir="true"
                @editar="editarGuarda"
                @excluir="excluirGuarda"
            />
        </template>

        <template #formulario>
            <form @submit.prevent>
                <BaseField
                    v-model="nome"
                    @keydown="bloquearNumero"
                    @paste="bloquearColagemNumero"
                    rotulo="Nome completo"
                    placeholder="Nome do guarda"
                    obrigatorio
                />

                <BaseField
                    :model-value="cpf"
                    @update:model-value="validarCPF"
                    @keydown="bloquearLetra"
                    :disabled="modoEdicao"
                    :maxlength="14"
                    rotulo="CPF"
                    placeholder="000.000.000-00"
                    obrigatorio
                />

                <div class="form-group">
                    <label for="turno">Turno</label>
                    <select id="turno" v-model="turno" required>
                        <option value="" disabled>Selecione o turno</option>
                        <option value="manhã">Manhã</option>
                        <option value="tarde">Tarde</option>
                        <option value="noite">Noite</option>
                    </select>                
                </div>
                <template v-if="!modoEdicao">
                <BaseField
                    v-model="senha"
                    rotulo="Senha inicial"
                    placeholder="Mínimo de 8 caracteres"
                    tipo="password"
                    obrigatorio
                />

                <p class="form-info">
                    O guarda pode trocar a senha depois se desejar.
                </p>
                </template>

                <p v-if="mensagem" 
                    :class="mensagem.includes('sucesso') ? 'mensagem-sucesso': mensagem.includes('Editando') ? 'mensagem-info' : 'mensagem-erro'">
                    {{ mensagem }}
                </p>

                <div class="form-actions">
                    <BaseButton 
                        variante="primario"
                        :disabled="carregando"
                        @click="cadastrar">
                        {{ modoEdicao ? 'Salvar alterações' : 'Cadastrar guarda' }}
                    </BaseButton>

                    <BaseButton
                        variante="secundario"
                        :disabled="carregando"
                        @click="limparFormulario"
                    >
                        Limpar
                    </BaseButton>
                </div>
            </form>
        </template>
        
    </CrudLayout>
    <div v-if="modalExclusao" class="modal-overlay">
            <div class="modal">
                <h3>Excluir guarda</h3>
                <p>
                    Deseja realmente excluir
                    <strong>{{ guardaSelecionado?.Nome }}</strong>
                </p>

                <div class="modal-actions">
                    <BaseButton
                        variante="secundario"
                        @click="cancelarExclusao"
                    >
                        Cancelar
                    </BaseButton>

                    <BaseButton
                        variante="primario"
                        :disabled="carregando"
                        @click="confirmarExclusao"
                    >
                        Excluir
                    </BaseButton>
                </div>
            </div>
        </div>
    
</template>

<style scoped>
form{
    display: flex;
    flex-direction: column;
    gap: 14px;
}

.form-info{
    margin: 0;
    color: var(--color-text-muted);
    font: 400 11px var(--font-family);
    line-height: 1.5;
}

.form-actions{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.form-actions button:first-child{
    flex: 1;
}

.form-group{
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.form-group label{
    font: 500 13px var(--font-family);
    color: var(--color-text);
}

.form-group select{
    padding: 10px;
    border: 1px solid var(--color-border);
    border-radius: 6px;
    font: 400 13px var(--font-family);
    color: var(--color-text);
    background: var(--color-surface);
}

.mensagem-sucesso{
    color:#15803d;
    font-size: 12px;
}

.mensagem-erro{
    color:var(--color-error);
    font-size:12px;
}

.mensagem-info{
    color: var(--color-primary);
    font-size: 12px;
}

.modal h3{
    margin: 0 0 12px;
    color: var(--color-text);
}

.modal p{
    color: var(--color-text-muted);
    font-size: 14px;
}

.modal-actions{
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 24px;
}

.modal-overlay{
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    padding: 16px;
}

.modal{
    width: 90%;
    max-width: 400px;
    padding: 24px;
    background: var(--color-surface);
    border-radius: 10px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.form-group label{
    font: 500 13px var(--font-family);
    color: var(--color-text);
}

.form-group select{
    width: 100%;
    padding: 11px 36px 11px 12px;
    border: 1px solid var(--color-border);
    border-radius: 8px;
    font: 400 13px var(--font-family);
    color: var(--color-text);
    background-color: var(--color-surface);
    cursor: pointer;
    outline: none;
    appearance: none;

    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23888888' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 12px center;
}

.form-group select:focus,
.form-group select:hover{
    border-color: var(--color-primary);
}

.form-group select option{
    background: var(--color-surface);
    color: var(--color-text);
    padding: 10px;
}

</style>