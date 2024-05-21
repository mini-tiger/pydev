<script setup lang='ts'>
import type { Ref } from 'vue'
import { computed, onBeforeMount, ref } from 'vue'
import { NAutoComplete, NButton, NConfigProvider, NInput, NTabs, NTabPane, useMessage, NForm, NFormItem } from 'naive-ui'
import ChatComponent from '../chat/index.vue'
import { useBasicLayout } from '@/hooks/useBasicLayout'
import { useChatStore } from '@/store'
import { SvgIcon } from '@/components/common'
import Initial from '../chat/components/Preview/Initial.vue'
import File from '../chat/components/Preview/File.vue'

// const route = useRoute()
const ms = useMessage()
const chatStore = useChatStore()
const themeOverrides = {
  Input: {
    paddingTiny: '0 8px',
    // color: 'rgba(0, 0, 0, 0.1)',
    // colorFocus: 'rgba(0, 0, 0, 0.5)',
    // textColor: 'rgba(255, 255, 255, 0.82)',
    // border: '1px solid rgba(111, 75, 41, 1)',
		border: 'none',
		heightLarge: '152px'
  },
}
const { isMobile } = useBasicLayout()

// const dataSourcesData = computed(() => chatStore.history)
const dataSourcesData = ref(computed(() => chatStore.history))

// const conversationListLen = computed(() => chatStore.history.length)

const annoListRef = ref<any>([])
const childRef = (el: any) => {
  annoListRef.value.push(el)
}
// 页面加载spin
// const show = ref(false)

const prompt = ref<string>(`请帮我生成一份研究报告：
主题：中国自行车发展的行业研究报告
行业：车辆交通
字数：10000以上。`)
const inputValue = ref<string>('')
const status = ref<boolean>(false)
const inputRef = ref<Ref | null>(null)
const nameRef = ref('文件预览')
const panelsRef = ref([{
	title: '文件预览 ', // 默认
	url: '',
	status: 'initial',
	index: 1
},
{
	title: '中国自行车发展的行业研究报告.docx', // 默认
	url: 'http://120.133.63.166:8012/onlinePreview?url=aHR0cDovLzEyMC4xMzMuNjMuMTY2OjUwMDEvYXR0YWNobWVudC9kb3dubG9hZC/kuK3lm73oh6rooYzovablj5HlsZXooYzkuJrnoJTnqbbmiqXlkYouZG9jeA%3D%3D&officePreviewType=pdf',
	status: 'preview',
	index: 2
},
{
	title: '任务执行日志 ', // 默认
	url: '',
	status: 'loading',
	index: 3
}])
const handleClose = (name: string) => {
	const { value: panels } = panelsRef
	if (panels.length === 1) {
		ms.error('最后一个了')
		return
	}
	ms.info('关掉 ' + name)
	const index = panels.findIndex((v) => name === v.title)
	panels.splice(index, 1)
	if (nameRef.value === name) {
		nameRef.value = panels[index].title
	}
}

const formRef = ref(null)
const formShowLabel = ref(true)
const formItemShowLabel = ref(true)
const formValue = ref({
				user: {
					name: '',
					age: ''
				},
				phone: ''
})
// 添加PromptStore
// const promptStore = usePromptStore()
const buttonDisabled = computed(() => {
  return !prompt.value || prompt.value.trim() === ''
})
// 历史记录相关
// const history: any = ref([])
// 使用storeToRefs，保证store修改后，联想部分能够重新渲染
// const { promptList: promptTemplate } = storeToRefs<any>(promptStore)

// const getDataFromLocalStorage = () => {
//   const data = localStorage.getItem('chatStorage') || '[]'
//   console.log(data)
//   dynamicText.value = data
// }

// watch(
//   () => dataSourcesData,
//   async (newVal: any) => {
//     await nextTick()
//     dataSourcesData = computed(() => chatStore.history)
//     console.log(newVal)
//   },
//   {
//     immediate: true,
//     deep: true,
//   },
// )

const handleSubmit = () => {
  // annoListRef.value.map((item: { handleSubmit: (arg0: string) => void }): void => {
  //   // return console.log(item) // 打印效果在下方
  //   if (prompt.value) {
  //     inputValue.value = prompt.value
  //     status.value = true
  //     // console.log("123")
  //     return item.handleSubmit(inputValue.value)
  //   }
  // })
  if (prompt.value)
    inputValue.value = prompt.value
  prompt.value = ''
  //   // status.value = true
  //   // console.log("123")
  // }
}
const footerClass = computed(() => {
  // let classes = ['p-4']
	let classes
  if (isMobile.value)
    classes = ['sticky', 'left-0', 'bottom-0', 'right-0', 'p-2', 'pr-3', 'overflow-hidden']
  return classes
})

const sendBtnClass = computed(() => {
  let classes = ['webSendBtn']
  if (isMobile.value)
    classes = ['h5SendBtn']
  return classes
})

function handleEnter(event: KeyboardEvent) {
  if (!isMobile.value) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      handleSubmit()
      // prompt.value = ''
    }
  }
  else {
    if (event.key === 'Enter' && event.ctrlKey) {
      event.preventDefault()
      handleSubmit()
      // prompt.value = ''
    }
  }
  onBeforeMount(() => {
    // await nextTick() // 等待下一次 DOM 更新
    // getDataFromLocalStorage()
    console.log(localStorage.getItem('chatStorage'))
  })
}
</script>

<template>
  <div class="flex flex-row w-full h-full chat_bg">
    <div class="chat_box">
      <main class="flex flex-col overflow-hidden mainer">
        <div id="scrollRef" ref="scrollRef" class="flex overflow-hidden overflow-y-auto">
          <template v-for="(item, index) of dataSourcesData" :key="index">
            <ChatComponent
              :ref="childRef" :chat-id="item.uuid" :model-name="item.title" :input-value="inputValue"
              :input-complete="status" :chat-index="index" :model-module="item"
            />
          </template>
        </div>
        <footer :class="footerClass">
          <div class="w-full m-auto">
            <div class="flex items-center justify-between space-x-2" style="position: relative;">
							<NInput
								ref="inputRef" v-model:value="prompt" class="input_value" type="textarea" clearable placeholder="请帮我生成一份研究报告：" size="large"
								:autosize="{ minRows: 2, maxRows: isMobile ? 4 : 8 }" @keypress="handleEnter"
							/>
							<div class="textarea_form">
								<!-- <n-form ref="formRef" :model="formValue" label-placement="left" label-width="auto">
									<n-form-item label="主题" path="user.name"
									>
										<n-input v-model:value="formValue.user.name" placeholder="输入主题" />
									</n-form-item>
									<n-form-item label="要求" path="user.age">
										<n-input v-model:value="formValue.user.age" placeholder="请输入报告要求，如：包含，概述、可行性分析、竞品分析、行业调研等；" />
									</n-form-item>
									<n-form-item label="年份" path="user.phone">
										<n-input v-model:value="formValue.phone" placeholder="输入年份" />
									</n-form-item>
									<n-form-item label="行业" path="user.phone">
										<n-input v-model:value="formValue.phone" placeholder="输入行业" />
									</n-form-item>
									<n-form-item label="字数" path="user.phone">
										<n-input v-model:value="formValue.phone" placeholder="输入字数" />
									</n-form-item>
								</n-form> -->
							</div>
							<!-- <NConfigProvider class="w-full" :theme-overrides="themeOverrides">
                <NAutoComplete v-model:value="prompt">
                  <template #default="{ handleInput, handleBlur, handleFocus }">
                    <NInput
                      ref="inputRef" v-model:value="prompt" class="input_value" type="textarea" clearable placeholder="请帮我生成一份研究报告：" size="large"
                      :autosize="{ minRows: 2, maxRows: isMobile ? 4 : 8 }" @input="handleInput" @focus="handleFocus"
                      @blur="handleBlur" @keypress="handleEnter"
                    />
                  </template>
                </NAutoComplete>
              </NConfigProvider> -->
              <NButton class="sendBtn" :class="sendBtnClass" type="primary" size="medium" color="#2853E0" :disabled="buttonDisabled" @click="handleSubmit">
								生成报告
                <!-- <template #icon>
                  <span class="dark:text-black">
                    <SvgIcon icon="ri:send-plane-fill" />
                  </span>
                </template> -->
              </NButton>
            </div>
          </div>
        </footer>
      </main>
    </div>
		<div class="preview_box">
			<NTabs
				v-model:value="nameRef"
				type="card"
				closable
				tab-style="min-width: 80px;"
				@close="handleClose"
			>
				<NTabPane
					v-for="panel in panelsRef"
					:key="panel.index"
					:tab="panel.title.toString()"
					:name="panel.title"
				>
					<!-- {{ panel }} -->
					<Initial v-if="!panel.url" :process-status="panel.status" />
					<File v-else :file-url="panel.url" />
				</NTabPane>
			</NTabs>
		</div>
  </div>
</template>

<style scoped lang="less">
.chat_bg {
  height: 100vh;
  background: url('@/assets/chat/bg_bigmodel.png');
  background-size: 100% 100%;
  background-repeat: no-repeat;
  position: relative;
}
.btn {
  display: flex;
  padding: 2rem;
  margin-left: 15px;
  align-items: center;
}

.btn:hover,
.btn_actived {
  border-top-left-radius: 15px;
  border-bottom-left-radius: 15px;
  background: #f2f3f7;
}

:deep(.n-image img) {
  border-radius: 8px;
  margin-right: 5px;
}

.chat_box {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  // padding: 15px;
  width: 50%;
  .mainer {
    // background-color: rgb(242, 243, 247);
    // border-radius: 1rem;
    height: 100%;
  }
}
.sendBtn {
  position: absolute;
  // top: 25%;
	bottom: 10px;
  --n-text-color: #fff !important;
  --n-text-color-hover: #fff !important;
  --n-text-color-disabled: #fff !important;
  --n-text-color-pressed: #000 !important;
  --n-text-color-focus: #000 !important;
}
.h5SendBtn {
  right: 5%;
}
.webSendBtn {
  right: 25px;
}
.modal {
  background-color: rgba(255, 255, 255, 0);
  box-shadow: none;
  margin: 0;
  width: 100%;
  color: #fff;
}

:deep(.n-spin-description) {
  color: #fff;
}
.input_value {
  height: 180px;
	border-radius: 0;
}
.textarea_form {
	position: absolute;
	bottom: 0;
}
:deep(.n-input.n-input--textarea .n-input__textarea-el) {
	padding-top: 10px;
	padding-bottom: 10px;
}
:deep(.n-input.n-input--textarea .n-input__placeholder) {
	padding-top: 10px;
	padding-bottom: 10px;
}
.preview_box {
	display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 50%;
	height: 100vh;
	background-color: #fff;
	:deep(.n-tabs) {
		height: 100%;
	}
	:deep(.n-tabs .n-tab-pane) {
		height: 100%;
	}
}
:deep(.n-form-item .n-form-item-feedback-wrapper) {
	min-height: 0;
}
// :deep(.n-input) {
// 	height: 18px;
// }
</style>
