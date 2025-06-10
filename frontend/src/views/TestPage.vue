<template>
    <div class="p-8">
        <!-- 需求选择和生成按钮 -->
        <div class="flex items-center justify-between mb-6">
            <div class="flex items-center space-x-4">
                <div class="text-lg font-medium">需求选择：</div>
                <select v-model="selectedRequirement"
                    class="border border-gray-300 rounded-button px-4 py-2 min-w-[200px] focus:outline-none focus:ring-2 focus:ring-primary"
                    @change="handleRequirementSelected(selectedRequirement)">
                    <option disabled value="">请选择需求</option>
                    <option v-for="req in requirements" :key="req.id" :value="req.id">
                        {{ req.name }} v{{ req.version }}
                    </option>
                </select>
            </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6 mb-6">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-lg font-medium">测试用例列表</h2>
                <button class="bg-primary text-white px-4 py-2 !rounded-button flex items-center">
                    <i class="fas fa-plus mr-2"></i>生成测试用例
                </button>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full">
                    <thead>
                        <tr class="bg-gray-50">
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">类型</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">输入数据</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">预期输出</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">创建时间</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        <!-- 加载状态 -->
                        <tr v-if="loading">
                            <td colspan="5" class="px-6 py-4 text-center">
                                <i class="fas fa-spinner fa-spin mr-2"></i>加载中...
                            </td>
                        </tr>

                        <!-- 空状态 -->
                        <tr v-else-if="testCases.length === 0">
                            <td colspan="5" class="px-6 py-4 text-center text-gray-500">
                                没有找到测试用例
                            </td>
                        </tr>

                        <!-- 测试用例数据 -->
                        <tr v-for="testCase in testCases" :key="testCase.id" class="hover:bg-gray-50">
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ testCase.id }}</td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="px-2 py-1 text-xs rounded-full" :class="getTypeBadgeClass(testCase.type)">
                                    {{ testCase.type }}
                                </span>
                            </td>
                            <td class="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">
                                <pre class="truncate">{{ formatJson(testCase.input_data) }}</pre>
                            </td>
                            <td class="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">
                                <pre class="truncate">{{ formatJson(testCase.expected_output) }}</pre>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {{ formatDate(testCase.created_at) }}
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
                <select id="pageSizeSelect"
                    class="border border-gray-300 rounded-button px-2 py-1 mx-2 focus:outline-none focus:ring-2 focus:ring-primary"
                    onchange="updateTestCases()">
                    <option value="6">6</option>
                    <option value="12">12</option>
                    <option value="18">18</option>
                </select>
                <span class="text-sm text-gray-700">条</span>
            </div>
            <div class="flex items-center">
                <button id="prevPageButton"
                    class="px-3 py-1 border border-gray-300 rounded-md hover:bg-gray-200 focus:outline-none focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
                    <i class="fas fa-angle-left"></i>
                </button>
                <span id="currentPage" class="mx-4 text-sm text-gray-700">1</span>
                <button id="nextPageButton"
                    class="px-3 py-1 border border-gray-300 rounded-md hover:bg-gray-200 focus:outline-none focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
                    <i class="fas fa-angle-right"></i>
                </button>
            </div>
        </div>
    </div>
</template>
  
  <script>
  import axios from 'axios';
  export default {
    name: 'TestPage',
    data() {
        return {
            // 已有数据...
            
            error: null,
            selectedRequirement: '',
            selectedRequirementId: null,
            testCases: [],
            loading: false,
            generating: false
        }
    },
    created() {
        this.fetchRequirements();
    },
    methods: {
        handleRequirementSelected(id) {
            this.selectedRequirementId = id;
            console.log('Selected Requirement ID:', this.selectedRequirementId);
            this.fetchTestCases(this.selectedRequirementId);
        },
        async fetchRequirements() {
            this.loading = true;
            this.error = null;
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/requirements/list');
                this.requirements = response.data;
            } catch (err) {
                console.error('Error fetching requirements:', err);
                this.error = '无法加载需求列表';
            } finally {
                this.loading = false;
            }
        },
        async fetchTestCases(requirementId) {
            this.loading = true;
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/test_cases', {
                    params: { requirement_id: requirementId }
                });
                this.testCases = response.data.data || [];
            } catch (error) {
                console.error('获取测试用例失败:', error);
                this.testCases = [];
            } finally {
                this.loading = false;
            }
        },

        async generateTestCases() {
            if (!this.selectedRequirement) return;

            this.generating = true;
            try {
                const response = await axios.post('/api/test_cases/generate', {
                    requirement_id: this.selectedRequirement
                });

                this.$toast.success(response.data.message);
                await this.fetchTestCases(this.selectedRequirement);
            } catch (error) {
                console.error('生成测试用例失败:', error);
                this.$toast.error(error.response?.data?.error || '生成失败');
            } finally {
                this.generating = false;
            }
        },

        formatJson(jsonStr) {
            try {
                const obj = JSON.parse(jsonStr);
                return JSON.stringify(obj, null, 2);
            } catch {
                return jsonStr;
            }
        },

        formatDate(dateStr) {
            return dateStr ? new Date(dateStr).toLocaleString() : '-';
        },

        getTypeBadgeClass(type) {
            const classes = {
                login: 'bg-blue-100 text-blue-800',
                purchase: 'bg-green-100 text-green-800',
                default: 'bg-gray-100 text-gray-800'
            };
            return classes[type] || classes.default;
        }
    },
    watch: {
        selectedRequirement(newVal) {
            if (newVal) {
                this.fetchTestCases(newVal);
            } else {
                this.testCases = [];
            }
        }
    }
  }
  </script>
  