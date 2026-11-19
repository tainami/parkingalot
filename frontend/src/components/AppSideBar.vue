<script setup lang="ts">
import {RouterLink} from 'vue-router'

const menuItems=[
    {name: 'Mapa de vagas', path:'/mapa', icon: 'mapa'},
    {name:'Registro', path:'/registros', icon:'registros'},
    {name:'Pagamentos', path:'/pagamentos', icon:'pagamentos'},
    {name:'Veículos', path:'/veiculos', icon:'veiculos'},
    {name:'Colaboradores', path:'/colaboradores', icon:'colaboradores'},
    {name:'Guardas', path:'/guardas', icon:'guardas'},
    {name:'Vagas', path:'/vagas', icon:'vagas'}
]
</script>


<template>
    <aside class="app-sidebar">
        <div class="sidebar-header">
            <div class="logo-icon">P</div>
            <span class="logo-text">ParkingAlot</span>
        </div>
        <nav class="sidebar-menu">
            <RouterLink
                v-for="item in menuItems"
                :key="item.path"
                :to="item.path"
                class="menu-item"
                active-class="active"
            >
                <svg 
                    v-if="item.icon === 'mapa'" 
                    viewBox="0 0 24 24"
                    class="menu-icon">

                    <path d="m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3z"/>
                    <path d="M9 3v15M15 6v15"/>
                </svg>

                <svg 
                    v-else-if="item.icon === 'registros'"
                    viewBox="0 0 24 24"
                    class="menu-icon">
                    
                    <path d="M3 12a9 9 0 1 0 2.64-6.36L3 8"/>
                    <path d="M3 3v5h5"/>
                    <path d="M12 7v5l3 2"/>
                </svg>

                <svg 
                    v-else-if="item.icon === 'pagamentos'"
                    viewBox="0 0 24 24"
                    class="menu-icon">

                    <rect x="2" y="5" width="20" height="14" rx="2"/>
                    <path d="M2 10h20M6 15h4"/>
                </svg>

                <svg 
                    v-else-if="item.icon === 'veiculos'"
                    viewBox="0 0 24 24"
                    class="menu-icon">

                    <path d="M3 13l2-6a2 2 0 0 1 2-1h10a2 2 0 0 1 2 1l2 6"/>
                    <path d="M2 13h20v5H2z"/>
                    <path d="M5 18v2M19 18v2"/>
                    <path d="M6 13l1-4h10l1 4"/>
                    <path d="M5 15h2M17 15h2"/>
                </svg>

                <svg 
                    v-else-if="item.icon === 'colaboradores'"
                    viewBox="0 0 24 24"
                    class="menu-icon">

                    <circle cx="9" cy="7" r="3.5"/>
                    <path d="M2.5 20v-2a6.5 6.5 0 0 1 13 0v2"/>
                    <path d="M16 4.2a3.5 3.5 0 0 1 0 6.6"/>
                    <path d="M17 14a6 6 0 0 1 4.5 5.8V20"/>
                </svg>

                <svg 
                    v-else-if="item.icon === 'guardas'"
                    viewBox="0 0 24 24"
                    class="menu-icon">

                    <path d="M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11z"/>
                </svg>

                <svg 
                    v-else-if="item.icon === 'vagas'"
                    viewBox="0 0 24 24"
                    class="menu-icon">

                    <rect x="3" y="3" width="18" height="18" rx="3"/>
                    <path d="M9 18V6h4a4 4 0 0 1 0 8H9"/>
                </svg>

                <span>{{ item.name }}</span>
            </RouterLink>

        </nav>

        <div class="sidebar-footer">
            <div class="user-info">
                <div class="user-avatar">EX</div>
                <div class="user-details">
                    <span class="user-name">Exemplo</span>
                    <span class="user-role">Guarda</span>
                </div>
            </div>       
                
            <button class="logout-button">
                <svg viewBox="0 0 24 24" class="menu-icon">
                    <path d="M10 7l-5 5 5 5"/>
                    <path d="M5 12h10"/>
                    <path d="M12 3h5a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-5"/>
                </svg>
                <span>Sair</span>
            </button>
        </div>

    </aside>
</template>

<style scoped>
.app-sidebar{
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
    width: 100%;
    height: 100%;
    min-height: 100vh;
    padding:24px 16px;
    background-color: #FFFFFF;
    }

.sidebar-header{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 36px;
}

.logo-icon{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 9px;
    background-color: #2879E8;
    color: #FFFFFF;
    font-size: 21px;
    font-weight: 700;
}

.logo-text{
    color: #172554;
    font-size: 21px;
    font-weight: 700;
}

.sidebar-menu{
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.menu-item{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 11px 12px;
    border-radius: 8px;
    color: #172554;
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    transition: 
        background-color 0.2s ease,
        color 0.2s ease,
        transform 0.15s ease;
}

.menu-icon{
    width: 20px;
    height: 20px;
    flex-shrink: 0;
    fill: none;
    stroke: currentColor;
    stroke-width: 1.8;
    stroke-linecap: round;
    stroke-linejoin: round;
}

.menu-item:hover,
.menu-item.active{
    background-color: #2879E8;
    color: #FFFFFF;
}

.menu-item:active{
    transform: scale(1.05);
}

.sidebar-footer{
    margin-top: auto;
    padding-top: 20px;
    border-top: 1px solid #E5E7EB;
}

.user-info{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;
}

.user-avatar{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    flex-shrink: 0;
    border-radius: 50%;
    background-color: #EAF2FF;
    color: #2879E8;
    font-size: 12px;
    font-weight: 700;
}

.user-details{
    display: flex;
    flex-direction: column;
    gap: 3px;
}

.user-name{
    color: #172554;
    font-size: 13px;
    font-weight: 600;
}

.user-role{
    color: #64748B;
    font-size: 12px;
}

.logout-button{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 11px 12px;
    width: 100%;
    border: none;
    border-radius: 8px;
    background: transparent;
    color: #DC2626;
    font-size: 14px;
    cursor: pointer;
    transition: 
    background-color 0.2s ease,
    color 0.2s ease;
}

.logout-button:hover{
    background-color: #FEE2E2;
    color: #DC2626;
}

.logout-button:active{
    transform: scale(1.06);
}

</style>