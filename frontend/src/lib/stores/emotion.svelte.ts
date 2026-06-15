import type { EmotionAxis } from '$lib/data/mock';
import { emotions as seedEmotions } from '$lib/data/mock';

let emotionState = $state<EmotionAxis[]>(seedEmotions.map((e) => ({ ...e })));

export function getEmotions(): EmotionAxis[] {
	return emotionState;
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
}

export function parseEmotionDelta(text: string): { label: string; delta: number } | null {
	const match = text.match(/^(애정|신뢰|존경|분노|공포|질투)\s*([+-]?\d+)/);
	if (!match) return null;
	return { label: match[1], delta: Number(match[2]) };
}

export function resetEmotions() {
	emotionState = seedEmotions.map((e) => ({ ...e }));
}

export function getIntimacy(): number {
	const affection = emotionState.find((e) => e.key === 'affection')?.value ?? 0;
	const trust = emotionState.find((e) => e.key === 'trust')?.value ?? 0;
	return Math.round((affection + trust) / 2);
}
