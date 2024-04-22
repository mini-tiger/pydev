<script setup lang='ts'>
import { ref, computed, watch } from 'vue'
import { NImage, NAvatar } from 'naive-ui'
import { SvgIcon } from '@/components/common'
import ai from '@/assets/aiagent.png'
import zzLogo from '@/assets/zz-logo.png'
import vNetLogo from '@/assets/vnet-logo.png'
import Progress from './Progress.vue'
import { useChatStore } from '@/store'
import { useScroll } from '../../hooks/useScroll'

interface Props {
	processStatus: string,
	processArr: any,
	chatUuid: number
}
const props = defineProps<Props>()
const logo = ref(import.meta.env.VITE_INITIAL_LOGO)
const isIntranet = ref(computed(() => import.meta.env.VITE_NODE_ENV === 'intranet'))

const { scrollRef, scrollToBottom } = useScroll()

const chatStore = useChatStore()
const logTracing = ref(computed(() => {
	scrollToBottom()
	const chat = chatStore.getChatByUuidAndIndex(0, props.chatUuid)
	const logArr = chat?.logTracing
	if (chat?.error) {
		logArr[logArr.length - 1].status = 'error'
	}
	return logArr
}))
</script>
<template>
	<div ref="scrollRef" class="w-full overflow-y-auto initial_main">
		<div v-if="processStatus === 'initial' && chatUuid === 0"
			class="flex flex-col items-center justify-center w-full h-full initial">
			<div class="flex flex-row items-center justify-center w-full">
				<NAvatar :class="[isIntranet ? 'intranetLogoAvatar' : 'devLogoAvatar']" :src="[isIntranet ? vNetLogo : zzLogo]" style="background-color: rgba(0, 0, 0, 0);" />
<!--				<SvgIcon v-if="!isIntranet" icon="material-symbols-light:add" style="margin: 0 3px" />-->
<!--				<NImage :src="ai" height="15" :width="67"></NImage>-->
			</div>
			<div class="text_content">报告文件在这里预览</div>
		</div>
		<div v-else class="flex flex-col w-full progress">
			<h1 class="flex justify-center title mt-[5px] mb-[-10px]">任务执行日志</h1>
			<div v-for="(item, index) in logTracing" :key="index">
				<Progress :time="item.time" :status="item.status" :title="item.title ? item.title : item.content"
					:content="item.sub_content" :action="item.action" :file_name="item.file_name" :download_url="item.download_url" :view_url="item.view_url" />
			</div>
			<!-- <Progress :time="'2022.06.06 10:00:00'" :status="'success'" :title="'文本摘要提取，调用成功！'" :content="'报告标题：《中国单片机行业研究报》'" /> -->
		</div>
	</div>
</template>

<style lang="less" scoped>
.initial_main {
	height: calc(100% - 50px);
	padding-bottom: 60px;

	.text_content {
		margin-top: 11.5px;
		font-family: PingFang SC;
		font-size: 14px;
		font-weight: normal;
		line-height: 18px;
		letter-spacing: 0px;
		color: #0C296E;
	}
	.intranetLogoAvatar {
		height: 20px;
		width: 48px;
		margin-top: 5px;
		margin-right: 9px;
	}
	.devLogoAvatar {
			height: 22px;
			width: 28.5px;
	}

	:deep(.n-image img) {
		height: 15px;
		border-radius: 0;
	}
}
</style>
