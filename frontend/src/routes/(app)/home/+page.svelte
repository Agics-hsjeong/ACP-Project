<script lang="ts">
	import CharacterCard from '$lib/components/cards/CharacterCard.svelte';
	import WorldCard from '$lib/components/cards/WorldCard.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import { characters, worlds } from '$lib/data/mock';
	import { Compass } from 'lucide-svelte';
</script>

<!-- Hero Banner -->
<section class="relative mb-8 overflow-hidden rounded-2xl border border-white/10">
	<div class="absolute inset-0 bg-gradient-to-r from-primary-900/80 via-bg-surface/60 to-transparent"></div>
	<img
		src="https://api.dicebear.com/9.x/shapes/svg?seed=hero&backgroundColor=312e81"
		alt=""
		class="absolute inset-0 h-full w-full object-cover opacity-40"
	/>
	<div class="relative flex flex-col justify-center gap-4 p-8 md:p-12 md:max-w-lg">
		<h2 class="text-2xl font-bold md:text-3xl">당신만의 캐릭터와 특별한 이야기를 만들어보세요</h2>
		<p class="text-sm text-text-secondary">Living World Engine이 기억하고, 감정하고, 함께 성장합니다.</p>
		<Button href="/explore" class="w-fit">
			<Compass class="h-4 w-4" />
			캐릭터 탐색하기
		</Button>
	</div>
</section>

<!-- Recommended Characters -->
<section class="mb-8">
	<div class="mb-4 flex items-center justify-between">
		<h2 class="text-lg font-semibold">추천 캐릭터</h2>
		<a href="/explore" class="text-sm text-primary-400 hover:underline">전체 보기</a>
	</div>
	<div class="flex gap-4 overflow-x-auto pb-2">
		{#each characters as character}
			<CharacterCard {character} />
		{/each}
	</div>
</section>

<!-- Popular Worlds -->
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

<!-- Phase 1: Recent Sessions (simplified) -->
<section>
	<div class="mb-4 flex items-center justify-between">
		<h2 class="text-lg font-semibold">최근 대화</h2>
	</div>
	<div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
		{#each characters.slice(0, 3) as character}
			<a
				href="/chat/{character.id}"
				class="flex items-center gap-4 rounded-xl border border-white/10 bg-bg-surface/50 p-4 transition hover:border-primary-500/30"
			>
				<img src={character.avatar} alt="" class="h-12 w-12 rounded-full bg-bg-card" />
				<div class="min-w-0 flex-1">
					<p class="font-medium">{character.name}</p>
					<p class="truncate text-sm text-text-muted">{character.world}</p>
				</div>
				<span class="text-xs text-primary-400">이어하기 →</span>
			</a>
		{/each}
	</div>
</section>
