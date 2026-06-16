<script lang="ts">
	import { page } from '$app/stores';
	import CharacterCard from '$lib/components/cards/CharacterCard.svelte';
	import WorldCard from '$lib/components/cards/WorldCard.svelte';
	import ExploreFilterPanel from '$lib/components/explore/ExploreFilterPanel.svelte';
	import SectionHeader from '$lib/components/ui/SectionHeader.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import { getCatalogCharacters, getCatalogWorlds } from '$lib/stores/catalog.svelte';
	import { getExploreGenres } from '$lib/stores/meta.svelte';
	import { getSearchQuery } from '$lib/stores/search.svelte';
	import { Shuffle } from 'lucide-svelte';

	let genre = $state('전체');
	let sort = $state('popular');
	let gender = $state('all');
	let selectedTags = $state<string[]>([]);

	const urlQuery = $derived($page.url.searchParams.get('q') ?? getSearchQuery());

	const catalogCharacters = $derived(getCatalogCharacters());
	const catalogWorlds = $derived(getCatalogWorlds());
	const exploreGenres = $derived(getExploreGenres());

	const filtered = $derived.by(() => {
		let list = [...catalogCharacters];

		if (urlQuery) {
			const q = urlQuery.toLowerCase();
			list = list.filter(
				(c) =>
					c.name.toLowerCase().includes(q) ||
					c.description.toLowerCase().includes(q) ||
					c.world.toLowerCase().includes(q) ||
					c.tags.some((t) => t.toLowerCase().includes(q))
			);
		}

		if (genre !== '전체') {
			list = list.filter(
				(c) =>
					c.genre?.includes(genre) ||
					c.tags.some((t) => t.includes(genre)) ||
					c.world.includes(genre)
			);
		}

		if (gender === 'female') {
			list = list.filter((c) => c.tags.includes('여성') || c.gender === '여성');
		} else if (gender === 'male') {
			list = list.filter((c) => c.tags.includes('남성') || c.gender === '남성');
		}

		if (selectedTags.length) {
			list = list.filter((c) => selectedTags.some((t) => c.tags.includes(t)));
		}

		if (sort === 'likes') {
			list.sort((a, b) => b.likes - a.likes);
		} else if (sort === 'latest') {
			list.reverse();
		} else {
			list.sort((a, b) => b.views - a.views);
		}

		return list;
	});

	const rising = $derived([...catalogCharacters].sort((a, b) => b.likes - a.likes).slice(0, 4));
</script>

<svelte:head>
	<title>캐릭터 탐색 — ACP</title>
</svelte:head>

<div class="flex gap-6">
	<div class="min-w-0 flex-1">
		<div class="mb-6">
			<h1 class="text-2xl font-bold">캐릭터 탐색</h1>
			<p class="mt-1 text-sm text-text-muted">무한한 캐릭터와 이야기를 만나보세요</p>
		</div>

		<div class="mb-6 flex gap-2 overflow-x-auto pb-1">
			{#each exploreGenres as g}
				<button
					class="shrink-0 rounded-full px-4 py-1.5 text-sm transition {genre === g
						? 'bg-primary-600 text-white'
						: 'bg-bg-surface text-text-secondary hover:bg-bg-card'}"
					onclick={() => (genre = g)}
				>
					{g}
				</button>
			{/each}
		</div>

		<section class="relative mb-8 overflow-hidden rounded-2xl border border-white/10">
			<div class="absolute inset-0 bg-gradient-to-r from-primary-900/90 via-bg-surface/70 to-transparent"></div>
			<img
				src="https://api.dicebear.com/9.x/shapes/svg?seed=explore-banner&backgroundColor=312e81"
				alt=""
				class="absolute inset-0 h-full w-full object-cover opacity-50"
			/>
			<div class="relative flex flex-col gap-3 p-8 md:max-w-xl">
				<h2 class="text-xl font-bold md:text-2xl">지금, 당신의 이야기를 시작할 캐릭터를 찾아보세요</h2>
				<p class="text-sm text-text-secondary">Living World Engine이 기억하는 캐릭터와 만나보세요</p>
				<Button href="/chat/elia" class="w-fit" size="sm">
					<Shuffle class="h-4 w-4" />
					랜덤 캐릭터 만나기
				</Button>
			</div>
		</section>

		<section class="mb-8">
			<SectionHeader title="추천 캐릭터" />
			<div class="flex gap-4 overflow-x-auto pb-2">
				{#each filtered as character}
					<CharacterCard {character} />
				{/each}
			</div>
		</section>

		<section class="mb-8">
			<SectionHeader title="급상승 인기 캐릭터" />
			<div class="grid grid-cols-2 gap-3 sm:grid-cols-4">
				{#each rising as character}
					<a
						href="/characters/{character.id}"
						class="flex items-center gap-3 rounded-xl border border-white/10 bg-bg-surface/50 p-3 transition hover:border-primary-500/30"
					>
						<img src={character.avatar} alt="" class="h-12 w-12 rounded-full bg-bg-card" />
						<div class="min-w-0">
							<p class="truncate font-medium">{character.name}</p>
							<p class="text-xs text-accent-pink">♥ {character.likes}%</p>
						</div>
					</a>
				{/each}
			</div>
		</section>

		<section class="mb-8">
			<SectionHeader title="인기 세계관" href="/explore" />
			<div class="flex gap-4 overflow-x-auto pb-2">
				{#each catalogWorlds as world}
					<WorldCard {world} />
				{/each}
			</div>
		</section>

		<section>
			<SectionHeader title="전체 캐릭터" />
			<div class="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 xl:grid-cols-3">
				{#each filtered as character}
					<CharacterCard {character} />
				{/each}
			</div>
		</section>
	</div>

	<div class="hidden w-72 shrink-0 xl:block">
		<ExploreFilterPanel bind:sort bind:gender bind:selectedTags />
	</div>
</div>
