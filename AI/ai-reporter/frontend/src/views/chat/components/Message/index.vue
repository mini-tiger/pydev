<script setup lang='ts'>
import { computed, ref, getCurrentInstance } from 'vue'
import { useMessage } from 'naive-ui'
import AvatarComponent from './Avatar.vue'
import TextComponent from './Text.vue'
import AttachmentComponent from './Attachment.vue'
import { SvgIcon } from '@/components/common'
import { useIconRender } from '@/hooks/useIconRender'
import { t } from '@/locales'
import { useBasicLayout } from '@/hooks/useBasicLayout'
import { copyToClip } from '@/utils/copy'

interface Props {
  dateTime?: string
  text?: string
  inversion?: boolean
  error?: boolean
  loading?: boolean
  knowledge?: boolean
  source?: string[]
  image?: string
	actionEnd?: boolean
	fileName?: string
	downloadUrl?: string
	viewUrl?: string
	chatUuid?: number
	system?: boolean
}

interface Emit {
  (ev: 'regenerate'): void
  (ev: 'delete'): void
}

const props = defineProps<Props>()

const emit = defineEmits<Emit>()

const { isMobile } = useBasicLayout()

const { iconRender } = useIconRender()

const message = useMessage()

const textRef = ref<HTMLElement>()

const asRawText = ref(props.inversion)

const messageRef = ref<HTMLElement>()

const options = computed(() => {
  const common = [
    {
      label: t('chat.copy'),
      key: 'copyText',
      icon: iconRender({ icon: 'ri:file-copy-2-line' }),
    },
    {
      label: t('common.delete'),
      key: 'delete',
      icon: iconRender({ icon: 'ri:delete-bin-line' }),
    },
  ]

  if (!props.inversion) {
    common.unshift({
      label: asRawText.value ? t('chat.preview') : t('chat.showRawText'),
      key: 'toggleRenderType',
      icon: iconRender({ icon: asRawText.value ? 'ic:outline-code-off' : 'ic:outline-code' }),
    })
  }

  return common
})
// 对话下more更多功能
function handleSelect(key: 'copyText' | 'delete' | 'toggleRenderType') {
  switch (key) {
    case 'copyText':
      handleCopy()
      return
    case 'toggleRenderType':
      asRawText.value = !asRawText.value
      return
    case 'delete':
      emit('delete')
  }
}
// 重新生成
function handleRegenerate() {
  messageRef.value?.scrollIntoView()
  emit('regenerate')
}

async function handleCopy() {
  try {
    await copyToClip(props.text || '')
    message.success('复制成功')
  }
  catch {
    message.error('复制失败')
  }
}

// 获取组件 key
const messageKey = getCurrentInstance()?.vnode.key;
</script>

<template>
  <div
    ref="messageRef"
    class="flex w-full mb-4 overflow-hidden"
		:class="[inversion ? 'flex-row-reverse' : 'flex-row', inversion ? 'request-text' : 'reply-text']"
  >
		<span class="triangle"></span>
    <!-- flex-row-reverse -->
    <div
      class="flex items-center justify-center flex-shrink-0 h-8 overflow-hidden rounded-full basis-8"
      :class="[inversion ? 'ml-3' : 'mr-3']"
    >
      <!-- 头像模块 -->
      <AvatarComponent :image="inversion" :customed="image" />
    </div>
    <div class="items-start w-full overflow-hidden text-sm">
      <!-- <p class="text-xs text-[#b4bbc4]" :class="[inversion ? 'text-right' : 'text-left']">
        {{ dateTime }}
      </p> -->
      <div
        class="flex items-end gap-1"
				:class="[inversion ? 'flex-row-reverse' : 'flex-row']"
      >
        <!-- 对话内容 -->
        <TextComponent
          ref="textRef"
          :inversion="inversion"
          :error="error"
          :text="text"
          :loading="loading"
          :as-raw-text="asRawText"
          :is-know-ledge="knowledge"
          :source="source"
					:chatUuid="chatUuid"
					:system="system"
        />
        <div class="flex flex-col">
          <button
            v-if="!inversion"
            class="mb-2 transition text-neutral-300 hover:text-neutral-800 dark:hover:text-neutral-300"
            @click="handleRegenerate"
          >
            <SvgIcon icon="3-dots-scale" />
          </button>
          <!-- <NDropdown
            :trigger="isMobile ? 'click' : 'hover'"
            :placement="!inversion ? 'right' : 'left'"
            :options="options"
            @select="handleSelect"
          >
            <button class="transition text-neutral-300 hover:text-neutral-800 dark:hover:text-neutral-200">
              <SvgIcon icon="ri:more-2-fill" />
            </button>
          </NDropdown> -->
        </div>
      </div>
      <!-- <div v-if="!inversion " class="flex items-center mt-1 ml-3 cursor-pointer justify-left" @click="handleRegenerate">
        <SvgIcon icon="lucide:rotate-ccw" class="text-[#2853E0] font-bold" />
        <button class="text-xs text-[#2853E0] font-sans font-bold">
          重新生成
        </button>
      </div> -->
    </div>
  </div>
	<div
		v-if="!inversion"
    ref="messageRef"
    class="flex w-full mb-4 overflow-hidden mt-[-20px]"
		:class="[{ 'flex-row-reverse': inversion }]"
  >
    <div class="items-start w-full overflow-hidden text-sm">
      <div
        class="flex items-end gap-1"
				:class="[inversion ? 'flex-row-reverse' : 'flex-row']"
				style="display: inline-block;"
      >
        <!-- 对话内容 -->
        <AttachmentComponent
          ref="textRef"
          :inversion="inversion"
          :error="error"
          :text="text"
          :loading="loading"
          :as-raw-text="asRawText"
          :is-know-ledge="knowledge"
          :source="source"
					:file-name="fileName"
					:download-url="downloadUrl"
					:view-url="viewUrl"
					:action-end="actionEnd"
					:message-key="messageKey"
        />
      </div>
    </div>
  </div>
</template>
<style scoped lang="less">
.request-text {
	position: relative;
	.triangle{
		display: inline-block;
		position: absolute;
		right: 42px;
		top: 10px;
		width: 12px;
		height: 12px;
		transform: rotate(45deg);
		border-radius: 1px;
		opacity: 1;
		background: #2853E0;
	}
}
.reply-text {
	position: relative;
	.triangle{
		display: inline-block;
		position: absolute;
		left: 40px;
		top: 10px;
		width: 12px;
		height: 12px;
		transform: rotate(45deg);
		border-radius: 1px;
		opacity: 1;
		background: #fff;
	}
}
</style>
