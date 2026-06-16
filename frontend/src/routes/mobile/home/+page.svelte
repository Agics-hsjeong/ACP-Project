<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
	import WorldCard from '$lib/components/cards/WorldCard.svelte';
	import {
		getCatalogCharacters,
		getCatalogWorlds,
		getCatalogRecentChats,
		getDailyQuests
	} from '$lib/stores/catalog.svelte';
	import { MessageCircle, Sparkles, Target } from 'lucide-svelte';

	const characters = $derived(getCatalogCharacters());
	const worlds = $derived(getCatalogWorlds());
	const recentChats = $derived(getCatalogRecentChats());
	const dailyQuests = $derived(getDailyQuests());
	const featured = $derived(characters[0]);
</script>

<svelte:head>
	<title>홈 — Mobile</title>
</svelte:head>

<header class="flex items-center gap-2 border-b border-white/10 px-4 py-3">
	<Sparkles class="h-4 w-4 text-primary-400" />
	<span class="text-sm font-semibold">AI Character Playground</span>
</header>

{#if featured}
	<section class="relative m-4 overflow-hidden rounded-2xl border border-white/10">
		<img src={featured.cover} alt="" class="h-40 w-full object-cover opacity-60" />
		<div class="absolute inset-0 bg-gradient-to-t from-bg-primary via-transparent to-transparent"></div>
		<div class="absolute bottom-0 p-4">
			<p class="text-xs text-primary-300">추천 캐릭터</p>
			<p class="text-lg font-bold">{featured.name}</p>
			<p class="text-xs text-text-muted">{featured.title}</p>
			<Button href="/mobile/chat/{featured.id}" size="sm" class="mt-3">
				<MessageCircle class="h-3.5 w-3.5" />
				대화 시작
			</Button>
		</div>
	</section>
{/if}

<section class="px-4">
	<h2 class="mb-3 text-sm font-semibold">최근 대화</h2>
	<div class="space-y-2">
		{#each recentChats.slice(0, 4) as chat}
			<a href="/mobile/chat/{chat.id}" class="flex items-center gap-3 rounded-xl border border-white/10 p-3">
				<img src={chat.avatar} alt="" class="h-10 w-10 rounded-full bg-bg-card" />
				<div class="min-w-0 flex-1">
					<p class="text-sm font-medium">{chat.name}</p>
					<p class="truncate text-xs text-text-muted">{chat.preview}</p>
				</div>
			</a>
		{/each}
	</div>
</section>

<section class="mt-6 px-4">
	<h2 class="mb-3 text-sm font-semibold">세계관</h2>
	<div class="flex gap-3 overflow-x-auto pb-2">
		{#each worlds as world}
			<WorldCard {world} compact />
		{/each}
	</div>
</section>

<section class="m-4 rounded-2xl border border-white/10 bg-bg-surface/50 p-4">
	<h2 class="mb-3 flex items-center gap-2 text-sm font-semibold">
		<Target class="h-4 w-4 text-accent-gold" />
		데일리 퀘스트
	</h2>
	{#each dailyQuests as quest}
		<div class="mb-2 rounded-lg border border-white/10 p-2 text-xs">
			<p>{quest.title} — {quest.progress}/{quest.total}</p>
		</div>
	{/each}
</section>
