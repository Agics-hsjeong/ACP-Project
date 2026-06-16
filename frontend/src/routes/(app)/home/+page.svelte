<script lang="ts">
	import CharacterCard from '$lib/components/cards/CharacterCard.svelte';
	import WorldCard from '$lib/components/cards/WorldCard.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import {
		getCatalogCharacters,
		getCatalogWorlds,
		getCatalogRecentChats,
		getDailyQuests,
		getRecommendedStories,
		isCatalogLoading
	} from '$lib/stores/catalog.svelte';
	import { Compass, BookOpen, Target } from 'lucide-svelte';

	const characters = $derived(getCatalogCharacters());
	const worlds = $derived(getCatalogWorlds());
	const recentChats = $derived(getCatalogRecentChats());
	const recommendedStories = $derived(getRecommendedStories());
	const dailyQuests = $derived(getDailyQuests());
	const loading = $derived(isCatalogLoading());
</script>

<section class="relative mb-8 overflow-hidden rounded-2xl border border-white/10">
	<div class="absolute inset-0 bg-gradient-to-r from-primary-900/80 via-bg-surface/60 to-transparent"></div>
	<img
		src="https://api.dicebear.com/9.x/shapes/svg?seed=hero&backgroundColor=312e81"
		alt=""
		class="absolute inset-0 h-full w-full object-cover opacity-40"
	/>
	<div class="relative flex flex-col justify-center gap-4 p-8 md:max-w-lg md:p-12">
		<h2 class="text-2xl font-bold md:text-3xl">당신만의 캐릭터와 특별한 이야기를 만들어보세요</h2>
		<p class="text-sm text-text-secondary">Living World Engine이 기억하고, 감정하고, 함께 성장합니다.</p>
		<Button href="/explore" class="w-fit">
			<Compass class="h-4 w-4" />
			캐릭터 탐색하기
		</Button>
	</div>
</section>

{#if loading}
	<p class="mb-6 text-center text-sm text-text-muted">데이터를 불러오는 중…</p>
{/if}

<section class="mb-8">
	<div class="mb-4 flex items-center justify-between">
		<h2 class="text-lg font-semibold">추천 캐릭터</h2>
		<a href="/explore" class="text-sm text-primary-400 hover:underline">전체 보기</a>
	</div>
	<div class="flex gap-4 overflow-x-auto pb-2">
		{#each characters as character}
			<CharacterCard {character} />
		{:else}
			<p class="text-sm text-text-muted">등록된 캐릭터가 없습니다.</p>
		{/each}
	</div>
</section>

<section class="mb-8">
	<div class="mb-4 flex items-center justify-between">
		<h2 class="flex items-center gap-2 text-lg font-semibold">
			<BookOpen class="h-4 w-4 text-primary-400" />
			추천 스토리
		</h2>
	</div>
	<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
		{#each recommendedStories as story}
			<a
				href="/chat/{story.characterId}"
				class="group overflow-hidden rounded-2xl border border-white/10 bg-bg-surface/50 transition hover:border-primary-500/40"
			>
				<img src={story.cover} alt="" class="h-32 w-full object-cover opacity-80 group-hover:opacity-100" />
				<div class="p-4">
					<p class="text-xs text-primary-300">{story.world}</p>
					<p class="font-semibold">{story.title}</p>
					<p class="mt-1 line-clamp-2 text-xs text-text-muted">{story.summary}</p>
					<p class="mt-2 text-[10px] text-text-muted">{story.characterName} · {story.reads.toLocaleString()} 읽음</p>
				</div>
			</a>
		{/each}
	</div>
</section>

<section class="mb-8">
	<div class="mb-4 flex items-center justify-between">
		<h2 class="text-lg font-semibold">인기 세계관</h2>
		<a href="/explore" class="text-sm text-primary-400 hover:underline">전체 보기</a>
	</div>
	<div class="flex gap-4 overflow-x-auto pb-2">
		{#each worlds as world}
			<WorldCard {world} />
		{/each}
	</div>
</section>

<section class="mb-8 grid gap-6 lg:grid-cols-3">
	<div class="lg:col-span-2">
		<div class="mb-4 flex items-center justify-between">
			<h2 class="text-lg font-semibold">최근 대화</h2>
		</div>
		<div class="grid gap-3 sm:grid-cols-2">
			{#each recentChats as chat}
				<a
					href="/chat/{chat.id}"
					class="flex items-center gap-4 rounded-xl border border-white/10 bg-bg-surface/50 p-4 transition hover:border-primary-500/30"
				>
					<img
						src={chat.avatar || `https://api.dicebear.com/9.x/notionists/svg?seed=${chat.id}`}
						alt=""
						class="h-12 w-12 rounded-full bg-bg-card"
					/>
					<div class="min-w-0 flex-1">
						<p class="font-medium">{chat.name}</p>
						<p class="truncate text-sm text-text-muted">{chat.preview}</p>
					</div>
					{#if chat.time}
						<span class="text-xs text-text-muted">{chat.time}</span>
					{/if}
				</a>
			{/each}
		</div>
	</div>

	<div class="rounded-2xl border border-white/10 bg-bg-surface/50 p-5">
		<h2 class="mb-4 flex items-center gap-2 text-lg font-semibold">
			<Target class="h-4 w-4 text-accent-gold" />
			데일리 퀘스트
		</h2>
		<div class="space-y-3">
			{#each dailyQuests as quest}
				<div class="rounded-xl border border-white/10 bg-bg-primary/40 p-3">
					<div class="mb-2 flex justify-between text-sm">
						<span>{quest.title}</span>
						<span class="text-xs text-primary-300">{quest.reward}</span>
					</div>
					<div class="h-1.5 overflow-hidden rounded-full bg-bg-card">
						<div
							class="h-full rounded-full bg-primary-500"
							style="width: {(quest.progress / quest.total) * 100}%"
						></div>
					</div>
					<p class="mt-1 text-[10px] text-text-muted">{quest.progress}/{quest.total}</p>
				</div>
			{/each}
		</div>
	</div>
</section>
