<template>
    <div class="p-8">
        <!-- 需求选择区
                <div class="flex items-center mb-6 space-x-4">
                    <div class="text-lg font-medium">需求选择：</div>
                    <select id="projectSelect"
                        class="border border-gray-300 rounded-button px-4 py-2 min-w-[200px] focus:outline-none focus:ring-2 focus:ring-primary"
                        onchange="updateDatabaseDesigns()">
                        <option value="1">智能客服系统 v1.0</option>
                        <option value="2">数据分析平台 v2.0</option>
                        <option value="3">企业协同办公系统 v3.0</option>
                        <option value="4">电商管理平台 v1.5</option>
                    </select>

                    <div class="text-lg font-medium ml-8">数据库设计：</div>
                    <select id="dbDesignSelect"
                        class="border border-gray-300 rounded-button px-4 py-2 min-w-[200px] focus:outline-none focus:ring-2 focus:ring-primary"
                        onchange="showTables()">
                        <option value="">请先选择需求</option>
                    </select> 
                </div> -->
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

        <!-- 表展示区 -->
        <div class="bg-white rounded-lg shadow p-6 mb-6">
            <div class="flex items-center justify-between mb-4">
                <div class="flex items-center">
                    <i class="fas fa-table text-primary text-xl"></i>
                    <h3 class="ml-2 text-lg font-medium">数据表设计(ER图展示)</h3>
                </div>
                <div class="flex space-x-2">
                    <button class="px-4 py-2 bg-primary text-white !rounded-button" @click="exportSQL">
                        <i class="fas fa-file-export mr-2"></i>导出SQL
                    </button>
                    <button class="px-4 py-2 border border-gray-300 !rounded-button">
                        <i class="fas fa-print mr-2"></i>生成数据库
                    </button>
                </div>
            </div>

            <div id="tablesContainer" class="space-y-6">
                <!-- 表结构将在这里动态生成 -->
                <div class="text-center text-gray-500 py-10">
                    <i class="fas fa-database text-4xl mb-2"></i>
                    <p>请选择需求查看表结构</p>
                </div>
            </div>
        </div>

        <!-- SQL预览区 -->
        <div class="bg-white rounded-lg shadow p-6">
            <div class="flex items-center justify-between mb-4">
                <div class="flex items-center">
                    <i class="fas fa-code text-primary text-xl"></i>
                    <h3 class="ml-2 text-lg font-medium">SQL预览</h3>
                </div>
                <div class="flex space-x-2">
                    <button class="px-4 py-2 bg-primary text-white !rounded-button" @click="copySQL">
                        <i class="far fa-copy mr-2"></i>复制SQL
                    </button>
                </div>
            </div>
            <pre id="sqlPreview"
                class="bg-gray-50 p-4 rounded-lg overflow-x-auto text-sm font-mono text-left whitespace-pre-wrap"
                style="height: 300px;">
-- SQL语句将在这里显示
-- 请先选择数据库设计</pre>
        </div>
    </div>
</template>
  
  <script>
import axios from 'axios';
import mermaid from 'mermaid';
  export default {
    name: 'DatabaseDesign',
    data() {
        return {
            requirements: [],
            selectedRequirement: '',
            selectedRequirementId: null,
            loading: false,
            error: null,
            architecture: null,
            databaseDesigns: [],
            techIcons: {
                frontend: 'fab fa-vuejs',
                backend: 'fab fa-python',
                database: 'fas fa-database'
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
            this.fetchDatabaseDesigns(this.selectedRequirementId);
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
        async fetchDatabaseDesigns(requirementId) {
            this.loading = true;
            this.error = null;

            try {
                const response = await axios.get('http://127.0.0.1:5000/api/database_designs', {
                    params: { requirement_id: requirementId }
                });

                if (response.data.error) {
                    throw new Error(response.data.error);
                }

                this.databaseDesigns = response.data;
                this.renderDatabaseDesigns();

            } catch (error) {
                console.error('Error fetching database designs:', error);
                this.error = error.message;
                this.databaseDesigns = [];
                this.clearDesignsDisplay();
            } finally {
                this.loading = false;
            }
        },

        renderDatabaseDesigns() {
            // 清空现有内容
            this.clearDesignsDisplay();

            if (this.databaseDesigns.length === 0) return;

            // 取最新的设计（按创建时间排序后的第一个）
            const latestDesign = this.databaseDesigns[0];

            // 渲染ER图
            this.renderERDiagram(latestDesign.erd_diagram);

            // 渲染SQL脚本
            this.renderSQLScript(latestDesign.sql_script);
        },

        renderERDiagram(erdData) {
            const container = document.getElementById('tablesContainer');

            // 这里根据你的ER图数据格式进行渲染
            // 示例：假设erdData是Mermaid.js格式的字符串
            container.innerHTML = `
  <pre>
${erdData}
  </pre>
`;


            // 如果有Mermaid.js，可以初始化渲染
            if (window.mermaid) {
                mermaid.init();
            }
        },

        renderSQLScript(sqlScript) {
            const sqlPreview = document.getElementById('sqlPreview');
            sqlPreview.textContent = sqlScript;

            // // 如果有语法高亮库，可以在这里初始化
            // if (window.hljs) {
            //     hljs.highlightElement(sqlPreview);
            // }
        },

        clearDesignsDisplay() {
            document.getElementById('tablesContainer').innerHTML = `
      <div class="text-center text-gray-500 py-10">
        <i class="fas fa-database text-4xl mb-2"></i>
        <p>${this.databaseDesigns.length === 0 ? '没有找到数据库设计' : '加载中...'}</p>
      </div>
    `;

            document.getElementById('sqlPreview').textContent =
                '-- SQL语句将在这里显示\n-- 请先选择数据库设计';
        },

        // 导出SQL方法
        exportSQL() {
            if (!this.databaseDesigns || this.databaseDesigns.length === 0) return;

            const latestDesign = this.databaseDesigns[0];
            const blob = new Blob([latestDesign.sql_script], { type: 'text/sql' });
            const url = URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.href = url;
            a.download = `database_design_${this.selectedRequirementId}.sql`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        },

        // 复制SQL方法
        copySQL() {
            if (!this.databaseDesigns || this.databaseDesigns.length === 0) return;

            const latestDesign = this.databaseDesigns[0];
            navigator.clipboard.writeText(latestDesign.sql_script)
                .then(() => {
                    alert('SQL已复制到剪贴板');
                })
                .catch(err => {
                    console.error('复制失败:', err);
                });
        }
    }

  }
  </script>
  