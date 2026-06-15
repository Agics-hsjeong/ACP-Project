<script lang="ts">
	import { page } from '$app/stores';
	import { Home, Compass, MessageCircle, Brain, User } from 'lucide-svelte';

	const tabs = [
		{ href: '/mobile/home', label: '홈', icon: Home },
		{ href: '/mobile/explore', label: '탐색', icon: Compass },
		{ href: '/mobile/chat/elia', label: '대화', icon: MessageCircle, match: '/mobile/chat' },
		{ href: '/mobile/memory', label: '기억', icon: Brain },
		{ href: '/mobile/profile', label: '마이', icon: User, match: '/mobile/profile' }
	];

	let { children }: { children: import('svelte').Snippet } = $props();
</script>

<div class="mx-auto flex min-h-dvh w-full max-w-[360px] flex-col bg-bg-primary shadow-2xl lg:min-h-[800px] lg:rounded-[2rem] lg:border lg:border-white/10">
	<div class="flex-1 overflow-y-auto pb-16">
		{@render children()}
	</div>
	<nav class="fixed bottom-0 left-1/2 z-50 flex w-full max-w-[360px] -translate-x-1/2 border-t border-white/10 bg-bg-surface/95 backdrop-blur-md lg:rounded-b-[2rem]">
		{#each tabs as tab}
			{@const active = tab.match
				? $page.url.pathname.startsWith(tab.match)
				: $page.url.pathname === tab.href}
			<a
				href={tab.href}
				class="flex flex-1 flex-col items-center gap-0.5 py-2.5 text-[10px] {active
					? 'text-primary-400'
					: 'text-text-muted'}"
			>
				<tab.icon class="h-5 w-5" />
				{tab.label}
			</a>
		{/each}
	</nav>
</div>
