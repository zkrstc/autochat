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
                component: RequirementPage,
                meta: { title: '需求管理' }
            },
            {
                path: 'architecture',
                name: 'Architecture',
                component: ArchitecturePage,
                meta: { title: '架构设计' }
            },
            {
                path: 'databasedesign',
                name: 'DatabaseDesign',
                component: DatabaseDesignPage,
                meta: { title: '数据库设计' }
            },
            {
                path: 'modulecode',
                name: 'ModuleCode',
                component: ModuleCodePage,
                meta: { title: '模块代码' }
            },
            {
                path: 'testcases',
                name: 'TestCases',
                component: TestCasesPage,
                meta: { title: '测试用例生成' }
            },
            {
                path: 'history',
                name: 'History',
                component: HistoryPage,
                meta: { title: '版本历史' }
            }
        ]
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;