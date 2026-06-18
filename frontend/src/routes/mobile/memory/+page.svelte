<script lang="ts">
	import {
		getCatalogMemories,
		getCatalogMemoryStats,
		getMemoryTopTags,
		getCatalogCharacters,
		refreshMemories
	} from '$lib/stores/catalog.svelte';
	import MemoryCard from '$lib/components/memory/MemoryCard.svelte';
	import MemoryDetailPanel from '$lib/components/memory/MemoryDetailPanel.svelte';
	import MemoryFidelityGauge from '$lib/components/memory/MemoryFidelityGauge.svelte';

	const memories = $derived(getCatalogMemories());
	const memoryStats = $derived(getCatalogMemoryStats());
	const memoryTopTags = $derived(getMemoryTopTags());
	const memoryFidelity = $derived(memoryStats.fidelity);
	const characters = $derived(getCatalogCharacters());

	let characterId = $state('elia');
	let selectedId = $state('');

	const activeCharacter = $derived(characters.find((c) => c.id === characterId));

	$effect(() => {
		void refreshMemories(characterId);
	});

	$effect(() => {
		if (!selectedId && memories.length) selectedId = memories[0].id;
	});

	const selected = $derived(memories.find((m) => m.id === selectedId) ?? null);
</script>

<svelte:head>
	<title>기억 — Mobile</title>
</svelte:head>

<div class="border-b border-white/10 p-4">
	<h1 class="text-lg font-bold">기억 보관소</h1>
	<p class="text-xs text-text-muted">{activeCharacter?.name ?? '캐릭터'} · Episodic Memory</p>
	<select
		bind:value={characterId}
		class="mt-2 h-9 w-full rounded-lg border border-white/10 bg-bg-primary/60 px-3 text-xs outline-none focus:border-primary-500"
	>
		{#each characters as c}
			<option value={c.id}>{c.name}</option>
		{/each}
	</select>
</div>

<div class="p-4">
	<MemoryFidelityGauge value={memoryFidelity} />
	<div class="mt-3 flex flex-wrap gap-2">
		{#each memoryTopTags.slice(0, 3) as tag}
			<span class="rounded-full bg-primary-600/20 px-2 py-1 text-[10px] text-primary-300">{tag.tag}</span>
		{/each}
	</div>
</div>

<div class="space-y-3 px-4 pb-4">
	{#each memories as memory}
		<MemoryCard
			{memory}
			selected={selectedId === memory.id}
			onclick={() => (selectedId = memory.id)}
		/>
	{/each}
</div>

{#if selected}
	<div class="border-t border-white/10 p-4">
		<MemoryDetailPanel memory={selected} />
	</div>
{/if}
