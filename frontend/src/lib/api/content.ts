import { apiFetch } from './client';

export type LandingFeature = { key: string; title: string; description: string };

export type LandingContent = {
	key: string;
	payload: { features?: LandingFeature[] } & Record<string, unknown>;
	updated_at: string;
};

export async function fetchLandingContent(): Promise<LandingContent> {
	return apiFetch<LandingContent>('/content/landing/');
}

