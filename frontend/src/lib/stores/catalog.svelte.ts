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

const DEFAULT_CHARACTER = 'elia';

export async function initCatalog(force = false): Promise<void> {
	if (loading) return;
	if (loaded && !force) return;

	loading = true;
	try {
		if (!(await apiHealth())) {
			useApi = false;
			return;
		}
		useApi = true;

		const [c, w, m, sessions] = await Promise.all([
			fetchCharacters(),
			fetchWorlds(),
			fetchMemories({ character: DEFAULT_CHARACTER }),
			fetchChatSessions()
		]);

		characters = c;
		worlds = w;
		memories = m;
		recentChats = sessions.length
			? sessions
			: c.slice(0, 5).map((ch) => ({
					id: ch.id,
					name: ch.name,
					avatar: ch.avatar,
					preview: ch.quote || ch.description.slice(0, 60),
					time: ''
				}));

		const stats = await apiFetch<{
			total: number;
			important: number;
			days_together: number;
			story_volume: string;
			fidelity: number;
		}>(`/memory-stats/?character=${DEFAULT_CHARACTER}`);

		memoryStats = {
			total: stats.total,
			important: stats.important,
			daysTogether: stats.days_together,
			storyVolume: stats.story_volume,
			fidelity: stats.fidelity
		};
		loaded = true;
	} catch (err) {
		console.error('Catalog API load failed:', err);
		useApi = false;
	} finally {
		loading = false;
	}
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
			progress: Math.min(characters.length, 1),
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
		importance: m.importance
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
		charactersCreated: characters.length,
		worldsCreated: worlds.length,
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

export function getRelationshipGraph() {
	const nodes = characters.map((c) => ({
		id: c.id,
		label: c.name,
		kind: 'character' as const,
		subtitle: c.world,
		tags: c.tags,
		avatar: c.avatar,
		isCenter: c.id === DEFAULT_CHARACTER,
		worldId: c.worldId ?? worlds.find((w) => c.world.includes(w.name))?.id ?? worlds[0]?.id
	}));
	const edges = characters
		.filter((c) => c.id !== DEFAULT_CHARACTER)
		.map((c) => ({
			id: `elia-${c.id}`,
			source: DEFAULT_CHARACTER,
			target: c.id,
			type: 'friend' as const,
			label: '친구'
		}));
	return {
		nodes,
		edges,
		worlds: worlds.map((w) => ({ id: w.id, name: w.name }))
	};
}

export function getRelationshipNode(id: string) {
	return getRelationshipGraph().nodes.find((n) => n.id === id);
}

export function getRelationshipEdgesForNode(nodeId: string) {
	const { edges } = getRelationshipGraph();
	return edges.filter((e) => e.source === nodeId || e.target === nodeId);
}

export function getEliaRelationships() {
	const { edges, nodes } = getRelationshipGraph();
	return edges
		.filter((e) => e.source === DEFAULT_CHARACTER || e.target === DEFAULT_CHARACTER)
		.map((e) => {
			const otherId = e.source === DEFAULT_CHARACTER ? e.target : e.source;
			const other = nodes.find((n) => n.id === otherId);
			return {
				characterId: otherId,
				name: other?.label ?? otherId,
				type: e.type,
				score: 65 + (otherId.length % 30)
			};
		});
}

export function getRelationshipHistory() {
	return memories.slice(0, 6).map((m) => ({
		id: m.id,
		title: m.title,
		date: m.date,
		summary: m.summary
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
	memories = await fetchMemories({ character: characterId });
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

export async function refreshChatSessions() {
	if (!useApi) return;
	recentChats = await fetchChatSessions();
}
