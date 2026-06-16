import { apiHealth } from '$lib/api/client';
import { fetchExploreMeta } from '$lib/api/meta';

let genres = $state<string[]>(['전체']);
let tags = $state<string[]>([]);
let loaded = $state(false);

export async function initMeta(force = false) {
	if (loaded && !force) return;
	if (!(await apiHealth())) return;
	try {
		const data = await fetchExploreMeta();
		genres = data.genres?.length ? data.genres : ['전체'];
		tags = data.tags ?? [];
		loaded = true;
	} catch (err) {
		console.error('Explore meta load failed:', err);
	}
}

export function getExploreGenres(): string[] {
	return genres;
}

export function getExploreTags(): string[] {
	return tags;
}

