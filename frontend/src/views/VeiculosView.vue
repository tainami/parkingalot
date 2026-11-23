
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import CrudLayout from '@/components/CrudLayout.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseField from '@/components/BaseField.vue'
import DataTable from '@/components/DataTable.vue'

interface Veiculo {
    placa: string
    modelo: string
    cor: string
    tipo_veiculo: string
    tipo_vinculo: string
    matricula_colaborador: number | null
    documento_responsavel: string | null
}

interface VeiculoTabela {
    Placa: string
    'Modelo e cor': string
    Vínculo: string
    Responsável: string
    placaCompleta: string
}

const columns = ['Placa', 'Modelo e cor', 'Vínculo', 'Responsável']

const rows = ref<VeiculoTabela[]>([])

const busca = ref('')
const placa = ref('')
const modelo = ref('')
const cor = ref('')
const tipoVeiculo = ref('')
const tipoVinculo = ref('')
const matriculaColaborador = ref('')
const documentoResponsavel = ref('')

const modoEdicao = ref(false)
const placaOriginal = ref('')

const modalExclusao = ref(false)
const veiculoSelecionado = ref<VeiculoTabela | null>(null)

const mensagem = ref('')
const carregando = ref(false)

const linhasFiltradas = computed(() => {
    const termo = busca.value
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')

    return rows.value.filter(veiculo => {
        const dados = [
            veiculo.Placa,
            veiculo['Modelo e cor'],
            veiculo.Vínculo,
            veiculo.Responsável
        ]

        return dados.some(valor =>
            valor.toLowerCase()
                .normalize('NFD')
                .replace(/[\u0300-\u036f]/g, '')
                .includes(termo)
        )
    })
})

async function listarVeiculos() {
    carregando.value = true

    try {
        const resposta = await api.get<Veiculo[]>('/veiculos/')

        rows.value = resposta.data.map(veiculo => ({
            Placa: veiculo.placa,
            'Modelo e cor': `${veiculo.modelo}, ${veiculo.cor}`,
            Vínculo: veiculo.tipo_vinculo === 'COLABORADOR'
                ? 'Colaborador'
                : 'Terceiro',
            Responsável: veiculo.tipo_vinculo === 'COLABORADOR'
                ? `Matrícula ${veiculo.matricula_colaborador}`
                : veiculo.documento_responsavel || 'Não informado',
            placaCompleta: veiculo.placa
        }))
    } catch (erro: any) {
        console.error('Erro ao listar veículos:', erro)

        mensagem.value =
            erro.response?.data?.error ||
            'Não foi possível carregar os veículos.'
    } finally {
        carregando.value = false
    }
}

function formatarPlaca(valor: string) {
    placa.value = valor
        .toUpperCase()
        .replace(/[^A-Z0-9]/g, '')
        .slice(0, 7)
}

function limparFormulario() {
    placa.value = ''
    modelo.value = ''
    cor.value = ''
    tipoVeiculo.value = ''
    tipoVinculo.value = ''
    matriculaColaborador.value = ''
    documentoResponsavel.value = ''

    modoEdicao.value = false
    placaOriginal.value = ''
    mensagem.value = ''
}

async function cadastrar() {
    mensagem.value = ''

    if (
        !placa.value.trim() ||
        !modelo.value.trim() ||
        !cor.value.trim() ||
        !tipoVeiculo.value ||
        !tipoVinculo.value
    ) {
        mensagem.value = 'Preencha todos os campos.'
        return
    }

    if (tipoVinculo.value === 'COLABORADOR' && !matriculaColaborador.value.trim()) {
        mensagem.value = 'Informe a matrícula do colaborador.'
        return
    }

    if (tipoVinculo.value === 'TERCEIRO' && !documentoResponsavel.value.trim()) {
        mensagem.value = 'Informe o documento do responsável.'
        return
    }

    if (!modoEdicao.value && !/^[A-Z0-9]{7}$/.test(placa.value)) {
        mensagem.value = 'Informe uma placa válida com 7 caracteres.'
        return
    }

    if (
        tipoVinculo.value === 'COLABORADOR' &&
        (!/^\d+$/.test(matriculaColaborador.value) ||
            Number(matriculaColaborador.value) <= 0)
    ) {
        mensagem.value = 'Informe uma matrícula válida.'
        return
    }

    carregando.value = true

    const dados = {
        placa: placa.value,
        modelo: modelo.value.trim(),
        cor: cor.value.trim(),
        tipo_veiculo: tipoVeiculo.value,
        tipo_vinculo: tipoVinculo.value,
        matricula_colaborador: tipoVinculo.value === 'COLABORADOR'
            ? Number(matriculaColaborador.value)
            : null,
        documento_responsavel: tipoVinculo.value === 'TERCEIRO'
            ? documentoResponsavel.value.trim()
            : null
    }

    try {
        if (modoEdicao.value) {
            const { placa: placaIgnorada, ...dadosEdicao } = dados

            await api.put(`/veiculos/${placaOriginal.value}`, dadosEdicao)
        } else {
            await api.post('/veiculos/', dados)
        }

        const textoSucesso = modoEdicao.value
            ? 'Veículo atualizado com sucesso.'
            : 'Veículo cadastrado com sucesso.'

        limparFormulario()
        await listarVeiculos()
        mensagem.value = textoSucesso
    } catch (erro: any) {
        console.error('Erro ao salvar veículo:', erro)

        mensagem.value =
            erro.response?.data?.error ||
            'Não foi possível salvar o veículo.'
    } finally {
        carregando.value = false
    }
}

function editarVeiculo(veiculo: VeiculoTabela) {
    console.log('CLIQUE EM EDITAR:', veiculo)
    mensagem.value = ''

    const original = rows.value.find(
        item => item.placaCompleta === veiculo.placaCompleta
    )

    if (!original) return

    modoEdicao.value = true
    placaOriginal.value = original.placaCompleta

    placa.value = original.Placa

    const resposta = veiculoOriginal.value.find(
        item => item.placa === original.placaCompleta
    )

    if (!resposta) return

    modelo.value = resposta.modelo
    cor.value = resposta.cor
    tipoVeiculo.value = resposta.tipo_veiculo
    tipoVinculo.value = resposta.tipo_vinculo
    matriculaColaborador.value = resposta.matricula_colaborador
        ? String(resposta.matricula_colaborador)
        : ''
    documentoResponsavel.value = resposta.documento_responsavel || ''

    mensagem.value = 'Editando os dados do veículo.'
}

const veiculoOriginal = ref<Veiculo[]>([])

async function carregarDados() {
    carregando.value = true

    try {
        const resposta = await api.get<Veiculo[]>('/veiculos/')
        veiculoOriginal.value = resposta.data

        rows.value = resposta.data.map(veiculo => ({
            Placa: veiculo.placa,
            'Modelo e cor': `${veiculo.modelo}, ${veiculo.cor}`,
            Vínculo: veiculo.tipo_vinculo === 'COLABORADOR'
                ? 'Colaborador'
                : 'Terceiro',
            Responsável: veiculo.tipo_vinculo === 'COLABORADOR'
                ? `Matrícula ${veiculo.matricula_colaborador}`
                : veiculo.documento_responsavel || 'Não informado',
            placaCompleta: veiculo.placa
        }))
    } catch (erro: any) {
        console.error('Erro ao carregar veículos:', erro)

        mensagem.value =
            erro.response?.data?.error ||
            'Não foi possível carregar os veículos.'
    } finally {
        carregando.value = false
    }
}

function excluirVeiculo(veiculo: VeiculoTabela) {
    veiculoSelecionado.value = veiculo
    modalExclusao.value = true
}

function cancelarExclusao() {
    modalExclusao.value = false
    veiculoSelecionado.value = null
}

async function confirmarExclusao() {
    if (!veiculoSelecionado.value) return

    carregando.value = true

    try {
        await api.delete(
            `/veiculos/${veiculoSelecionado.value.placaCompleta}`
        )

        cancelarExclusao()
        limparFormulario()
        await carregarDados()
        mensagem.value = 'Veículo excluído com sucesso.'
    } catch (erro: any) {
        console.error('Erro ao excluir veículo:', erro)

        mensagem.value =
            erro.response?.data?.error ||
            'Não foi possível excluir o veículo.'

        cancelarExclusao()
    } finally {
        carregando.value = false
    }
}

onMounted(() => {
    carregarDados()
})
</script>

<template>
    <CrudLayout
        v-model:busca="busca"
        titulo="Veículos"
        subtitulo="Veículos de colaboradores e de terceiros."
        :titulo-formulario="modoEdicao ? 'Editar veículo' : 'Novo veículo'"
        placeholder-busca="Placa, modelo ou responsável"
    >
        <template #tabela>
            <DataTable
                :columns="columns"
                :rows="linhasFiltradas"
                :mostrar-excluir="true"
                @editar="editarVeiculo"
                @excluir="excluirVeiculo"
            />
        </template>

        <template #formulario>
            <form @submit.prevent="cadastrar">
                <BaseField
                    :model-value="placa"
                    @update:model-value="formatarPlaca"
                    rotulo="Placa"
                    placeholder="ABC1D23"
                    :disabled="modoEdicao"
                    obrigatorio
                />

                <BaseField
                    v-model="modelo"
                    rotulo="Modelo"
                    placeholder="Modelo do veículo"
                    obrigatorio
                />

                <BaseField
                    v-model="cor"
                    rotulo="Cor"
                    placeholder="Cor do veículo"
                    obrigatorio
                />

                <div class="form-group">
                    <label for="tipoVeiculo">Tipo de veículo</label>
                    <select id="tipoVeiculo" v-model="tipoVeiculo" required>
                        <option value="" disabled>Selecione o tipo</option>
                        <option value="CARRO">Carro</option>
                        <option value="MOTO">Moto</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="tipoVinculo">Vínculo</label>
                    <select id="tipoVinculo" v-model="tipoVinculo" required>
                        <option value="" disabled>Selecione o vínculo</option>
                        <option value="COLABORADOR">Colaborador</option>
                        <option value="TERCEIRO">Terceiro</option>
                    </select>
                </div>

                <BaseField
                    v-if="tipoVinculo === 'COLABORADOR'"
                    v-model="matriculaColaborador"
                    rotulo="Matrícula do colaborador"
                    placeholder="Número da matrícula"
                    tipo="number"
                    obrigatorio
                />

                <BaseField
                    v-if="tipoVinculo === 'TERCEIRO'"
                    v-model="documentoResponsavel"
                    rotulo="Documento do responsável"
                    placeholder="CPF ou documento"
                    obrigatorio
                />

                <p class="form-info" v-if="tipoVinculo === 'TERCEIRO'">
                    Informe o documento do responsável pelo veículo.
                </p>

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
                        {{ modoEdicao ? 'Salvar alterações' : 'Cadastrar veículo' }}
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
            <h3>Excluir veículo</h3>

            <p>
                Deseja realmente excluir o veículo
                <strong>{{ veiculoSelecionado?.Placa }}</strong>?
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

.form-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.form-group label {
    font: 500 13px var(--font-family);
    color: var(--color-text);
}

.form-group select {
    width: 100%;
    padding: 11px 36px 11px 12px;
    border: 1px solid var(--color-border);
    border-radius: 8px;
    font: 400 13px var(--font-family);
    color: var(--color-text);
    background-color: var(--color-surface);
    cursor: pointer;
}

.form-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.form-actions button:first-child {
    flex: 1;
}

.form-info {
    margin: 0;
    color: var(--color-text-muted);
    font-size: 11px;
    line-height: 1.5;
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
