// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import RequirementPage from '../views/RequirementPage.vue';
import ArchitecturePage from '../views/ArchitecturePage.vue';
import DatabaseDesignPage from '../views/DatabaseDesign.vue';
import ModuleCodePage from '../views/ModulesPage.vue';
import TestCasesPage from '../views/TestPage.vue';
import HistoryPage from '../views/HistoryPage.vue';
import LoginPage from '../views/LoginPage.vue';
import App from '../App.vue';
const routes = [
    {
        path: '/',
        redirect: '/login'  // ⬅ 默认重定向到登录页
    },
    // 登录页（独立，不包裹在 App.vue 中）
    {
        path: '/login',
        name: 'Login',
        component: LoginPage
    },
    // 登录后的页面（使用 App.vue 包裹）
    {
        path: '/',
        component: App,
        children: [
            {
                path: 'requirements',
                name: 'Requirements',
                component: RequirementPage
            },
            {
                path: 'architecture',
                name: 'Architecture',
                component: ArchitecturePage
            },
            {
                path: 'databasedesign',
                name: 'DatabaseDesign',
                component: DatabaseDesignPage
            },
            {
                path: 'modulecode',
                name: 'ModuleCode',
                component: ModuleCodePage
            },
            {
                path: 'testcases',
                name: 'TestCases',
                component: TestCasesPage
            },
            {
                path: 'history',
                name: 'History',
                component: HistoryPage
            }
        ]
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;