declare namespace Chat {
	interface Chat {
file_name: any
download_url: any
view_url: any
file_name: any
[x: string]: any
[x: string]: any
		dateTime: string
		text: string
		source?: string[]
		knowledge: boolean
		inversion?: boolean
		error?: boolean
		loading?: boolean
		conversationOptions?: ConversationRequest | null
		requestOptions: { prompt: string; options?: ConversationRequest | null }
		logTracing: any[]
		actionEnd?: boolean
		fileName?: string
		downloadUrl?: string
		viewUrl?: string
		system?: boolean
	}

	interface ChatParams {
		chatMode: string
		temperature: number
		chatRound: number
	}

	interface KnowledgeParams {
		knowledgeBase: string
		threshold: number
		matchItems: number
	}

	interface History {
		title: string
		isEdit: boolean
		uuid: number
	}

	interface ChatState {
		active: number | null
		usingContext: boolean;
		history: History[]
		chat: { uuid: number; data: Chat[] }[]
	}

	interface ConversationRequest {
		conversationId?: string
		parentMessageId?: string
	}

	interface ConversationResponse {
		conversationId: string
		detail: {
			choices: { finish_reason: string; index: number; logprobs: any; text: string }[]
			created: number
			id: string
			model: string
			object: string
			usage: { completion_tokens: number; prompt_tokens: number; total_tokens: number }
		}
		id: string
		parentMessageId: string
		role: string
		text: string
	}

	interface GenerateActionProcess {
		action: string
		index: string
		time: string
		status: string
		title?: string
		content?: string
		sub_content?: string
	}

	interface TabsListItem {
		title: string
		url?: string
		status: string
		index: number
	}
}
