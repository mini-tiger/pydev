<script lang="ts" setup>
import { computed, ref, inject, onMounted } from 'vue'
import { NAvatar, NSelect, NButton, NPopover } from 'naive-ui'
import { useChatStore } from '@/store'
// import { useBasicLayout } from '@/hooks/useBasicLayout'
// import { debounce } from '@/utils/functions/debounce'
import zzLogo from '@/assets/zz-logo.png'
import vNetLogo from '@/assets/reporter-logo.png'
import ListOfIntelligentAgents from './listOfIntelligentAgents.vue';
import bgzs from '@/assets/bgzs.png'
import gwb from '@/assets/gwb.png'
import gz from '@/assets/gz.png'

const props = defineProps<Props>()
const emit = defineEmits<Emit>()

const globalConfig: any = inject('globalConfig');

// const { isMobile } = useBasicLayout()
interface Props {
	usingContext?: boolean
	modelIcon?: string
	modelItem?: Chat.History
	modelIndex?: number
}

interface Emit {
	// (ev: 'export'): void
	// (ev: 'toggleUsingContext'): void
	(ev: 'modelAdd'): void

	(ev: 'modelDelete'): void
}

interface OptionsArr {
	label: string
	value: string
	icon: string
}

interface SelectedOption {
	title: string
	uuid: number
	isEdit: boolean
}

// const appStore = useAppStore()
const chatStore = useChatStore()

// const themeOverrides = {
// 	Select: {
// 		border: '0px solid rgba(111, 75, 41, 1)',
// 	},
// }
const value = ref('')
const options = ref<any>([])

const data1 = [
	{
		"name": "百川-13B",
		"alias": "百川-13B",
		"enable": "True",
		"url": "http://120.133.63.162:33382/v1"
	},
	{
		"name": "01/YI",
		"alias": "Yi-34B",
		"enable": "False",
		"url": ""
	},
	{
		"name": "通义千问-7B",
		"alias": "Qwen-7B",
		"enable": "True",
		"url": ""
	}
];

const data2 = [
	{
		"name": "百川-13B",
		"alias": "百川-13B",
		"enable": "False",
		"url": "http://120.133.63.162:33382/v1"
	},
	{
		"name": "01/YI",
		"alias": "Yi-34B",
		"enable": "True",
		"url": ""
	},
	{
		"name": "通义千问-7B",
		"alias": "Qwen-7B",
		"enable": "True",
		"url": ""
	}
];

onMounted(async () => {
	const selectedData = import.meta.env.MODE === 'zz' ? data2 : data1;
	options.value = selectedData.map(item => ({
		label: item.alias,
		value: item.name,
		url: item.url,
		style: { fontSize: '12px' },
		disabled: item.enable === 'True'
	}));
	// 选择enabled为true的第一个
	value.value = options.value.find((item: any) => !item.disabled)?.value
});

// const collapsed = computed(() => appStore.siderCollapsed)
// const currentChatHistory = computed(() => chatStore.getChatHistoryByCurrentActive)
const isIntranet = ref(computed(() => import.meta.env.VITE_NODE_ENV === 'intranet'))
const logo = ref(import.meta.env.VITE_APP_LOGO)

// logo选择
const switchLogo = (logo: string) => {
	switch (logo) {
		case 'zzLogo':
			return zzLogo
		case 'vNetLogo':
			return vNetLogo
		case 'bgzs':
			return bgzs
		case 'gwb':
			return gwb
		case 'gz':
			return gz
		default:
			return vNetLogo
	}
}

const cardsData = ref(import.meta.env.MODE === 'zz' ? [
	{
		"title": "中咨办公助手",
		"description": "一个能够智能对话的助手",
		"logo": bgzs,
		"url": "http://172.21.10.144:9301/#/aiContent"
	},
	{
		"title": "中咨法务助手",
		"description": "一个能够智能核对合同的助手",
		"logo": gz,
		"url": "http://172.21.10.144:9201/#/chat"
	},
	{
		"title": "中咨报告助手",
		"description": "一个能够智能生成报告的助手",
		"logo": gwb,
		"url": "http://172.21.10.144:9216/#/chat"
	}
] : [
	{
		"title": "中咨办公助手",
		"description": "一个能够智能对话的助手",
		"logo": bgzs,
		"url": "http://120.133.63.166:9301/#/aiContent"
	},
	{
		"title": "中咨法务助手",
		"description": "一个能够智能核对合同的助手",
		"logo": gz,
		"url": "http://120.133.63.166:9201/#/chat"
	},
	{
		"title": "中咨报告助手",
		"description": "一个能够智能生成报告的助手",
		"logo": gwb,
		"url": "http://120.133.63.166:9001/#/chat"
	}
])

const appTitle = ref(import.meta.env.VITE_APP_TITLE)
</script>

<template>
	<div class="relative flex items-center justify-between assistant">
		<div class="flex items-center logo-bg justify-start"
				 style="background: #E6EAF1; 	border-radius: 4px 0px 0px 4px; width: 500px;">
			<button class="flex pl-2 ">
				<NAvatar :class="[isIntranet ? 'intranet-logo' : 'development-logo']" :src="[isIntranet ? vNetLogo : zzLogo]"
								 style="background-color: rgba(0, 0, 0, 0); border-radius: 50%;"/>
			</button>
			<h1
				class="flex-1 overflow-hidden cursor-pointer select-none model_name text-ellipsis whitespace-nowrap pl-1"
			>
				{{ appTitle }}
			</h1>
			<NSelect class="headerSelect" v-model:value="value" size="medium"
							 style="margin-left: 4px; width: 90px;" :options="options"/>
		</div>
		<n-popover trigger="click" placement="bottom" style="padding: 0;height: 250px;" class="assistant-content">
			<template #trigger>
				<n-button class="popoverStyle" type="tertiary" style="border: none">我的智能助手</n-button>
			</template>
			<div class="assistantList">
				<div v-for="(card, index) in cardsData" :key="index" class="cardDeck">
					<ListOfIntelligentAgents :title="card.title" :description="card.description" :logo="card.logo"
																	 :url="card.url"/>
				</div>
			</div>
		</n-popover>
	</div>
</template>

<style lang="less" scoped>
:deep(.popoverStyle) {
	width: 250px;
	height: 32px;
	border-radius: 0px 4px 4px 0px;
	background: #FFFFFF;
	box-sizing: border-box;
	border: 1px solid #DCE5FF !important;

	.n-button,
	.n-button__border,
	.n-button__state-border {
		border: 0 solid #DCE5FF !important;
	}

	.n-base-wave--active {
		/* 禁用过渡效果 */
		transition: none !important;
		/* 禁用动画 */
		animation: none !important;
	}

	&:hover {
		border: 1px solid #2853E0 !important;
	}

	&:focus,
	&:active {
		border: 1px solid #2853E0 !important;
	}
}

.assistant {
	width: 500px;
	height: 32px;
	opacity: 1;
	box-sizing: border-box;
	border: 0px solid #DCE5FF;
	border-left: none;
	position: absolute;
	top: 9px;
	left: calc(50% - 250px);


	:deep(.n-button__content) {
		font-size: 14px;
		font-weight: normal;
		line-height: 14px;
		text-align: center;
		letter-spacing: 0em;
		color: #0E1C4C;

	}
}

.assistant-content {
	width: 448px;
	height: 250px;
	border: 1px solid #EBEFFD;
}

.assistantList {
	display: grid;
	grid-template-columns: repeat(2, 200px);
	grid-auto-rows: minmax(64px, auto);
	padding: 14px 16px;
	width: 448px;
	border-radius: 4px;
	background: #FFFFFF;
	box-sizing: border-box;
	gap: 14px;

	.cardDeck {
		width: 200px;
		height: 64px;
	}
}

.model_top {
	width: 100%;
	height: 50px;
	background-size: 100% 100%;
	background: #fff no-repeat;
	display: flex;
	justify-content: space-between;
	align-items: center;

	.model_name {
		font-size: 14px;
		font-weight: normal;
		line-height: 14px;
		letter-spacing: 0em;
		color: #0E1C4C;
	}

	.n-select {
		height: 100%;
		// width: 260px;
	}

	//
	.logo-bg {
		// width: 455px;
		width: 250px;
		height: 32px;
		padding-right: 0px;
		padding-left: 16px;
		border-radius: 4px;
		opacity: 1;
		background: linear-gradient(0deg, #E6EAF1, #E6EAF1), linear-gradient(0deg, #EFF2F7, #EFF2F7), #FFFFFF;
	}

	:deep(.n-base-select-menu .n-base-select-option) {
		height: 45px;
	}

	:deep(.n-base-selection) {
		height: 100%;
		color: #2853E0 !important;
		--n-border: none !important;
		--n-border-hover: none !important;
		--n-border-active: none !important;
		--n-border-focus: none !important;
		--n-box-shadow-active: none !important;
		--n-box-shadow-focus: none !important;
	}

	:deep(.n-base-selection .n-base-selection-label) {
		height: 100%;
		background-color: rgba(0, 0, 0, 0);

	}

	:deep(.n-base-selection .n-base-selection-label .n-base-selection-input) {
		border-bottom: none;
	}
}

:deep(.n-base-select-menu .n-base-select-option.n-base-select-option--selected) {
	color: #2853E0 !important;
}

:deep(.n-base-select-menu .n-base-select-option .n-base-select-option__check) {
	color: #2853E0 !important;
}

.development-logo {
	background-color: rgba(0, 0, 0, 0);
	height: 22px;
	width: 28.5px;
	object-fit: contain;
}

.intranet-logo {
	background-color: rgba(0, 0, 0, 0);
	height: 22px;
	width: 22px;
}

:deep(.v-binder-follower-content .n-base-select-menu) {
	background-color: rgba(43, 32, 26, 1) !important;
}

.n-select-menu {
	background-color: rgba(43, 32, 26, 1) !important;
}

:deep(.n-base-select-menu .n-base-select-option) {
	color: #0E1C4C;
}

:deep(.n-base-selection .n-base-selection-label .n-base-selection-input .n-base-selection-input__content) {
	color: #8092A9 !important;
	padding-right: 0 !important;
}

:deep(.n-base-selection .n-base-suffix) {
	right: 16px;
}

:deep(.headerSelect .n-base-selection .n-base-selection-label .n-base-selection-input) {
	padding: 0 42px 0 8px !important;
}

</style>
