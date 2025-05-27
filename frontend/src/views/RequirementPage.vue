<template>
    <div class="p-8">
        <div class="bg-white rounded-lg shadow p-6 mb-6">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-lg font-medium">需求列表</h2>
                <button class="bg-primary text-white px-4 py-2 !rounded-button flex items-center">
                    <i class="fas fa-plus mr-2"></i>新建需求
                </button>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full">
                    <!-- <thead>
                                <tr class="bg-gray-50">
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">需求名称</th>
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">优先级</th>
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">状态</th>
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">创建时间</th>
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">操作</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="border-t">
                                    <td class="px-4 py-4 text-sm">设计一个医院系统</td>
                                    <td class="px-4 py-4"><span
                                            class="px-2 py-1 bg-red-100 text-red-800 rounded text-sm">高</span></td>
                                    <td class="px-4 py-4"><span
                                            class="px-2 py-1 bg-green-100 text-green-800 rounded text-sm">进行中</span>
                                    </td>
                                    <td class="px-4 py-4 text-sm">2024-01-15</td>
                                    <td class="px-4 py-4">
                                        <button class="text-primary hover:text-primary-dark mr-2"><i
                                                class="fas fa-edit"></i></button>
                                        <button class="text-red-500 hover:text-red-600"><i
                                                class="fas fa-trash"></i></button>
                                    </td>
                                </tr>
                                <tr class="border-t">
                                    <td class="px-4 py-4 text-sm">设计一个商城系统</td>
                                    <td class="px-4 py-4"><span
                                            class="px-2 py-1 bg-yellow-100 text-yellow-800 rounded text-sm">中</span>
                                    </td>
                                    <td class="px-4 py-4"><span
                                            class="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm">待审核</span></td>
                                    <td class="px-4 py-4 text-sm">2024-01-14</td>
                                    <td class="px-4 py-4">
                                        <button class="text-primary hover:text-primary-dark mr-2"><i
                                                class="fas fa-edit"></i></button>
                                        <button class="text-red-500 hover:text-red-600"><i
                                                class="fas fa-trash"></i></button>
                                    </td>
                                </tr>
                                <tr class="border-t">
                                    <td class="px-4 py-4 text-sm">设计一个某某系统</td>
                                    <td class="px-4 py-4"><span
                                            class="px-2 py-1 bg-yellow-100 text-yellow-800 rounded text-sm">中</span>
                                    </td>
                                    <td class="px-4 py-4"><span
                                            class="px-2 py-1 bg-gray-100 text-gray-800 rounded text-sm">已完成</span></td>
                                    <td class="px-4 py-4 text-sm">2024-01-13</td>
                                    <td class="px-4 py-4">
                                        <button class="text-primary hover:text-primary-dark mr-2"><i
                                                class="fas fa-edit"></i></button>
                                        <button class="text-red-500 hover:text-red-600"><i
                                                class="fas fa-trash"></i></button>
                                    </td>
                                </tr>
                            </tbody> -->
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>User ID</th>
                            <th>Name</th>
                            <th>Version</th>
                            <!-- <th>Content</th> -->
                            <th>Created At</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="requirement in requirements" :key="requirement.id">
                            <td>{{ requirement.id }}</td>
                            <td>{{ requirement.user_id }}</td>
                            <td>{{ requirement.name }}</td>
                            <td>{{ requirement.version }}</td>
                            <!-- <td>{{ requirement.content }}</td> -->
                            <td>{{ requirement.created_at }}</td>
                            <td class="px-4 py-4">

                                <button class="text-primary hover:text-primary-dark mr-2"
                                    @click="editRequirement(requirement)">Edit</button>
                                <button class="btn btn-danger btn-sm"
                                    @click="deleteRequirement(requirement.id)">Delete</button>

                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>
            <div v-if="showModal" class="modal">
                <div class="modal-content">
                    <h3>Edit Requirement</h3>
                    <textarea v-model="editedContent" class="textarea"></textarea>
                    <button @click="saveRequirement">Save</button>
                    <button @click="closeModal">Cancel</button>
                </div>
            </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-lg font-medium mb-6">需求统计</h2>
            <div class="grid grid-cols-4 gap-6">
                <div class="p-4 bg-blue-50 rounded-lg">
                    <div class="text-blue-600 mb-2">
                        <i class="fas fa-clipboard-list text-xl"></i>
                    </div>
                    <div class="text-2xl font-semibold text-gray-800">24</div>
                    <div class="text-sm text-gray-500">总需求数</div>
                </div>
                <div class="p-4 bg-green-50 rounded-lg">
                    <div class="text-green-600 mb-2">
                        <i class="fas fa-check-circle text-xl"></i>
                    </div>
                    <div class="text-2xl font-semibold text-gray-800">18</div>
                    <div class="text-sm text-gray-500">已完成</div>
                </div>
                <div class="p-4 bg-yellow-50 rounded-lg">
                    <div class="text-yellow-600 mb-2">
                        <i class="fas fa-clock text-xl"></i>
                    </div>
                    <div class="text-2xl font-semibold text-gray-800">4</div>
                    <div class="text-sm text-gray-500">进行中</div>
                </div>
                <div class="p-4 bg-red-50 rounded-lg">
                    <div class="text-red-600 mb-2">
                        <i class="fas fa-exclamation-circle text-xl"></i>
                    </div>
                    <div class="text-2xl font-semibold text-gray-800">2</div>
                    <div class="text-sm text-gray-500">待处理</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';


const requirements = ref([]);
const showModal = ref(false)
const editedContent = ref('')
const editingId = ref(null)
// const showModalForAdd = () => {
//     newRequirement.value = '';
//     editing.value = false;
//     showModal.value = true;
// };


const closeModal = () => {
    showModal.value = false;
};

const saveRequirement = async () => {
    try {
        if (editingId.value) {
            await axios.put(`http://127.0.0.1:5000/api/requirements/${editingId.value}`, { content: editedContent.value });
        } 
        await fetchRequirements();
        closeModal();
    } catch (error) {
        console.error('Error saving requirement:', error);
    }
};

const fetchRequirements = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5000/api/requirements');
        requirements.value = response.data;
    } catch (error) {
        console.error('Error fetching requirements:', error);
    }
};
const editRequirement = (requirement) => {
    editedContent.value = requirement.content
    editingId.value = requirement.id
    showModal.value = true
}
onMounted(() => {
    fetchRequirements();
});
// const deleteRequirement = async (id) => {
//     try {
//         await axios.delete(`/api/requirements/${id}`);
//         await fetchRequirements();
//     } catch (error) {
//         console.error('Error deleting requirement:', error);
//     }
// };


// export default {
//     setup() {
//         const requirements = ref([]);

//         onMounted(() => {
//             axios.get('http://127.0.0.1:5000/api/requirements')
//                 .then(response => {
//                     requirements.value = response.data;
//                 })
//                 .catch(error => {
//                     console.error('There was an error!', error);
//                 });
//         });

//         return {
//             requirements
//         };
//     }
    
// };
</script>

<style>
.modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
}

.modal-content {
    background: white;
    padding: 1em;
    margin: 10% auto;
    width: 600px;
    border-radius: 8px;
}

.textarea {
    width: 100%;
    height: 600px;
    
    margin-bottom: 1em;
}
</style>