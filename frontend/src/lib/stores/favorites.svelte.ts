import { browser } from '$app/environment';

const STORAGE_KEY = 'acp-favorites';

let favoriteIds = $state<string[]>(load());

function load(): string[] {
	if (!browser) return ['elia'];
	try {
		const raw = localStorage.getItem(STORAGE_KEY);
		return raw ? (JSON.parse(raw) as string[]) : ['elia'];
	} catch {
		return ['elia'];
	}
}

function persist() {
	if (!browser) return;
	localStorage.setItem(STORAGE_KEY, JSON.stringify(favoriteIds));
}

export function getFavorites(): string[] {
	return favoriteIds;
}

export function isFavorite(id: string): boolean {
	return favoriteIds.includes(id);
}

export function toggleFavorite(id: string): boolean {
	const next = favoriteIds.includes(id)
		? favoriteIds.filter((f) => f !== id)
		: [...favoriteIds, id];
	favoriteIds = next;
	persist();
	return favoriteIds.includes(id);
}
