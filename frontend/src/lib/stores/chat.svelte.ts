import type { ChatMessage } from '$lib/data/mock';
import { fetchChatMessages, streamChatMessageApi } from '$lib/api/chat';
import { createMemory } from '$lib/api/resources';
import { apiHealth } from '$lib/api/client';
import { refreshChatSessions, refreshMemories } from '$lib/stores/catalog.svelte';
import { applyEmotionDelta } from '$lib/stores/emotion.svelte';
import { uuid } from '$lib/utils/uuid';

export type InteractionType = 'action' | 'expression' | 'gift' | 'record';

export const actionPresets = [
	'손을 잡는다',
	'어깨에 손을 얹는다',
	'고개를 끄덕인다',
	'창밖을 바라본다',
	'조용히 다가선다'
];

export const expressionPresets = [
	{ emoji: '😊', label: '미소', text: '(따뜻하게 미소 짓는다)' },
	{ emoji: '😳', label: '홍조', text: '(살짝 얼굴이 붉어진다)' },
	{ emoji: '😢', label: '눈물', text: '(눈시울이 붉어진다)' },
	{ emoji: '😠', label: '분노', text: '(눈썹을 찌푸린다)' },
	{ emoji: '🤔', label: '고민', text: '(잠시 생각에 잠긴다)' }
];

export const giftPresets = [
	{ id: 'rose', name: '장미 꽃다발', delta: { label: '애정', value: 5 } },
	{ id: 'letter', name: '손편지', delta: { label: '신뢰', value: 4 } },
	{ id: 'necklace', name: '달빛 목걸이', delta: { label: '애정', value: 8 } },
	{ id: 'book', name: '고서', delta: { label: '존경', value: 3 } }
];

let sessions = $state<Record<string, ChatMessage[]>>({});

const streamingTimers = new Map<string, ReturnType<typeof setInterval>>();

let isReplying = $state<Record<string, boolean>>({});
let apiEnabled = $state(false);
let apiReady = false;

export async function initChatApi(): Promise<boolean> {
	if (apiReady) return apiEnabled;
	apiReady = true;
	apiEnabled = await apiHealth();
	return apiEnabled;
}

export async function loadChatHistory(characterId: string): Promise<void> {
	await initChatApi();
	if (!apiEnabled) return;
	try {
		const msgs = await fetchChatMessages(characterId);
		if (msgs.length) patchSession(characterId, msgs);
	} catch {
		/* mock fallback */
	}
}

function setReplying(characterId: string, value: boolean) {
	isReplying = { ...isReplying, [characterId]: value };
}

function patchSession(characterId: string, messages: ChatMessage[]) {
	sessions = { ...sessions, [characterId]: messages };
}

function nowTime() {
	return new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' });
}

function ensureSession(characterId: string) {
	if (!sessions[characterId]) {
		patchSession(characterId, []);
	}
}

function appendMessages(characterId: string, messages: ChatMessage[]) {
	ensureSession(characterId);
	patchSession(characterId, [...(sessions[characterId] ?? []), ...messages]);
}

function updateMessage(characterId: string, messageId: string, patch: Partial<ChatMessage>) {
	ensureSession(characterId);
	patchSession(
		characterId,
		(sessions[characterId] ?? []).map((m) => (m.id === messageId ? { ...m, ...patch } : m))
	);
}

function parseUserInput(text: string): ChatMessage[] {
	const trimmed = text.trim();
	if (!trimmed) return [];

	if (/^\*.+\*$/.test(trimmed)) {
		return [
			{
				id: uuid(),
				role: 'narration',
				content: trimmed.slice(1, -1)
			}
		];
	}

	return [
		{
			id: uuid(),
			role: 'user',
			content: trimmed,
			timestamp: nowTime()
		}
	];
}

const replyTemplates = [
	'…그렇게 말해주니, 조금은 마음이 놓이네요.',
	'흥미로운 이야기예요. 더 들려주실 수 있나요?',
	'오늘 밤하늘처럼, 당신의 말도 참 고요하고 따뜻하네요.',
	'잠시 당신의 말을 곱씹는 듯 눈을 내리깔았다.',
	'그런 마음… 저도 이해할 수 있어요.'
];

function pickReply(characterName: string, interaction?: InteractionType): string {
	if (interaction === 'gift') {
		return '…정말요? 이런 선물을 받아도 될까요. 마음이 따뜻해지네요.';
	}
	if (interaction === 'expression') {
		return `${characterName}이(가) 당신의 표정에 시선을 맞추며 작게 미소 지었다.`;
	}
	if (interaction === 'action') {
		return `${characterName}이(가) 잠시 망설이다가, 조용히 고개를 끄덕였다.`;
	}
	return replyTemplates[Math.floor(Math.random() * replyTemplates.length)];
}

function streamCharacterReply(
	characterId: string,
	characterName: string,
	interaction?: InteractionType,
	emotionDelta?: string
) {
	const fullText = pickReply(characterName, interaction);
	const messageId = uuid();

	appendMessages(characterId, [
		{
			id: messageId,
			role: 'character',
			content: '',
			isStreaming: true,
			timestamp: nowTime(),
			emotionDelta
		}
	]);

	setReplying(characterId, true);
	let index = 0;

	const existing = streamingTimers.get(characterId);
	if (existing) clearInterval(existing);

	const timer = setInterval(() => {
		index += 1;
		const partial = fullText.slice(0, index);
		updateMessage(characterId, messageId, { content: partial, isStreaming: index < fullText.length });

		if (index >= fullText.length) {
			clearInterval(timer);
			streamingTimers.delete(characterId);
			updateMessage(characterId, messageId, { isStreaming: false });
			setReplying(characterId, false);

			if (emotionDelta) {
				const match = emotionDelta.match(/^(애정|신뢰|존경|분노|공포|질투)\s*([+-]?\d+)/);
				if (match) applyEmotionDelta(match[1], Number(match[2]));
			}
		}
	}, 28);

	streamingTimers.set(characterId, timer);
}

function triggerReply(
	characterId: string,
	characterName: string,
	interaction?: InteractionType,
	emotionDelta?: string
) {
	setTimeout(() => {
		streamCharacterReply(characterId, characterName, interaction, emotionDelta);
	}, 400);
}

export function getChatMessages(characterId: string): ChatMessage[] {
	return sessions[characterId] ?? [];
}

export function sendChatMessage(characterId: string, characterName: string, text: string) {
	const trimmed = text.trim();
	if (!trimmed) return;

	if (apiEnabled) {
		void sendChatMessageViaApi(characterId, trimmed);
		return;
	}

	const parsed = parseUserInput(text);
	if (!parsed.length) return;

	appendMessages(characterId, parsed);

	const last = parsed[parsed.length - 1];
	if (last.role === 'user' || last.role === 'narration') {
		triggerReply(characterId, characterName);
	}
}

async function sendChatMessageViaApi(characterId: string, text: string) {
	const parsed = parseUserInput(text);
	appendMessages(characterId, parsed);

	const streamId = uuid();
	appendMessages(characterId, [
		{
			id: streamId,
			role: 'character',
			content: '',
			isStreaming: true,
			timestamp: nowTime()
		}
	]);

	setReplying(characterId, true);
	try {
		const finalMsg = await streamChatMessageApi(characterId, text, (partial) => {
			updateMessage(characterId, streamId, { content: partial, isStreaming: true });
		});
		updateMessage(characterId, streamId, {
			...finalMsg,
			id: streamId,
			isStreaming: false
		});
		if (finalMsg.emotionDelta) {
			const match = finalMsg.emotionDelta.match(/^(애정|신뢰|존경|분노|공포|질투)\s*([+-]?\d+)/);
			if (match) applyEmotionDelta(match[1], Number(match[2]));
		}
	} catch {
		updateMessage(characterId, streamId, {
			role: 'character',
			content: '…잠시 연결에 문제가 있었어요.',
			isStreaming: false,
			timestamp: nowTime()
		});
	} finally {
		setReplying(characterId, false);
		void refreshChatSessions();
	}
}

export function sendInteraction(
	characterId: string,
	characterName: string,
	type: InteractionType,
	payload: string
) {
	let messages: ChatMessage[] = [];
	let emotionDelta: string | undefined;

	switch (type) {
		case 'action':
			messages = [
				{
					id: uuid(),
					role: 'narration',
					content: `*당신이 ${payload}*`,
					interactionType: 'action'
				}
			];
			emotionDelta = '신뢰 +2';
			break;
		case 'expression':
			messages = [
				{
					id: uuid(),
					role: 'user',
					content: payload,
					timestamp: nowTime(),
					interactionType: 'expression'
				}
			];
			emotionDelta = '애정 +2';
			break;
		case 'gift': {
			const gift = giftPresets.find((g) => g.id === payload);
			if (!gift) return;
			messages = [
				{
					id: uuid(),
					role: 'user',
					content: `🎁 ${gift.name}을(를) 선물했다`,
					timestamp: nowTime(),
					interactionType: 'gift'
				}
			];
			emotionDelta = `${gift.delta.label} +${gift.delta.value}`;
			break;
		}
		case 'record':
			messages = [
				{
					id: uuid(),
					role: 'system',
					content: `✦ 기억이 저장되었습니다 — [${payload}]`,
					interactionType: 'record'
				}
			];
			applyEmotionDelta('신뢰', 3);
			appendMessages(characterId, messages);
			if (apiEnabled) {
				void createMemory({
					characterId,
					title: payload,
					summary: payload,
					importance: 'high',
					tags: ['기록']
				})
					.then(() => refreshMemories(characterId))
					.catch(() => undefined);
			}
			return;
	}

	appendMessages(characterId, messages);
	triggerReply(characterId, characterName, type, emotionDelta);
}

export function isCharacterReplying(characterId: string): boolean {
	return !!isReplying[characterId];
}
