<script setup lang="ts">
import {ref, computed, onMounted} from 'vue'
import CrudLayout from '@/components/CrudLayout.vue';
import BaseButton from '@/components/BaseButton.vue';
import BaseField from '@/components/BaseField.vue';
import DataTable from '@/components/DataTable.vue';
import StatusPill from '@/components/StatusPill.vue';
import { atualizarVaga, criarVaga, listarVagas } from '@/services/vagas'

interface VagaTabela {
    'Número': number
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

type TipoMensagem = 'sucesso' | 'erro' | 'info'

const mensagem = ref('')
const tipoMensagem = ref<TipoMensagem>('info')
const carregando = ref(false)

function mostrarMensagem(texto: string, tipo: TipoMensagem){
    mensagem.value = texto
    tipoMensagem.value = tipo
}

const linhasFiltradas = computed(()=>{
    const termo = busca.value.toLowerCase()

    return rows.value.filter(vaga =>
        String(vaga['Número']).includes(termo) ||
        vaga.Tipo.toLowerCase().includes(termo) ||
        vaga.Status.toLowerCase().includes(termo)
    )
})

async function carregarVagas(){
    carregando.value = true

    try{
        const vagas = await listarVagas()

        rows.value = vagas.map((vaga)=>({
            'Número': vaga.numero,
            Tipo: vaga.tipo_vaga === 'COLABORADOR' ? 'Colaborador' : 'Terceiro',
            Status: vaga.status_vaga ? 'Ocupada' : 'Livre',
            numeroCompleto: vaga.numero
        }))
    }
    catch (erro){
        mostrarMensagem('Erro ao carregar vagas', 'erro')
    }
    finally{
        carregando.value = false
    }
}

async function cadastrar(){
    if(!numero.value){
        mostrarMensagem('Preencha todos os campos', 'erro')
        return
    }

    carregando.value = true
    mensagem.value = ''

    const textoSucesso = modoEdicao.value
        ? 'Vaga atualizada com sucesso'
        : 'Vaga cadastrada com sucesso.'

    try{

        if(modoEdicao.value && numeroOriginal.value !== null){
            await atualizarVaga(numeroOriginal.value, Number(numero.value))
        }
        else{
            await criarVaga(Number(numero.value))
        }

        await carregarVagas()
        limparFormulario()
        mostrarMensagem(textoSucesso, 'sucesso')
        }
    
    catch (erro: any){
        mostrarMensagem(erro.response?.data?.error || 'Erro ao salvar vaga', 'erro')
    }
    finally{
        carregando.value = false
    }
}

function editarVaga(vaga:VagaTabela){
    modoEdicao.value = true
    numeroOriginal.value = vaga.numeroCompleto
    numero.value = String(vaga.numeroCompleto)
    mostrarMensagem('Editando vaga', 'info')
}

function limparFormulario(){
    numero.value = ''
    modoEdicao.value = false
    numeroOriginal.value = null
    mensagem.value = ''
}

onMounted(()=>{
    carregarVagas()
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
                    :class="`mensagem-${tipoMensagem}`"
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
            >
                <template #celula="{ coluna, valor }">
                    <StatusPill
                        v-if="coluna === 'Status'"
                        :texto="valor"
                        :variante="valor === 'Ocupada' ? 'azul-claro' : 'cinza'"
                    />
                    <template v-else>{{ valor }}</template>
                </template>
            </DataTable>
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