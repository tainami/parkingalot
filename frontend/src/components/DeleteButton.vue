<script setup lang="ts">

defineEmits<{
    click:[]
}>()

</script>

<template>
    <button class="icon-button
        delete-button" 
        type="button" 
        title="Excluir"
        @click="$emit('click')">
        <svg
            viewBox="0 0 24 24"
            class="button-icon"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
        >
            <path d="M3 6h18"/>
            <path d="M8 6V4h8v2"/>
            <path d="m19 6-1 14H6L5 6"/>
            <path d="M10 11v5"/>
            <path d="M14 11v5"/>
        </svg>
    </button>
</template>

<style scoped>
.icon-button{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    background-color: #FFFFFF;
    border: 1px solid #bfc5ca;
    border-radius: 6px;
    cursor: pointer;
    transition:
    background-color 0.2s ease,
    color 0.2s ease,
    transform 0.15s ease;
}

.delete-button{
    color: #DC2626;
    border-color: #bfc5ca;
}

.delete-button:hover{
    background-color: #DC2626;
    color: #FFFFFF;
}

.delete-button:active{
    transform: scale(1.05);
}

.button-icon{
    width: 18px;
    height: 18px;
}

</style>