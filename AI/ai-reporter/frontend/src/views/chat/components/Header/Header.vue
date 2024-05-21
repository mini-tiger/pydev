<template>
	<div class="main w-full flex justify-between items-center">
		<!-- 左 -->
		<div class="flex justify-start items-center pl-4 cursor-pointer" @click="goToTheHomePage">
			<img src="@/assets/zz-logo.png" alt="" class="w-7">
			<div class="ml-2">大模型助手</div>
		</div>
		<!--中-->
		<div>
			<IntelligentAssistant></IntelligentAssistant>
		</div>
		<!-- 右 -->
		<div class="flex justify-end items-center pr-4">
			<div class="underline cursor-pointer mr-[10px]" @click="reportTemplate">报告模板管理</div>
			<!-- <el-popover placement="bottom" trigger="click" persistent width="250px">
				<template #reference>
					<el-button class="mx-3" type="text">
						<el-icon class="icon">
							<Setting/>
						</el-icon>
					</el-button>
				</template>
				<div class="dropdownContent">
					<div class="h-8 flex justify-between items-center cursor-pointer">
						<div class="font-bold text-black">
							知识库(RAG)
						</div>
					</div>
					<div class="h-8 flex justify-between items-center cursor-pointer">
						<div :class="!isKnowledgeBase ? 'text-gray-500' : 'text-black'">打开不含知识库版本</div>
						<el-button v-show="isKnowledgeBase" type="default" size="small" @click="noKnowledgeBase">打开</el-button>
					</div>
					<div class="h-8 flex justify-between items-center cursor-pointer">
						<div :class="isKnowledgeBase ? 'text-gray-500' : 'text-black'">打开包含知识库版本</div>
						<el-button v-show="!isKnowledgeBase" type="default" size="small" @click="knowledgeBase">打开</el-button>
					</div>
				</div>
			</el-popover> -->
			<img src="@/assets/user.png" alt="" style="width: 22px; height: 22px;" class="cursor-pointer"/>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ElPopover, ElButton } from 'element-plus';
import { Setting } from '@element-plus/icons-vue';
import IntelligentAssistant from './IntelligentAssistant.vue';
// import { useRoute } from 'vue-router';
import { useMessage } from 'naive-ui'
import { onMounted, ref } from 'vue';


const message = useMessage()

// const route = useRoute();
// const ragQuery = route.query.rag;
const isKnowledgeBase = ref<boolean | null>(null);

// 在 setup 中或者全局注册组件
const reportTemplate = () => {
	message.warning('正在升级中')
}

function checkPort(): boolean {
	const port = window.location.port;
	console.log("port", port);
	return port === '9003' || port === '9004';
}

// function checkPortPeriodically(): Promise<boolean> {
// 	return new Promise((resolve) => {
// 		const intervalId = setInterval(() => {
// 			if (portCheckResult.value !== null) {
// 				// 如果已经有结果（无论是什么结果），提前结束
// 				clearInterval(intervalId);
// 				resolve(portCheckResult.value);
// 			}
//
// 			// 更新端口检查结果
// 			portCheckResult.value = checkPort();
//
// 			if (portCheckCounter.value >= 3) {
// 				clearInterval(intervalId);
// 				resolve(portCheckResult.value);
// 			}
//
// 			portCheckCounter.value++;
// 		}, 1000);
// 	});
// }

// 有 rag 的只有 9003
const knowledgeBase = () => {
	window.open('http://120.133.63.166:9003/#/chat', '_blank')
}

// 没有rag
const noKnowledgeBase = () => {
	window.open('http://120.133.63.166:9001/#/chat', '_blank')
}

const goToTheHomePage = () => {
	// window.open('http://ai.vnet.com/#/aiTool')
}

onMounted(() => {
	isKnowledgeBase.value = checkPort();
	console.log("isKnowledgeBase.value", isKnowledgeBase.value)
});
</script>

<style lang="less" scoped>
.main {
	height: 50px;
	border-bottom: 1px solid #D3DEFF;

	.icon {
		width: 22px;
		height: 22px;
		color: #000;

		svg {
			width: 22px;
			height: 22px;
		}
	}


	:deep(.el-popover) {
		box-shadow: none !important;
	}
}
</style>
