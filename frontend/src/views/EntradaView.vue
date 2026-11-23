<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import OperacaoLayout from '@/components/OperacaoLayout.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseField from '@/components/BaseField.vue'
import BaseSelect from '@/components/BaseSelect.vue'
import StatusPill from '@/components/StatusPill.vue'
import { listarVagas, type Vaga } from '@/services/vagas'
import { buscarVeiculo, criarVeiculo, type Veiculo } from '@/services/veiculos'
import { buscarColaborador } from '@/services/colaboradores'
import { listarRegistros, registrarEntrada } from '@/services/registros'

const TIPOS_VEICULO = [
  { valor: 'CARRO', texto: 'Carro' },
  { valor: 'MOTO', texto: 'Moto' },
]

type Busca = 'inicial' | 'buscando' | 'encontrado' | 'nao-cadastrado'

const route = useRoute()
const router = useRouter()

const nomeGuarda: string = (() => {
  try {
    return JSON.parse(sessionStorage.getItem('guarda') || '{}').nome_guarda ?? ''
  } catch {
    return ''
  }
})()

const placa = ref('')
const busca = ref<Busca>('inicial')
const veiculo = ref<Veiculo | null>(null)
const descricaoVinculo = ref('')

const novoModelo = ref('')
const novaCor = ref('')
const novoTipo = ref('CARRO')
const novoDocumento = ref('')

const vagasLivres = ref<Vaga[]>([])
const vaga = ref('')

const agora = ref(new Date())
const salvando = ref(false)
const erro = ref('')

const opcoesVagas = computed(() =>
  vagasLivres.value.map((v) => ({
    valor: String(v.numero),
    texto: `Vaga ${v.numero} (livre)`,
  })),
)

const guardaEHorario = computed(() => {
  const dia = String(agora.value.getDate()).padStart(2, '0')
  const mes = String(agora.value.getMonth() + 1).padStart(2, '0')
  const hora = String(agora.value.getHours()).padStart(2, '0')
  const minuto = String(agora.value.getMinutes()).padStart(2, '0')
  return `${nomeGuarda || 'Guarda logado'}, ${dia}/${mes} às ${hora}:${minuto}`
})

const podeConfirmar = computed(() => {
  if (!vaga.value || salvando.value) return false
  if (busca.value === 'encontrado') return true
  return (
    busca.value === 'nao-cadastrado' &&
    !!novoModelo.value.trim() &&
    !!novaCor.value.trim() &&
    !!novoDocumento.value.trim()
  )
})

function normalizarPlaca(valor: string) {
  return valor.toUpperCase().replace(/[^A-Z0-9]/g, '')
}

function mensagemDeErro(e: unknown, padrao: string) {
  const resposta = (e as { response?: { status?: number; data?: { error?: string } } }).response
  return resposta?.data?.error || padrao
}

async function buscarPlaca() {
  const termo = normalizarPlaca(placa.value)
  if (!termo) return

  placa.value = termo
  busca.value = 'buscando'
  veiculo.value = null
  erro.value = ''

  try {
    const [encontrado, abertos] = await Promise.all([
      buscarVeiculo(termo),
      listarRegistros(),
    ])

    const noPatio = abertos.find((r) => r.placa === termo && !r.data_saida)
    if (noPatio) {
      erro.value = `Este veículo já está no pátio, na vaga ${noPatio.numero_vaga}.`
      busca.value = 'inicial'
      return
    }

    if (encontrado.tipo_vinculo === 'COLABORADOR' && encontrado.matricula_colaborador) {
      const colaborador = await buscarColaborador(encontrado.matricula_colaborador).catch(() => null)
      descricaoVinculo.value = `Colaborador: ${colaborador?.nome ?? 'não encontrado'}, matrícula ${encontrado.matricula_colaborador}`
    } else {
      descricaoVinculo.value = `Terceiro: documento ${encontrado.documento_responsavel ?? 'não informado'}`
    }

    veiculo.value = encontrado
    busca.value = 'encontrado'
  } catch (e) {
    const status = (e as { response?: { status?: number } }).response?.status
    if (status === 404) {
      busca.value = 'nao-cadastrado'
      return
    }
    erro.value = mensagemDeErro(e, 'Não foi possível buscar o veículo.')
    busca.value = 'inicial'
  }
}

function aoMudarPlaca() {
  if (busca.value !== 'inicial') busca.value = 'inicial'
  veiculo.value = null
}

async function confirmar() {
  if (!podeConfirmar.value) return

  salvando.value = true
  erro.value = ''

  try {
    if (busca.value === 'nao-cadastrado') {
      await criarVeiculo({
        placa: placa.value,
        modelo: novoModelo.value.trim(),
        cor: novaCor.value.trim(),
        tipo_veiculo: novoTipo.value as Veiculo['tipo_veiculo'],
        tipo_vinculo: 'TERCEIRO',
        documento_responsavel: novoDocumento.value.trim(),
      })
    }

    await registrarEntrada(Number(vaga.value), placa.value)
    router.push('/')
  } catch (e) {
    erro.value = mensagemDeErro(e, 'Não foi possível registrar a entrada.')
  } finally {
    salvando.value = false
  }
}

let relogio: ReturnType<typeof setInterval> | undefined

onMounted(async () => {
  relogio = setInterval(() => (agora.value = new Date()), 30_000)

  try {
    vagasLivres.value = (await listarVagas()).filter((v) => !v.status_vaga)
    const vagaSugerida = String(route.query.vaga ?? '')
    vaga.value = vagasLivres.value.some((v) => String(v.numero) === vagaSugerida)
      ? vagaSugerida
      : String(vagasLivres.value[0]?.numero ?? '')
    if (!vagasLivres.value.length) erro.value = 'Não existem vagas livres disponíveis.'
  } catch (e) {
    erro.value = mensagemDeErro(e, 'Não foi possível carregar as vagas.')
  }
})

onBeforeUnmount(() => clearInterval(relogio))
</script>

<template>
  <OperacaoLayout
    titulo="Registrar entrada"
    subtitulo="Busque o veículo pela placa. Se ainda não tiver cadastro, cadastre como terceiro."
    :erro="erro"
  >
    <form class="busca" @submit.prevent="buscarPlaca">
      <BaseField
        v-model="placa"
        rotulo="Placa do veículo"
        placeholder="ABC1D23"
        :maxlength="8"
        class="campo-placa"
        @update:model-value="aoMudarPlaca"
      />
      <BaseButton variante="secundario" type="submit" :disabled="busca === 'buscando'">
        {{ busca === 'buscando' ? 'Buscando...' : 'Buscar' }}
      </BaseButton>
    </form>

    <div v-if="busca === 'encontrado' && veiculo" class="resultado encontrado">
      <div class="icone" :class="veiculo.tipo_vinculo === 'TERCEIRO' ? 'terceiro' : 'colaborador'" />
      <div class="resultado-texto">
        <p class="resultado-titulo">{{ veiculo.placa }}, {{ veiculo.modelo }} {{ veiculo.cor.toLowerCase() }}</p>
        <p class="resultado-sub">{{ descricaoVinculo }}</p>
      </div>
      <StatusPill texto="Cadastrado" variante="azul-claro" />
    </div>

    <div v-else-if="busca === 'nao-cadastrado'" class="resultado nao-cadastrado">
      <div class="resultado-texto">
        <p class="resultado-titulo">Placa {{ placa }} sem cadastro</p>
        <p class="resultado-sub">Preencha os dados para cadastrar o veículo como terceiro.</p>
      </div>
      <StatusPill texto="Novo terceiro" variante="laranja" />
    </div>

    <div v-if="busca === 'nao-cadastrado'" class="grade">
      <BaseField v-model="novoModelo" rotulo="Modelo" placeholder="Fiat Argo" obrigatorio />
      <BaseField v-model="novaCor" rotulo="Cor" placeholder="Prata" obrigatorio />
      <BaseSelect v-model="novoTipo" rotulo="Tipo de veículo" :opcoes="TIPOS_VEICULO" obrigatorio />
      <BaseField
        v-model="novoDocumento"
        rotulo="Documento do responsável"
        placeholder="CPF ou RG"
        obrigatorio
      />
    </div>

    <div class="grade">
      <BaseSelect
        v-model="vaga"
        rotulo="Vaga"
        :opcoes="opcoesVagas"
        placeholder="Nenhuma vaga livre"
        dica="Só aparecem vagas livres."
        obrigatorio
      />
      <BaseField
        :model-value="guardaEHorario"
        rotulo="Guarda e horário"
        dica="Preenchido automaticamente pelo login."
        disabled
      />
    </div>

    <template #acoes>
      <BaseButton variante="secundario" :disabled="salvando" @click="router.push('/')">Cancelar</BaseButton>
      <BaseButton variante="primario" :disabled="!podeConfirmar" @click="confirmar">
        {{ salvando ? 'Registrando...' : 'Confirmar entrada' }}
      </BaseButton>
    </template>
  </OperacaoLayout>
</template>

<style scoped>
p {
  margin: 0;
}

.busca {
  display: flex;
  align-items: flex-end;
  gap: 10px;
}

.campo-placa {
  flex: 1;
}

.resultado {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  border-radius: 10px;
}

.encontrado {
  border: 1px solid #c9d9ee;
  background: #f1f6fc;
}

.nao-cadastrado {
  border: 1px solid #f1d3a8;
  background: var(--color-aviso-bg);
}

.icone {
  flex: none;
  width: 44px;
  height: 44px;
  border-radius: 10px;
}

.icone.colaborador {
  background: var(--color-vaga-colaborador);
}

.icone.terceiro {
  background: var(--color-vaga-terceiro);
}

.resultado-texto {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.resultado-titulo {
  font-size: 15px;
  font-weight: 600;
}

.resultado-sub {
  color: var(--color-text-soft);
  font-size: 13px;
}

.grade {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}
</style>
