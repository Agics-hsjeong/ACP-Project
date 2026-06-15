<script lang="ts">
	import { userProfile } from '$lib/data/mock';
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

	const menu = [
		{ href: '/memory', label: '기억 보관소', icon: Brain },
		{ href: '/emotion', label: '감정 분석', icon: Heart },
		{ href: '/relationship', label: '인물 관계도', icon: GitBranch },
		{ href: '/studio/character', label: '캐릭터 스튜디오', icon: Palette, phase: 2 },
		{ href: '/studio/world', label: '세계관 스튜디오', icon: Globe, phase: 2 },
		{ href: '/mobile', label: 'Mobile Design (Screen 12)', icon: Smartphone },
		{ href: '/settings', label: '설정', icon: Settings }
	];
</script>

<svelte:head>
	<title>마이페이지 — ACP</title>
</svelte:head>

<div class="mx-auto max-w-2xl">
	<div class="rounded-2xl border border-white/10 bg-bg-surface/50 p-6">
		<div class="flex items-center gap-5">
			<img src={userProfile.avatar} alt="" class="h-20 w-20 rounded-full border-2 border-primary-500/30 bg-bg-card" />
			<div class="flex-1">
				<h1 class="text-2xl font-bold">{userProfile.name}</h1>
				<p class="text-sm text-text-muted">Lv. {userProfile.level} · Creator</p>
				<div class="mt-3">
					<div class="mb-1 flex justify-between text-xs text-text-muted">
						<span>경험치</span>
						<span>{userProfile.xp}%</span>
					</div>
					<div class="h-2 rounded-full bg-bg-card">
						<div class="h-full rounded-full bg-primary-500" style="width: {userProfile.xp}%"></div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<div class="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
		{#each [
			{ label: '제작 캐릭터', value: userProfile.stats.charactersCreated },
			{ label: '제작 세계관', value: userProfile.stats.worldsCreated },
			{ label: '총 대화', value: userProfile.stats.totalChats },
			{ label: '저장 기억', value: userProfile.stats.savedMemories }
		] as stat}
			<div class="rounded-xl border border-white/10 bg-bg-surface/40 p-4 text-center">
				<p class="text-xl font-bold">{stat.value}</p>
				<p class="mt-1 text-xs text-text-muted">{stat.label}</p>
			</div>
		{/each}
	</div>

	<nav class="mt-6 space-y-1">
		{#each menu as item}
			<a
				href={item.href}
				class="flex items-center gap-3 rounded-xl border border-transparent px-4 py-3 transition hover:border-white/10 hover:bg-bg-surface/40"
			>
				<item.icon class="h-4 w-4 text-text-muted" />
				<span class="flex-1 text-sm">{item.label}</span>
				{#if item.phase}
					<span class="text-[10px] text-text-muted">P{item.phase}</span>
				{/if}
				<ChevronRight class="h-4 w-4 text-text-muted" />
			</a>
		{/each}
	</nav>

	<div class="mt-6">
		<Button href="/login" variant="ghost">로그아웃</Button>
	</div>
</div>
