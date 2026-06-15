<script lang="ts">
	import { page } from '$app/stores';
	import {
		Home,
		MessageCircle,
		Compass,
		Brain,
		GitBranch,
		Heart,
		Palette,
		Globe,
		Settings,
		Sparkles,
		User
	} from 'lucide-svelte';
	import { recentChats } from '$lib/data/mock';

	const navItems = [
		{ href: '/home', label: '홈', icon: Home },
		{ href: '/chat/elia', label: '채팅', icon: MessageCircle, match: '/chat' },
		{ href: '/explore', label: '탐색', icon: Compass },
		{ href: '/memory', label: '기억 보관소', icon: Brain },
		{ href: '/relationship', label: '인물 관계도', icon: GitBranch },
		{ href: '/emotion', label: '감정 분석', icon: Heart },
		{ href: '/studio/character', label: '캐릭터 스튜디오', icon: Palette, phase: 2 },
		{ href: '/studio/world', label: '세계관 스튜디오', icon: Globe, phase: 2 },
		{ href: '/settings', label: '설정', icon: Settings },
		{ href: '/mypage', label: '마이페이지', icon: User, match: '/mypage' }
	];
</script>

<aside class="flex h-screen w-64 shrink-0 flex-col border-r border-white/10 bg-bg-surface/50">
	<a href="/home" class="flex items-center gap-2 border-b border-white/10 px-5 py-4">
		<Sparkles class="h-5 w-5 text-primary-400" />
		<div class="leading-tight">
			<p class="text-sm font-semibold">AI Character</p>
			<p class="text-[10px] tracking-widest text-text-muted">PLAYGROUND</p>
		</div>
	</a>

	<nav class="flex-1 space-y-0.5 overflow-y-auto p-3">
		{#each navItems as item}
			{@const active = item.match
				? $page.url.pathname.startsWith(item.match)
				: $page.url.pathname.startsWith(item.href)}
			<a
				href={item.href}
				class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition {active
					? 'bg-primary-600/20 text-primary-300'
					: 'text-text-secondary hover:bg-white/5 hover:text-text-primary'}"
			>
				<item.icon class="h-4 w-4 shrink-0" />
				<span class="flex-1">{item.label}</span>
				{#if item.phase}
					<span class="text-[10px] text-text-muted">P{item.phase}</span>
				{/if}
			</a>
		{/each}
	</nav>

	<div class="border-t border-white/10 p-3">
		<p class="mb-2 px-2 text-xs font-medium text-text-muted">최근 대화</p>
		<div class="space-y-1">
			{#each recentChats.slice(0, 4) as chat}
				<a
					href="/chat/{chat.id}"
					class="flex items-center gap-2 rounded-lg px-2 py-2 hover:bg-white/5"
				>
					<img src="https://api.dicebear.com/9.x/notionists/svg?seed={chat.id}" alt="" class="h-8 w-8 rounded-full bg-bg-card" />
					<div class="min-w-0 flex-1">
						<p class="truncate text-xs font-medium">{chat.name}</p>
						<p class="truncate text-[10px] text-text-muted">{chat.preview}</p>
					</div>
					<span class="text-[10px] text-text-muted">{chat.time}</span>
				</a>
			{/each}
		</div>
	</div>

	<div class="border-t border-white/10 p-3">
		<div class="rounded-xl bg-gradient-to-br from-primary-600/30 to-secondary-600/20 p-4">
			<p class="text-xs font-semibold text-primary-200">Premium Plan</p>
			<p class="mt-1 text-[10px] text-text-muted">무제한 대화 & 고급 기억</p>
			<button class="mt-3 w-full rounded-lg bg-primary-600 py-1.5 text-xs font-medium text-white hover:bg-primary-500">
				업그레이드
			</button>
		</div>
	</div>
</aside>
