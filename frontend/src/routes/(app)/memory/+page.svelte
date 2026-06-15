<script lang="ts">
	import { memories, memoryStats } from '$lib/data/mock';
	import MemoryCard from '$lib/components/memory/MemoryCard.svelte';
	import MemoryDetailPanel from '$lib/components/memory/MemoryDetailPanel.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import SearchBar from '$lib/components/ui/SearchBar.svelte';
	import { Plus } from 'lucide-svelte';

	let selectedId = $state(memories[0]?.id ?? '');
	let query = $state('');

	const selected = $derived(memories.find((m) => m.id === selectedId) ?? null);
	const filtered = $derived(
		memories.filter(
			(m) =>
				!query ||
				m.title.includes(query) ||
				m.summary.includes(query) ||
				m.tags?.some((t) => t.includes(query))
		)
	);
</script>

<svelte:head>
	<title>기억 보관소 — ACP</title>
</svelte:head>

<div class="mb-6 flex flex-wrap items-end justify-between gap-4">
	<div>
		<h1 class="text-2xl font-bold">기억 보관소</h1>
		<p class="mt-1 text-sm text-text-muted">Episodic Memory Timeline — 엘리아와의 추억</p>
	</div>
	<Button size="sm">
		<Plus class="h-4 w-4" />
		새 기억 저장
	</Button>
</div>

<div class="mb-6 grid grid-cols-2 gap-3 lg:grid-cols-4">
	{#each [
		{ label: '총 기억', value: memoryStats.total },
		{ label: '중요 기억', value: memoryStats.important },
		{ label: '함께한 시간', value: `${memoryStats.daysTogether}일` },
		{ label: '스토리 분량', value: `${memoryStats.storyVolume}자` }
	] as stat}
		<div class="rounded-xl border border-white/10 bg-bg-surface/50 p-4">
			<p class="text-xs text-text-muted">{stat.label}</p>
			<p class="mt-1 text-2xl font-bold">{stat.value}</p>
		</div>
	{/each}
</div>

<div class="mb-4 max-w-md">
	<SearchBar bind:value={query} placeholder="기억 검색..." />
</div>

<div class="flex gap-6">
	<div class="relative min-w-0 flex-1">
		<div class="absolute left-4 top-0 h-full w-px bg-white/10"></div>
		<div class="space-y-4">
			{#each filtered as memory}
				<div class="relative pl-10">
					<div
						class="absolute left-2.5 top-6 h-3 w-3 -translate-x-1/2 rounded-full border-2 {memory.importance ===
						'high'
							? 'border-accent-gold bg-accent-gold'
							: 'border-primary-500 bg-bg-primary'}"
					></div>
					<MemoryCard
						{memory}
						selected={selectedId === memory.id}
						onclick={() => (selectedId = memory.id)}
					/>
				</div>
			{/each}
		</div>
	</div>
	<MemoryDetailPanel memory={selected} />
</div>
