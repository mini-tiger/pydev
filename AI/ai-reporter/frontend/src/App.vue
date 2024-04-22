<script setup lang="ts">
import { NConfigProvider } from 'naive-ui'
import { NaiveProvider } from '@/components/common'
import { useTheme } from '@/hooks/useTheme'
import { useLanguage } from '@/hooks/useLanguage'
import { useGlobalEvents } from '@/composables/events';

const { theme, themeOverrides } = useTheme()
const { language } = useLanguage()

useGlobalEvents();
</script>

<template>
  <NConfigProvider
    class="h-full"
    :theme="theme"
    :theme-overrides="themeOverrides"
    :locale="language"
  >
    <NaiveProvider>
      <RouterView />
    </NaiveProvider>
  </NConfigProvider>
</template>

<style>
.n-base-select-menu .n-base-select-option.n-base-select-option--selected {
	color: #2853E0 !important;
}
.n-base-select-menu .n-base-select-option .n-base-select-option__check {
	color: #2853E0 !important;
}
/* .n-select-menu {
  background-color: rgba(43,32,26,1) !important;
}
.n-base-select-menu .n-base-select-option.n-base-select-option--pending::before {
  background-color: rgba(10, 4, 1, 0.7) !important;
} */
</style>
