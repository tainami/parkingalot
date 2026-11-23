<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import PageHeader from '@/components/PageHeader.vue'
import BaseField from '@/components/BaseField.vue'
import BaseButton from '@/components/BaseButton.vue'
import DataTable from '@/components/DataTable.vue'
import StatusPill from '@/components/StatusPill.vue'
import { listarRegistros, type Registro } from '@/services/registros'
import { listarVeiculos, type Veiculo } from '@/services/veiculos'
import { listarGuardas } from '@/services/guardas'
import { listarPagamentos, type Pagamento } from '@/services/pagamentos'
import {
  dataDeHoje,
  formatarDataHora,
  formatarDiaMes,
  formatarMoeda,
} from '@/utils/formatar'
import { exportarExcel } from '@/utils/exportarExcel'

type SituacaoPagamento = 'isento' | 'na-saida' | 'pago' | 'pendente'

const TEXTO_SITUACAO: Record<SituacaoPagamento, string> = {
  isento: 'Isento',
  'na-saida': 'Na saída',
  pago: 'Pago',
  pendente: 'Pendente',
}

const columns = ['ID', 'Placa', 'Vínculo', 'Vaga', 'Entrada', 'Saída', 'Guarda', 'Pagamento']

const route = useRoute()

const data = ref('')
const placa = ref('')
const dataAplicada = ref('')
const placaAplicada = ref('')

const registros = ref<Registro[]>([])
const veiculos = ref(new Map<string, Veiculo>())
const guardas = ref(new Map<string, string>())
const pagamentos = ref(new Map<number, Pagamento>())

const carregando = ref(false)
const exportando = ref(false)
const erro = ref('')

function normalizarPlaca(valor: string) {
  return valor.trim().toUpperCase().replace(/[^A-Z0-9]/g, '')
}

function filtrarPorPlaca(lista: Registro[], termo: string) {
  const busca = normalizarPlaca(termo)
  return busca ? lista.filter((r) => r.placa.includes(busca)) : lista
}

function montarLinhas(lista: Registro[]) {
  return [...lista]
    .sort((a, b) => b.id_registro - a.id_registro)
    .map((registro) => {
      const terceiro = veiculos.value.get(registro.placa)?.tipo_vinculo === 'TERCEIRO'
      const pagamento = pagamentos.value.get(registro.id_registro)

      let situacao: SituacaoPagamento = 'isento'
      if (terceiro) situacao = !registro.data_saida ? 'na-saida' : pagamento ? 'pago' : 'pendente'

      return {
        ID: `#${registro.id_registro}`,
        Placa: registro.placa,
        Vínculo: terceiro ? 'Terceiro' : 'Colaborador',
        Vaga: registro.numero_vaga,
        Entrada: formatarDataHora(registro.data_entrada),
        Saída: registro.data_saida ? formatarDataHora(registro.data_saida) : null,
        Guarda: guardas.value.get(registro.cpf_guarda) ?? registro.cpf_guarda,
        Pagamento: situacao,
        Valor: pagamento ? formatarMoeda(pagamento.valor) : '',
      }
    })
}

type Linha = ReturnType<typeof montarLinhas>[number]

const registrosFiltrados = computed(() => filtrarPorPlaca(registros.value, placaAplicada.value))

const linhas = computed(() => montarLinhas(registrosFiltrados.value))

const resumo = computed(() => {
  const lista = registrosFiltrados.value
  const total = lista.length
  const noPatio = lista.filter((r) => !r.data_saida).length
  const comPagamento = lista.filter((r) => pagamentos.value.has(r.id_registro)).length
  const emData = dataAplicada.value ? ` em ${formatarDiaMes(dataAplicada.value)}` : ''

  return [
    `${total} ${total === 1 ? 'registro' : 'registros'}${emData}`,
    `${noPatio} ${noPatio === 1 ? 'veículo' : 'veículos'} no pátio`,
    `${comPagamento} ${comPagamento === 1 ? 'saída' : 'saídas'} com pagamento`,
  ]
})

function mensagemDeErro(e: unknown, padrao: string) {
  const resposta = (e as { response?: { data?: { error?: string } } }).response
  return resposta?.data?.error || padrao
}

async function carregarApoio() {
  const [listaVeiculos, listaGuardas, listaPagamentos] = await Promise.all([
    listarVeiculos(),
    listarGuardas(),
    listarPagamentos(),
  ])

  veiculos.value = new Map(listaVeiculos.map((v) => [v.placa, v]))
  guardas.value = new Map(listaGuardas.map((g) => [g.cpf_guarda, g.nome_guarda]))
  pagamentos.value = new Map(listaPagamentos.map((p) => [p.id_registro, p]))
}

async function carregarRegistros() {
  registros.value = await listarRegistros(data.value ? { data: data.value } : {})
  dataAplicada.value = data.value
}

async function filtrar() {
  carregando.value = true
  erro.value = ''

  try {
    if (data.value !== dataAplicada.value) await carregarRegistros()
    placaAplicada.value = placa.value
  } catch (e) {
    erro.value = mensagemDeErro(e, 'Erro ao carregar registros.')
  } finally {
    carregando.value = false
  }
}

function limparFiltros() {
  data.value = ''
  placa.value = ''
  filtrar()
}

async function baixarRelatorio() {
  if (exportando.value) return

  exportando.value = true
  erro.value = ''

  try {
    const dataRelatorio = dataAplicada.value || dataDeHoje()
    const doDia = dataAplicada.value ? registros.value : await listarRegistros({ data: dataRelatorio })
    const lista = filtrarPorPlaca(doDia, placaAplicada.value)

    if (lista.length === 0) {
      erro.value = `Nenhum registro em ${formatarDiaMes(dataRelatorio)} para gerar o relatório.`
      return
    }

    await exportarExcel<Linha>(
      `registros-${dataRelatorio}`,
      'Registros',
      [
        { titulo: 'ID', valor: (l) => l.ID },
        { titulo: 'Placa', valor: (l) => l.Placa },
        { titulo: 'Vínculo', valor: (l) => l.Vínculo, largura: 14 },
        { titulo: 'Vaga', valor: (l) => l.Vaga },
        { titulo: 'Entrada', valor: (l) => l.Entrada, largura: 14 },
        { titulo: 'Saída', valor: (l) => l.Saída ?? 'No pátio', largura: 14 },
        { titulo: 'Guarda', valor: (l) => l.Guarda, largura: 24 },
        { titulo: 'Pagamento', valor: (l) => TEXTO_SITUACAO[l.Pagamento] },
        { titulo: 'Valor', valor: (l) => l.Valor },
      ],
      montarLinhas(lista),
    )
  } catch (e) {
    erro.value = mensagemDeErro(e, 'Erro ao gerar o relatório.')
  } finally {
    exportando.value = false
  }
}

watch(
  () => route.query.placa,
  (valor) => {
    placa.value = typeof valor === 'string' ? valor : ''
    placaAplicada.value = placa.value
  },
  { immediate: true },
)

onMounted(async () => {
  carregando.value = true

  try {
    await Promise.all([carregarApoio(), carregarRegistros()])
  } catch (e) {
    erro.value = mensagemDeErro(e, 'Erro ao carregar registros.')
  } finally {
    carregando.value = false
  }
})
</script>

<template>
  <div class="registros">
    <PageHeader
      titulo="Registros"
      subtitulo="Histórico de entradas e saídas. Filtre por data ou por veículo."
      :texto-botao="exportando ? 'Gerando relatório...' : 'Baixar relatório do dia (Excel)'"
      @click="baixarRelatorio"
    />

    <form class="filtros" @submit.prevent="filtrar">
      <BaseField v-model="data" rotulo="Data" tipo="date" class="campo-data" />
      <BaseField v-model="placa" rotulo="Veículo (placa)" placeholder="QHT8A14" class="campo-placa" />
      <BaseButton variante="secundario" type="submit" :disabled="carregando">Filtrar</BaseButton>
      <BaseButton
        v-if="dataAplicada || placaAplicada"
        variante="secundario"
        :disabled="carregando"
        @click="limparFiltros"
      >
        Limpar
      </BaseButton>
    </form>

    <p v-if="erro" class="erro">{{ erro }}</p>

    <ul class="resumo">
      <li v-for="item in resumo" :key="item">{{ item }}</li>
    </ul>

    <DataTable :columns="columns" :rows="linhas" :mostrar-acoes="false">
      <template #celula="{ coluna, valor, row }">
        <span v-if="coluna === 'ID'" class="apagado">{{ valor }}</span>
        <strong v-else-if="coluna === 'Placa'">{{ valor }}</strong>
        <StatusPill
          v-else-if="coluna === 'Vínculo'"
          :texto="valor"
          :variante="valor === 'Terceiro' ? 'laranja' : 'azul'"
        />
        <template v-else-if="coluna === 'Saída'">
          <StatusPill v-if="!valor" texto="No pátio" variante="amarelo" />
          <template v-else>{{ valor }}</template>
        </template>
        <template v-else-if="coluna === 'Pagamento'">
          <RouterLink
            v-if="valor === 'pago'"
            :to="{ path: '/pagamentos', query: { busca: row.ID } }"
            class="link"
          >
            Ver pagamento
          </RouterLink>
          <span v-else class="apagado">{{ TEXTO_SITUACAO[valor as SituacaoPagamento] }}</span>
        </template>
        <template v-else>{{ valor }}</template>
      </template>
    </DataTable>
  </div>
</template>

<style scoped>
.registros {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.filtros {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 12px;
}

.campo-data {
  width: 200px;
}

.campo-placa {
  width: 280px;
  max-width: 100%;
}

.resumo {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin: 0;
  padding: 0;
  list-style: none;
  color: var(--color-text-soft);
  font: 400 13px var(--font-family);
}

.apagado {
  color: var(--color-text-muted);
}

.link {
  color: var(--color-primary);
  font-weight: 500;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.erro {
  margin: 0;
  color: var(--color-error);
  font: 400 13px var(--font-family);
}
</style>
