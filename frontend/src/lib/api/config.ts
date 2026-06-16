import { browser } from '$app/environment';
import { env } from '$env/dynamic/public';

export function getApiBase(): string {
	const base = env.PUBLIC_API_BASE ?? '/api';
	return base.replace(/\/$/, '');
}

export function isApiEnabled(): boolean {
	if (!browser) return false;
	return getApiBase().length > 0;
}

export function getAuthToken(): string | null {
	if (!browser) return null;
	return localStorage.getItem('acp-token');
}

export function setAuthToken(token: string | null) {
	if (!browser) return;
	if (token) localStorage.setItem('acp-token', token);
	else localStorage.removeItem('acp-token');
}
