<script lang="ts">
	import { page } from '$app/stores';
	import { Home, Compass, MessageCircle, Brain, User } from 'lucide-svelte';

	const tabs = [
		{ href: '/home', label: '홈', icon: Home },
		{ href: '/explore', label: '탐색', icon: Compass },
		{ href: '/chat/elia', label: '채팅', icon: MessageCircle, match: '/chat' },
		{ href: '/memory', label: '기억', icon: Brain },
		{ href: '/mypage', label: '마이', icon: User, match: '/mypage' }
	];
</script>

<nav
	class="fixed inset-x-0 bottom-0 z-50 flex border-t border-white/10 bg-bg-surface/95 backdrop-blur-md lg:hidden"
>
	{#each tabs as tab}
		{@const active = tab.match
			? $page.url.pathname.startsWith(tab.match)
			: $page.url.pathname.startsWith(tab.href)}
		<a
			href={tab.href}
			class="flex flex-1 flex-col items-center gap-0.5 py-2 text-[10px] transition {active
				? 'text-primary-400'
				: 'text-text-muted'}"
		>
			<tab.icon class="h-5 w-5" />
			{tab.label}
		</a>
	{/each}
</nav>
