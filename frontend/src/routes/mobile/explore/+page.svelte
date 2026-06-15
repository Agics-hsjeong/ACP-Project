<script lang="ts">
	import { characters, exploreGenres } from '$lib/data/mock';
	import SearchBar from '$lib/components/ui/SearchBar.svelte';
	let genre = $state('전체');
	let query = $state('');

	const filtered = $derived(
		characters.filter(
			(c) =>
				(genre === '전체' || c.genre?.includes(genre) || c.tags.some((t) => t.includes(genre))) &&
				(!query || c.name.includes(query) || c.world.includes(query))
		)
	);
</script>

<svelte:head>
	<title>탐색 — Mobile</title>
</svelte:head>

<div class="border-b border-white/10 p-4">
	<h1 class="text-lg font-bold">캐릭터 탐색</h1>
	<SearchBar bind:value={query} class="mt-3" placeholder="캐릭터 검색..." />
</div>

<div class="flex gap-2 overflow-x-auto px-4 py-3">
	{#each exploreGenres.slice(0, 6) as g}
		<button
			class="shrink-0 rounded-full px-3 py-1 text-xs {genre === g
				? 'bg-primary-600 text-white'
				: 'bg-bg-surface text-text-muted'}"
			onclick={() => (genre = g)}
		>
			{g}
		</button>
	{/each}
</div>

<div class="grid grid-cols-2 gap-3 px-4 pb-4">
	{#each filtered as c}
		<a href="/mobile/characters/{c.id}" class="overflow-hidden rounded-xl border border-white/10 bg-bg-surface/60">
			<img src={c.avatar} alt="" class="aspect-square w-full object-cover" />
			<div class="p-2.5">
				<p class="truncate text-sm font-medium">{c.name}</p>
				<p class="truncate text-[10px] text-text-muted">{c.title}</p>
				<p class="mt-1 text-[10px] text-accent-pink">♥ {c.likes}%</p>
			</div>
		</a>
	{/each}
</div>
