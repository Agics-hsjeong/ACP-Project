import { browser } from '$app/environment';
import { goto } from '$app/navigation';
import { fetchMe, loginApi, loginWithFirebaseToken, type AuthUser } from '$lib/api/auth';
import { apiHealth } from '$lib/api/client';
import { setAuthToken } from '$lib/api/config';
import { getLoginUrl } from '$lib/auth/access';
import { isFirebaseConfigured, mapFirebaseAuthError, signInWithGoogle } from '$lib/firebase/client';

const STORAGE_KEY = 'acp-auth';

let user = $state<AuthUser | null>(loadUser());

function loadUser(): AuthUser | null {
	if (!browser) return null;
	try {
		const raw = localStorage.getItem(STORAGE_KEY);
		return raw ? (JSON.parse(raw) as AuthUser) : null;
	} catch {
		return null;
	}
}

function persist(next: AuthUser | null) {
	if (!browser) return;
	if (next) localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
	else localStorage.removeItem(STORAGE_KEY);
}

export function getUser(): AuthUser | null {
	return user;
}

export function isLoggedIn(): boolean {
	return !!user;
}

export function login(email: string, password?: string) {
	user = { email, name: email.split('@')[0] || 'Creator' };
	persist(user);
}

export async function loginWithApi(email: string, password?: string, provider?: string) {
	if (!(await apiHealth())) {
		throw new Error('서버에 연결할 수 없습니다. 잠시 후 다시 시도해 주세요.');
	}
	const apiUser = await loginApi(email, password, provider);
	user = apiUser;
	persist(user);
}

export async function loginWithGoogle(): Promise<void> {
	if (!isFirebaseConfigured()) {
		throw new Error('Firebase 설정이 필요합니다. .env의 PUBLIC_FIREBASE_* 값을 확인하세요.');
	}
	try {
		const idToken = await signInWithGoogle();
		const apiUser = await loginWithFirebaseToken(idToken);
		user = apiUser;
		persist(user);
	} catch (err) {
		throw new Error(mapFirebaseAuthError(err));
	}
}

export function loginSocial(provider: string) {
	user = { email: `${provider}@acp.local`, name: 'Creator', provider };
	persist(user);
}

export function logout() {
	user = null;
	persist(null);
	setAuthToken(null);
}

export async function requireAuth(redirectTo?: string) {
	if (!user) await goto(getLoginUrl(redirectTo));
}

export function redirectToLogin(returnPath: string) {
	if (!browser) return;
	goto(getLoginUrl(returnPath));
}

export async function restoreSession(): Promise<void> {
	if (!browser || user) return;
	try {
		const me = await fetchMe();
		if (me) {
			user = me;
			persist(me);
		}
	} catch {
		/* not logged in */
	}
}
