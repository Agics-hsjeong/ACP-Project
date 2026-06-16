import type { ChatMessage } from '$lib/data/mock';
import { getApiBase, getAuthToken } from './config';
import { apiFetch } from './client';

type ApiChatMessage = {
	id: number;
	role: ChatMessage['role'];
	content: string;
	timestamp?: string;
	emotion_delta?: string;
	interaction_type?: string;
};

function mapMessage(m: ApiChatMessage): ChatMessage {
	return {
		id: String(m.id),
		role: m.role,
		content: m.content,
		timestamp: m.timestamp,
		emotionDelta: m.emotion_delta,
		interactionType: m.interaction_type as ChatMessage['interactionType']
	};
}

export async function fetchChatMessages(characterId: string): Promise<ChatMessage[]> {
	const data = await apiFetch<ApiChatMessage[]>(`/chat/${characterId}/`);
	return data.map(mapMessage);
}

export async function sendChatMessageApi(
	characterId: string,
	content: string
): Promise<ChatMessage[]> {
	const data = await apiFetch<{ messages: ApiChatMessage[] }>(`/chat/${characterId}/`, {
		method: 'POST',
		json: { content }
	});
	return data.messages.map(mapMessage);
}

export async function streamChatMessageApi(
	characterId: string,
	content: string,
	onToken: (partial: string) => void
): Promise<ChatMessage> {
	const token = getAuthToken();
	const res = await fetch(`${getApiBase()}/chat/${characterId}/stream/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			...(token ? { Authorization: `Token ${token}` } : {})
		},
		body: JSON.stringify({ content })
	});

	if (!res.ok || !res.body) {
		throw new Error(`Stream failed: ${res.status}`);
	}

	const reader = res.body.getReader();
	const decoder = new TextDecoder();
	let buffer = '';
	let finalMessage: ChatMessage | null = null;

	while (true) {
		const { done, value } = await reader.read();
		if (done) break;
		buffer += decoder.decode(value, { stream: true });
		const lines = buffer.split('\n');
		buffer = lines.pop() ?? '';

		for (const line of lines) {
			if (!line.startsWith('data: ')) continue;
			const payload = JSON.parse(line.slice(6)) as {
				type: string;
				content?: string;
				partial?: string;
				message?: ApiChatMessage;
			};
			if (payload.type === 'token' && payload.partial) {
				onToken(payload.partial);
			}
			if (payload.type === 'done' && payload.message) {
				finalMessage = mapMessage(payload.message);
			}
		}
	}

	if (!finalMessage) throw new Error('No final message');
	return finalMessage;
}
