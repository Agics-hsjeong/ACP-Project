<script lang="ts">
	import { getUser, logout } from '$lib/stores/auth.svelte';
	import { getDailyQuests, getUserProfileStats } from '$lib/stores/catalog.svelte';
	import { goto } from '$app/navigation';
	import Button from '$lib/components/ui/Button.svelte';
	import {
		Brain,
		Heart,
		GitBranch,
		Palette,
		Settings,
		ChevronRight
	} from 'lucide-svelte';

	const user = $derived(getUser());
	const dailyQuests = $derived(getDailyQuests());
	const stats = $derived(getUserProfileStats());

	const menu = [
		{ href: '/mobile/memory', label: '기억 보관소', icon: Brain },
		{ href: '/mobile/emotion', label: '감정 분석', icon: Heart },
		{ href: '/mobile/relationship', label: '인물 관계도', icon: GitBranch },
		{ href: '/studio/character', label: '캐릭터 제작', icon: Palette },
		{ href: '/settings', label: '설정', icon: Settings }
	];
</script>

<svelte:head>
	<title>마이페이지 — Mobile</title>
</svelte:head>

<div class="border-b border-white/10 p-4">
	<div class="flex items-center gap-4">
		<img
			src={user?.picture || `https://api.dicebear.com/9.x/notionists/svg?seed=${user?.email || 'user'}`}
			alt=""
			class="h-14 w-14 rounded-full bg-bg-card"
		/>
		<div class="flex-1">
			<p class="font-bold">{user?.name || 'Creator'}</p>
			<p class="text-xs text-text-muted">{user?.email || ''}</p>
		</div>
	</div>
</div>

<div class="grid grid-cols-2 gap-2 p-4">
	{#each [
		{ label: '캐릭터', value: stats.charactersCreated },
		{ label: '세계관', value: stats.worldsCreated },
		{ label: '총 대화', value: stats.totalChats },
		{ label: '저장 기억', value: stats.savedMemories }
	] as stat}
		<div class="rounded-xl border border-white/10 bg-bg-surface/50 p-3 text-center">
			<p class="text-lg font-bold">{stat.value}</p>
			<p class="text-[10px] text-text-muted">{stat.label}</p>
		</div>
	{/each}
</div>

<section class="px-4 pb-4">
	<h2 class="mb-2 text-sm font-semibold">데일리 퀘스트</h2>
	{#each dailyQuests as quest}
		<div class="mb-2 rounded-xl border border-white/10 bg-bg-surface/50 p-3 text-xs">
			{quest.title} · {quest.progress}/{quest.total}
		</div>
	{/each}
</section>

<nav class="space-y-1 px-4">
	{#each menu as item}
		<a
			href={item.href}
			class="flex items-center gap-3 rounded-xl px-3 py-3 hover:bg-white/5"
		>
			<item.icon class="h-4 w-4 text-text-muted" />
			<span class="flex-1 text-sm">{item.label}</span>
			<ChevronRight class="h-4 w-4 text-text-muted" />
		</a>
	{/each}
</nav>

<div class="p-4">
	<Button variant="ghost" fullWidth onclick={() => { logout(); goto('/login'); }}>로그아웃</Button>
</div>
