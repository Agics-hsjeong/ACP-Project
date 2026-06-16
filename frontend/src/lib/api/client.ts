import { getApiBase, getAuthToken } from './config';

export class ApiError extends Error {
	status: number;
	constructor(message: string, status: number) {
		super(message);
		this.status = status;
	}
}

type RequestOptions = RequestInit & { json?: unknown };

export async function apiFetch<T>(path: string, options: RequestOptions = {}): Promise<T> {
	const { json, headers, ...rest } = options;
	const token = getAuthToken();

	const res = await fetch(`${getApiBase()}${path}`, {
		...rest,
		headers: {
			'Content-Type': 'application/json',
			...(token ? { Authorization: `Token ${token}` } : {}),
			...headers
		},
		body: json !== undefined ? JSON.stringify(json) : rest.body
	});

	if (!res.ok) {
		const text = await res.text().catch(() => res.statusText);
		throw new ApiError(text || `HTTP ${res.status}`, res.status);
	}

	if (res.status === 204) return undefined as T;
	return res.json() as Promise<T>;
}

export async function apiHealth(): Promise<boolean> {
	try {
		const res = await fetch(`${getApiBase()}/health/`);
		return res.ok;
	} catch {
		return false;
	}
}
