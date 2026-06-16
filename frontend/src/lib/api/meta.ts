import { apiFetch } from './client';

export type ExploreMeta = { genres: string[]; tags: string[] };

export async function fetchExploreMeta(): Promise<ExploreMeta> {
	return apiFetch<ExploreMeta>('/meta/explore/');
}

