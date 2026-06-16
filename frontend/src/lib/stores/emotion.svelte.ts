import type { EmotionAxis } from '$lib/data/mock';
import { fetchEmotion } from '$lib/api/resources';
import { apiHealth } from '$lib/api/client';

let emotionState = $state<EmotionAxis[]>([]);
let intimacy = $state(0);
let loaded = $state(false);
let activeCharacterId = $state('elia');

export function getEmotions(): EmotionAxis[] {
	return emotionState;
}

export function getIntimacy(): number {
	return intimacy;
}

export async function initEmotionApi(characterId = 'elia'): Promise<void> {
	activeCharacterId = characterId;
	if (!(await apiHealth())) return;

	try {
		const data = await fetchEmotion(characterId);
		emotionState = data.axes.map((a) => ({ ...a }));
		intimacy = data.intimacy;
		loaded = true;
	} catch (err) {
		console.error('Emotion API load failed:', err);
	}
}

export function applyEmotionDelta(label: string, delta: number) {
	const keyMap: Record<string, string> = {
		애정: 'affection',
		신뢰: 'trust',
		존경: 'respect',
		분노: 'anger',
		공포: 'fear',
		질투: 'jealousy'
	};
	const key = keyMap[label];
	if (!key) return;

	emotionState = emotionState.map((e) =>
		e.key === key ? { ...e, value: Math.min(100, Math.max(0, e.value + delta)) } : e
	);
	const affection = emotionState.find((e) => e.key === 'affection')?.value ?? 0;
	const trust = emotionState.find((e) => e.key === 'trust')?.value ?? 0;
	intimacy = Math.round((affection + trust) / 2);
}

export function parseEmotionDelta(text: string): { label: string; delta: number } | null {
	const match = text.match(/^(애정|신뢰|존경|분노|공포|질투)\s*([+-]?\d+)/);
	if (!match) return null;
	return { label: match[1], delta: Number(match[2]) };
}

export function getEmotionTrend() {
	const affection = emotionState.find((e) => e.key === 'affection')?.value ?? 50;
	const trust = emotionState.find((e) => e.key === 'trust')?.value ?? 50;
	const anger = emotionState.find((e) => e.key === 'anger')?.value ?? 20;
	const len = 14;
	return Array.from({ length: len }, (_, i) => {
		const t = i / (len - 1);
		return {
			day: i + 1,
			affection: Math.round(affection - (1 - t) * 18 + Math.sin(i) * 2),
			trust: Math.round(trust - (1 - t) * 15 + Math.cos(i) * 2),
			anger: Math.round(anger + (1 - t) * 6 - Math.sin(i * 2) * 2)
		};
	});
}

export async function refreshEmotion(characterId = activeCharacterId) {
	await initEmotionApi(characterId);
}
