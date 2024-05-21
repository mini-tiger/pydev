<script setup lang='ts'>
import { computed, ref } from 'vue'

interface Props {
  fileUrl: string
}

defineProps<Props>()

</script>
<template>
	<div class="flex w-full h-full overflow-hidden">
		<iframe :src="fileUrl" frameborder="0" width="100%" hight="100%"></iframe>
	</div>
</template>

<style>

</style>
