<script setup lang="ts">
import AppSideBar from './AppSideBar.vue'
</script>

<template>
    <div class="app-layout">
        <aside class="sidebar-container">
            <AppSideBar />
        </aside>

        <main class="main-content">
            <div class="content-container">
                <RouterView />
            </div>
        </main>
    </div>

</template>

<style scoped>

.app-layout {
    box-sizing: border-box;
    display: flex;
    min-height: 100vh;
    width: 100%;
    background-color: #F1F3F7
}

.sidebar-container{
    box-sizing: border-box;
    width: 250px;
    min-width: 200px;
    min-height: 100vh;
    flex-shrink: 0;
    background-color: #FFFF;
    border-right: 1px solid #E5E7EB;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
}

.main-content{
    box-sizing: border-box;
    flex:1;
    min-width: 0;
    padding: 18px 20px;
    
}

.content-container{
    box-sizing: border-box;
    width: 100%;
    min-height: calc(100vh - 36px);
    background-color: #FFFF;
    border-radius: 14px;
    padding: 20px 24px;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
}

</style>