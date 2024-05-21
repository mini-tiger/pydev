<script setup lang="ts">
</script>
<template>
	<div class="loading">
		<div class="dot"></div>
		<div class="dot"></div>
		<div class="dot"></div>
		<div class="dot"></div>
		<div class="dot"></div>
		<div class="dot"></div>
	</div>
</template>
<style scoped>
.loading {
	display: flex;
	/* justify-content: center;
	align-items: center;
	height: 100px; */
}

.dot {
	width: 2px;
	height: 2px;
	background-color: #0C296E;
	border-radius: 50%;
	margin: 0 2px;
	animation: pulse 0.5s infinite alternate;
}

@keyframes pulse {
	0% {
		transform: scale(1);
		opacity: 0.5;
	}

	100% {
		transform: scale(1.5);
		opacity: 1;
	}
}

.dot:nth-child(2) {
	animation-delay: 0.1s;
}

.dot:nth-child(3) {
	animation-delay: 0.2s;
}

.dot:nth-child(4) {
	animation-delay: 0.3s;
}

.dot:nth-child(5) {
	animation-delay: 0.4s;
}

.dot:nth-child(6) {
	animation-delay: 0.5s;
}
</style>
