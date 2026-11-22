<script setup lang="ts">
import {ref, computed, onMounted} from 'vue'
import api from '@/services/api'
import CrudLayout from '@/components/CrudLayout.vue';
import BaseButton from '@/components/BaseButton.vue';
import BaseField from '@/components/BaseField.vue';
import DataTable from '@/components/DataTable.vue';

interface Vaga {
    numero: number
    tipo_vaga: string
    status_vaga: boolean
}

interface VagaTabela {
    Numero: number
    Tipo: string
    Status: string
    numeroCompleto: number
}

const columns = ['Número', 'Tipo', 'Status']
const rows = ref<VagaTabela[]>([])

const busca = ref('')
const numero = ref('')

const modoEdicao = ref(false)
const numeroOriginal = ref<number | null>(null)

const mensagem = ref('')
const carregando = ref(false)

const linhasFiltradas = computed(()=>{
    const termo = busca.value.toLowerCase()

    return rows.value.filter(vaga =>
        String(vaga.Numero).includes(termo) ||
        vaga.Tipo.toLowerCase().includes(termo) ||
        vaga.Status.toLowerCase().includes(termo)
    )
})

async function listarVagas(){
    carregando.value = true

    try{
        const resposta = await api.get('/vagas/')

        rows.value = resposta.data.map((vaga:Vaga)=>({
            Numero: vaga.numero,
            Tipo: vaga.tipo_vaga === 'COLABORADOR' ? 'Colaborador' : 'Terceiro',
            Status: vaga.status_vaga ? 'Ocupada' : 'Livre',
            numeroCompleto: vaga.numero
        }))
    }
    catch (erro){
        mensagem.value = 'Erro ao carregar vagas'
    }
    finally{
        carregando.value = false
    }
}

async function cadastrar(){
    if(!numero.value){
        mensagem.value = 'Preencha todos os campos'
        return
    }

    carregando.value = true
    mensagem.value = ''

    const textoSucesso = modoEdicao.value
        ? 'Vaga atualizada com sucesso'
        : 'Vaga cadastrada com sucesso.'

    try{

        if(modoEdicao.value){
            await api.put(`/vagas/${numeroOriginal.value}`, {
                numero: Number(numero.value)
            }
            )
        }
        else{
            await api.post('/vagas/',{
                numero: Number(numero.value)
            })
        }
        

        await listarVagas()
        limparFormulario()
        mensagem.value = textoSucesso
        }
    
    catch (erro: any){
        mensagem.value = erro.response?.data?.error || 'Erro ao salvar vaga'
    }
    finally{
        carregando.value = false
    }
}

function editarVaga(vaga:VagaTabela){
    modoEdicao.value = true
    numeroOriginal.value = vaga.numeroCompleto
    numero.value = String(vaga.numeroCompleto)
    mensagem.value = 'Editando vaga'
}

function limparFormulario(){
    numero.value = ''
    modoEdicao.value = false
    numeroOriginal.value = null
    mensagem.value = ''
}

onMounted(()=>{
    listarVagas()
})

</script>

<template>
    <CrudLayout 
        v-model:busca="busca"
        titulo="Vagas" 
        subtitulo="Gerenciamento de vagas"
        :titulo-formulario="modoEdicao ? 'Editar vaga' : 'Cadastro de vagas'"
        placeholderBusca="Digite o número, tipo ou status"
    >
        <template #formulario>
            <form @submit.prevent class="formulario">
                <div class="form-group">
                    <BaseField
                        v-model="numero"
                        rotulo="Número da vaga"
                        placeholder="Digite o número"
                        obrigatorio
                    />
                </div>

                <p
                    v-if="mensagem"
                    :class="{
                        'mensagem-sucesso': mensagem.includes('sucesso'),
                        'mensagem-erro': mensagem.includes('Erro') ||  mensagem.includes('Preencha'),
                        'mensagem-info': mensagem.includes('Editando')
                    }"
                >
                    {{ mensagem }}
                </p>

                <div class="form-actions">
                    <BaseButton
                        variante="primario"
                        @click="cadastrar"
                        :disabled="carregando"
                    >
                        {{ modoEdicao ? 'Salvar alterações' : 'Cadastrar vaga' }}
                    </BaseButton>

                    <BaseButton
                        variante="secundario"
                        type="button"
                        :disabled="carregando"
                        @click="limparFormulario"
                    >
                        Limpar
                    </BaseButton>
                </div>
            </form>
        </template>

        <template #tabela>

            <DataTable
                :columns="columns"
                :rows="linhasFiltradas"
                :mostrarExcluir="false"
                @editar="editarVaga"
            />
        </template>

    </CrudLayout>

</template>

<style scoped>
form{
    display: flex;
    flex-direction: column;
    gap: 14px;
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




.mensagem-sucesso{
    color: #15803d;
    font-size: 12px;
}

.mensagem-erro{
    color: var(--color-error);
    font-size: 12px;
}

.mensagem-info{
    color: var(--color-primary);
    font-size: 12px;
}

</style>