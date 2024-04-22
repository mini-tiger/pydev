<script setup lang='ts'>
import { computed, inject } from 'vue'
import { NAvatar, NButton } from 'naive-ui'
import loadingIcon from '@/assets/loading.gif'
import successIcon from '@/assets/success.png'
import failureIcon from '@/assets/failure.png'

interface Props {
	time: string,
	title: string,
	content: string,
	status: string,
	index: string,
	action?: string,
	file_name?: string,
	download_url?: string,
	view_url?: string
}
const props = defineProps<Props>()
// defineProps<Props>()
const progressIcon = computed(() => {
	return props.status === 'generating' ? loadingIcon : props.status === 'finish' ? successIcon : failureIcon
})
const sendGrandson = inject('sendGrandson')
const sendtoYe = (file_name: any, view_url: any) => {
	sendGrandson(file_name, view_url)
}
</script>
<template>
	<div class="w-full pl-4 mt-3 overflow-hidden">
		<main class="flex flex-col w-full">
			<div class="time normal">{{ time }}</div>
			<div class="flex flex-col justify-center content">
				<div class="flex flex-col justify-center content_bg">
					<div class="title normal">
						<span>{{ title }}</span>
						<NAvatar :src="progressIcon" :size="18" style="margin-left: 8px; background-color: rgba(0, 0, 0, 0); border-radius: 50%; vertical-align: sub;">
						</NAvatar>
					</div>
					<div v-if="content" class="detail normal">
						{{ content }}
					</div>
					<NButton v-if="view_url" style="color:#2853E0; position: absolute; right:12px;" class="previewBtn title" text @click="sendtoYe(file_name, view_url)">预览</NButton>
				</div>
			</div>
		</main>
	</div>
</template>

<style lang="less">
.normal {
	font-family: PingFang SC;
	font-weight: normal;
	line-height: 10px;
	letter-spacing: 0px;
}

.time {
	margin-bottom: 8px;
	font-size: 10px;
	color: #8092A9;
}

.content {
	width: 75%;
	height: 68px;
	background: linear-gradient(90deg, rgba(244, 247, 255, 0.66) 0%, rgba(244, 247, 255, 0) 100%), #FCFDFF;
	position: relative;
	.content_bg {
		width: 100%;
		height: 100%;
		padding-left: 14px;
		position: relative;
		background: url('@/assets/border.png');
		background-size: 100% 100%;
		background-repeat: no-repeat;
	}
}

.content:hover {
	background: linear-gradient(90deg, rgba(244, 247, 255, 0.66) 0%, rgba(244, 247, 255, 0) 100%), #FCFDFF;
	box-shadow: 0px 4px 16px 0px rgba(182, 196, 255, 0.4);
}

.title {
	color: #0C296E;
	font-size: 12px;
	line-height: 16px;
}

.detail {
	font-size: 12px;
	color: #8092A9;
	line-height: 16px;
	padding-top: 6px;
}
.previewBtn:hover {
	border-bottom: 1px solid #2853E0;
}
</style>
