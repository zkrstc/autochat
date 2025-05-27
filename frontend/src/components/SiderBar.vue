<template>
    <aside class="w-64 bg-white shadow-lg">
        <div class="p-6">
            <h1 class="text-2xl font-['Pacifico'] text-primary">Logo</h1>
        </div>
        <nav class="mt-4">

            <router-link to="/requirements" class="menu-item flex items-center px-6 py-3 text-gray-700" active-class="active">
                <i class="fas fa-tasks w-5 h-5 mr-3 flex justify-center items-center"></i>
                <span>需求管理</span>
            </router-link>

            <router-link to="/architecture" class="menu-item flex items-center px-6 py-3 text-gray-700" active-class="active">
                <i class="fas fa-sitemap w-5 h-5 mr-3 flex justify-center items-center"></i>
                <span>架构设计</span>
            </router-link>

            <router-link to="/modulecode" class="menu-item flex items-center px-6 py-3 text-gray-700" active-class="active">
                <i class="fas fa-code w-5 h-5 mr-3 flex justify-center items-center"></i>
                <span>模块代码</span>
            </router-link>

            <router-link to="/databasedesign" class="menu-item flex items-center px-6 py-3 text-gray-700" active-class="active">
                <i class="fas fa-database w-5 h-5 mr-3 flex justify-center items-center"></i>
                <span>数据库设计</span>
            </router-link>

            <router-link to="/testcases" class="menu-item flex items-center px-6 py-3 text-gray-700" active-class="active">
                <i class="fas fa-vial w-5 h-5 mr-3 flex justify-center items-center"></i>
                <span>测试用例生成</span>
            </router-link>

            <router-link to="/history" class="menu-item flex items-center px-6 py-3 text-gray-700" active-class="active">
                <i class="fas fa-history w-5 h-5 mr-3 flex justify-center items-center"></i>
                <span>版本历史</span>
            </router-link>
            <!-- 其他导航项 -->
        </nav>
    </aside>
</template>
