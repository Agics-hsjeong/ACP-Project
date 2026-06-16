import { ApiError, apiFetch } from './client';
import { setAuthToken } from './config';

export type AuthUser = {
	email: string;
	name: string;
	picture?: string;
	provider?: string;
};

export async function loginApi(
	email: string,
	password?: string,
	provider?: string
): Promise<AuthUser> {
	const data = await apiFetch<{ token: string; user: AuthUser }>('/auth/login/', {
		method: 'POST',
		json: { email, password, provider }
	});
	setAuthToken(data.token);
	return data.user;
}

export async function loginWithFirebaseToken(idToken: string): Promise<AuthUser> {
	try {
		const data = await apiFetch<{ token: string; user: AuthUser }>('/auth/firebase/', {
			method: 'POST',
			json: { id_token: idToken }
		});
		setAuthToken(data.token);
		return data.user;
	} catch (err) {
		if (err instanceof ApiError) {
			try {
				const body = JSON.parse(err.message) as { detail?: string };
				if (body.detail) throw new Error(body.detail);
			} catch (parseErr) {
				if (parseErr instanceof Error && parseErr.message !== err.message) throw parseErr;
			}
		}
		throw err;
	}
}

export async function fetchMe(): Promise<AuthUser | null> {
	const data = await apiFetch<{ user: AuthUser | null }>('/auth/me/');
	return data.user;
}
