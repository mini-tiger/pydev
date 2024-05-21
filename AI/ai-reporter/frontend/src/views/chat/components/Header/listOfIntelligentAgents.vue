<template>
	<div class="main flex justify-start align-center" @click="jumpAddress">
		<div class="left">
			<img :src="logo" alt="" class="avatar">
		</div>
		<div class="right">
			<div class="title">{{ title }}</div>
			<div class="description">{{ description }}</div>
		</div>
	</div>
</template>

<script setup lang="ts">
// 获取父组件传递的参数
import { useMessage } from "naive-ui";

const message = useMessage()
const props = defineProps<{
	title?: string;
	description?: string;
	logo?: string;
	url?: string;
}>();

const jumpAddress = () => {
	if (!props.url) {
		message.warning('没有找到跳转地址');
	}

	if (props.url) {
		window.open(props.url);
	}
};
</script>


<style scoped lang="less">
.avatar {
	width: 32px;
	height: 32px;
}

.main {
	cursor: pointer;
	width: 200px;
	height: 64px;
	border-radius: 8px;
	border: 1px solid #DCE5FF;
	background: #FFFFFF;
	padding: 9px 10px;
}

.right {
	margin-left: 8px;

	.title {
		font-size: 12px;
		font-weight: normal;
		line-height: 18px;
		letter-spacing: 0px;
		color: #3D3D3D;
	}

	.description {
		width: 132px;
		font-size: 12px;
		font-weight: normal;
		line-height: 16px;
		letter-spacing: 0px;
		color: #999999;
	}
}
</style>
