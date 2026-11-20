<script setup lang="ts">
import EditButton from './EditButton.vue'
import DeleteButton from './DeleteButton.vue'
defineProps<{
    columns: string[]
    rows: Record<string, any>[]
}>()

</script>

<template>
    <div class="table-container">
        <table class="data-table">
            <thead>
                <tr>
                    <th v-for="column in columns" :key="column">
                        {{ column }}
                    </th>
                    <th>Ações</th>
                </tr>
            </thead>

                <tbody>
                    <tr v-for="(row, index) in rows" :key="index">
                        <td v-for="column in columns" :key="column">
                            {{ row[column] }}
                        </td>
                        <td class="actions">
                            <EditButton />
                            <DeleteButton />
                        </td>
                    </tr>

                    <tr v-if="rows.length === 0">
                        <td :colspan="columns.length + 1" class="no-data">
                            Nenhum dado disponível
                        </td>
                    </tr>
                </tbody>
        </table>
    </div>
</template>

<style scoped>

.table-container{
    width: 100%;
    overflow-x: auto;
    border-radius: 8px;
    border: 1px solid #bfc5ca;
}

.data-table{
    width: 100%;
    border-collapse: collapse;
    text-align: left;
}

.data-table th{
    padding: 14px 16px;
    background-color: #F1F3F7;
    color: #172554;
    font-size: 14px;
    font-weight: 600;
}

.data-table td{
    padding: 14px 16px;
    border-bottom: 1px solid #E5E7EB;
    color: #172554;
    font-size: 14px;
}

.actions{
    white-space: nowrap;
    gap: 8px;
    display: flex;
    align-items: center;
}

.no-data{
    text-align: center;
    color: #64748B;
}



</style>