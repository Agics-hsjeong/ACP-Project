import { apiFetch } from './client';
import type { Character, World } from '$lib/data/mock';
import { mapCharacter, mapWorld } from './resources';

export async function listStudioCharacters(): Promise<Character[]> {
	const data = await apiFetch<{ results: Record<string, unknown>[] } | Record<string, unknown>[]>(
		'/studio/characters/'
	);
	const items = Array.isArray(data) ? data : data.results;
	return items.map(mapCharacter);
}

export async function createStudioCharacter(payload: {
	id: string;
	name: string;
	title: string;
	world_id: string;
	description: string;
	tags?: string[];
	genre?: string[];
	personality?: string[];
	occupation?: string;
	race?: string;
	age?: number;
	gender?: string;
	quote?: string;
	memory_summary?: string;
	avatar?: string;
	cover?: string;
	studio_meta?: Record<string, unknown>;
}): Promise<Character> {
	const data = await apiFetch<Record<string, unknown>>('/studio/characters/', {
		method: 'POST',
		json: payload
	});
	return mapCharacter(data);
}

export async function patchStudioCharacter(
	id: string,
	payload: Partial<{
		name: string;
		title: string;
		world_id: string;
		description: string;
		tags: string[];
		genre: string[];
		personality: string[];
		occupation: string;
		race: string;
		age: number;
		gender: string;
		quote: string;
		memory_summary: string;
		avatar: string;
		cover: string;
		studio_meta: Record<string, unknown>;
	}>
): Promise<Character> {
	const data = await apiFetch<Record<string, unknown>>(`/studio/characters/${id}/`, {
		method: 'PATCH',
		json: payload
	});
	return mapCharacter(data);
}

export async function listStudioWorlds(): Promise<World[]> {
	const data = await apiFetch<{ results: Record<string, unknown>[] } | Record<string, unknown>[]>(
		'/studio/worlds/'
	);
	const items = Array.isArray(data) ? data : data.results;
	return items.map(mapWorld);
}

export async function patchStudioWorld(
	id: string,
	payload: Partial<{
		name: string;
		genre: string[];
		cover: string;
		studio_meta: Record<string, unknown>;
	}>
): Promise<World> {
	const data = await apiFetch<Record<string, unknown>>(`/studio/worlds/${id}/`, {
		method: 'PATCH',
		json: {
			...(payload.name !== undefined ? { name: payload.name } : {}),
			...(payload.genre !== undefined ? { genre: payload.genre } : {}),
			...(payload.cover !== undefined ? { cover: payload.cover } : {}),
			...(payload.studio_meta !== undefined ? { studio_meta: payload.studio_meta } : {})
		}
	});
	return mapWorld(data);
}

