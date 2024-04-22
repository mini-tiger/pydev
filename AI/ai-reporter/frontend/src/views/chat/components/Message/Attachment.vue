<script lang="ts" setup>
import { computed, inject, ref, watch, onUnmounted, reactive, isReactive } from 'vue'
import { NButton, NImage } from 'naive-ui'
import { useBasicLayout } from '@/hooks/useBasicLayout'
import wordIcon from '@/assets/word-icon.png'
import { useChatStore } from "@/store";

interface Props {
  inversion?: boolean // 是否用户
  error?: boolean // 是否出错
  text?: string // 文本
  loading?: boolean
  asRawText?: boolean // 是否文本
  isKnowLedge?: boolean // 是否知识库对话
  source?: string[] // 知识库问答中的匹配结果来源 默认3条
	fileName?: string
	downloadUrl?: string
	viewUrl?: string
	actionEnd?: boolean
	messageKey: number
}

const props = defineProps<Props>()

const { isMobile } = useBasicLayout()
const wrapClass = computed(() => {
  return [
    'text-wrap',
    'min-w-[20px]',
    'rounded-md',
		'px-3',
    isMobile.value ? 'p-2' : 'py-2',
    // props.inversion ? '' : 'bg-[#fff]',
    props.inversion ? 'dark:bg-[#a1dc95]' : 'dark:bg-[#1e1e20]',
    props.inversion ? 'message-request' : 'message-reply',
    props.inversion ? 'text-user' : 'text-model',
    { 'text-red-500': props.error },
    // { 'w-full': !props.inversion },
    // { 'px-3': !props.inversion },
  ]
})

const sendGrandson = inject('sendGrandson')
const viewAttachment = (file_name: any, viewUrl: any) => {
	sendGrandson(file_name, viewUrl)
}

const downloadAttachment = (downloadUrl: any) => {
	window.open(downloadUrl)
}

// 进度条样式
const progressStyle = computed(() => {
	return {
		background: `linear-gradient(to right, rgba(40, 83, 224, 0.1) 0%, rgba(40, 83, 224, 0.1) ${progress.value}%, transparent ${progress.value}%, transparent 100%)`,
		backgroundColor: 'white'
	};
});

// 获取数据
const chatStore = useChatStore()
const dataChat = reactive(chatStore.$state.chat[0].data)

// 获取对话标题
const extractSubjectFromText = (text: string) => {
	const lines = text.split('\n');

	for (const line of lines) {
		if (line.startsWith('主题：')) {
			// 提取这一行的剩余部分，即主题的内容
			return line.substring('主题：'.length).trim();
		}
	}

	// 如果没有找到匹配的行，返回一个空字符串或者其他指示没有找到的值
	return '';
}

// 标题
const messageTitle = computed(() => {
	const text = dataChat[props.messageKey]?.requestOptions.prompt
	return extractSubjectFromText(text)
})

// 当前进度次数
const currentCount = computed(() => {
	if (dataChat[props.messageKey].logTracing){
		return dataChat[props.messageKey]?.logTracing.length
	}else {
		return 0
	}
})

// 进度
const totalCounts = ref<number>(40); // 总进度数，此处假设为40

const progress = computed(() => {
	if (props.actionEnd) {
		return 100; // 进度直接设置为 100%
	} else {
		if (currentCount.value > 0 && totalCounts.value > 0) {
			const ratio = currentCount.value / totalCounts.value; // 计算当前进度比例
			return Math.min(100, ratio * 100); // 计算进度值，并确保不超过 100%
		} else {
			return 0;
		}
	}
});

interface ProgressUpdate {
	time: number;
	progress: number;
}

const windowSize = 7;
const progressUpdates = ref<ProgressUpdate[]>([]);

// 剩余时间计算逻辑，示例定义
const remainingTime = ref<string>('计算中...');
const lastRemainingTime = ref<number>(Infinity); // 存储上一次的剩余时间（秒）

watch(currentCount, (newVal, oldVal) => {
	const currentTime = Date.now();
	progressUpdates.value.push({ time: currentTime, progress: newVal });

	if (progressUpdates.value.length > windowSize) {
		progressUpdates.value.shift();
	}

	if (progressUpdates.value.length === windowSize) {
		const first = progressUpdates.value[0];
		const last = progressUpdates.value[progressUpdates.value.length - 1];
		const elapsedTime = last.time - first.time;
		const progressChange = last.progress - first.progress;
		const averageSpeed = progressChange / (elapsedTime || 1); // 防止除以0

		const remainingProgress = totalCounts.value - last.progress;
		const estimatedRemainingTime = averageSpeed > 0 ? remainingProgress / averageSpeed : 0;

		// 当剩余时间小于等于1秒时，显示"正在合并"
		if (estimatedRemainingTime <= 1000) {
			remainingTime.value = '报告正在合并';
		} else {
			const remainingTimeInSeconds = estimatedRemainingTime / 1000; // 转换成秒
			if (remainingTimeInSeconds < lastRemainingTime.value) { // 仅更新小于上次的剩余时间
				const minutes = Math.floor(estimatedRemainingTime / 60000);
				const seconds = Math.floor((estimatedRemainingTime % 60000) / 1000);
				remainingTime.value = `${minutes > 0 ? `${minutes}分钟` : ''}${seconds}秒`;
				lastRemainingTime.value = remainingTimeInSeconds; // 更新上一次的剩余时间
			}
		}
	} else {
		remainingTime.value = '计算中...';
	}
}, { immediate: true });


// 动态监听
watch(() => dataChat[props.messageKey]?.logTracing, (newVal) => {
	if (newVal && newVal.length > 0) {
		const total = newVal[0].totalCounts; // 第一项包含totalCounts属性
		if (total) {
			totalCounts.value = total + 3;
		}
	}
}, { immediate: true, deep: true });


// 是否显示进度
const showProgress = computed(() => {
	// 如果 actionEnd 已经完成
	if (props.actionEnd){
		return true;
	}
	// 进行中为 true
	if (props.loading) {
		return true;
	}
	// 有错误为 true
	if (props.error){
		return false;
	}

	return false;
});
</script>

<template>
	<div v-if="showProgress">
		<div class="text-black ml-[40px] flex" style="align-items: center; margin-top: 10px;" :style="progressStyle" :class="wrapClass">
			<NImage width="30" preview-disabled :src="wordIcon" />
			<div class="title ml-[3px]" style="line-height: 20px; width: 100%;">
				{{ messageTitle || fileName }}.docx
			</div>
		</div>
		<div class="mt-[5px]" style="text-align: end;" v-show="actionEnd">
			<n-button class="attachBtn" size="tiny" ghost style="background-color: #fff;" color="#2853e0" @click="viewAttachment(fileName, viewUrl)">
				文件预览
			</n-button>
			<n-button class="attachBtn" size="tiny" ghost style="background-color: #fff; margin-left: 5px;" color="#2853e0" @click="downloadAttachment(downloadUrl)">
				文件下载
			</n-button>
		</div>
		<div class="mt-[5px] text-xs text-right" style="color: #2853E0;" v-if="!actionEnd">
			预计剩余: {{ remainingTime }}
		</div>
	</div>
</template>

<style lang="less" scoped>
// @import url(./style.less);
.attachBtn {
	--n-color: #fff !important;
	--n-color-hover: rgba(40, 83, 224, 0.08) !important;
	--n-color-pressed:  rgba(40, 83, 224, 0.15) !important;
	--n-color-focus: rgba(40, 83, 224, 0.15) !important;
}

.progress-element {
	transition: background 3s ease;
}
</style>
