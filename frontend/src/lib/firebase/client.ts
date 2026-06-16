import { browser } from '$app/environment';
import { env } from '$env/dynamic/public';
import { initializeApp, type FirebaseApp } from 'firebase/app';
import { getAnalytics, isSupported, type Analytics } from 'firebase/analytics';
import { FirebaseError } from 'firebase/app';
import { getAuth, GoogleAuthProvider, signInWithPopup, type Auth } from 'firebase/auth';

let app: FirebaseApp | null = null;
let auth: Auth | null = null;
let analytics: Analytics | null = null;

export function isFirebaseConfigured(): boolean {
	return Boolean(
		env.PUBLIC_FIREBASE_API_KEY &&
			env.PUBLIC_FIREBASE_AUTH_DOMAIN &&
			env.PUBLIC_FIREBASE_PROJECT_ID
	);
}

function getFirebaseApp(): FirebaseApp {
	if (!browser) throw new Error('Firebase is only available in the browser');
	if (!isFirebaseConfigured()) {
		throw new Error('Firebase environment variables are not configured');
	}
	if (!app) {
		const config: Record<string, string> = {
			apiKey: env.PUBLIC_FIREBASE_API_KEY!,
			authDomain: env.PUBLIC_FIREBASE_AUTH_DOMAIN!,
			projectId: env.PUBLIC_FIREBASE_PROJECT_ID!,
			storageBucket: env.PUBLIC_FIREBASE_STORAGE_BUCKET ?? '',
			messagingSenderId: env.PUBLIC_FIREBASE_MESSAGING_SENDER_ID ?? '',
			appId: env.PUBLIC_FIREBASE_APP_ID ?? ''
		};
		if (env.PUBLIC_FIREBASE_MEASUREMENT_ID) {
			config.measurementId = env.PUBLIC_FIREBASE_MEASUREMENT_ID;
		}
		app = initializeApp(config);
		void initAnalytics();
	}
	return app;
}

async function initAnalytics(): Promise<void> {
	if (!browser || analytics || !env.PUBLIC_FIREBASE_MEASUREMENT_ID || !app) return;
	try {
		if (await isSupported()) {
			analytics = getAnalytics(app);
		}
	} catch {
		/* analytics optional */
	}
}

function getFirebaseAuth(): Auth {
	if (!auth) auth = getAuth(getFirebaseApp());
	return auth;
}

export function mapFirebaseAuthError(err: unknown): string {
	if (err instanceof FirebaseError) {
		if (err.code === 'auth/configuration-not-found') {
			return (
				'Firebase Authentication이 활성화되지 않았습니다. ' +
				'Firebase Console → Authentication → 시작하기 → 로그인 방법에서 Google을 켜주세요. ' +
				'(https://console.firebase.google.com/project/aicharacterplayground/authentication)'
			);
		}
		if (err.code === 'auth/popup-closed-by-user') {
			return '로그인 창이 닫혔습니다. 다시 시도해 주세요.';
		}
		if (err.code === 'auth/unauthorized-domain') {
			const host = browser ? window.location.hostname : 'localhost';
			const port = browser ? window.location.port : '28433';
			const isPrivateIp = /^192\.168\.|^10\.|^172\.(1[6-9]|2\d|3[01])\./.test(host);
			if (isPrivateIp) {
				return (
					`LAN IP(${host})가 Firebase 승인 도메인에 없습니다. ` +
					`방법 1) Console → Authentication → Settings → 승인된 도메인에 ` +
					`\`${host}\` 입력 후 경고가 나와도 [추가] 클릭 (포트 제외). ` +
					`방법 2) hosts에 \`192.168.0.63 acp.local\` 추가 후 Firebase에 \`acp.local\` 등록 → http://acp.local:${port || '28433'} 접속`
				);
			}
			if (host === '127.0.0.1') {
				return `127.0.0.1은 Firebase 승인 도메인이 아닙니다. 주소창을 http://localhost:${port || '28433'} 로 바꿔 접속한 뒤 다시 시도하세요.`;
			}
			return (
				`승인되지 않은 도메인입니다 (현재: ${host}). ` +
				`Firebase Console → Authentication → Settings → 승인된 도메인에 ` +
				`\`${host}\`를 추가하거나 http://localhost:${port || '28433'} 로 접속하세요.`
			);
		}
		return err.message;
	}
	if (err instanceof Error) return err.message;
	return '로그인에 실패했습니다.';
}

export async function signInWithGoogle(): Promise<string> {
	const provider = new GoogleAuthProvider();
	provider.setCustomParameters({ prompt: 'select_account' });
	const result = await signInWithPopup(getFirebaseAuth(), provider);
	return result.user.getIdToken();
}
