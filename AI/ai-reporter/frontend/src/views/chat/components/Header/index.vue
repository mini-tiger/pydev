<script lang="ts" setup>
import { computed, h, ref } from 'vue'
import type { SelectRenderLabel, SelectRenderTag } from 'naive-ui'
import { NAvatar, NConfigProvider, NSelect } from 'naive-ui'
import { SvgIcon } from '@/components/common'
import { /* useAppStore, */ useChatStore } from '@/store'
// import { useBasicLayout } from '@/hooks/useBasicLayout'
// import { debounce } from '@/utils/functions/debounce'
import spark from '@/assets/spark-icon.ico'
import qianwen from '@/assets/qwen.png'
import baichuan from '@/assets/baichuan.png'
import chatglm from '@/assets/chatglm.png'
import zzLogo from '@/assets/zz-logo.png'
import vNetLogo from '@/assets/reporter-logo.png'

const props = defineProps<Props>()
const emit = defineEmits<Emit>()

// const { isMobile } = useBasicLayout()
interface Props {
  usingContext: boolean
  modelIcon: string
  modelItem: Chat.History
  modelIndex: number
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

const themeOverrides = {
  Select: {
    border: '0px solid rgba(111, 75, 41, 1)',
  },
}
const value = ref('YI-34B')
const options = ref([{
	label: '模型：百川-13B',
	value: '百川-13B',
	style: {
		fontSize: '12px'
	},
	disabled: true
}, {
	label: '模型：YI-34B',
	value: 'YI-34B',
	style: {
		fontSize: '12px'
	},
},{
	label: '模型：通义千问-7B',
	value: '通义千问-7B',
	style: {
		fontSize: '12px'
	},
	disabled: true
}])
// const collapsed = computed(() => appStore.siderCollapsed)
// const currentChatHistory = computed(() => chatStore.getChatHistoryByCurrentActive)
const appTitle = ref(import.meta.env.VITE_APP_TITLE)
const isIntranet = ref(computed(() => import.meta.env.VITE_NODE_ENV === 'intranet'))
const logo = ref(import.meta.env.VITE_APP_LOGO)
const dataSourcesData = computed(() => chatStore.history)
const modelInfo = ref(computed(() => props.modelItem))
const modelValue = ref(computed(() => modelInfo.value.title))
const ModelIndex = computed(() => chatStore.history.findIndex(item => item.title === props.modelItem.title))
const newModelOptions = ref<OptionsArr[]>([
  {
    label: 'chatglm3-6b',
    value: 'chatglm3-6b',
    icon: chatglm,
  },
  {
    label: '通义千问',
    value: '通义千问',
    icon: qianwen,
  },
  {
    label: '讯飞星火',
    value: '讯飞星火',
    icon: spark,
  },
  {
    label: '百川大模型',
    value: '百川大模型',
    icon: baichuan,
  },
])
const modelOptions = ref<OptionsArr[]>([
  {
    label: 'chatglm3-6b',
    value: 'chatglm3-6b',
    icon: chatglm,
  },
  {
    label: '通义千问',
    value: '通义千问',
    icon: qianwen,
  },
  {
    label: '讯飞星火',
    value: '讯飞星火',
    icon: spark,
  },
  {
    label: '百川大模型',
    value: '百川大模型',
    icon: baichuan,
  },
])

const renderSingleSelectTag: SelectRenderTag = ({ option }) => {
  return h(
    'div',
    {
      style: {
        display: 'flex',
        alignItems: 'center',
      },
    },
    [
      h(NAvatar, {
        src: option.icon as string,
        round: true,
        size: 24,
        style: {
          marginRight: '12px',
        },
      }),
      option.label as string,
    ],
  )
}

const renderLabel: SelectRenderLabel = (option) => {
  return h(
    'div',
    {
      style: {
        display: 'flex',
        alignItems: 'center',
      },
    },
    [
      h(NAvatar, {
        src: option.icon as string,
        round: true,
        size: 'medium',
        style: {
          backgroundColor: 'rgba(0, 0, 0, 0)',
        },
      }),
      h(
        'div',
        {
          style: {
            marginLeft: '12px',
            padding: '14px 0',
            color: '#d8d1c0',
          },
        },
        [
          h('div', null, [option.label as string]),
          // h(
          //   NText,
          //   { depth: 3, tag: 'div' },
          //   {
          //     default: () => 'description',
          //   },
          // ),
        ],
      ),
    ],
  )
}
// function handleUpdateCollapsed() {
//   appStore.setSiderCollapsed(!collapsed.value)
// }

// function onScrollToTop() {
//   const scrollRef = document.querySelector('#scrollRef')
//   if (scrollRef)
//     nextTick(() => scrollRef.scrollTop = 0)
// }

// function handleExport() {
//   emit('export')
// }

// function toggleUsingContext() {
//   emit('toggleUsingContext')
// }
// function handleAdd() {
//   chatStore.addHistory({ title: 'New Chat', uuid: Date.now(), isEdit: false })
//   if (isMobile.value)
//     appStore.setSiderCollapsed(true)
// }

</script>

<template>
  <header v-show="false"
    class="sticky top-0 left-0 right-0 z-30 model_top dark:border-neutral-800 bg-white/80 dark:bg-black/20 backdrop-blur"
  >
    <div class="relative flex items-center justify-center w-full min-w-0 overflow-hidden h-14" >
      <div class="flex items-center justify-center logo-bg" >
        <button class="flex items-center justify-center">
          <NAvatar :class="[isIntranet ? 'intranet-logo' : 'development-logo']" :src="[isIntranet ? vNetLogo : zzLogo]" style="background-color: rgba(0, 0, 0, 0); border-radius: 50%;" />
        </button>
        <h1
          class="flex-1 overflow-hidden cursor-pointer select-none model_name text-ellipsis whitespace-nowrap"
        >
				{{ appTitle }}
          <!-- 中咨报告助手 -->
        </h1>
				<NSelect class="headerSelect" v-model:value="value" size="medium" style="margin-left: 32px; width: auto; text-align: end;" :options="options" />
      </div>
    </div>
  </header>
</template>

<style lang="less" scoped>
// @import url(${import.meta.env.VITE_HEADER_LOGO_CSS_PATH});
.model_top {
  width: 100%;
  height: 50px;
  background: #fff;
  background-size: 100% 100%;
  background-repeat: no-repeat;
  display: flex;
  justify-content: space-between;
  align-items: center;

  .model_name {
		padding-left: 6px;
    font-size: 14px;
    color: #0E1C4C;
  }
  .n-select {
    height: 100%;
		// width: 260px;
  }
  //
	.logo-bg {
		// width: 455px;
		padding-right: 0px;
		padding-left: 16px;
		height: 32px;
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
  // :deep(.n-base-selection .n-base-selection-label .n-base-selection-input) {
  //   height: 56px;
  //   line-height: 56px;
  //   font-size: 16px;
  //   color: #d8d1c0;
  // }
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
}

.intranet-logo {
  background-color: rgba(0, 0, 0, 0);
  height: 22px;
	width: 22px;
}

:deep(.v-binder-follower-content .n-base-select-menu) {
  background-color: rgba(43,32,26,1) !important;
}
.n-select-menu {
  background-color: rgba(43,32,26,1) !important;
}
:deep(.n-base-select-menu .n-base-select-option) {
	color: #0E1C4C;
}
:deep(.n-base-selection .n-base-selection-label .n-base-selection-input .n-base-selection-input__content) {
	color: #8092A9 !important;
}
:deep(.n-base-selection .n-base-suffix) {
	right: 16px;
}
:deep(.headerSelect .n-base-selection .n-base-selection-label .n-base-selection-input){
	padding: 0 42px 0 12px !important;
}
// :deep(.n-base-selection .n-base-selection-label .n-base-selection-input) {
// 	padding: 0;
// }
</style>
