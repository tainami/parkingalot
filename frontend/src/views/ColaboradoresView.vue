
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import CrudLayout from '@/components/CrudLayout.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseField from '@/components/BaseField.vue'
import DataTable from '@/components/DataTable.vue'

interface Colaborador {
    matricula: number
    nome: string
    setor: string
    cargo: string
}

interface ColaboradorTabela {
    Matrícula: string
    Nome: string
    Setor: string
    Cargo: string
    Veículos: string
    matriculaCompleta: number
}

const columns = ['Matrícula', 'Nome', 'Setor', 'Cargo', 'Veículos']

const rows = ref<ColaboradorTabela[]>([])

const busca = ref('')
const matricula = ref('')
const nome = ref('')
const setor = ref('')
const cargo = ref('')

const modoEdicao = ref(false)
const matriculaOriginal = ref<number | null>(null)

const modalExclusao = ref(false)
const colaboradorSelecionado = ref<ColaboradorTabela | null>(null)

const mensagem = ref('')
const carregando = ref(false)

const linhasFiltradas = computed(() => {
    const termo = busca.value
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')

    return rows.value.filter(colaborador => {
        const dados = [
            colaborador.Matrícula,
            colaborador.Nome,
            colaborador.Setor,
            colaborador.Cargo
        ]

        return dados.some(valor =>
            valor.toLowerCase()
                .normalize('NFD')
                .replace(/[\u0300-\u036f]/g, '')
                .includes(termo)
        )
    })
})

async function listarColaboradores() {
    carregando.value = true

    try {
        const resposta = await api.get<Colaborador[]>('/colaboradores/')

        rows.value = resposta.data.map(colaborador => ({
            Matrícula: String(colaborador.matricula),
            Nome: colaborador.nome,
            Setor: colaborador.setor,
            Cargo: colaborador.cargo,
            Veículos: '—',
            matriculaCompleta: colaborador.matricula
        }))
    } catch (erro: any) {
        console.error('Erro ao listar colaboradores:', erro)
        mensagem.value =
            erro.response?.data?.erro ||
            erro.response?.data?.error ||
            'Não foi possível carregar os colaboradores.'
    } finally {
        carregando.value = false
    }
}

async function cadastrar() {
    mensagem.value = ''

    if (modoEdicao.value) {
        await atualizarColaborador()
        return
    }

    if (!matricula.value.trim() || !nome.value.trim() ||
        !setor.value.trim() || !cargo.value.trim()) {
        mensagem.value = 'Preencha todos os campos.'
        return
    }

    const matriculaNumerica = Number(matricula.value)

    if (!Number.isInteger(matriculaNumerica) || matriculaNumerica <= 0) {
        mensagem.value = 'Informe uma matrícula válida.'
        return
    }

    carregando.value = true

    try {
        await api.post('/colaboradores/', {
            matricula: matriculaNumerica,
            nome: nome.value.trim(),
            setor: setor.value.trim(),
            cargo: cargo.value.trim()
        })

        mensagem.value = 'Colaborador cadastrado com sucesso.'

        limparFormulario()
        await listarColaboradores()
        mensagem.value = 'Colaborador cadastrado com sucesso.'
    } catch (erro: any) {
        console.error('Erro ao cadastrar colaborador:', erro)

        mensagem.value =
            erro.response?.data?.erro ||
            erro.response?.data?.error ||
            'Não foi possível cadastrar o colaborador.'
    } finally {
        carregando.value = false
    }
}

function editarColaborador(colaborador: ColaboradorTabela) {
    mensagem.value = ''

    modoEdicao.value = true
    matriculaOriginal.value = colaborador.matriculaCompleta

    matricula.value = colaborador.Matrícula
    nome.value = colaborador.Nome
    setor.value = colaborador.Setor
    cargo.value = colaborador.Cargo

    mensagem.value = 'Editando os dados do colaborador.'
}

async function atualizarColaborador() {
    if (!matriculaOriginal.value) return

    if (!nome.value.trim() || !setor.value.trim() || !cargo.value.trim()) {
        mensagem.value = 'Preencha todos os campos.'
        return
    }

    carregando.value = true

    try {
        await api.put(`/colaboradores/${matriculaOriginal.value}`, {
            nome: nome.value.trim(),
            setor: setor.value.trim(),
            cargo: cargo.value.trim()
        })

        limparFormulario()
        await listarColaboradores()
        mensagem.value = 'Colaborador atualizado com sucesso.'
    } catch (erro: any) {
        console.error('Erro ao atualizar colaborador:', erro)

        mensagem.value =
            erro.response?.data?.erro ||
            erro.response?.data?.error ||
            'Não foi possível atualizar o colaborador.'
    } finally {
        carregando.value = false
    }
}

function excluirColaborador(colaborador: ColaboradorTabela) {
    colaboradorSelecionado.value = colaborador
    modalExclusao.value = true
}

function cancelarExclusao() {
    modalExclusao.value = false
    colaboradorSelecionado.value = null
}

async function confirmarExclusao() {
    if (!colaboradorSelecionado.value) return

    carregando.value = true

    try {
        await api.delete(
            `/colaboradores/${colaboradorSelecionado.value.matriculaCompleta}`
        )

        cancelarExclusao()
        limparFormulario()
        await listarColaboradores()
        mensagem.value = 'Colaborador excluído com sucesso.'
    } catch (erro: any) {
        console.error('Erro ao excluir colaborador:', erro)

        mensagem.value =
            erro.response?.data?.erro ||
            erro.response?.data?.error ||
            'Não foi possível excluir o colaborador.'

        cancelarExclusao()
    } finally {
        carregando.value = false
    }
}

function limparFormulario() {
    matricula.value = ''
    nome.value = ''
    setor.value = ''
    cargo.value = ''

    modoEdicao.value = false
    matriculaOriginal.value = null
    mensagem.value = ''
}

onMounted(() => {
    listarColaboradores()
})
</script>

<template>
    <CrudLayout
        v-model:busca="busca"
        titulo="Colaboradores"
        subtitulo="Gerenciamento dos colaboradores cadastrados no estacionamento"
        :titulo-formulario="modoEdicao ? 'Editar colaborador' : 'Novo colaborador'"
        placeholder-busca="Nome, matrícula, setor ou cargo"
    >
        <template #tabela>
            <DataTable
                :columns="columns"
                :rows="linhasFiltradas"
                :mostrar-excluir="true"
                @editar="editarColaborador"
                @excluir="excluirColaborador"
            />
        </template>

        <template #formulario>
            <form @submit.prevent="cadastrar">
                <BaseField
                    v-model="matricula"
                    rotulo="Matrícula"
                    placeholder="Número da matrícula"
                    tipo="number"
                    :disabled="modoEdicao"
                    obrigatorio
                />

                <BaseField
                    v-model="nome"
                    rotulo="Nome completo"
                    placeholder="Nome do colaborador"
                    obrigatorio
                />

                <BaseField
                    v-model="setor"
                    rotulo="Setor"
                    placeholder="Setor do colaborador"
                    obrigatorio
                />

                <BaseField
                    v-model="cargo"
                    rotulo="Cargo"
                    placeholder="Cargo do colaborador"
                    obrigatorio
                />

                <p
                    v-if="mensagem"
                    :class="mensagem.includes('sucesso')
                        ? 'mensagem-sucesso'
                        : mensagem.includes('Editando')
                            ? 'mensagem-info'
                            : 'mensagem-erro'"
                >
                    {{ mensagem }}
                </p>

                <div class="form-actions">
                    <BaseButton
                        variante="primario"
                        :disabled="carregando"
                        @click="cadastrar"
                    >
                        {{ modoEdicao ? 'Salvar alterações' : 'Cadastrar colaborador' }}
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
            <h3>Excluir colaborador</h3>

            <p>
                Deseja realmente excluir
                <strong>{{ colaboradorSelecionado?.Nome }}</strong>?
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
form {
    display: flex;
    flex-direction: column;
    gap: 14px;
}

.form-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.form-actions button:first-child {
    flex: 1;
}

.mensagem-sucesso {
    color: #15803d;
    font-size: 12px;
}

.mensagem-erro {
    color: var(--color-error);
    font-size: 12px;
}

.mensagem-info {
    color: var(--color-primary);
    font-size: 12px;
}

.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    padding: 16px;
}

.modal {
    width: 90%;
    max-width: 400px;
    padding: 24px;
    background: var(--color-surface);
    border-radius: 10px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.modal h3 {
    margin: 0 0 12px;
    color: var(--color-text);
}

.modal p {
    color: var(--color-text-muted);
    font-size: 14px;
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 24px;
}
</style>
