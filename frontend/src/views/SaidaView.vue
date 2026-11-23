<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import OperacaoLayout from '@/components/OperacaoLayout.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseSelect from '@/components/BaseSelect.vue'
import StatusPill from '@/components/StatusPill.vue'
import { buscarRegistro, registrarSaida, type Registro } from '@/services/registros'
import { buscarVeiculo, type Veiculo } from '@/services/veiculos'
import { buscarColaborador } from '@/services/colaboradores'
import { buscarGuarda } from '@/services/guardas'
import { criarPagamento } from '@/services/pagamentos'
import { formatarDuracao, formatarMoeda, paraDataLocal } from '@/utils/formatar'
import { calcularValorEstimado, MINUTOS_GRATIS, TARIFA_POR_HORA } from '@/utils/pagamento'

const props = defineProps<{ idRegistro: number }>()

const FORMAS_PAGAMENTO = [
  { valor: 'Débito', texto: 'Débito' },
  { valor: 'Crédito', texto: 'Crédito' },
  { valor: 'Pix', texto: 'Pix' },
  { valor: 'Dinheiro', texto: 'Dinheiro' },
]

const router = useRouter()

const registro = ref<Registro | null>(null)
const veiculo = ref<Veiculo | null>(null)
const responsavel = ref('')
const guarda = ref('')
const formaPagamento = ref('')

const agora = ref(new Date())
const carregando = ref(true)
const salvando = ref(false)
const erro = ref('')

const terceiro = computed(() => veiculo.value?.tipo_vinculo === 'TERCEIRO')

const entrada = computed(() => (registro.value ? paraDataLocal(registro.value.data_entrada) : null))

const saida = computed(() =>
  registro.value?.data_saida ? paraDataLocal(registro.value.data_saida) : agora.value,
)

const minutosPermanencia = computed(() =>
  entrada.value ? (saida.value.getTime() - entrada.value.getTime()) / 60000 : 0,
)

const valorEstimado = computed(() => calcularValorEstimado(minutosPermanencia.value))

function formatarMomento(data: Date) {
  const dia = String(data.getDate()).padStart(2, '0')
  const mes = String(data.getMonth() + 1).padStart(2, '0')
  const hora = String(data.getHours()).padStart(2, '0')
  const minuto = String(data.getMinutes()).padStart(2, '0')
  return `${dia}/${mes} às ${hora}:${minuto}`
}

function mensagemDeErro(e: unknown, padrao: string) {
  const resposta = (e as { response?: { data?: { error?: string } } }).response
  return resposta?.data?.error || padrao
}

async function carregar() {
  try {
    const dadosRegistro = await buscarRegistro(props.idRegistro)
    const dadosVeiculo = await buscarVeiculo(dadosRegistro.placa)

    const [nomeGuarda, nomeColaborador] = await Promise.all([
      buscarGuarda(dadosRegistro.cpf_guarda)
        .then((g) => g.nome_guarda)
        .catch(() => dadosRegistro.cpf_guarda),
      dadosVeiculo.matricula_colaborador
        ? buscarColaborador(dadosVeiculo.matricula_colaborador)
            .then((c) => c.nome)
            .catch(() => '')
        : Promise.resolve(''),
    ])

    registro.value = dadosRegistro
    veiculo.value = dadosVeiculo
    guarda.value = nomeGuarda
    responsavel.value =
      dadosVeiculo.tipo_vinculo === 'TERCEIRO'
        ? `Documento ${dadosVeiculo.documento_responsavel ?? 'não informado'}`
        : `${nomeColaborador || 'Colaborador'} (mat. ${dadosVeiculo.matricula_colaborador})`

    if (dadosRegistro.data_saida) erro.value = 'Este registro já tem saída registrada.'
  } catch (e) {
    erro.value = mensagemDeErro(e, 'Não foi possível carregar o registro.')
  } finally {
    carregando.value = false
  }
}

async function confirmar() {
  if (!registro.value || salvando.value) return

  if (terceiro.value && !formaPagamento.value) {
    erro.value = 'Selecione a forma de pagamento.'
    return
  }

  salvando.value = true
  erro.value = ''

  try {
    await registrarSaida(registro.value.id_registro)
  } catch (e) {
    erro.value = mensagemDeErro(e, 'Não foi possível registrar a saída.')
    salvando.value = false
    return
  }

  if (terceiro.value) {
    try {
      await criarPagamento(registro.value.id_registro, formaPagamento.value)
    } catch (e) {
      erro.value = `A saída foi registrada, mas o pagamento não foi criado: ${mensagemDeErro(e, 'erro desconhecido')}.`
      salvando.value = false
      return
    }
  }

  router.push('/')
}

let relogio: ReturnType<typeof setInterval> | undefined

onMounted(() => {
  carregar()
  relogio = setInterval(() => (agora.value = new Date()), 30_000)
})

onBeforeUnmount(() => clearInterval(relogio))
</script>

<template>
  <OperacaoLayout
    titulo="Registrar saída"
    subtitulo="Confira os dados do registro antes de liberar a vaga."
    :erro="erro"
  >
    <p v-if="carregando" class="apagado">Carregando registro...</p>

    <template v-if="registro && veiculo">
      <div class="topo">
        <div>
          <p class="rotulo">Registro #{{ registro.id_registro }}</p>
          <p class="placa">{{ registro.placa }}</p>
        </div>
        <StatusPill
          :texto="terceiro ? 'Terceiro' : 'Colaborador'"
          :variante="terceiro ? 'laranja' : 'azul'"
        />
      </div>

      <dl class="dados">
        <div>
          <dt>Veículo</dt>
          <dd>{{ veiculo.modelo }}, {{ veiculo.cor.toLowerCase() }}</dd>
        </div>
        <div>
          <dt>Responsável</dt>
          <dd>{{ responsavel }}</dd>
        </div>
        <div>
          <dt>Vaga</dt>
          <dd>{{ registro.numero_vaga }}</dd>
        </div>
        <div>
          <dt>Guarda da entrada</dt>
          <dd>{{ guarda }}</dd>
        </div>
        <div>
          <dt>Entrada</dt>
          <dd>{{ entrada && formatarMomento(entrada) }}</dd>
        </div>
        <div>
          <dt>Saída</dt>
          <dd>{{ formatarMomento(saida) }}{{ registro.data_saida ? '' : ' (agora)' }}</dd>
        </div>
      </dl>

      <div v-if="terceiro" class="pagamento">
        <p class="pagamento-titulo">Pagamento do terceiro</p>
        <div class="linha">
          <span>Permanência</span>
          <strong>{{ formatarDuracao(minutosPermanencia) }}</strong>
        </div>
        <div class="linha">
          <span>Tarifa</span>
          <strong>{{ formatarMoeda(TARIFA_POR_HORA) }}/hora ({{ MINUTOS_GRATIS }} min grátis)</strong>
        </div>
        <div class="linha total">
          <span>Total a pagar</span>
          <strong>{{ formatarMoeda(valorEstimado) }}</strong>
        </div>
        <BaseSelect
          v-model="formaPagamento"
          rotulo="Forma de pagamento"
          :opcoes="FORMAS_PAGAMENTO"
          placeholder="Selecione a forma de pagamento"
          obrigatorio
        />
        <p class="aviso">O pagamento é criado automaticamente ao confirmar a saída.</p>
      </div>

    </template>

    <template #acoes>
      <BaseButton variante="secundario" :disabled="salvando" @click="router.push('/')">Cancelar</BaseButton>
      <BaseButton
        variante="primario"
        :disabled="salvando || !registro || !!registro.data_saida"
        @click="confirmar"
      >
        {{ salvando ? 'Registrando...' : 'Confirmar saída e liberar vaga' }}
      </BaseButton>
    </template>
  </OperacaoLayout>
</template>

<style scoped>
p {
  margin: 0;
}

.topo {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.rotulo {
  color: var(--color-text-muted);
  font-size: 12px;
  font-weight: 500;
}

.placa {
  font-size: 26px;
  font-weight: 600;
}

.dados {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px 24px;
  margin: 0;
}

.dados dt {
  color: var(--color-text-muted);
  font-size: 13px;
}

.dados dd {
  margin: 4px 0 0;
  font-size: 15px;
  font-weight: 500;
}

.pagamento {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 18px 20px;
  border: 1px solid #f1d3a8;
  border-radius: 10px;
  background: var(--color-aviso-bg);
}

.pagamento-titulo {
  color: var(--color-aviso-text);
  font-size: 15px;
  font-weight: 600;
}

.linha {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  font-size: 14px;
}

.linha span {
  color: var(--color-text-soft);
}

.total {
  padding-top: 12px;
  border-top: 1px solid #f1d3a8;
  align-items: baseline;
}

.total span {
  color: var(--color-text);
  font-weight: 600;
}

.total strong {
  font-size: 24px;
}

.aviso {
  color: var(--color-aviso-text);
  font-size: 13px;
}

.apagado {
  color: var(--color-text-muted);
  font-size: 14px;
}

</style>
