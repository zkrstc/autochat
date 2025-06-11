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
            <button id="generateBtn"
                class="px-6 py-2 bg-primary text-white !rounded-button hover:bg-blue-600 transition-colors"
                @click="generateArchitecture" :disabled="!selectedRequirement || isLoading">
                <i class="fas fa-magic mr-2"></i>
                {{ isLoading ? '生成中...' : '生成架构' }}
            </button>
        </div>

        <!-- 架构展示区域 -->
        <div class="bg-white rounded-lg shadow p-6 mb-6">
            <div class="flex items-center justify-between mb-4">
                <div class="flex items-center">
                    <i class="fas fa-sitemap text-primary text-xl"></i>
                    <h3 class="ml-2 text-lg font-medium">系统架构图</h3>
                </div>
                <div class="flex space-x-2">
                    <button @click="downloadDiagram" class="px-4 py-2 border border-gray-300 !rounded-button">
                        <i class="fas fa-download mr-2"></i>下载
                    </button>
                </div>
            </div>

            <div id="architectureContainer" class="architecture-diagram">
                <div v-if="loading" class="text-center py-10">
                    <i class="fas fa-spinner fa-spin text-4xl mb-2 text-primary"></i>
                    <p>正在加载架构图...</p>
                </div>
                <div v-else-if="error" class="text-center py-10 text-red-500">
                    <i class="fas fa-exclamation-circle text-4xl mb-2"></i>
                    <p>{{ error }}</p>
                </div>
                <div v-else-if="!architecture" class="text-center py-10">
                    <i class="fas fa-sitemap text-4xl mb-2"></i>
                    <p>请选择需求并点击"生成架构"按钮</p>
                </div>
                <pre v-else
                    class="bg-gray-100 p-4 rounded overflow-auto">{{ architecture.architectureDiagram.diagram }}</pre>
            </div>
        </div>

        <!-- 技术栈和模块划分 -->
        <div class="grid grid-cols-2 gap-6">
            <!-- 技术栈 -->
            <div class="bg-white rounded-lg shadow p-6">
                <div class="flex items-center mb-4">
                    <i class="fas fa-code-branch text-primary text-xl"></i>
                    <h3 class="ml-2 text-lg font-medium">推荐技术栈</h3>
                </div>
                <div id="techStackContainer" class="space-y-3">
                    <div v-if="loading" class="text-center py-10">
                        <i class="fas fa-spinner fa-spin text-4xl mb-2 text-primary"></i>
                        <p>正在加载技术栈...</p>
                    </div>
                    <div v-else-if="error" class="text-center py-10 text-red-500">
                        <i class="fas fa-exclamation-circle text-4xl mb-2"></i>
                        <p>{{ error }}</p>
                    </div>
                    <div v-else-if="!architecture" class="text-center text-gray-500 py-10">
                        <i class="fas fa-cog text-4xl mb-2"></i>
                        <p>架构生成后将显示推荐技术栈</p>
                    </div>
                    <div v-else>
                        <!-- Frontend -->
                        <div class="flex items-start">
                            <div class="bg-gray-100 rounded-full p-2 mr-3">
                                <i class="fab fa-vuejs text-primary"></i>
                            </div>
                            <div>
                                <h4 class="font-medium">前端技术</h4>
                                <p class="text-gray-600">{{ architecture.technologyStack.frontend }}</p>
                            </div>
                        </div>

                        <!-- Backend -->
                        <div class="flex items-start">
                            <div class="bg-gray-100 rounded-full p-2 mr-3">
                                <i class="fas fa-server text-primary"></i>
                            </div>
                            <div>
                                <h4 class="font-medium">后端技术</h4>
                                <p class="text-gray-600">{{ architecture.technologyStack.backend }}</p>
                            </div>
                        </div>

                        <!-- Database -->
                        <div class="flex items-start">
                            <div class="bg-gray-100 rounded-full p-2 mr-3">
                                <i class="fas fa-database text-primary"></i>
                            </div>
                            <div>
                                <h4 class="font-medium">数据库</h4>
                                <p class="text-gray-600">{{ architecture.technologyStack.database }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- 模块划分 -->
            <div class="bg-white rounded-lg shadow p-6">
                <div class="flex items-center mb-4">
                    <i class="fas fa-tasks text-primary text-xl"></i>
                    <h3 class="ml-2 text-lg font-medium">模块划分</h3>
                </div>
                <div id="modulesContainer" class="space-y-3">
                    <div v-if="loading" class="text-center py-10">
                        <i class="fas fa-spinner fa-spin text-4xl mb-2 text-primary"></i>
                        <p>正在加载模块...</p>
                    </div>
                    <div v-else-if="error" class="text-center py-10 text-red-500">
                        <i class="fas fa-exclamation-circle text-4xl mb-2"></i>
                        <p>{{ error }}</p>
                    </div>
                    <div v-else-if="!architecture" class="text-center text-gray-500 py-10">
                        <i class="fas fa-project-diagram text-4xl mb-2"></i>
                        <p>架构生成后将显示模块划分</p>
                    </div>
                    <div v-else>
                        <div v-for="(module, index) in architecture.modules" :key="index"
                            class="flex items-center p-3 bg-gray-50 rounded">
                            <i class="fas fa-cube text-primary mr-3"></i>
                            <span>{{ module }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'ArchitecturePage',
    data() {
        return {
            requirements: [],
            selectedRequirement: '',
            selectedRequirementId: null,
            loading: false,
            error: null,
            architecture: null,

            techIcons: {
                frontend: 'fab fa-vuejs',
                backend: 'fab fa-python',
                database: 'fas fa-database'
            }
        }
    },
    computed: {
        technologyStack() {
            if (!this.architecture) return [];

            return Object.entries(this.architecture.architecture_json.technologyStack).map(
                ([category, value]) => ({
                    category: category.charAt(0).toUpperCase() + category.slice(1),
                    value,
                    icon: this.techIcons[category] || 'fas fa-code'
                })
            );
        }
    },
    watch: {
        requirementId(newVal) {
            if (newVal) {
                this.fetchArchitecture(newVal);
            }
        }
    },
    created() {
        this.fetchRequirements();
    },
    methods: {
        handleRequirementSelected(id) {
            this.selectedRequirementId = id;
            console.log('Selected Requirement ID:', this.selectedRequirementId);
            this.fetchArchitecture(this.selectedRequirementId);
            const user = JSON.parse(localStorage.getItem('user'));
            console.log('当前用户:', user.username);
            
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
        onRequirementChange() {
            this.$emit('requirement-selected', this.selectedRequirement);
        },
        async fetchArchitecture(requirementId) {
            this.loading = true;
            this.error = null;

            try {
                const response = await axios.get(`http://127.0.0.1:5000/api/architectures/${requirementId}`);
                console.log('Response:', response.data);
                if (response.data.status === 'success') {
                    this.architecture = JSON.parse(response.data.data.architecture_json);
                } else {
                    throw new Error(response.data.message || 'Failed to fetch data.');
                }

            } catch (err) {
                console.error('Error fetching architecture:', err);
                this.error = err.response?.data?.error ||
                    err.message ||
                    '获取架构信息失败';
                this.architecture = null;

                // 可以在这里添加更多特定的错误处理
                if (err.response?.status === 404) {
                    this.error = "未找到对应的架构设计";
                }
            } finally {
                this.loading = false;
            }
        },
        downloadDiagram() {
            if (!this.architecture) return;

            // Implement download functionality
            const blob = new Blob([this.architecture.architecture_json.architectureDiagram.diagram],
                { type: 'text/plain' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `architecture-${this.architecture.id}.txt`;
            link.click();
        },
        // 生成架构按钮点击处理
        async generateArchitecture() {
            if (!this.selectedRequirement) {
                this.$toast.warning('请先选择需求');
                return;
            }

            this.isLoading = true;
            try {
                // 获取存储的用户信息
                const user = JSON.parse(localStorage.getItem('user'));
                
                const username = user.username;
                if (user) {
                    console.log('当前用户:', user.username);
                    // 使用 user.username 或 user.id
                } else {
                    console.log('用户未登录');
                }

                const response = await axios.post('http://127.0.0.1:5000/api/architectures/generate', {
                    requirement_id: this.selectedRequirement,
                    user_name: username
                });
                //this.architecture = JSON.parse(response.data.data.architecture_json);
                const data = await response.json();



                if (response.ok) {
                    this.architecture = data.data.architecture_json;
                    this.$toast.success('架构生成成功！');
                } else {
                    throw new Error(data.message || 'Failed to generate architecture');
                }
            } catch (error) {
                console.error('Error generating architecture:', error);
            } finally {
                this.isLoading = false;
            }
        }
    }
}
</script>