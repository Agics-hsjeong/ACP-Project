<script lang="ts">
	import {
		getCatalogMemories,
		getCatalogMemoryStats,
		getMemoryTopTags
	} from '$lib/stores/catalog.svelte';
	import MemoryCard from '$lib/components/memory/MemoryCard.svelte';
	import MemoryDetailPanel from '$lib/components/memory/MemoryDetailPanel.svelte';
	import MemoryFidelityGauge from '$lib/components/memory/MemoryFidelityGauge.svelte';
	import MemoryTagPanel from '$lib/components/memory/MemoryTagPanel.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import SearchBar from '$lib/components/ui/SearchBar.svelte';
	import { Plus } from 'lucide-svelte';

	const memories = $derived(getCatalogMemories());
	const memoryStats = $derived(getCatalogMemoryStats());
	const memoryTopTags = $derived(getMemoryTopTags());
	const memoryFidelity = $derived(memoryStats.fidelity);

	let selectedId = $state('');
	let query = $state('');
	let importanceFilter = $state<'all' | 'high' | 'medium' | 'low'>('all');
	let tagFilter = $state('');

	$effect(() => {
		if (!selectedId && memories.length) selectedId = memories[0].id;
	});

	const selected = $derived(memories.find((m) => m.id === selectedId) ?? null);
	const filtered = $derived(
		memories.filter((m) => {
			if (importanceFilter !== 'all' && m.importance !== importanceFilter) return false;
			if (tagFilter && !m.tags?.some((t) => t.includes(tagFilter.replace('#', '')))) return false;
			if (
				query &&
				!m.title.includes(query) &&
				!m.summary.includes(query) &&
				!m.tags?.some((t) => t.includes(query))
			)
				return false;
			return true;
		})
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
		{ label: '스토리 분량', value: memoryStats.storyVolume }
	] as stat}
		<div class="rounded-xl border border-white/10 bg-bg-surface/50 p-4">
			<p class="text-xs text-text-muted">{stat.label}</p>
			<p class="mt-1 text-2xl font-bold">{stat.value}</p>
		</div>
	{/each}
</div>

<div class="mb-4 flex flex-wrap items-center gap-3">
	<div class="max-w-md flex-1">
		<SearchBar bind:value={query} placeholder="기억 검색..." />
	</div>
	<select
		bind:value={importanceFilter}
		class="h-11 rounded-xl border border-white/10 bg-bg-primary/60 px-3 text-sm outline-none"
	>
		<option value="all">전체 중요도</option>
		<option value="high">중요</option>
		<option value="medium">보통</option>
		<option value="low">낮음</option>
	</select>
	{#if tagFilter}
		<button
			type="button"
			class="text-xs text-primary-400 hover:underline"
			onclick={() => (tagFilter = '')}
		>
			태그 필터 해제 ({tagFilter})
		</button>
	{/if}
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
			{:else}
				<p class="py-12 text-center text-sm text-text-muted">조건에 맞는 기억이 없습니다.</p>
			{/each}
		</div>
	</div>

	<aside class="hidden w-72 shrink-0 space-y-4 xl:block">
		<MemoryFidelityGauge value={memoryFidelity} />
		<MemoryTagPanel
			tags={memoryTopTags}
			{memories}
			activeTag={tagFilter}
			onselect={(tag) => (tagFilter = tagFilter === tag ? '' : tag)}
		/>
		<MemoryDetailPanel memory={selected} />
	</aside>
</div>

<!-- 모바일: 상세 패널 하단 -->
<div class="mt-6 xl:hidden">
	<MemoryDetailPanel memory={selected} />
</div>
