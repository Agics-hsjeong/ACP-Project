import type { Character, Memory, World } from '$lib/data/mock';
import { apiHealth } from '$lib/api/client';
import {
	fetchCharacters,
	fetchChatSessions,
	fetchMemories,
	fetchWorlds,
	toRecommendedStories,
	type RecentChat,
	type RecommendedStory
} from '$lib/api/resources';
import { apiFetch } from '$lib/api/client';
import { isLoggedIn } from '$lib/stores/auth.svelte';

let characters = $state<Character[]>([]);
let worlds = $state<World[]>([]);
let memories = $state<Memory[]>([]);
let recentChats = $state<RecentChat[]>([]);
let memoryStats = $state({
	total: 0,
	important: 0,
	daysTogether: 0,
	storyVolume: '0',
	fidelity: 0
});
let loaded = $state(false);
let loading = $state(false);
let useApi = $state(false);
let loadError = $state('');

const DEFAULT_CHARACTER = 'elia';

export async function initCatalog(force = false): Promise<void> {
	if (loading) return;
	if (loaded && !force) return;

	loading = true;
	loadError = '';
	try {
		if (!(await apiHealth())) {
			useApi = false;
			loadError = '서버에 연결할 수 없습니다.';
			return;
		}
		useApi = true;

		const [c, w] = await Promise.all([fetchCharacters(), fetchWorlds()]);
		characters = c;
		worlds = w;
		loaded = true;

		if (isLoggedIn()) {
			await refreshPrivateCatalogData(DEFAULT_CHARACTER);
		}
	} catch (err) {
		console.error('Catalog API load failed:', err);
		useApi = false;
		loadError = '데이터를 불러오지 못했습니다.';
	} finally {
		loading = false;
	}
}

export async function refreshPrivateCatalogData(characterId = DEFAULT_CHARACTER) {
	if (!useApi || !isLoggedIn()) return;

	const [m, sessions] = await Promise.all([
		fetchMemories({ character: characterId }),
		fetchChatSessions()
	]);

	memories = m;
	recentChats = sessions;

	const stats = await apiFetch<{
		total: number;
		important: number;
		days_together: number;
		story_volume: string;
		fidelity: number;
	}>(`/memory-stats/?character=${characterId}`);

	memoryStats = {
		total: stats.total,
		important: stats.important,
		daysTogether: stats.days_together,
		storyVolume: stats.story_volume,
		fidelity: stats.fidelity
	};
}

export function getCatalogLoadError(): string {
	return loadError;
}

export function isCatalogLoaded(): boolean {
	return loaded;
}

export function isCatalogApi(): boolean {
	return useApi;
}

export function isCatalogLoading(): boolean {
	return loading;
}

export function getCatalogCharacters(): Character[] {
	return characters;
}

export function getCatalogWorlds(): World[] {
	return worlds;
}

export function getCatalogMemories(): Memory[] {
	return memories;
}

export function getCatalogMemoryStats() {
	return memoryStats;
}

export function getCatalogRecentChats(): RecentChat[] {
	return recentChats;
}

export function getRecommendedStories(): RecommendedStory[] {
	return toRecommendedStories(characters);
}

export function getCatalogCharacter(id: string): Character | undefined {
	return characters.find((c) => c.id === id);
}

export function getDailyQuests() {
	const chatCount = recentChats.length;
	const memoryCount = memoryStats.total;
	return [
		{
			id: 'q1',
			title: '캐릭터와 3회 대화',
			progress: Math.min(chatCount, 3),
			total: 3,
			reward: 'XP +50'
		},
		{
			id: 'q2',
			title: '기억 1개 저장',
			progress: memoryCount > 0 ? 1 : 0,
			total: 1,
			reward: 'XP +30'
		},
		{
			id: 'q3',
			title: '새 캐릭터 탐색',
			progress: characters.length > 0 ? 1 : 0,
			total: 1,
			reward: 'XP +20'
		}
	];
}

export function getMemoryFragments() {
	return memories.slice(0, 5).map((m) => ({
		id: m.id,
		title: m.title,
		date: m.date,
		delta: m.emotion,
		importance: m.importance,
		thumbnail: m.thumbnail
	}));
}

export function getExploreTags() {
	const tags = new Set<string>();
	for (const c of characters) {
		for (const t of c.tags ?? []) {
			tags.add(t.replace(/^#/, ''));
		}
	}
	return [...tags].slice(0, 12);
}

export function getUserProfileStats() {
	return {
		charactersCreated: 0,
		worldsCreated: 0,
		totalChats: recentChats.length,
		savedMemories: memoryStats.total
	};
}

export function getEmotionEvents() {
	return memories
		.filter((m) => m.emotion)
		.slice(0, 8)
		.map((m) => ({
			id: m.id,
			date: m.date?.slice(5) || '',
			title: m.title,
			delta: m.emotion,
			type: (m.emotion.startsWith('+') ? 'positive' : 'negative') as 'positive' | 'negative'
		}));
}

export function getMemoryTopTags() {
	const counts = new Map<string, number>();
	for (const m of memories) {
		for (const tag of m.tags ?? []) {
			const key = tag.replace(/^#/, '');
			counts.set(key, (counts.get(key) ?? 0) + 1);
		}
	}
	return [...counts.entries()]
		.sort((a, b) => b[1] - a[1])
		.slice(0, 5)
		.map(([tag, count]) => ({ tag: `#${tag}`, count }));
}

export async function refreshMemories(characterId = DEFAULT_CHARACTER) {
	if (!useApi) return;
	await refreshPrivateCatalogData(characterId);
}

export async function refreshChatSessions() {
	if (!useApi || !isLoggedIn()) return;
	recentChats = await fetchChatSessions();
}
