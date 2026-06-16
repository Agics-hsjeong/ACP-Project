import type { Character, Memory, World } from '$lib/data/mock';
import { apiFetch } from './client';

type Paginated<T> = { results: T[] } | T[];

export type RecentChat = {
	id: string;
	name: string;
	avatar?: string;
	preview: string;
	time: string;
};

export type RecommendedStory = {
	id: string;
	title: string;
	summary: string;
	characterId: string;
	characterName: string;
	world: string;
	cover: string;
	reads: number;
};

function unwrap<T>(data: Paginated<T>): T[] {
	return Array.isArray(data) ? data : data.results;
}

export async function fetchCharacters(params?: { q?: string; world?: string }): Promise<Character[]> {
	const search = new URLSearchParams();
	if (params?.q) search.set('q', params.q);
	if (params?.world) search.set('world', params.world);
	const qs = search.toString();
	const path = '/characters/' + (qs ? `?${qs}` : '');
	const data = await apiFetch<Paginated<Record<string, unknown>>>(path);
	return unwrap(data).map(mapCharacter);
}

export async function fetchCharacter(id: string): Promise<Character | null> {
	try {
		const data = await apiFetch<Record<string, unknown>>(`/characters/${id}/`);
		return mapCharacter(data);
	} catch {
		return null;
	}
}

export async function fetchWorlds(): Promise<World[]> {
	const data = await apiFetch<Paginated<Record<string, unknown>>>('/worlds/');
	return unwrap(data).map(mapWorld);
}

export async function fetchMemories(params?: {
	character?: string;
	q?: string;
	importance?: string;
}): Promise<Memory[]> {
	const search = new URLSearchParams();
	if (params?.character) search.set('character', params.character);
	if (params?.q) search.set('q', params.q);
	if (params?.importance) search.set('importance', params.importance);
	const qs = search.toString();
	const path = '/memories/' + (qs ? `?${qs}` : '');
	const data = await apiFetch<Paginated<Record<string, unknown>>>(path);
	return unwrap(data).map(mapMemory);
}

export async function fetchChatSessions(): Promise<RecentChat[]> {
	const data = await apiFetch<RecentChat[]>('/chat-sessions/');
	return data.map((s) => ({
		...s,
		time: formatRelativeTime(s.time)
	}));
}

export async function fetchEmotion(characterId: string) {
	return apiFetch<{
		character_id: string;
		axes: Array<{ key: string; label: string; value: number; color: string }>;
		intimacy: number;
	}>(`/emotion/${characterId}/`);
}

export async function createMemory(input: {
	characterId: string;
	title: string;
	summary: string;
	importance?: Memory['importance'];
	tags?: string[];
}): Promise<Memory> {
	const data = await apiFetch<Record<string, unknown>>('/memories/', {
		method: 'POST',
		json: {
			character_id: input.characterId,
			title: input.title,
			summary: input.summary,
			importance: input.importance ?? 'medium',
			tags: input.tags ?? []
		}
	});
	return mapMemory(data);
}

export async function ragSearch(characterId: string, query: string, topK = 5) {
	return apiFetch<{
		character_id: string;
		query: string;
		results: Array<{
			id: number;
			source_type: string;
			chunk_text: string;
			importance: number;
			archive_key: string | null;
		}>;
	}>('/rag/search/', {
		method: 'POST',
		json: { character_id: characterId, query, top_k: topK }
	});
}

function formatRelativeTime(iso: string): string {
	const diff = Date.now() - new Date(iso).getTime();
	const mins = Math.floor(diff / 60000);
	if (mins < 1) return '방금 전';
	if (mins < 60) return `${mins}분 전`;
	const hours = Math.floor(mins / 60);
	if (hours < 24) return `${hours}시간 전`;
	const days = Math.floor(hours / 24);
	if (days < 7) return `${days}일 전`;
	return new Date(iso).toLocaleDateString('ko-KR');
}

export function mapCharacter(raw: Record<string, unknown>): Character {
	return {
		id: String(raw.id),
		name: String(raw.name),
		title: String(raw.title),
		world: String(raw.world ?? raw.world_name ?? ''),
		worldId: raw.world_id ? String(raw.world_id) : undefined,
		tags: (raw.tags as string[]) ?? [],
		genre: (raw.genre as string[]) ?? [],
		likes: Number(raw.likes ?? 0),
		views: Number(raw.views ?? 0),
		description: String(raw.description ?? ''),
		personality: (raw.personality as string[]) ?? [],
		occupation: String(raw.occupation ?? ''),
		race: String(raw.race ?? ''),
		age: raw.age ? Number(raw.age) : undefined,
		gender: raw.gender ? String(raw.gender) : undefined,
		quote: raw.quote ? String(raw.quote) : undefined,
		memorySummary: raw.memory_summary ? String(raw.memory_summary) : undefined,
		avatar: String(raw.avatar ?? ''),
		cover: String(raw.cover ?? '')
	};
}

export function mapWorld(raw: Record<string, unknown>): World {
	return {
		id: String(raw.id),
		name: String(raw.name),
		genre: (raw.genre as string[]) ?? [],
		characterCount: Number(raw.characterCount ?? raw.character_count ?? 0),
		cover: String(raw.cover ?? '')
	};
}

function mapMemory(raw: Record<string, unknown>): Memory {
	return {
		id: String(raw.id),
		title: String(raw.title),
		summary: String(raw.summary),
		detail: raw.detail ? String(raw.detail) : undefined,
		emotion: String(raw.emotion ?? ''),
		date: String(raw.date),
		importance: raw.importance as Memory['importance'],
		tags: (raw.tags as string[]) ?? undefined,
		quote: raw.quote ? String(raw.quote) : undefined,
		location: raw.location ? String(raw.location) : undefined,
		thumbnail: raw.thumbnail ? String(raw.thumbnail) : undefined,
		characterId: raw.character_id ? String(raw.character_id) : undefined,
		dday: raw.dday ? Number(raw.dday) : undefined,
		stats: raw.stats as Memory['stats']
	};
}

export function toRecommendedStories(characters: Character[]): RecommendedStory[] {
	return characters.slice(0, 6).map((c) => ({
		id: c.id,
		title: c.memorySummary || c.title,
		summary: c.description,
		characterId: c.id,
		characterName: c.name,
		world: c.world,
		cover: c.cover,
		reads: c.views
	}));
}
