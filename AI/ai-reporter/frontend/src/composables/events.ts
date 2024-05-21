import { useEventListener } from '@vueuse/core';
import { useChatStore } from '@/store';

/** 全局事件 */
export function useGlobalEvents() {
	const chat = useChatStore();

  // /** 页面离开时缓存多页签数据 */
	useEventListener(window, 'beforeunload', function (e) {
		let loading = false

		if (chat.$state.chat) {
      chat.$state.chat.forEach((item: any) => {
        const data = item.data;
        if (data && data.length > 0) {
          const last = data[data.length - 1];
					if (last.loading === true) {
						loading = true;
					}
          // if (last.actionEnd !== true) {
          //   last.text = '报告生成失败，请重试';
          // }
        }
      });
    }
    // chat.recordState();

		if (loading) {
			// Cancel the event
			e.preventDefault();
			// Chrome requires returnValue to be set
			e.returnValue = '自定义文本';
		}
	});
}
