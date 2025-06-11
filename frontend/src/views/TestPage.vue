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
                <button @click="generateTestCases"
                    class="bg-primary text-white px-4 py-2 !rounded-button flex items-center" :disabled="isGenerating">
                    <i class="fas fa-plus mr-2"></i>
                    {{ isGenerating ? '生成中...' : '生成测试用例' }}
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
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">操作</th>
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
                                <button @click="openEditModal(testCase)"
                                    class="text-blue-500 hover:underline">修改</button>
                                <button @click="deleteTestCase(testCase.id)"
                                    class="text-red-500 hover:underline ml-2">删除</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>


    </div>

    <!-- 弹窗编辑框 -->
    <div v-if="showEditModal" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex justify-center items-center z-50">
        <div class="bg-white p-6 rounded shadow w-96">
            <h3 class="text-lg font-semibold mb-4">编辑测试用例</h3>
            <div class="mb-4">
                <label class="block text-sm">输入数据：</label>
                <textarea v-model="editData.input_data" class="w-full border p-2 text-sm" rows="3"></textarea>
            </div>
            <div class="mb-4">
                <label class="block text-sm">预期输出：</label>
                <textarea v-model="editData.expected_output" class="w-full border p-2 text-sm" rows="3"></textarea>
            </div>
            <div class="flex justify-end space-x-2">
                <button @click="showEditModal = false" class="text-gray-600">取消</button>
                <button @click="submitEdit" class="bg-blue-500 text-white px-4 py-1 rounded">保存</button>
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
            showEditModal: false,
            editData: {
                id: null,
                input_data: '',
                expected_output: ''
            },
            error: null,
            selectedRequirement: '',
            selectedRequirementId: null,
            testCases: [],
            loading: false,
            generating: false,
            isGenerating: false,
            selectedArchitectureId: '',
        }
    },
    created() {
        this.fetchRequirements();
    },
    methods: {
        
        handleRequirementSelected(id) {
            this.selectedRequirementId = id;
            console.log('Selected Requirement ID:', this.selectedRequirementId);
            this.fetchArchitecture(id);
            this.fetchTestCases(id);
            
        },
        async fetchArchitecture(requirementId) {
            this.loading = true;
            this.error = null;

            try {
                const response = await axios.get(`http://127.0.0.1:5000/api/architectures/${requirementId}`);
                if (response.data.status === 'success') {
                    this.architecture = JSON.parse(response.data.data.architecture_json);
                    this.selectedArchitectureId = response.data.data.id;
                    this.architectureModules = this.architecture.modules || [];
                } else {
                    throw new Error(response.data.message || 'Failed to fetch architecture');
                }
            } catch (error) {
                console.error('Error fetching architecture:', error);
                this.error = error.message;
                this.architectureModules = [];
            } finally {
                this.loading = false;
            }
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
            if (!this.selectedRequirementId) {
                this.$toast.error('请先选择需求')
                return
            }

            this.isGenerating = true

            try {
                const response = await axios.post('http://127.0.0.1:5000/api/test-cases/generate', {
                    requirement_id: this.selectedRequirementId,
                    architecture_id: this.selectedArchitectureId
                })

                if (response.data.error) {
                    throw new Error(response.data.error)
                }

            } catch (error) {
                console.error('生成测试用例失败:', error)
            } finally {
                this.isGenerating = false
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
        },
        openEditModal(testCase) {
            this.editData = {
                id: testCase.id,
                input_data: testCase.input_data,
                expected_output: testCase.expected_output
            }
            this.showEditModal = true
        },
        submitEdit() {
            axios
                .put(`http://127.0.0.1:5000/api/test_cases/${this.editData.id}`, {
                    input_data: this.editData.input_data,
                    expected_output: this.editData.expected_output
                })
                .then(() => {
                    this.showEditModal = false
                    this.fetchTestCases(this.editData.id) // 刷新数据
                })
                .catch(err => {
                    console.error('更新失败', err)
                })
        },
        deleteTestCase(id) {
            if (!confirm('确定删除该测试用例吗？')) return
            axios
                .delete(`http://127.0.0.1:5000/api/test_cases/${id}`)
                .then(() => {
                    this.fetchTestCases(this.editData.id)
                })
                .catch(err => {
                    console.error('删除失败', err)
                })
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
  