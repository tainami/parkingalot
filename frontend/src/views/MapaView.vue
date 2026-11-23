
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import PageHeader from '@/components/PageHeader.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseField from '@/components/BaseField.vue'
import StatusPill from '@/components/StatusPill.vue'

interface Vaga {
  numero: number
  tipo_vaga: string
  status_vaga: boolean
}

interface Veiculo {
  placa: string
  modelo: string
  cor: string
  tipo_veiculo: string
  tipo_vinculo: string
  matricula_colaborador: number | null
  documento_responsavel: string | null
}

interface Registro {
  id_registro: number
  numero_vaga: number
  placa: string
  cpf_guarda: string
  data_entrada: string
  data_saida: string | null
}

interface Colaborador {
  matricula: number
  nome: string
  setor: string
  cargo: string
}

const vagas = ref<Vaga[]>([])
const veiculos = ref<Veiculo[]>([])
const registros = ref<Registro[]>([])
const colaboradores = ref<Colaborador[]>([])

const carregando = ref(false)
const salvando = ref(false)
const erro = ref('')

const busca = ref('')
const filtro = ref('TODAS')
const vagaSelecionada = ref<number | null>(null)

const modalEntrada = ref(false)
const numeroVagaEntrada = ref<number | null>(null)
const placaEntrada = ref('')

const vagasDoMapa = computed(() => {
  return Array.from({ length: 48 }, (_, index) => {
    const numero = index + 1
    const letra = String.fromCharCode(65 + Math.floor(index / 8))
    const coluna = String(index % 8 + 1).padStart(2, '0')

    return {
      numero,
      codigo: `${letra}${coluna}`,
      vaga: vagas.value.find(item => item.numero === numero)
    }
  })
})

const veiculosAtivos = computed(() =>
  registros.value.filter(registro => !registro.data_saida)
)

const vagasLivres = computed(() =>
  vagas.value.filter(vaga => !vaga.status_vaga)
)

const vagasFiltradas = computed(() => {
  const termo = busca.value.trim().toUpperCase()

  return vagasDoMapa.value.filter(item => {
    const registro = veiculosAtivos.value.find(
      registro => registro.numero_vaga === item.numero
    )

    const correspondeBusca =
      !termo ||
      item.codigo.includes(termo) ||
      String(item.numero).includes(termo) ||
      (registro?.placa || '').toUpperCase().includes(termo)

    const status = !item.vaga
      ? 'NAO_CADASTRADAS'
      : item.vaga.status_vaga
        ? 'OCUPADAS'
        : 'LIVRES'

    const correspondeFiltro =
      filtro.value === 'TODAS' || filtro.value === status

    return correspondeBusca && correspondeFiltro
  })
})

const fileiras = computed(() => {
  return ['A', 'B', 'C', 'D', 'E', 'F'].map(letra =>
    vagasFiltradas.value.filter(item => item.codigo.startsWith(letra))
  )
})

const vagaAtual = computed(() =>
  vagasDoMapa.value.find(item => item.numero === vagaSelecionada.value) || null
)

const registroSelecionado = computed(() => {
  if (!vagaAtual.value) return null

  return veiculosAtivos.value.find(
    registro => registro.numero_vaga === vagaAtual.value?.numero
  ) || null
})

const veiculoSelecionado = computed(() => {
  if (!registroSelecionado.value) return null

  return veiculos.value.find(
    veiculo => veiculo.placa === registroSelecionado.value?.placa
  ) || null
})

const colaboradorSelecionado = computed(() => {
  const matricula = veiculoSelecionado.value?.matricula_colaborador

  if (!matricula) return null

  return colaboradores.value.find(
    colaborador => colaborador.matricula === matricula
  ) || null
})

const historico = computed(() =>
  [...registros.value]
    .sort((a, b) =>
      new Date(b.data_entrada).getTime() -
      new Date(a.data_entrada).getTime()
    )
    .slice(0, 8)
)

const contadorLivres = computed(() =>
  vagas.value.filter(vaga => !vaga.status_vaga).length
)

const contadorColaboradores = computed(() =>
  vagas.value.filter(vaga =>
    vaga.status_vaga && vaga.tipo_vaga === 'COLABORADOR'
  ).length
)

const contadorTerceiros = computed(() =>
  vagas.value.filter(vaga =>
    vaga.status_vaga && vaga.tipo_vaga === 'TERCEIRO'
  ).length
)

function classeVaga(numero: number) {
  const vaga = vagas.value.find(item => item.numero === numero)

  if (!vaga) return 'nao-cadastrada'
  if (!vaga.status_vaga) return 'livre'

  return vaga.tipo_vaga === 'TERCEIRO'
    ? 'terceiro'
    : 'colaborador'
}

function varianteStatus(numero: number) {
  const vaga = vagas.value.find(item => item.numero === numero)

  if (!vaga || !vaga.status_vaga) return 'cinza'

  return vaga.tipo_vaga === 'TERCEIRO'
    ? 'laranja'
    : 'azul'
}

function textoStatus(numero: number) {
  const vaga = vagas.value.find(item => item.numero === numero)

  if (!vaga) return '—'
  return vaga.status_vaga ? 'Ocupada' : 'Livre'
}

function selecionarVaga(numero: number) {
  vagaSelecionada.value = numero
}

function formatarData(data: string | null | undefined) {
  if (!data) return '—'

  const dataObj = new Date(data)

  if (Number.isNaN(dataObj.getTime())) return '—'

  return dataObj.toLocaleString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function nomeResponsavel() {
  const veiculo = veiculoSelecionado.value

  if (!veiculo) return '—'

  if (veiculo.tipo_vinculo === 'COLABORADOR') {
    return colaboradorSelecionado.value?.nome ||
      (veiculo.matricula_colaborador
        ? `Matrícula ${veiculo.matricula_colaborador}`
        : 'Não informado')
  }

  return veiculo.documento_responsavel || 'Não informado'
}

function abrirEntrada() {
  if (vagasLivres.value.length === 0) {
    erro.value = 'Não existem vagas livres disponíveis.'
    return
  }

  const vagaEscolhida = vagasLivres.value.find(
    vaga => vaga.numero === vagaSelecionada.value
  )

  numeroVagaEntrada.value =
    vagaEscolhida?.numero ?? vagasLivres.value[0]?.numero ?? null

  placaEntrada.value = ''
  erro.value = ''
  modalEntrada.value = true
}

async function carregarDados() {
  carregando.value = true
  erro.value = ''

  try {
    const [resVagas, resVeiculos, resRegistros, resColaboradores] =
      await Promise.all([
        api.get('/vagas/'),
        api.get('/veiculos/'),
        api.get('/registros/'),
        api.get('/colaboradores/')
      ])

    vagas.value = resVagas.data
    veiculos.value = resVeiculos.data
    registros.value = resRegistros.data
    colaboradores.value = resColaboradores.data

    if (
      vagaSelecionada.value === null ||
      !vagas.value.some(vaga => vaga.numero === vagaSelecionada.value)
    ) {
      vagaSelecionada.value =
        vagas.value.find(vaga => vaga.status_vaga)?.numero ??
        vagas.value[0]?.numero ??
        null
    }
  } catch (e: any) {
    erro.value =
      e.response?.data?.error ||
      'Não foi possível carregar os dados do mapa.'
  } finally {
    carregando.value = false
  }
}

async function registrarEntrada() {
  if (!numeroVagaEntrada.value || !placaEntrada.value.trim()) {
    erro.value = 'Selecione uma vaga e informe a placa.'
    return
  }

  salvando.value = true
  erro.value = ''

  try {
    await api.post('/registros/', {
      numero_vaga: numeroVagaEntrada.value,
      placa: placaEntrada.value.trim().toUpperCase()
    })

    vagaSelecionada.value = numeroVagaEntrada.value
    modalEntrada.value = false

    await carregarDados()
  } catch (e: any) {
    erro.value =
      e.response?.data?.error ||
      'Não foi possível registrar a entrada.'
  } finally {
    salvando.value = false
  }
}

async function registrarSaida() {
  if (!registroSelecionado.value) return

  if (!window.confirm('Deseja realmente registrar a saída deste veículo?')) {
    return
  }

  salvando.value = true
  erro.value = ''

  try {
    await api.put(
      `/registros/${registroSelecionado.value.id_registro}/saida`
    )

    await carregarDados()
  } catch (e: any) {
    erro.value =
      e.response?.data?.error ||
      'Não foi possível registrar a saída.'
  } finally {
    salvando.value = false
  }
}

onMounted(carregarDados)
</script>

<template>
  <div class="mapa-page">
    <PageHeader
      titulo="Mapa de vagas"
      subtitulo="Acompanhe a ocupação do estacionamento em tempo real."
      texto-botao="+ Nova entrada"
      variante-botao="primario"
      @click="abrirEntrada"
    />

    <div class="barra-ferramentas">
      <div class="busca">
        <BaseField
          v-model="busca"
          rotulo="Buscar"
          placeholder="Placa do veículo ou código da vaga"
          tipo="search"
        />
      </div>

      <div class="filtros">
        <button
          v-for="opcao in [
            { valor: 'TODAS', texto: 'Todas' },
            { valor: 'LIVRES', texto: 'Livres' },
            { valor: 'OCUPADAS', texto: 'Ocupadas' }
          ]"
          :key="opcao.valor"
          :class="{ ativo: filtro === opcao.valor }"
          @click="filtro = opcao.valor"
        >
          {{ opcao.texto }}
        </button>
      </div>
    </div>

    <div v-if="erro" class="mensagem-erro">
      {{ erro }}
      <button @click="erro = ''">×</button>
    </div>

    <div v-if="carregando" class="estado-carregamento">
      Carregando informações do estacionamento...
    </div>

    <template v-else>
      <div class="resumo-vagas">
        <div class="resumo-item">
          <span class="indicador indicador-azul"></span>
          <span>Colaboradores</span>
          <strong>{{ contadorColaboradores }}</strong>
        </div>

        <div class="resumo-item">
          <span class="indicador indicador-laranja"></span>
          <span>Terceiros</span>
          <strong>{{ contadorTerceiros }}</strong>
        </div>

        <div class="resumo-item">
          <span class="indicador indicador-cinza"></span>
          <span>Livres</span>
          <strong>{{ contadorLivres }}</strong>
        </div>
      </div>

      <div class="conteudo-mapa">
        <section class="mapa-card">
          <div class="secao-titulo">
            <div>
              <h2>Estacionamento</h2>
              <p>Selecione uma vaga para visualizar os detalhes.</p>
            </div>
          </div>

          <div class="legenda">
            <span><i class="legenda-azul"></i> Colaboradores</span>
            <span><i class="legenda-laranja"></i> Terceiros</span>
            <span><i class="legenda-cinza"></i> Livres</span>
          </div>

          <div class="estacionamento">
            <div
              v-for="(fileira, index) in fileiras"
              :key="index"
              class="fileira"
            >
              <div class="identificacao-fileira">
                {{ String.fromCharCode(65 + index) }}
              </div>

              <div class="vagas-fileira">
                <button
                  v-for="item in fileira"
                  :key="item.numero"
                  class="vaga"
                  :class="[
                    classeVaga(item.numero),
                    { selecionada: vagaSelecionada === item.numero }
                  ]"
                  @click="selecionarVaga(item.numero)"
                >
                  <span>{{ item.codigo }}</span>
                  <small>{{ textoStatus(item.numero) }}</small>
                </button>
              </div>
            </div>
          </div>

          <div v-if="vagasFiltradas.length === 0" class="aviso-vazio">
            Nenhuma vaga encontrada para essa busca ou filtro.
          </div>
        </section>

        <aside class="painel-lateral">
          <section class="detalhes-card">
            <div class="secao-titulo">
              <div>
                <h2>Detalhes da vaga</h2>
                <p>Informações da posição selecionada.</p>
              </div>
            </div>

            <template v-if="vagaAtual">
              <div class="vaga-destaque">
                <div>
                  <span class="rotulo">Vaga selecionada</span>
                  <h3>{{ vagaAtual.codigo }}</h3>
                </div>

                <StatusPill
                  :texto="textoStatus(vagaAtual.numero)"
                  :variante="varianteStatus(vagaAtual.numero)"
                />
              </div>

              <template v-if="registroSelecionado && veiculoSelecionado">
                <div class="detalhes-lista">
                  <div class="detalhe">
                    <span>Placa</span>
                    <strong>{{ veiculoSelecionado.placa }}</strong>
                  </div>

                  <div class="detalhe">
                    <span>Modelo</span>
                    <strong>{{ veiculoSelecionado.modelo }}</strong>
                  </div>

                  <div class="detalhe">
                    <span>Cor</span>
                    <strong>{{ veiculoSelecionado.cor }}</strong>
                  </div>

                  <div class="detalhe">
                    <span>Tipo de veículo</span>
                    <strong>{{ veiculoSelecionado.tipo_veiculo }}</strong>
                  </div>

                  <div class="detalhe">
                    <span>Vínculo</span>
                    <strong>{{ veiculoSelecionado.tipo_vinculo }}</strong>
                  </div>

                  <div class="detalhe">
                    <span>Responsável</span>
                    <strong>{{ nomeResponsavel() }}</strong>
                  </div>

                  <div class="detalhe">
                    <span>Entrada</span>
                    <strong>{{ formatarData(registroSelecionado.data_entrada) }}</strong>
                  </div>

                  <div class="detalhe">
                    <span>CPF do guarda</span>
                    <strong>{{ registroSelecionado.cpf_guarda }}</strong>
                  </div>
                </div>

                <p
                  v-if="veiculoSelecionado.tipo_vinculo === 'TERCEIRO'"
                  class="observacao-terceiro"
                >
                  Veículo de terceiro. Consulte o registro para informações de pagamento.
                </p>

                <BaseButton
                  variante="contorno"
                  :disabled="salvando"
                  @click="registrarSaida"
                >
                  Registrar saída
                </BaseButton>
              </template>

              <div
                v-else-if="vagaAtual.vaga && !vagaAtual.vaga.status_vaga"
                class="detalhes-vazio"
              >
                <span class="icone-vazio">✓</span>
                <strong>Esta vaga está livre</strong>
                <p>
                  Você pode selecionar esta posição ao registrar uma nova entrada.
                </p>
                <BaseButton variante="primario" @click="abrirEntrada">
                  Nova entrada
                </BaseButton>
              </div>

              <div v-else class="detalhes-vazio">
                <strong>Selecione uma vaga disponível</strong>
                <p>As informações aparecerão aqui quando houver dados da vaga.</p>
              </div>
            </template>

            <div v-else class="detalhes-vazio">
              <strong>Nenhuma vaga selecionada</strong>
              <p>
                Selecione uma posição no mapa para visualizar os detalhes.
              </p>
            </div>
          </section>

          <section class="historico-card">
            <div class="secao-titulo">
              <div>
                <h2>Últimas movimentações</h2>
                <p>Registros recentes do estacionamento.</p>
              </div>
            </div>

            <div v-if="historico.length === 0" class="historico-vazio">
              Nenhuma movimentação registrada.
            </div>

            <div v-else class="historico-lista">
              <div
                v-for="registro in historico"
                :key="registro.id_registro"
                class="historico-item"
              >
                <div class="historico-icone">
                  {{ registro.data_saida ? '↗' : '↘' }}
                </div>

                <div class="historico-info">
                  <strong>{{ registro.placa }}</strong>
                  <span>
                    {{ registro.data_saida ? 'Saída' : 'Entrada' }}
                    · Vaga {{ registro.numero_vaga }}
                  </span>
                </div>

                <StatusPill
                  :texto="registro.data_saida ? 'Saiu' : 'No local'"
                  :variante="registro.data_saida ? 'cinza' : 'azul-claro'"
                />
              </div>
            </div>
          </section>
        </aside>
      </div>
    </template>

    <div
      v-if="modalEntrada"
      class="modal-fundo"
      @click.self="modalEntrada = false"
    >
      <div class="modal">
        <div class="modal-cabecalho">
          <div>
            <h2>Registrar entrada</h2>
            <p>Informe o veículo e a vaga de estacionamento.</p>
          </div>

          <button class="fechar-modal" @click="modalEntrada = false">
            ×
          </button>
        </div>

        <form @submit.prevent="registrarEntrada">
          <label for="vaga-entrada">Vaga disponível</label>

          <select
            id="vaga-entrada"
            v-model.number="numeroVagaEntrada"
            required
          >
            <option
              v-for="vaga in vagasLivres"
              :key="vaga.numero"
              :value="vaga.numero"
            >
              {{ String.fromCharCode(65 + Math.floor((vaga.numero - 1) / 8)) }}{{ String((vaga.numero - 1) % 8 + 1).padStart(2, '0') }}
              — Vaga {{ vaga.numero }}
            </option>
          </select>

          <BaseField
            v-model="placaEntrada"
            rotulo="Placa do veículo"
            placeholder="Digite a placa"
            obrigatorio
          />

          <div class="modal-acoes">
            <BaseButton
              variante="secundario"
              @click="modalEntrada = false"
            >
              Cancelar
            </BaseButton>

            <BaseButton
              variante="primario"
              :disabled="salvando || !placaEntrada.trim()"
              @click="registrarEntrada"
            >
              {{ salvando ? 'Registrando...' : 'Confirmar entrada' }}
            </BaseButton>
          </div>
        </form>
      </div>
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

.barra-ferramentas {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
}

.busca {
  width: min(430px, 100%);
}

.filtros {
  display: flex;
  gap: 7px;
}

.filtros button {
  padding: 9px 15px;
  border: 1px solid var(--color-border);
  border-radius: 7px;
  background: var(--color-surface);
  color: var(--color-text-muted);
  font-size: 12px;
  cursor: pointer;
}

.filtros button.ativo {
  border-color: var(--color-primary);
  background: #edf3ff;
  color: var(--color-primary);
  font-weight: 600;
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

.estado-carregamento,
.aviso-vazio,
.historico-vazio {
  padding: 24px;
  color: var(--color-text-muted);
  text-align: center;
  font-size: 13px;
}

.resumo-vagas {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 24px;
  padding: 14px 17px;
  border: 1px solid var(--color-border);
  border-radius: 9px;
  background: var(--color-surface);
}

.resumo-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--color-text-muted);
  font-size: 12px;
}

.resumo-item strong {
  color: var(--color-text);
  font-size: 13px;
}

.indicador {
  width: 9px;
  height: 9px;
  border-radius: 50%;
}

.indicador-azul {
  background: #3478df;
}

.indicador-laranja {
  background: #ed9a3e;
}

.indicador-cinza {
  background: #b9c0ca;
}

.conteudo-mapa {
  display: grid;
  grid-template-columns: minmax(0, 1.55fr) minmax(300px, .9fr);
  align-items: start;
  gap: 18px;
}

.mapa-card,
.detalhes-card,
.historico-card {
  min-width: 0;
  padding: 19px;
  border: 1px solid var(--color-border);
  border-radius: 9px;
  background: var(--color-surface);
}

.painel-lateral {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.secao-titulo {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 17px;
}

.secao-titulo h2 {
  margin: 0 0 5px;
  color: var(--color-text);
  font-size: 15px;
  font-weight: 700;
}

.secao-titulo p {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 12px;
}

.legenda {
  display: flex;
  flex-wrap: wrap;
  gap: 13px;
  padding: 12px 0 17px;
  border-bottom: 1px solid var(--color-border);
}

.legenda span {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--color-text-muted);
  font-size: 10px;
}

.legenda i {
  width: 9px;
  height: 9px;
  border-radius: 3px;
}

.legenda-azul {
  background: #3478df;
}

.legenda-laranja {
  background: #ed9a3e;
}

.legenda-cinza {
  background: #b9c0ca;
}

.estacionamento {
  display: flex;
  flex-direction: column;
  gap: 13px;
  padding: 20px 0 8px;
}

.fileira {
  display: flex;
  align-items: center;
  gap: 11px;
}

.identificacao-fileira {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 23px;
  height: 23px;
  border-radius: 5px;
  background: var(--color-bg);
  color: var(--color-text-muted);
  font-size: 11px;
  font-weight: 700;
}

.vagas-fileira {
  display: grid;
  grid-template-columns: repeat(8, minmax(0, 1fr));
  gap: 7px;
  width: 100%;
}

.vaga {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 0;
  min-height: 58px;
  padding: 5px 2px;
  border: 1px solid #dce2ea;
  border-radius: 6px;
  background: #fafbfc;
  color: #aeb6c2;
  cursor: pointer;
  transition: transform .15s, border .15s;
}

.vaga:hover {
  transform: translateY(-2px);
  border-color: var(--color-primary);
}

.vaga span {
  font-size: 11px;
  font-weight: 700;
}

.vaga small {
  margin-top: 4px;
  font-size: 9px;
}

.vaga.colaborador {
  border-color: #3478df;
  background: #eaf2ff;
  color: #2463d3;
}

.vaga.terceiro {
  border-color: #edaa62;
  background: #fff2e3;
  color: #b86b1c;
}

.vaga.livre {
  border-color: #dce2ea;
  background: #f0f2f5;
  color: #707b8b;
}

.vaga.nao-cadastrada {
  border-style: dashed;
}

.vaga.selecionada {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.vaga-destaque {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 13px;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-bg);
}

.rotulo {
  color: var(--color-text-muted);
  font-size: 10px;
}

.vaga-destaque h3 {
  margin: 4px 0 0;
  color: var(--color-text);
  font-size: 25px;
}

.detalhes-lista {
  display: flex;
  flex-direction: column;
  margin-top: 12px;
}

.detalhe {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid var(--color-border);
}

.detalhe span {
  color: var(--color-text-muted);
  font-size: 11px;
}

.detalhe strong {
  color: var(--color-text);
  font-size: 11px;
  font-weight: 600;
  text-align: right;
  overflow-wrap: anywhere;
}

.observacao-terceiro {
  margin: 13px 0;
  padding: 10px;
  border-radius: 6px;
  background: #fff6eb;
  color: #a86622;
  font-size: 11px;
  line-height: 1.5;
}

.detalhes-vazio {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 9px;
  padding: 27px 12px;
  color: var(--color-text-muted);
  text-align: center;
}

.detalhes-vazio strong {
  color: var(--color-text);
  font-size: 13px;
}

.detalhes-vazio p {
  max-width: 240px;
  margin: 0 0 8px;
  font-size: 11px;
  line-height: 1.5;
}

.icone-vazio {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #edf5ef;
  color: #36824c;
  font-size: 18px;
}

.historico-lista {
  display: flex;
  flex-direction: column;
}

.historico-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 0;
  border-bottom: 1px solid var(--color-border);
}

.historico-item:last-child {
  border-bottom: none;
}

.historico-icone {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 29px;
  height: 29px;
  border-radius: 50%;
  background: #edf3ff;
  color: #3478df;
  font-size: 16px;
}

.historico-info {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}

.historico-info strong {
  color: var(--color-text);
  font-size: 11px;
}

.historico-info span {
  color: var(--color-text-muted);
  font-size: 10px;
}

.modal-fundo {
  position: fixed;
  z-index: 1000;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: rgba(20, 30, 45, .48);
}

.modal {
  width: 100%;
  max-width: 440px;
  padding: 23px;
  border-radius: 11px;
  background: var(--color-surface);
  box-shadow: 0 15px 50px rgba(0, 0, 0, .17);
}

.modal-cabecalho {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 22px;
}

.modal-cabecalho h2 {
  margin: 0 0 5px;
  color: var(--color-text);
  font-size: 18px;
}

.modal-cabecalho p {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 12px;
}

.fechar-modal {
  border: none;
  background: none;
  color: var(--color-text-muted);
  font-size: 25px;
  cursor: pointer;
}

.modal form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.modal label {
  margin-top: 7px;
  color: var(--color-text);
  font-size: 12px;
  font-weight: 600;
}

.modal select {
  width: 100%;
  height: 42px;
  padding: 0 11px;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-surface);
  color: var(--color-text);
  font-size: 12px;
  outline-color: var(--color-primary);
}

.modal-acoes {
  display: flex;
  justify-content: flex-end;
  gap: 9px;
  margin-top: 12px;
}

@media (max-width: 1050px) {
  .conteudo-mapa {
    grid-template-columns: 1fr;
  }

  .painel-lateral {
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-items: start;
  }
}

@media (max-width: 700px) {
  .barra-ferramentas {
    align-items: stretch;
    flex-direction: column;
  }

  .busca {
    width: 100%;
  }

  .filtros {
    overflow-x: auto;
  }

  .resumo-vagas {
    gap: 13px;
  }

  .painel-lateral {
    display: flex;
  }

  .mapa-card {
    padding: 13px;
  }

  .vagas-fileira {
    gap: 4px;
  }

  .vaga {
    min-height: 49px;
  }

  .vaga span {
    font-size: 9px;
  }

  .vaga small {
    font-size: 8px;
  }

  .legenda {
    gap: 9px;
  }
}
</style>
