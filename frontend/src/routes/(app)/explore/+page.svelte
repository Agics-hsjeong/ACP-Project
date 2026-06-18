<script lang="ts">
	import { page } from '$app/stores';
	import ScreenSearchBar from '$lib/components/mockup/ScreenSearchBar.svelte';
	import MockSectionHeader from '$lib/components/mockup/MockSectionHeader.svelte';
	import CharacterPortraitCard from '$lib/components/mockup/CharacterPortraitCard.svelte';
	import WorldStripCard from '$lib/components/mockup/WorldStripCard.svelte';
	import ExploreHelpPanel from '$lib/components/mockup/ExploreHelpPanel.svelte';
	import ExploreFilterPanel from '$lib/components/explore/ExploreFilterPanel.svelte';
	import { getCatalogCharacters, getCatalogWorlds } from '$lib/stores/catalog.svelte';
	import { getExploreGenres } from '$lib/stores/meta.svelte';
	import { getSearchQuery } from '$lib/stores/search.svelte';
	import { ChevronDown } from 'lucide-svelte';

	let genre = $state('전체');
	let sort = $state('popular');
	let gender = $state('all');
	let world = $state('all');
	let selectedTags = $state<string[]>([]);
	let searchInput = $state('');
	let showFilters = $state(false);

	const urlQuery = $derived($page.url.searchParams.get('q') ?? getSearchQuery());

	const catalogCharacters = $derived(getCatalogCharacters());
	const catalogWorlds = $derived(getCatalogWorlds());
	const exploreGenres = $derived(getExploreGenres());

	const filtered = $derived.by(() => {
		let list = [...catalogCharacters];
		const q = (searchInput || urlQuery).toLowerCase();

		if (q) {
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

		if (world !== 'all') {
			list = list.filter((c) => c.worldId === world || c.world.toLowerCase().includes(world));
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

	const recommended = $derived(filtered.slice(0, 6));
	const newCharacters = $derived([...catalogCharacters].reverse().slice(0, 4));
	const popularWorlds = $derived(catalogWorlds.slice(0, 5));

	const sortLabel = $derived(
		sort === 'latest' ? '최신순' : sort === 'likes' ? '호감도순' : '인기순'
	);

	const activeFilters = $derived.by(() => {
		const chips: { key: string; label: string; clear: () => void }[] = [];
		if (genre !== '전체') chips.push({ key: 'genre', label: genre, clear: () => (genre = '전체') });
		if (gender !== 'all')
			chips.push({
				key: 'gender',
				label: gender === 'female' ? '여성' : '남성',
				clear: () => (gender = 'all')
			});
		if (world !== 'all')
			chips.push({
				key: 'world',
				label: catalogWorlds.find((w) => w.id === world)?.name ?? world,
				clear: () => (world = 'all')
			});
		for (const t of selectedTags) {
			chips.push({
				key: `tag-${t}`,
				label: `#${t}`,
				clear: () => (selectedTags = selectedTags.filter((x) => x !== t))
			});
		}
		return chips;
	});

	function resetAllFilters() {
		genre = '전체';
		sort = 'popular';
		gender = 'all';
		world = 'all';
		selectedTags = [];
	}

	function handleTagClick(tag: string) {
		selectedTags = selectedTags.includes(tag)
			? selectedTags.filter((t) => t !== tag)
			: [...selectedTags, tag];
	}

	function cycleSort() {
		sort = sort === 'popular' ? 'latest' : sort === 'latest' ? 'likes' : 'popular';
	}
</script>

<svelte:head>
	<title>캐릭터 탐색 — ACP</title>
</svelte:head>

<div class="-m-2 min-h-full bg-mock-bg p-2 lg:-m-4 lg:p-4">
	<div class="mb-1 flex items-start justify-between gap-4">
		<div class="min-w-0 flex-1">
			<ScreenSearchBar bind:value={searchInput} placeholder="캐릭터, 세계관, 태그 검색…" />
		</div>
		<div class="hidden shrink-0 items-center gap-2 pt-1 sm:flex">
			<button
				type="button"
				class="rounded-lg border border-mock-border bg-mock-panel px-3 py-2 text-xs text-text-secondary transition hover:border-mock-accent/40"
				onclick={cycleSort}
			>
				{sortLabel}
			</button>
			<button
				type="button"
				class="flex items-center gap-1 rounded-lg border border-mock-border bg-mock-panel px-3 py-2 text-xs text-text-secondary transition hover:border-mock-accent/40"
				onclick={() => (showFilters = !showFilters)}
			>
				필터
				<ChevronDown class="h-3.5 w-3.5 transition {showFilters ? 'rotate-180' : ''}" />
			</button>
		</div>
	</div>

	<p class="mb-4 text-xs text-text-muted">
		{#if searchInput || urlQuery}
			「{searchInput || urlQuery}」 검색 결과 {filtered.length}명
		{:else}
			무한한 캐릭터와 이야기를 만나보세요 · {filtered.length}명
		{/if}
	</p>

	<div class="flex gap-5">
		<div class="min-w-0 flex-1 space-y-6">
			<!-- 장르 칩 -->
			<div class="flex gap-2 overflow-x-auto pb-1">
				{#each exploreGenres as g}
					<button
						type="button"
						class="shrink-0 rounded-full border px-4 py-1.5 text-sm transition {genre === g
							? 'border-mock-accent bg-mock-accent text-white'
							: 'border-mock-border bg-mock-panel text-text-secondary hover:border-mock-accent/40'}"
						onclick={() => (genre = g)}
					>
						{g}
					</button>
				{/each}
			</div>

			{#if activeFilters.length}
				<div class="flex flex-wrap items-center gap-2">
					{#each activeFilters as chip}
						<button
							type="button"
							class="inline-flex items-center gap-1 rounded-full border border-mock-accent/40 bg-mock-accent/10 px-3 py-1 text-xs text-mock-accent"
							onclick={chip.clear}
						>
							{chip.label} ×
						</button>
					{/each}
					<button type="button" class="text-xs text-text-muted hover:text-mock-accent" onclick={resetAllFilters}>
						필터 초기화
					</button>
				</div>
			{/if}

			{#if showFilters}
				<div class="max-w-xl">
					<ExploreFilterPanel bind:sort bind:gender bind:world bind:selectedTags />
				</div>
			{/if}

			<!-- 히어로 배너 -->
			<section class="relative overflow-hidden rounded-xl border border-mock-border">
				<div class="absolute inset-0 bg-gradient-to-r from-mock-bg via-mock-bg/80 to-transparent"></div>
				<img
					src={catalogWorlds[0]?.cover ?? 'https://api.dicebear.com/9.x/shapes/svg?seed=explore-banner&backgroundColor=312e81'}
					alt=""
					class="absolute inset-0 h-full w-full object-cover opacity-35"
				/>
				<div class="relative flex min-h-[180px] flex-col justify-center gap-2 p-8 md:max-w-xl">
					<p class="text-[10px] font-medium tracking-widest text-mock-accent">WORLD UPDATE</p>
					<h2 class="text-xl font-bold md:text-2xl">아르카디아 왕국 — 새로운 챕터가 열렸습니다</h2>
					<p class="text-sm text-text-secondary">
						Living World Engine이 기억하는 캐릭터와 만나보세요
					</p>
				</div>
			</section>

			<!-- 추천 캐릭터 -->
			<section>
				<MockSectionHeader title="추천 캐릭터" href="/explore" />
				<div class="flex gap-3 overflow-x-auto pb-1">
					{#each recommended as character}
						<CharacterPortraitCard {character} />
					{/each}
				</div>
			</section>

			<!-- 인기 세계관 -->
			<section>
				<MockSectionHeader title="인기 세계관" href="/explore" />
				<div class="flex gap-3 overflow-x-auto pb-1">
					{#each popularWorlds as w}
						<WorldStripCard world={w} />
					{/each}
				</div>
			</section>

			<!-- 신규 캐릭터 -->
			<section>
				<MockSectionHeader title="신규 캐릭터" href="/explore" />
				<div class="flex gap-3 overflow-x-auto pb-1">
					{#each newCharacters as character}
						<CharacterPortraitCard {character} />
					{/each}
				</div>
			</section>

			<!-- 전체 결과 -->
			<section>
				<MockSectionHeader title="전체 캐릭터" />
				<div class="flex flex-wrap gap-3">
					{#each filtered as character}
						<CharacterPortraitCard {character} />
					{:else}
						<p class="text-sm text-text-muted">조건에 맞는 캐릭터가 없습니다.</p>
					{/each}
				</div>
			</section>
		</div>

		<div class="hidden shrink-0 lg:block">
			<ExploreHelpPanel {selectedTags} ontagclick={handleTagClick} />
		</div>
	</div>
</div>
