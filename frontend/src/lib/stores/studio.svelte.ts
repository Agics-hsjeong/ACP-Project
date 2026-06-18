import type { Character, World } from '$lib/data/mock';
import { apiHealth } from '$lib/api/client';
import {
	listStudioCharacters,
	listStudioWorlds,
	createStudioCharacter,
	patchStudioCharacter,
	patchStudioWorld
} from '$lib/api/studio';

let studioCharacters = $state<Character[]>([]);
let studioWorlds = $state<World[]>([]);
let loaded = $state(false);
let loading = $state(false);

export async function initStudio(force = false) {
	if (loading) return;
	if (loaded && !force) return;
	if (!(await apiHealth())) return;

	loading = true;
	try {
		const [chars, worlds] = await Promise.all([listStudioCharacters(), listStudioWorlds()]);
		studioCharacters = chars;
		studioWorlds = worlds;
		loaded = true;
	} catch (err) {
		console.error('Studio API load failed:', err);
	} finally {
		loading = false;
	}
}

export function getStudioCharacters() {
	return studioCharacters;
}

export function getStudioWorlds() {
	return studioWorlds;
}

export async function saveStudioCharacter(id: string, patch: Parameters<typeof patchStudioCharacter>[1]) {
	const updated = await patchStudioCharacter(id, patch);
	studioCharacters = studioCharacters.map((c) => (c.id === id ? updated : c));
	return updated;
}

export async function saveStudioWorld(id: string, patch: Parameters<typeof patchStudioWorld>[1]) {
	const updated = await patchStudioWorld(id, patch);
	studioWorlds = studioWorlds.map((w) => (w.id === id ? updated : w));
	return updated;
}

export async function addStudioCharacter(payload: Parameters<typeof createStudioCharacter>[0]) {
	const created = await createStudioCharacter(payload);
	studioCharacters = [...studioCharacters, created];
	return created;
}

