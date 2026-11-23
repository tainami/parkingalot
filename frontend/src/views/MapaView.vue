<script setup lang="ts">
import { computed, nextTick, onMounted, ref, useTemplateRef } from 'vue'
import { useRouter } from 'vue-router'
import PageHeader from '@/components/PageHeader.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseField from '@/components/BaseField.vue'
import ParkingMap from '@/components/ParkingMap.vue'
import SpotDetailsPanel from '@/components/SpotDetailsPanel.vue'
import { listarVagas, type Vaga } from '@/services/vagas'
import { listarVeiculos, type Veiculo } from '@/services/veiculos'
import {
  listarRegistros,
  type Registro,
} from '@/services/registros'
import { listarColaboradores, type Colaborador } from '@/services/colaboradores'
import { listarGuardas } from '@/services/guardas'
import { formatarDataHora, formatarHora } from '@/utils/formatar'
import type { FiltroVagas, Movimentacao, OcupacaoVaga, VagaMapa } from '@/types/mapa'

const FILTROS: { valor: FiltroVagas; texto: string }[] = [
  { valor: 'todas', texto: 'Todas' },
  { valor: 'livre', texto: 'Livres' },
  { valor: 'ocupada', texto: 'Ocupadas' },
]

const router = useRouter()

const vagas = ref<Vaga[]>([])
const veiculos = ref(new Map<string, Veiculo>())
const registros = ref<Registro[]>([])
const colaboradores = ref(new Map<number, Colaborador>())
const guardas = ref(new Map<string, string>())

const carregando = ref(false)
const erro = ref('')

const busca = ref('')
const filtro = ref<FiltroVagas>('todas')
const selecionada = ref<number | null>(null)

const registrosAbertos = computed(
  () => new Map(registros.value.filter((r) => !r.data_saida).map((r) => [r.numero_vaga, r])),
)

const vagasDoMapa = computed<VagaMapa[]>(() =>
  vagas.value.map((vaga) => ({
    numero: vaga.numero,
    estado: !vaga.status_vaga ? 'livre' : vaga.tipo_vaga === 'TERCEIRO' ? 'terceiro' : 'colaborador',
  })),
)

const contagem = computed(() => ({
  colaboradores: vagasDoMapa.value.filter((v) => v.estado === 'colaborador').length,
  terceiros: vagasDoMapa.value.filter((v) => v.estado === 'terceiro').length,
  livres: vagasDoMapa.value.filter((v) => v.estado === 'livre').length,
}))

const vagaSelecionada = computed(
  () => vagasDoMapa.value.find((v) => v.numero === selecionada.value) ?? null,
)

const registroSelecionado = computed(() => {
  if (selecionada.value === null) return null
  return registrosAbertos.value.get(selecionada.value) ?? null
})

const ocupacao = computed<OcupacaoVaga | null>(() => {
  const registro = registroSelecionado.value
  const veiculo = registro ? veiculos.value.get(registro.placa) : undefined
  if (!registro || !veiculo) return null

  const colaborador = veiculo.matricula_colaborador
    ? colaboradores.value.get(veiculo.matricula_colaborador)
    : undefined
  const terceiro = veiculo.tipo_vinculo === 'TERCEIRO'

  return {
    placa: veiculo.placa,
    veiculo: `${veiculo.modelo}, ${veiculo.cor.toLowerCase()}`,
    vinculo: terceiro ? 'Terceiro' : `Colaborador (mat. ${veiculo.matricula_colaborador})`,
    responsavel: terceiro
      ? veiculo.documento_responsavel || 'Não informado'
      : colaborador?.nome || 'Não informado',
    entrada: formatarDataHora(registro.data_entrada),
    guarda: guardas.value.get(registro.cpf_guarda) ?? registro.cpf_guarda,
  }
})

const movimentacoes = computed<Movimentacao[]>(() =>
  registros.value
    .flatMap((r) => {
      const eventos = [{ placa: r.placa, descricao: `entrou na vaga ${r.numero_vaga}`, momento: r.data_entrada }]
      if (r.data_saida) eventos.push({ placa: r.placa, descricao: `saiu da vaga ${r.numero_vaga}`, momento: r.data_saida })
      return eventos
    })
    .sort((a, b) => Date.parse(b.momento) - Date.parse(a.momento))
    .slice(0, 3)
    .map(({ placa, descricao, momento }) => ({ placa, descricao, hora: formatarHora(momento) })),
)

const mapa = useTemplateRef<InstanceType<typeof ParkingMap>>('mapa')

async function limparSelecao() {
  const numero = selecionada.value
  selecionada.value = null
  if (numero === null) return

  await nextTick()
  mapa.value?.focarVaga(numero)
}

function mensagemDeErro(e: unknown, padrao: string) {
  const resposta = (e as { response?: { data?: { error?: string } } }).response
  return resposta?.data?.error || padrao
}

function buscarVaga() {
  const termo = busca.value.trim().toUpperCase().replace(/[^A-Z0-9]/g, '')
  if (!termo) return

  if (/^\d+$/.test(termo) && vagas.value.some((v) => v.numero === Number(termo))) {
    selecionada.value = Number(termo)
    return
  }

  const registro = [...registrosAbertos.value.values()].find((r) => r.placa === termo)
  if (registro) {
    selecionada.value = registro.numero_vaga
    return
  }

  erro.value = `Nenhuma vaga ou veículo no pátio encontrado para "${busca.value.trim()}".`
}

function abrirEntrada(numero?: number) {
  router.push({ path: '/entrada', query: numero ? { vaga: String(numero) } : {} })
}

async function carregarDados() {
  carregando.value = true
  erro.value = ''

  try {
    const [listaVagas, listaVeiculos, listaRegistros, listaColaboradores, listaGuardas] =
      await Promise.all([
        listarVagas(),
        listarVeiculos(),
        listarRegistros(),
        listarColaboradores(),
        listarGuardas(),
      ])

    vagas.value = listaVagas
    veiculos.value = new Map(listaVeiculos.map((v) => [v.placa, v]))
    registros.value = listaRegistros
    colaboradores.value = new Map(listaColaboradores.map((c) => [c.matricula, c]))
    guardas.value = new Map(listaGuardas.map((g) => [g.cpf_guarda, g.nome_guarda]))
  } catch (e) {
    erro.value = mensagemDeErro(e, 'Não foi possível carregar os dados do mapa.')
  } finally {
    carregando.value = false
  }
}

function irParaSaida() {
  if (registroSelecionado.value) router.push(`/saida/${registroSelecionado.value.id_registro}`)
}

onMounted(carregarDados)
</script>

<template>
  <div class="mapa-page">
    <PageHeader titulo="Mapa de vagas" subtitulo="Acompanhe a ocupação do estacionamento em tempo real." />

    <div class="barra">
      <form class="busca" role="search" @submit.prevent="buscarVaga">
        <BaseField
          v-model="busca"
          rotulo="Buscar por placa ou vaga"
          tipo="search"
          placeholder="Placa do veículo ou número da vaga"
        />
      </form>
      <BaseButton variante="contorno" icone @click="abrirEntrada()">Nova entrada</BaseButton>
    </div>

    <div v-if="erro" class="mensagem-erro" role="alert">
      {{ erro }}
      <button type="button" aria-label="Fechar mensagem" @click="erro = ''">×</button>
    </div>

    <div v-if="carregando && !vagas.length" class="estado-carregamento">
      Carregando informações do estacionamento...
    </div>

    <div v-else class="conteudo">
      <section class="vagas" aria-label="Vagas">
        <div class="controles">
          <div class="filtros" role="group" aria-label="Filtrar vagas">
            <button
              v-for="opcao in FILTROS"
              :key="opcao.valor"
              type="button"
              :aria-pressed="filtro === opcao.valor"
              @click="filtro = opcao.valor"
            >
              {{ opcao.texto }}
            </button>
          </div>

          <div class="legenda">
            <span><i class="ponto colaborador" />{{ contagem.colaboradores }} colaboradores</span>
            <span><i class="ponto terceiro" />{{ contagem.terceiros }} terceiros</span>
            <span><i class="ponto livre" />{{ contagem.livres }} livres</span>
          </div>
        </div>

        <ParkingMap ref="mapa" v-model:selecionada="selecionada" :vagas="vagasDoMapa" :filtro="filtro" />
      </section>

      <SpotDetailsPanel
        class="painel"
        :vaga="vagaSelecionada"
        :ocupacao="ocupacao"
        :total-vagas="vagas.length"
        :vagas-ocupadas="vagas.length - contagem.livres"
        :movimentacoes="movimentacoes"
        @limpar-selecao="limparSelecao"
        @registrar-entrada="abrirEntrada"
        @registrar-saida="irParaSaida"
      />
    </div>

  </div>
</template>

<style scoped>
.mapa-page {
  display: flex;
  flex-direction: column;
  gap: 22px;
  color: var(--color-text);
}

.barra {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 14px;
}

.busca {
  flex: 0 1 380px;
}

.conteudo {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  gap: 24px;
}

.vagas {
  flex: 999 1 560px;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.painel {
  flex: 1 1 var(--largura-painel);
  max-width: var(--largura-painel);
}

@media (max-width: 960px) {
  .painel {
    max-width: none;
  }
}

.controles {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px 20px;
}

.filtros {
  display: flex;
  gap: 4px;
  padding: 4px;
  border-radius: 10px;
  background: var(--color-bg);
}

.filtros button {
  min-height: 40px;
  padding: 0 16px;
  border: 0;
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--color-text);
  font: 500 14px var(--font-family);
  cursor: pointer;
}

.filtros button[aria-pressed='true'] {
  background: var(--color-text);
  color: var(--color-surface);
}

.legenda {
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  font: 500 14px var(--font-family);
}

.legenda span {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.ponto {
  width: 14px;
  height: 14px;
  border-radius: 50%;
}

.ponto.colaborador {
  background: var(--color-vaga-colaborador);
}

.ponto.terceiro {
  background: var(--color-vaga-terceiro);
}

.ponto.livre {
  background: var(--color-vaga-livre);
}

.mensagem-erro {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 11px 14px;
  border: 1px solid #f2caca;
  border-radius: 7px;
  background: #fff3f3;
  color: #b42318;
  font-size: 13px;
}

.mensagem-erro button {
  border: none;
  background: none;
  color: inherit;
  font-size: 20px;
  cursor: pointer;
}

.estado-carregamento {
  padding: 24px;
  color: var(--color-text-muted);
  text-align: center;
  font-size: 13px;
}










</style>
