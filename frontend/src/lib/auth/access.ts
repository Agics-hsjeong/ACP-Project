/** 비회원(로그인 없이) 열람 가능한 경로 */
const GUEST_PATHS = new Set(['/home', '/explore']);

export function isGuestAllowedPath(pathname: string): boolean {
	if (GUEST_PATHS.has(pathname)) return true;
	if (pathname.startsWith('/characters/')) return true;
	return false;
}

export function safeRedirectPath(path: string | null | undefined, fallback = '/home'): string {
	if (!path || !path.startsWith('/') || path.startsWith('//')) return fallback;
	return path;
}

export function getLoginUrl(redirect?: string): string {
	const target = safeRedirectPath(redirect, '');
	if (!target) return '/login';
	return `/login?redirect=${encodeURIComponent(target)}`;
}

export const guestNavItems = [
	{ href: '/home', label: '홈', icon: 'Home' as const },
	{ href: '/explore', label: '탐색', icon: 'Compass' as const }
];

export const memberNavItems = [
	{ href: '/home', label: '홈', icon: 'Home' as const },
	{ href: '/chat/elia', label: '채팅', icon: 'MessageCircle' as const, match: '/chat' },
	{ href: '/explore', label: '탐색', icon: 'Compass' as const },
	{ href: '/memory', label: '기억 보관소', icon: 'Brain' as const },
	{ href: '/relationship', label: '인물 관계도', icon: 'GitBranch' as const },
	{ href: '/emotion', label: '감정 분석', icon: 'Heart' as const },
	{ href: '/studio/character', label: '캐릭터 스튜디오', icon: 'Palette' as const },
	{ href: '/studio/world', label: '세계관 스튜디오', icon: 'Globe' as const },
	{ href: '/settings', label: '설정', icon: 'Settings' as const },
	{ href: '/mypage', label: '마이페이지', icon: 'User' as const, match: '/mypage' }
];
