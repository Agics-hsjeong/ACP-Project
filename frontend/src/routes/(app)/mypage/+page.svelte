<script lang="ts">
	import { goto } from '$app/navigation';
	import { getUser, logout } from '$lib/stores/auth.svelte';
	import { getDailyQuests } from '$lib/stores/catalog.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import {
		Brain,
		Heart,
		GitBranch,
		Palette,
		Globe,
		Settings,
		Smartphone,
		ChevronRight
	} from 'lucide-svelte';

	const user = $derived(getUser());
	const dailyQuests = $derived(getDailyQuests());

	const menu = [
		{ href: '/memory', label: '기억 보관소', icon: Brain },
		{ href: '/emotion', label: '감정 분석', icon: Heart },
		{ href: '/relationship', label: '인물 관계도', icon: GitBranch },
		{ href: '/studio/character', label: '캐릭터 스튜디오', icon: Palette },
		{ href: '/studio/world', label: '세계관 스튜디오', icon: Globe },
		{ href: '/mobile', label: 'Mobile Design (Screen 12)', icon: Smartphone },
		{ href: '/settings', label: '설정', icon: Settings }
	];

	function handleLogout() {
		logout();
		goto('/login');
	}
</script>

<svelte:head>
	<title>마이페이지 — ACP</title>
</svelte:head>

<div class="mx-auto max-w-2xl">
	<div class="rounded-2xl border border-white/10 bg-bg-surface/50 p-6">
		<div class="flex items-center gap-5">
			<img
				src={user?.picture || `https://api.dicebear.com/9.x/notionists/svg?seed=${user?.email || 'user'}`}
				alt=""
				class="h-20 w-20 rounded-full border-2 border-primary-500/30 bg-bg-card"
			/>
			<div class="flex-1">
				<h1 class="text-2xl font-bold">{user?.name || 'Creator'}</h1>
				<p class="text-sm text-text-muted">{user?.email || ''}</p>
				<p class="mt-1 text-xs text-primary-300">{user?.provider === 'google' ? 'Google 계정' : '로컬 계정'}</p>
			</div>
		</div>
	</div>

	<div class="mt-6 space-y-2">
		{#each menu as item}
			<a
				href={item.href}
				class="flex items-center gap-3 rounded-xl border border-white/10 bg-bg-surface/40 px-4 py-3 transition hover:border-primary-500/30"
			>
				<item.icon class="h-5 w-5 text-primary-400" />
				<span class="flex-1 text-sm">{item.label}</span>
				<ChevronRight class="h-4 w-4 text-text-muted" />
			</a>
		{/each}
	</div>

	<div class="mt-6 rounded-2xl border border-white/10 bg-bg-surface/50 p-5">
		<h2 class="mb-4 font-semibold">데일리 퀘스트</h2>
		<div class="space-y-3">
			{#each dailyQuests as quest}
				<div class="rounded-xl border border-white/10 bg-bg-primary/40 p-3 text-sm">
					<div class="mb-1 flex justify-between">
						<span>{quest.title}</span>
						<span class="text-xs text-primary-300">{quest.reward}</span>
					</div>
					<p class="text-[10px] text-text-muted">{quest.progress}/{quest.total}</p>
				</div>
			{/each}
		</div>
	</div>

	<div class="mt-6">
		<Button variant="ghost" fullWidth onclick={handleLogout}>로그아웃</Button>
	</div>
</div>
