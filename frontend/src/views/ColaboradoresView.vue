
<script setup lang="ts">
import { ref, computed } from 'vue'
import CrudLayout from '@/components/CrudLayout.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseField from '@/components/BaseField.vue'
import DataTable from '@/components/DataTable.vue'

interface ColaboradorTabela {
  Matrícula: number
  Nome: string
  Veículos: string
  matriculaCompleta: number
  setor: string
  cargo: string
}

const columns = ['Matrícula', 'Nome', 'Veículos']

const rows = ref<ColaboradorTabela[]>([])

const busca = ref('')

const matricula = ref('')
const nome = ref('')
const setor = ref('')
const cargo = ref('')

const modoEdicao = ref(false)
const matriculaOriginal = ref<number | null>(null)

const mensagem = ref('')
const tipoMensagem = ref<'sucesso' | 'erro' | 'info'>('info')

const modalExclusao = ref(false)
const colaboradorSelecionado = ref<ColaboradorTabela | null>(null)

const linhasFiltradas = computed(() => {
  const pesquisa = busca.value.toLowerCase()

  return rows.value.filter((colaborador) =>
    colaborador.Nome.toLowerCase().includes(pesquisa) ||
    String(colaborador.Matrícula).includes(pesquisa)
  )
})

function exibirMensagem(
  texto: string,
  tipo: 'sucesso' | 'erro' | 'info'
) {
  mensagem.value = texto
  tipoMensagem.value = tipo
}

function limparFormulario() {
  matricula.value = ''
  nome.value = ''
  setor.value = ''
  cargo.value = ''

  modoEdicao.value = false
  matriculaOriginal.value = null
}

function validarFormulario(): boolean {
  if (
    !matricula.value.trim() ||
    !nome.value.trim() ||
    !setor.value.trim() ||
    !cargo.value.trim()
  ) {
    exibirMensagem('Preencha todos os campos.', 'erro')
    return false
  }

  const numeroMatricula = Number(matricula.value)

  if (!Number.isInteger(numeroMatricula) || numeroMatricula <= 0) {
    exibirMensagem('Informe uma matrícula válida.', 'erro')
    return false
  }

  return true
}

function editarColaborador(colaborador: ColaboradorTabela) {
  matricula.value = String(colaborador.matriculaCompleta)
  nome.value = colaborador.Nome
  setor.value = colaborador.setor
  cargo.value = colaborador.cargo

  matriculaOriginal.value = colaborador.matriculaCompleta
  modoEdicao.value = true

  mensagem.value = ''
}

function excluirColaborador(colaborador: ColaboradorTabela) {
  colaboradorSelecionado.value = colaborador
  modalExclusao.value = true
}

function cancelarExclusao() {
  modalExclusao.value = false
  colaboradorSelecionado.value = null
}

function salvar() {
  if (!validarFormulario()) return

  exibirMensagem(
    'A integração com o backend ainda não foi realizada.',
    'info'
  )
}

function confirmarExclusao() {
  modalExclusao.value = false
  colaboradorSelecionado.value = null

  exibirMensagem(
    'A integração com o backend ainda não foi realizada.',
    'info'
  )
}
</script>

<template>
  <CrudLayout
    titulo="Colaboradores"
    subtitulo="Gerencie os colaboradores cadastrados no sistema."
    tituloFormulario="Cadastro de colaborador"
    placeholderBusca="Buscar por nome ou matrícula..."
    v-model:busca="busca"
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
      <form @submit.prevent="salvar">
        <BaseField
          v-model="matricula"
          rotulo="Matrícula"
          placeholder="Digite a matrícula"
          tipo="text"
          obrigatorio
        />

        <BaseField
          v-model="nome"
          rotulo="Nome completo"
          placeholder="Digite o nome completo"
          tipo="text"
          obrigatorio
        />

        <BaseField
          v-model="setor"
          rotulo="Setor"
          placeholder="Digite o setor"
          tipo="text"
          obrigatorio
        />

        <BaseField
          v-model="cargo"
          rotulo="Cargo"
          placeholder="Digite o cargo"
          tipo="text"
          obrigatorio
        />

        <div class="botoes-formulario">
          <BaseButton @click="salvar">
            {{ modoEdicao ? 'Salvar alterações' : 'Cadastrar colaborador' }}
          </BaseButton>

          <button
            v-if="modoEdicao"
            type="button"
            class="botao-cancelar"
            @click="limparFormulario"
          >
            Cancelar edição
          </button>
        </div>
      </form>

      <p
        v-if="mensagem"
        class="mensagem"
        :class="`mensagem-${tipoMensagem}`"
      >
        {{ mensagem }}
      </p>
    </template>
  </CrudLayout>

  <div v-if="modalExclusao" class="modal-fundo">
    <div class="modal">
      <h2>Excluir colaborador</h2>

      <p>
        Tem certeza que deseja excluir
        <strong>{{ colaboradorSelecionado?.Nome }}</strong>?
      </p>

      <div class="modal-botoes">
        <button
          type="button"
          class="botao-cancelar"
          @click="cancelarExclusao"
        >
          Cancelar
        </button>

        <button
          type="button"
          class="botao-excluir"
          @click="confirmarExclusao"
        >
          Confirmar exclusão
        </button>
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

.botoes-formulario {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 8px;
}

.botao-cancelar,
.botao-excluir {
  padding: 10px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}

.botao-cancelar {
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text);
}

.mensagem {
  margin: 12px 0 0;
  font-size: 13px;
}

.mensagem-sucesso {
  color: #16803c;
}

.mensagem-erro {
  color: #d32f2f;
}

.mensagem-info {
  color: var(--color-text-muted);
}

.modal-fundo {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal {
  width: 100%;
  max-width: 400px;
  padding: 24px;
  border-radius: 12px;
  background: var(--color-surface);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.18);
}

.modal h2 {
  margin: 0 0 12px;
  color: var(--color-text);
  font-size: 18px;
}

.modal p {
  color: var(--color-text-muted);
  font-size: 14px;
  line-height: 1.5;
}

.modal-botoes {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 22px;
}

.botao-excluir {
  border: none;
  background: #d32f2f;
  color: white;
}
</style>
