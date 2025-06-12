<template>
    <div class="p-8">
        <!-- 需求选择区 -->
        <div class="flex items-center mb-6 space-x-4">
            <div class="text-lg font-medium">需求选择：</div>
            <select v-model="selectedProject"
                class="border border-gray-300 rounded-button px-4 py-2 min-w-[200px] focus:outline-none focus:ring-2 focus:ring-primary">
                <option v-for="project in projects" :key="project.id" :value="project.id">
                    {{ project.name }}
                </option>
            </select>
        </div>

        <!-- 版本历史表格 -->
        <div class="bg-white rounded-lg shadow p-6 mb-6">
            <h2 class="text-lg font-medium mb-6">版本历史</h2>
            <div class="overflow-x-auto">
                <table class="w-full">
                    <thead>
                        <tr class="bg-gray-50">
                            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">版本号</th>
                            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">更新内容</th>
                            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">更新时间</th>
                            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="version in paginatedVersions" :key="version.id"
                            class="border-b border-gray-200 hover:bg-gray-50">
                            <td class="px-4 py-3 text-sm text-gray-900">{{ version.version }}</td>
                            <td class="px-4 py-3 text-sm text-gray-700">{{ version.content }}</td>
                            <td class="px-4 py-3 text-sm text-gray-500">{{ formatDate(version.date) }}</td>
                            <td class="px-4 py-3 text-sm">
                                <button @click="viewDetails(version)"
                                    class="text-primary hover:text-primary-dark">查看详情</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 分页部分 -->
        <div class="flex justify-between items-center mt-4">
            <div class="flex items-center">
                <span class="text-sm text-gray-700">显示</span>
                <select v-model="pageSize"
                    class="border border-gray-300 rounded-button px-2 py-1 mx-2 focus:outline-none focus:ring-2 focus:ring-primary">
                    <option v-for="size in pageSizes" :key="size" :value="size">{{ size }}</option>
                </select>
                <span class="text-sm text-gray-700">条</span>
            </div>
            <div class="flex items-center">
                <button @click="prevPage" :disabled="currentPage === 1"
                    class="px-3 py-1 border border-gray-300 rounded-md hover:bg-gray-200 focus:outline-none focus:ring focus:ring-indigo-200 focus:ring-opacity-50 disabled:opacity-50">
                    <i class="fas fa-angle-left"></i>
                </button>
                <span class="mx-4 text-sm text-gray-700">{{ currentPage }} / {{ totalPages }}</span>
                <button @click="nextPage" :disabled="currentPage === totalPages"
                    class="px-3 py-1 border border-gray-300 rounded-md hover:bg-gray-200 focus:outline-none focus:ring focus:ring-indigo-200 focus:ring-opacity-50 disabled:opacity-50">
                    <i class="fas fa-angle-right"></i>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'HistoryPage',
    data() {
        return {
            selectedProject: 1,
            currentPage: 1,
            pageSize: 6,
            pageSizes: [6, 12, 18],
            projects: [
                { id: 1, name: '智能客服系统 v1.0' },
                { id: 2, name: '数据分析平台 v2.0' },
                { id: 3, name: '企业协同办公系统 v3.0' },
                { id: 4, name: '电商管理平台 v1.5' }
            ],
            versions: {
                1: [
                    { id: 1, version: 'v1.0.0', content: '基础客服功能上线', date: '2023-01-15' },
                    { id: 2, version: 'v1.0.1', content: '修复消息推送问题', date: '2023-01-20' },
                    { id: 3, version: 'v1.1.0', content: '新增知识库管理', date: '2023-02-05' },
                    { id: 4, version: 'v1.2.0', content: '增加多语言支持', date: '2023-03-10' },
                    { id: 5, version: 'v1.2.1', content: '优化响应速度', date: '2023-03-15' },
                    { id: 6, version: 'v1.3.0', content: '新增用户满意度评价', date: '2023-04-01' },
                    { id: 7, version: 'v1.3.1', content: '修复评价系统bug', date: '2023-04-05' }
                ],
                2: [
                    { id: 1, version: 'v2.0.0', content: '数据分析平台初始版本', date: '2023-02-10' },
                    { id: 2, version: 'v2.0.1', content: '修复数据导入问题', date: '2023-02-15' },
                    { id: 3, version: 'v2.1.0', content: '新增可视化图表', date: '2023-03-01' },
                    { id: 4, version: 'v2.2.0', content: '增加数据导出功能', date: '2023-03-20' }
                ],
                3: [
                    { id: 1, version: 'v3.0.0', content: '协同办公系统上线', date: '2023-03-01' },
                    { id: 2, version: 'v3.0.1', content: '修复日程同步问题', date: '2023-03-05' },
                    { id: 3, version: 'v3.1.0', content: '新增项目管理模块', date: '2023-04-01' },
                    { id: 4, version: 'v3.1.1', content: '优化文件上传速度', date: '2023-04-10' },
                    { id: 5, version: 'v3.2.0', content: '增加即时通讯功能', date: '2023-05-01' }
                ],
                4: [
                    { id: 1, version: 'v1.5.0', content: '商品管理功能升级', date: '2023-03-15' },
                    { id: 2, version: 'v1.5.1', content: '修复订单处理问题', date: '2023-03-20' },
                    { id: 3, version: 'v1.5.2', content: '优化支付流程', date: '2023-04-01' }
                ]
            }
        }
    },
    computed: {
        filteredVersions() {
            return this.versions[this.selectedProject] || []
        },
        totalPages() {
            return Math.ceil(this.filteredVersions.length / this.pageSize)
        },
        paginatedVersions() {
            const start = (this.currentPage - 1) * this.pageSize
            const end = start + this.pageSize
            return this.filteredVersions.slice(start, end)
        }
    },
    methods: {
        formatDate(dateString) {
            const options = { year: 'numeric', month: 'long', day: 'numeric' }
            return new Date(dateString).toLocaleDateString('zh-CN', options)
        },
        viewDetails(version) {
            alert(`查看版本详情: ${version.version}\n更新内容: ${version.content}`)
        },
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++
            }
        }
    },
    watch: {
        selectedProject() {
            this.currentPage = 1
        },
        pageSize() {
            this.currentPage = 1
        }
    }
}
</script>

<style scoped>
.rounded-button {
    border-radius: 6px;
}
</style>