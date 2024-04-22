<script setup lang='ts'>
import type { Ref } from 'vue'
import { computed, defineExpose, onMounted, onUnmounted, ref, watch, provide } from 'vue'
import { NButton, NModal, NSpin, useDialog, useMessage, NInput, NAutoComplete, NTabs, NTabPane, NSelect, NForm, NFormItem, FormInst, SelectOption, NImage ,NAvatar, NSplit } from 'naive-ui'
import html2canvas from 'html2canvas'
import { Message } from './components'
import { useScroll } from './hooks/useScroll'
import { useChat } from './hooks/useChat'
import { useUsingContext } from './hooks/useUsingContext'
import HeaderComponent from './components/Header/index.vue'
import { SvgIcon } from '@/components/common'
import { useBasicLayout } from '@/hooks/useBasicLayout'
import { useAppStore, useChatStore } from '@/store'
import { t } from '@/locales'
import { debounce } from '@/utils/functions/debounce'
import spark from '@/assets/spark-icon.ico'
import qianwen from '@/assets/qwen.png'
import chatgpt from '@/assets/baichuan.png'
import chatglm from '@/assets/chatglm.png'
import dragIcon from '@/assets/drag-icon.png'
import Initial from '../chat/components/Preview/Initial.vue'
import File from '../chat/components/Preview/File.vue'
import axios from 'axios'
import Header from "@/views/chat/components/Header/Header.vue";
import { currentEnvironment } from "@/api/axios";
interface Props {
  chatId: number // 对话id
  chatIndex: number // 对话序号
  modelName: string // 模型名称
  inputValue: string // 对话框文本内容
  inputComplete: boolean // 是否完成文本输入
  modelModule: Chat.History // 循环的dataSourcesData的item
}
interface Emit {
  (ev: 'getInputValue'): void
}
const props = defineProps<Props>()
// 定义是否清空input
const emit = defineEmits<Emit>()

let controller = new AbortController()
const formRef = ref<FormInst | null>(null)
// const openLongReply = import.meta.env.VITE_GLOB_OPEN_LONG_REPLY === 'true'
const dialog = useDialog()
const ms = useMessage()
const chatStore = useChatStore()
const appStore = useAppStore()

const { isMobile } = useBasicLayout()
const { addChat, updateChat, updateChatSome, getChatByUuidAndIndex } = useChat()
const { scrollRef, scrollToBottom, scrollToBottomIfAtBottom } = useScroll()
const { usingContext, toggleUsingContext } = useUsingContext()

// const { uuid } = route.params as { uuid: string }
const uuid = ref(computed(() => props.chatId))
// const modelName = props.modelName
const dataSourcesData = computed(() => chatStore.history)
const modelItem = ref(computed(() => props.modelModule))
// const modelLogo = ref(computed(() => props.modelIcon))
const dataSources = ref(computed(() => chatStore.getChatByUuid(+uuid.value)))
const conversationList = computed(() => dataSources.value.filter(item => (!item.inversion && !!item.conversationOptions)))
const isIntranet = ref(computed(() => import.meta.env.VITE_NODE_ENV === 'intranet'))

// 页面加载spin
const show = ref(false)
const formShow = ref(false)  // 主题输入框blur时查询keyword和行业
const formItemShow = ref(false)
const processText = ref([])
const prompt = ref<string>(`请帮我生成一份研究报告：`)
const myModel = ref<string>('')
const currentIcon = ref<string>('')
const loading = ref<boolean>(false)
const inputRef = ref<Ref | null>(null)
const endData = ref({})
// 历史记录相关
const history: any = ref([])

const serverIp = ref('')
const nameRef = ref(0)
const templateUrl = ref()
const templateBtnShow = ref(false)
const panelsRef = ref([{
	title: '首页', // 默认
	url: '',
	status: 'initial',
	index: 1
},
// {
// 	title: '中国自行车发展的行业研究报告.docx', // 默认
// 	url: 'http://120.133.63.166:8012/onlinePreview?url=aHR0cDovLzEyMC4xMzMuNjMuMTY2OjUwMDEvYXR0YWNobWVudC9kb3dubG9hZC/kuK3lm73oh6rooYzovablj5HlsZXooYzkuJrnoJTnqbbmiqXlkYouZG9jeA%3D%3D&officePreviewType=pdf',
// 	status: 'preview',
// 	index: 2
// },
// {
// 	title: '任务执行日志 ', // 默认
// 	url: '',
// 	status: 'loading',
// 	index: 3
// }
])

const formValue = ref({
				subject: '',
				industryValue: '智能生成',
				wordsValue: 5000,
				keyword: '',
				year: '', // 年份
				life: '', // 年限
})
const formRules = {
				subject: {
					message: '请输入报告标题',
					trigger: 'blur'
				},
				keyword: {
					message: '请输入关键词',
					trigger: 'blur'
				},
}
const industryArr = ref([])
const years = [{
	label: '不限',
	value: '',
},{
	label: '2023',
	value: '2023',
}]

const lifes = [{
	label: '不限',
	value: '',
},{
	label: '近10年',
	value: '近10年',
}]
const words = [{
	label: '5000字以上',
	value: 5000,
	style: {
		fontSize: '12px'
	}
},{
	label: '10000字以上',
	value: 10000,
	style: {
		fontSize: '12px'
	}
},{
	label: '20000字以上',
	value: 20000,
	style: {
		fontSize: '12px'
	}
},{
	label: '30000字以上',
	value: 30000,
	style: {
		fontSize: '12px'
	}
}]

const chatUuid = ref(0)

const viewLogTracing = (thisChatUuid: any) => {
	console.log('日志追踪', chatUuid, typeof chatUuid)
	chatUuid.value = thisChatUuid
}
provide('viewLogTracing', viewLogTracing)

const sendGrandson = (file_name: any, view_url: any) => {
	// console.log('孙子传值给我', file_name, view_url)
	let inPanels = false
	const newIndex = panelsRef.value.length
	if (panelsRef.value.length > 1) {
		for (let i = 0; i < panelsRef.value.length; i++) {
			if (panelsRef.value[i].status === 'preview' &&
					panelsRef.value[i].url === view_url) {
					inPanels = true
					nameRef.value = i
				}
		}
	}
	if (!inPanels) {
		panelsRef.value.push({
			title: file_name, // 默认
			url: view_url,
			status: 'preview',
			index: newIndex,
		})
		nameRef.value = newIndex
	}
}
provide('sendGrandson', sendGrandson)
const handleClose = (name: number) => {
	const { value: panels } = panelsRef
	panels.splice(name, 1)
	if (panels.length > 1) {
		nameRef.value = panels.length - 1
	} else {
		nameRef.value = 0
	}
}

// watch(
//   () => props.inputValue,
//   (newVal: string) => {
//     // prompt.value = newVal
//     if (newVal.length > 0 && myModel.value) {
//       prompt.value = newVal
//       handleSubmit()
//     }
//   },
//   {
//     immediate: true,
//     deep: true,
//   },
// )
// 语言模型列表
// const loadModel = ref([])
const LlmData = ref([
  {
    label: 'chatglm3-6b',
    value: 'chatglm3-6b',
    icon: chatglm,
    status: false,
  },
  {
    label: '通义千问',
    value: 'qwen-api',
    icon: qianwen,
    status: false,
  },
  {
    label: '讯飞星火',
    value: 'xinghuo-api',
    icon: spark,
    status: false,
  },
  {
    label: '百川大模型',
    value: 'baichuan2-13b-chat',
    // value: 'baichuan2-7b',
    icon: chatgpt,
    status: false,
  },
])

const getModel = (val: string): any => {
  LlmData.value.forEach((item) => {
    if (item.label === val) {
      // console.log(item.value)
      myModel.value = item.value
      currentIcon.value = item.icon
    }
  })
}
watch(
  () => props.modelName,
  (newVal: string) => {
    getModel(newVal)
  },
  {
    immediate: true,
    deep: true,
  },
)
const getProcess = async (params: any) => {
	if(params.action === 'new' && params.index === 'normal_0') {
		processText.value.push(params)
	}
}
// 未知原因刷新页面，loading 状态不会重置，手动重置
dataSources.value.forEach((item, index) => {
  if (item.loading)
    updateChatSome(+uuid.value, index, { loading: false })
})
// 提交文本
function handleSubmit() {
	// getServerFree()

	// e.preventDefault()
	if (formValue.value.subject && (!formItemShow.value || formValue.value.keyword)) {
		getServerFree()
	} else {
		ms.error(`${formValue.value.subject ? '' : '主题' } ${formItemShow.value && !formValue.value.keyword ? '关键词' : ''} 不能为空！`)
	}
	// if (formItemShow || !formValue.value.subject) {
	// 	ms.error(`${formValue.value.subject ? '' : '主题' } ${formValue.value.keyword ? '关键词' : ''} 不能为空！`)
	// }
  // onConversation()
}
// 对话模型
async function onConversation() {
  // if (!myModel.value)
  //   return
  const message = prompt.value
  if (usingContext.value) {
    for (let i = 0; i < dataSources.value.length; i = i + 2) { // 获取历史记录
      if (i % 2 === 1) {
        history.value.push({
          role: 'assistant',
          content: dataSources.value[i].text,
        })
      }
      else {
        history.value.push({
          role: 'user',
          content: dataSources.value[i].text,
        })
      }
    }
    // history.value.push({ 'Human': dataSources.value[i].text, 'Assistant': dataSources.value[i + 1].text.split('\n\n数据来源：\n\n')[0] })
  }
  else { history.value.length = 0 }
  if (!message || message.trim() === '')
    return

  controller = new AbortController()

  addChat(
    +uuid.value,
    {
      dateTime: new Date().toLocaleString(),
      text: message,
      knowledge: false,
      inversion: true,
      error: false,
      conversationOptions: null,
      requestOptions: { prompt: message, options: null },
    },
  )
  scrollToBottom()

  loading.value = true
  prompt.value = '请帮我生成一份研究报告：'

  let options: Chat.ConversationRequest = {}
  const lastContext = conversationList.value[conversationList.value.length - 1]?.conversationOptions

  if (lastContext && usingContext.value)
    options = { ...lastContext }

  addChat(
    +uuid.value,
    {
      dateTime: new Date().toLocaleString(),
      text: '准备开始生成报告',
      loading: true,
      knowledge: false,
      inversion: false,
      error: false,
      conversationOptions: null,
      requestOptions: { prompt: message, options: { ...options } },
    },
  )
	chatUuid.value = dataSources.value.length - 1
  scrollToBottom()

  try {
    const lastText = ''
    // const apiData = {
    //   subject: "测试-中国自行车发展行业研究报告",
		// 	keyword: "电饭锅",
		// 	industry: "测试",
    // 	total_words: 1000
    // }
		const apiData = {
			subject: formValue.value.subject,
			keyword: formValue.value.keyword,
			industry: formValue.value.industryValue,
			total_words: formValue.value.wordsValue,
			ip: serverIp.value,
			version: isIntranet.value ? 'vnet' : '中咨'
		}
    const fetchChatAPIOnce = async () => {
      emit('getInputValue')
      const resData = {
        text: '',
      }
      const response = await fetch(`${currentEnvironment() === '/vnet' ? '/vnet/' : ''}api/chat-process`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(apiData),
      })
      if (!response.body)
        return
      const reader = response.body.pipeThrough(new TextDecoderStream()).getReader()
      const logTracing = []
			while (true) {
        const { value, done } = await reader.read()
        if (done)
          break
        const lastIndex = value.lastIndexOf('\n', value.length - 2)
				// console.log(lastIndex)
        let chunk = value
        if (lastIndex !== -1 && value.includes('data'))
          chunk = value.replace('data: ', '')
				// else {
				// 	endData.value = JSON.parse(chunk)
				// 	console.log(endData.value)
				// }
				// console.log('chunk ==>', chunk)
				if (lastIndex !== -1) {
					endData.value = JSON.parse(JSON.stringify(chunk))
					// console.log(endData.value)
				}
				// const data = JSON.parse(JSON.stringify(value))
				// resData.text += value
        try {
          const data = JSON.parse(chunk)
					console.log('success json parse chunk ==>', data)
					// processText.value.push(data)
					// getProcess(data)
          // resData.text += data?.text
					if (data?.index == "normal_0") {
						// resData.text = data?.title
						if (data?.action == "new") {
							resData.text = "正在生成报告中"
						} else {
							resData.text = "报告已生成"
						}
					}

					// 日志追踪数据处理
					if (data['index'] !== 'normal_0') {
						if (data['action'] === 'new') {
							logTracing.push(data)
						} else if (data['action'] === 'update') {
							for (let i = 0; i < logTracing.length; i++) {
								if (data['index'] === logTracing[i]['index']) {
									logTracing[i] = data
								}
							}
						} else if (data['action'] === 'end') {
							logTracing[logTracing.length - 1]['download_url'] = data['download_url']
							logTracing[logTracing.length - 1]['file_name'] = data['title']
							logTracing[logTracing.length - 1]['view_url'] = data['view_url']
						}
					}

          updateChat(
            +uuid.value,
            dataSources.value.length - 1,
            {
              dateTime: new Date().toLocaleString(),
              text: lastText + (resData.text ?? ''),
              knowledge: false,
              inversion: false,
              error: false,
              loading: true,
              conversationOptions: null,
              requestOptions: { prompt: message, options: { ...options } },
							logTracing: logTracing,
            },
          )

					formValue.value = {
						subject: '',
						industryValue: '智能生成',
						wordsValue: 5000,
						keyword: '',
						year: '', // 年份
						life: '', // 年限
					}
					formItemShow.value = false
					templateBtnShow.value = false

					if (data['action'] === 'end') {
						updateChatSome(+uuid.value, dataSources.value.length - 1, {
							actionEnd: true,
							fileName: data['title'],
							downloadUrl: data['download_url'],
							viewUrl: data['view_url'],
						})
					}
        }
        catch (error: any) {
					console.log('error json parse chunk ==>', chunk)
					console.log('error json parse error ==>', error)
				}
      }
      scrollToBottomIfAtBottom()
      loading.value = false
      updateChatSome(+uuid.value, dataSources.value.length - 1, { loading: false })
    }

    await fetchChatAPIOnce()
  }
  catch (error: any) {
    const errorMessage = error?.message ?? t('common.wrong')
		console.log('报告生成发生错误 ==>', errorMessage)
		releaseIp()

    if (error.message === 'canceled') {
      updateChatSome(
        +uuid.value,
        dataSources.value.length - 1,
        {
					text: '报告生成已取消',
					error: true,
          loading: false,
        },
      )
      scrollToBottomIfAtBottom()
      return
    }

    const currentChat = getChatByUuidAndIndex(+uuid.value, dataSources.value.length - 1)
    if (currentChat?.text && currentChat.text !== '') {
      updateChatSome(
        +uuid.value,
        dataSources.value.length - 1,
        {
          text: '报告生成已取消',
          error: true,
          loading: false,
        },
      )

			scrollToBottomIfAtBottom()
      return
    }
  }
  finally {
    loading.value = false
  }
}

async function handleRegenerate(index: number) {
  if (!myModel.value)
    return
  if (loading.value)
    return

  controller = new AbortController()

  const { requestOptions } = dataSources.value[index]

  const message = requestOptions?.prompt ?? ''

  let options: Chat.ConversationRequest = {}

  if (requestOptions.options)
    options = { ...requestOptions.options }

  loading.value = true

  updateChat(
    +uuid.value,
    index,
    {
      dateTime: new Date().toLocaleString(),
      text: '',
      inversion: false,
      knowledge: false,
      error: false,
      loading: true,
      conversationOptions: null,
      requestOptions: { prompt: message, options: { ...options } },
    },
  )

  try {
    const lastText = ''
    const apiData = {
			subject: formValue.value.subject,
			keyword: formValue.value.keyword,
			industry: formValue.value.industryValue,
			total_words: formValue.value.wordsValue,
}
    const fetchChatAPIOnce = async () => {
      const resData = {
        text: '',
      }
      const response = await fetch('api/chat-process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(apiData),
      })
      if (!response.body)
        return
      const reader = response.body.pipeThrough(new TextDecoderStream()).getReader()
      while (true) {
        const { value, done } = await reader.read()
        if (done)
          break
        const lastIndex = value.lastIndexOf('\n', value.length - 2)
        let chunk = value
        if (lastIndex !== -1)
          chunk = value.replace('data: ', '')
        try {
          const data = JSON.parse(chunk.replace(/\s+/g, ''))
          resData.text += data?.text
          updateChat(
            +uuid.value,
            index,
            {
              dateTime: new Date().toLocaleString(),
              text: lastText + (resData.text ?? ''),
              knowledge: false,
              inversion: false,
              error: false,
              loading: false,
              conversationOptions: null,
              requestOptions: { prompt: message, options: { ...options } },
            },
          )
        }
        catch (error: any) { }
      }
      scrollToBottomIfAtBottom()
      loading.value = false
      updateChatSome(+uuid.value, index, { loading: false })
    }

    await fetchChatAPIOnce()
  }
  catch (error: any) {
    if (error.message === 'canceled') {
      updateChatSome(
        +uuid.value,
        index,
        {
          loading: false,
        },
      )
      return
    }
    const errorMessage = error?.message ?? t('common.wrong')
    if (localStorage.getItem('chatMode') === 'knowledge') {
      updateChat(
        +uuid.value,
        index,
        {
          dateTime: new Date().toLocaleString(),
          text: errorMessage,
          inversion: false,
          knowledge: true,
          source: [],
          error: true,
          loading: false,
          conversationOptions: null,
          requestOptions: { prompt: message, options: { ...options } },
        },
      )
    }
    else {
      updateChat(
        +uuid.value,
        index,
        {
          dateTime: new Date().toLocaleString(),
          text: errorMessage,
          inversion: false,
          knowledge: false,
          error: true,
          loading: false,
          conversationOptions: null,
          requestOptions: { prompt: message, options: { ...options } },
        },
      )
    }
  }
  finally {
    loading.value = false
  }
}

function handleExport() {
  if (loading.value)
    return

  const d = dialog.warning({
    title: t('chat.exportImage'),
    content: t('chat.exportImageConfirm'),
    positiveText: t('common.yes'),
    negativeText: t('common.no'),
    onPositiveClick: async () => {
      try {
        d.loading = true
        const ele = document.getElementById('image-wrapper')
        const canvas = await html2canvas(ele as HTMLDivElement, {
          useCORS: true,
        })
        const imgUrl = canvas.toDataURL('image/png')
        const tempLink = document.createElement('a')
        tempLink.style.display = 'none'
        tempLink.href = imgUrl
        tempLink.setAttribute('download', 'chat-shot.png')
        if (typeof tempLink.download === 'undefined')
          tempLink.setAttribute('target', '_blank')

        document.body.appendChild(tempLink)
        tempLink.click()
        document.body.removeChild(tempLink)
        window.URL.revokeObjectURL(imgUrl)
        d.loading = false
        ms.success(t('chat.exportSuccess'))
        Promise.resolve()
      }
      catch (error: any) {
        ms.error(t('chat.exportFailed'))
      }
      finally {
        d.loading = false
      }
    },
  })
}

function handleDelete(index: number) {
  if (loading.value)
    return

  dialog.warning({
    title: t('chat.deleteMessage'),
    content: t('chat.deleteMessageConfirm'),
    positiveText: t('common.yes'),
    negativeText: t('common.no'),
    onPositiveClick: () => {
      chatStore.deleteChatByUuid(+uuid.value, index)
    },
  })
}

function modelAdd() {
  if (dataSourcesData.value.length >= 4) {
    ms.warning('最多选择4个模型进行对话')
  }
  else {
    chatStore.addHistory({ title: '请选择模型', uuid: Date.now(), isEdit: false })
    appStore.recordState()
    if (isMobile.value)
      appStore.setSiderCollapsed(true)
    // debounce(location.reload(), 500)
  }
}

function modelDelete(index: number, event?: MouseEvent | TouchEvent) {
  // console.log('删的除模型', index)
  if (dataSourcesData.value.length === 1) {
    ms.warning('最少需保留一个模型进行对话')
  }
  else {
    event?.stopPropagation()
    chatStore.deleteHistory(index)
    if (isMobile.value)
      appStore.setSiderCollapsed(true)
    // debounce(location.reload(), 500)
  }
}

const handleDeleteDebounce = debounce(modelDelete, 600)

// 回车输入文本对话
function handleEnter(event: KeyboardEvent) {
  if (!isMobile.value) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      handleSubmit()
    }
  }
  else {
    if (event.key === 'Enter' && event.ctrlKey) {
      event.preventDefault()
      handleSubmit()
    }
  }
}
// 停止返回对话
function handleStop() {
  if (loading.value) {
    controller.abort()
    loading.value = false
  }
}

// 可优化部分
// 搜索选项计算，这里使用value作为索引项，所以当出现重复value时渲染异常(多项同时出现选中效果)
// 理想状态下其实应该是key作为索引项,但官方的renderOption会出现问题，所以就需要value反renderLabel实现
// const searchOptions = computed(() => {
//   if (prompt.value.startsWith('/')) {
//     return promptTemplate.value.filter((item: { key: string }) => item.key.toLowerCase().includes(prompt.value.substring(1).toLowerCase())).map((obj: { value: any }) => {
//       return {
//         label: obj.value,
//         value: obj.value,
//       }
//     })
//   }
//   else {
//     return []
//   }
// })

// value反渲染key
// const renderOption = (option: { label: string }) => {
//   for (const i of promptTemplate.value) {
//     if (i.value === option.label)
//       return [i.key]
//   }
//   return []
// }

const placeholder = computed(() => {
  if (isMobile.value)
    return t('chat.placeholderMobile')
  return t('chat.placeholder')
})

const buttonDisabled = computed(() => {
  return loading.value || !prompt.value || prompt.value.trim() === ''
})

const footerClass = computed(() => {
  let classes = ['borderTop']
  if (isMobile.value)
    classes = ['sticky', 'left-0', 'bottom-0', 'right-0', 'p-2', 'pr-3', 'overflow-hidden']
  return classes
})
// 主题框blur
const setOptions = () => {
	if(formValue.value.subject) {
		getSubjectKeyword()
		// getSubjectIndustry()
	}
}
// 关键词框blur
// const setOptionKeyword = () => {
// 	if(formValue.value.keyword) {
// 		console.log('123')
// 		formItemShow.value = false
// 		// getSubjectIndustry()
// 	}
// }
// 主题框focus
const clearOptions = () => {
	if(!formValue.value.subject) {
		formShow.value = false
		formItemShow.value = false
	}
}
const getIndustryValue = (value: string, option: SelectOption) => {
	console.log(option?.temp_url)
	if (formValue.value.industryValue === '智能生成') {
		formItemShow.value = false
	} else {
		formItemShow.value = true
	}
	if (option?.temp_url) {
		templateBtnShow.value = true
		templateUrl.value = option?.temp_url
	} else {
		templateBtnShow.value = false
	}
}
// 获取行业类型
const getIndustryOption = async () => {
  const param = {}
	var config = {
		method: 'post',
		url: 'api/chat-industry-options',
		baseURL: currentEnvironment(),
		headers: {
			'Content-Type': 'application/json; charset=UTF-8',
		},
		data : param
	};

	axios(config)
	.then(function (res) {
		const { status, message, data } = res.data
		// console.log(JSON.stringify(res.data))
		if (status === "success") {
      console.log(data)
			let chunk = []
			const arr = data.new_industry_options
			arr.forEach(item => {
				formValue.value.industryValue = arr[0].option
				chunk.push({
					label: item.option,
					value: item.option,
					temp_url: item.view_url,
					style: {
						fontSize: '12px'
					}
				})
			})
			industryArr.value = chunk
    }
    else {
      ms.error(message)
    }
	})
	.catch(function (error) {
		console.log(error);
	});
}

// 获取主题中的关键词
const getSubjectKeyword = async () => {
	formShow.value = true
  const param = {
		subject: formValue.value.subject
	}
  var config = {
		method: 'post',
		url: 'api/chat-keyword',
		headers: {
			'Content-Type': 'application/json; charset=UTF-8',
		},
		data : param
	};

	axios(config)
	.then(function (res) {
		formShow.value = false
		const { status, message, data } = res.data
		if (status === "success") {
      console.log(data)
			if (data.keyword) {
				if(!data.keyword.isNeedKeyWord)
					formValue.value.keyword = data.keyword.keyword
				else
					formItemShow.value = true
			}
    }
    else {
      ms.error(message)
    }
	})
	.catch(function (error) {
		console.log(error);
	});
}

// 获取主题中的行业类型
const getSubjectIndustry = async () => {
	formShow.value = true
  const param = {
		subject: formValue.value.subject
	}
  var config = {
		method: 'post',
		url: 'api/chat-industry',
		headers: {
			'Content-Type': 'application/json; charset=UTF-8',
		},
		data : param
	};

	axios(config)
	.then(function (res) {
		formShow.value = false
		const { status, message, data } = res.data
		if (status === "success") {
      console.log(data)
			formValue.value.industryValue = data.industry
			// formItemShow.value = true
    }
    else {
      ms.error(message)
    }
	})
	.catch(function (error) {
		console.log(error);
	});
}
const getServerFree = async () =>{
	var data = {}

	var config = {
		method: 'post',
		url: 'api/chat-free',
		baseURL: currentEnvironment(),
		headers: {
			'Content-Type': 'application/json; charset=UTF-8',
		},
		data : data
	};

	axios(config)
	.then(function (res) {
		const { status, message, data } = res.data
		if (status === "success") {
			if (!!data.free) {
				serverIp.value = data.ip
				const temp: string = `请帮我生成一份研究报告：
主题：${formValue.value.subject}
行业：${formValue.value.industryValue}
字数：${formValue.value.wordsValue}字以上`
				prompt.value = temp
				onConversation()
			}
			else
				ms.error('队列已满，请稍后重试')
    }
	})
	.catch(function (error) {
		console.log(error);
	});
}

const releaseIp = async () => {
	var data = {
		'ip': serverIp.value
	}

	var config = {
		method: 'post',
		url: 'api/chat-release',
		baseURL: currentEnvironment(),
		headers: {
			'Content-Type': 'application/json; charset=UTF-8',
		},
		data : data
	};

	axios(config)
	.then(function (res) {
		console.log('释放 ip 成功 ==>', res)
	})
	.catch(function (error) {
		console.log('释放 ip 失败 ==>', error);
	});
}
// 预览模板
const handlePreviewTemp = () => {
	const newIndex = panelsRef.value.length
	panelsRef.value.push({
			title: `${formValue.value.industryValue}模板`, // 默认
			url: templateUrl.value,
			status: 'preview',
			index: newIndex,
		})
	nameRef.value = newIndex
	console.log('123')
}
onMounted(() => {
  scrollToBottom()
	getIndustryOption()
	// getIndustryValue()
  // getLoadModel()
  // if (inputRef.value && !isMobile.value)
  //   inputRef.value?.focus()

	// 判断dataSources是否有数据，没有则添加一条
	console.log("dataSources ==>", dataSources.value)
	if (!dataSources.value.length) {
		addChat(+uuid.value, {
			dateTime: new Date().toLocaleString(),
			// text: '我是中咨报告助手，可以帮您生成专业的研究报告，您可以输入报告的主题和行业，可快速生成报告，仅供参考。',
			text: `我是${isIntranet.value ? '世纪互联' : '中咨研究'}报告助手，可以帮您生成专业的研究报告，您可以输入报告的主题和行业，可快速生成报告，仅供参考。`,
			knowledge: false,
			inversion: false,
			error: false,
			loading: false,
			conversationOptions: null,
			requestOptions: { prompt: '', options: null },
			system: true,
		})
	}
})

onUnmounted(() => {
  if (loading.value)
    controller.abort()
})

defineExpose({
  handleSubmit,
})

const W = computed(() => {
  return `${100 / dataSourcesData.value.length}%`
})
</script>

<template>
	<div>
		<Header></Header>
		<div class="flex flex-row w-full chat_main" :style="{ width: W }">
			<!-- <NSplit
				direction="horizontal"
				style="height: 100%"
				:default-size="0.5"
				:min="0.3"
				:max="0.7"
				:resize-trigger-size="1">
				<template #1> -->
			<div class="chat_box">
				<HeaderComponent
					:model-item="modelItem"
					:model-icon="currentIcon"
					:model-index="chatIndex"
					:using-context="usingContext" @export="handleExport"
					@toggle-using-context="toggleUsingContext" @model-delete="handleDeleteDebounce(chatIndex, $event)"
					@model-add="modelAdd"
				/>
				<main class="flex flex-col overflow-hidden mainer">
					<div id="scrollRef" ref="scrollRef" class="flex overflow-hidden overflow-y-auto">
						<!-- <div
							v-for="(item, index) of dataSourcesData" id="image-wrapper" :key="index"
							class="w-full max-w-screen-xl m-auto dark:bg-[#101014]"
							:class="[isMobile ? 'p-2' : 'p-4']"
						> -->
						<div
							id="image-wrapper" class="w-full m-auto dark:bg-[#101014]"
							:class="[isMobile ? 'p-2' : 'p-4']"
						>
							<!-- <div>
								<NImage
									v-show="item.icon" width="30" :src="item.icon"
									:previewed-img-props="{ style: { marginRight: '13px' } }"
								/>
								<NButton text style="font-size: 15px;font-weight: 400;">
									{{ item.title }}
								</NButton>
							</div> -->
							<template v-if="!dataSources.length">
								<div class="flex items-center justify-center mt-4 text-center text-neutral-300">
									<SvgIcon icon="ri:bubble-chart-fill" class="mr-2 text-3xl" />
									<span>Say something~</span>
								</div>
							</template>
							<template v-else>
								<div>
									<Message
										v-for="(item, index) of dataSources" :key="index" :date-time="item.dateTime" :text="item.text"
										:knowledge="item.knowledge" :inversion="item.inversion" :image="currentIcon" :source="item.source" :error="item.error"
										:loading="item.loading" :action-end="item.actionEnd" :file-name="item.fileName" :download-url="item.downloadUrl" :view-url="item.viewUrl" :chatUuid="index" :system="item.system" @delete="handleDelete(index)" @regenerate="handleRegenerate(index)"
									/>
									<!-- <div class="sticky bottom-0 left-0 flex justify-center">
										<NButton v-if="loading" type="warning" @click="handleStop">
											<template #icon>
												<SvgIcon icon="ri:stop-circle-line" />
											</template>
											Stop Responding
										</NButton>
									</div> -->
								</div>
							</template>
						</div>
					</div>
				</main>
				<footer :class="footerClass">
					<div class="w-full m-auto">
						<NSpin size="medium" :stroke="'#2853E0'" :show="formShow">
							<div class="flex items-center justify-between space-x-2" style="position: relative;">
								<NInput
									ref="inputRef" v-model:value="prompt" class="input_value" type="textarea" placeholder="请帮我生成一份研究报告：" size="large"
									:autosize="{ minRows: 2, maxRows: isMobile ? 4 : 8 }" @keypress="handleEnter" disabled
								/>
								<div class="textarea_form">
									<NForm ref="formRef" :model="formValue" label-placement="left" label-width="55px" :rules="formRules" :size="small">
										<NFormItem label="主&nbsp;&nbsp;&nbsp;题：" path="subject"
										>
											<n-input v-model:value="formValue.subject" placeholder="请输入报告标题，如：企业数字化转型技术发展趋势研究报告" />
											<!-- <n-input v-model:value="formValue.subject" placeholder="请输入报告标题，如：企业数字化转型技术发展趋势研究报告" @blur="setOptions" @focus="clearOptions" /> -->
										</NFormItem>
										<!-- <NFormItem label="要求" path="user.age">
											<n-input v-model:value="formValue.user.age" placeholder="请输入报告要求，如：包含，概述、可行性分析、竞品分析、行业调研等；" />
										</NFormItem> -->
										<!-- <NFormItem label="年份：" path="year" class="flex flex-row">
											<NSelect v-model:value="formValue.year" size="large" :options="years" style="margin-right: 8px;" />
											<NSelect v-model:value="formValue.life" size="large" :options="lifes" />
										</NFormItem> -->
										<NFormItem label="行&nbsp;&nbsp;&nbsp;业：" path="industryValue">
											<NSelect v-model:value="formValue.industryValue" style="width: 172px; font-size: 12px;" size="large" @update:value="getIndustryValue" :options="industryArr" />
											<NButton v-if="templateBtnShow" class="previewTemp" type="primary" size="medium" text color="#2853E0" style="font-size: 12px; margin-top: 5px; margin-left: 10px;" @click="handlePreviewTemp">
												预览模板
											</NButton>
										</NFormItem>
										<NFormItem label="关键词：" v-if="formItemShow" path="keyword">
											<n-input v-model:value="formValue.keyword" style="width: 172px;" placeholder="请输入报告的关键词" />
										</NFormItem>
										<NFormItem label="字&nbsp;&nbsp;&nbsp;数：" path="wordsValue">
											<NSelect v-model:value="formValue.wordsValue" style="width: 172px;" size="large" :options="words" />
										</NFormItem>
									</NForm>
									</div>
								<NButton class="sendBtn" type="primary" size="medium" color="#2853E0" :disabled="buttonDisabled" @click="handleSubmit">
									生成报告
								</NButton>
							</div>
						</NSpin>
					</div>
				</footer>
			</div>
				<!-- </template>
				<template #2> -->
			<div class="preview_box">
				<NTabs
					v-model:value="nameRef"
					type="card"
					closable
					tab-style="justify-content: center; align-items: center; color: #0C296E; font-size: 12px; padding: 0 14px;border-radius: 6px 6px 0px 0px; height:38px;"
					@close="handleClose"
				>
					<NTabPane
						v-for="(panel, index) in panelsRef"
						:key="index"
						:tab="panel.title.toString()"
						:name="index"
						:closable="index !== 0"
					>

						<Initial v-if="!panel.url" :process-status="panel.status" :process-arr="processText" :chat-uuid="chatUuid" />
						<File v-else :file-url="panel.url" />
					</NTabPane>
				</NTabs>
			</div>
				<!-- </template> -->
				<!-- <template #resize-trigger>
					<div :style="{
						position: 'relative',
						height: '100%',
						backgroundColor: 'rgba(128, 146, 169, 0.6)',
						display: 'flex',
						justifyContent: 'center',
						alignItems: 'center',
						borderRadius: '8px'
					}">
						<NAvatar :src="dragIcon" style="position: absolute; background-color: rgba(0, 0, 0, 0);"></NAvatar>
					</div>
				</template> -->
			<!-- </NSplit> -->
			<NModal v-model:show="show" :mask-closable="false" class="modal">
				<NSpin size="large">
					<template #description>
						正在切换模型，请稍后...
					</template>
				</NSpin>
			</NModal>
		</div>
	</div>
</template>

<style scoped lang="less">
.chat_main {
  // padding: 20px;
  width: 25%;
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
  // justify-content: space-between;
  // padding: 15px;
  width: 50%;
	height: calc(100vh);

  .mainer {
    background-color: #F1F2F3;
    height: calc(100% - 230px);
  }
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
:deep(.n-auto-complete) {
  display: none;
}
.borderTop {
	border-top: 1px solid #D3DEFF;
}
.sendBtn {
  position: absolute;
  // top: 25%;
	bottom: 10px;
	right: 14px;
	--n-font-size: 12px !important;
	--n-color-hover: rgba(40, 83, 224, 0.8) !important;
  --n-text-color: #fff !important;
  --n-text-color-hover: #fff !important;
  --n-text-color-disabled: #fff !important;
  --n-text-color-pressed: #fff !important;
  --n-text-color-focus: #fff !important;
	--n-color-focus: linear-gradient(0deg, #1F48D1, #1F48D1), #2853E0;
}
.input_value {
  height: 180px;
	border-radius: 0;
}

:deep(.input_value .n-input-wrapper) {
		padding-left: 14px !important;
		padding-right: 14px;
	}

.preview_box {
	display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 50%;
	height: 100vh;
	background-color: #fff;
	border-left: 1px solid rgba(128, 146, 169, 0.6);
	:deep(.n-tabs) {
		height: 100%;
	}
	:deep(.n-tabs .n-tab-pane) {
		height: 100%;
	}
}
:deep(.n-split .n-split__resize-trigger) {
	background-color: rgba(128, 146, 169, 0.6) !important;
}
:deep(.n-tabs .n-tabs-nav.n-tabs-nav--card-type .n-tabs-tab.n-tabs-tab--active) {
	background-color: #fff;
	opacity: 1;
	border-bottom: none !important;
	color: #2853E0 !important;
}
.textarea_form {
	position: absolute;
	left: 14px;
	top: 30px;
	width: 40%;
	min-width: 390px;
	margin-left: 0 !important;
}
:deep(.n-form-item .n-form-item-label) {
	padding-right: 0;
}
:deep(.n-input) {
	--n-border: none !important;
	border-bottom: 1px solid #D3DEFF !important;
	--n-font-size: 12px !important;
	border-top: none !important;
	--n-box-shadow-focus: 0 1px 0 0 #2853E0 !important;
	--n-border-radius: 0 !important;
	--n-border-hover: none !important;
	--n-border-focus: none !important;
	--n-border-error: none !important;
	--n-border-disabled: none !important;
	--n-border-focus-error: none !important;
	--n-border-hover-error: none !important;
	--n-color: rgba(255, 255, 255, 0) !important;
	--n-color-disabled: rgba(255, 255, 255, 1) !important;
	--n-caret-color: #2853E0 !important;
}
:deep(.n-input:focus) {
	border-bottom: 1px solid #007bff !important; /* 这里设置你想要的颜色 */
}
:deep(.n-input .n-input-wrapper) {
	padding-left: 6px;
	padding-right: 6px;
}
:deep(.n-base-selection .n-base-selection-label .n-base-selection-input) {
	// padding-left: 6px;
	// padding-right: 6px;
}
:deep(.n-input .n-input__input-el) {
	color: #0C296E;
}
:deep(.n-form-item .n-form-item-label .n-form-item-label__asterisk){
	display: none;
}
// :deep(.n-input .n-input__input-el) {
// 	height: 25px;
// 	line-height: 25px;
// }
:deep(.n-base-selection .n-base-selection-label) {
	background-color: rgba(255, 255, 255, 0);
	height: 32px;
}
:deep(.n-base-selection) {
	--n-color: rgba(255, 255, 255, 0);
	--n-border: none !important;
	--n-border-active: none !important;
	--n-border-hover: none !important;
	--n-border-focus: none !important;
	border-bottom: 1px solid #D3DEFF !important;
	border-top: none !important;
	--n-box-shadow-focus: 0 1px 0 0 #2853E0 !important;
	--n-box-shadow-active: 0 1px 0 0 #2853E0 !important;
	--n-border-radius: 0 !important;
	--n-height: 32px !important;
}
:deep(.n-form-item .n-form-item-feedback-wrapper) {
	display: none;
}
:deep(.n-form-item.n-form-item--left-labelled .n-form-item-label .n-form-item-label__text) {
	font-weight: normal;
	color: #0C296E;
	font-size: 12px;
	text-align: left;
}
:deep(.n-base-selection .n-base-selection-label .n-base-selection-input .n-base-selection-input__content) {
	font-weight: normal;
	color: #0C296E;
	font-size: 12px;
}
:deep(.n-base-select-menu) {
	--n-option-font-size: 12px !important;
}
:deep(.n-select-menu) {
	--n-option-font-size: 12px !important;
}
:deep(.n-tabs .n-tabs-nav) {
	padding-top: 12px;
	background: #EFF2F7;
}
:deep(.n-tabs .n-tabs-nav.n-tabs-nav--card-type .n-tabs-tab) {
	border: 1px solid #D3DDF9;
	background: #EFF2F7;
}
:deep(.n-tabs .n-tabs-tab-pad) {
	display: none;
}
:deep(.n-tabs .n-tabs-nav.n-tabs-nav--card-type .n-tabs-tab.n-tabs-tab--closable) {
	border-bottom: none;
}

:deep(.n-base-selection .n-base-selection-label .n-base-selection-input) {
	padding: 0 6px;
}

:deep(.n-form-item .n-form-item-blank) {
	margin-left: -8px;
}
.previewTemp:hover {
	border-bottom: 1px solid #2853E0;
}
</style>
