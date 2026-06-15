<script lang="ts">
	import { memories } from '$lib/data/mock';
	import MemoryCard from '$lib/components/memory/MemoryCard.svelte';
</script>

<svelte:head>
	<title>기억 — Mobile</title>
</svelte:head>

<div class="border-b border-white/10 p-4">
	<h1 class="text-lg font-bold">기억 보관소</h1>
	<p class="text-xs text-text-muted">Episodic Memory</p>
</div>

<div class="space-y-3 p-4">
	{#each memories as memory}
		<MemoryCard {memory} />
	{/each}
</div>
