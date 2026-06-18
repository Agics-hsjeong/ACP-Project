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
	import MemorySidebar from '$lib/components/memory/MemorySidebar.svelte';
	import MockPanel from '$lib/components/mockup/MockPanel.svelte';
	import StatCard from '$lib/components/ui/StatCard.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import SearchBar from '$lib/components/ui/SearchBar.svelte';
	import { Brain, Calendar, Heart, Plus, BookOpen, Info } from 'lucide-svelte';

	const memories = $derived(getCatalogMemories());
	const memoryStats = $derived(getCatalogMemoryStats());
	const memoryTopTags = $derived(getMemoryTopTags());
	const characters = $derived(getCatalogCharacters());

	let selectedId = $state('');
	let characterId = $state('elia');
	let query = $state('');
	let importanceFilter = $state<'all' | 'high' | 'medium' | 'low'>('all');
	let tagFilter = $state('');
	let importantOnly = $state(false);
	let viewMode = $state<'timeline' | 'card'>('timeline');

	$effect(() => {
		void refreshMemories(characterId);
	});

	const activeCharacter = $derived(characters.find((c) => c.id === characterId));

	$effect(() => {
		if (!selectedId && memories.length) selectedId = memories[0].id;
	});

	const selected = $derived(memories.find((m) => m.id === selectedId) ?? null);
	const filtered = $derived(
		memories.filter((m) => {
			if (importantOnly && m.importance !== 'high') return false;
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

<div class="flex gap-5">
	<MemorySidebar
		fidelity={memoryStats.fidelity}
		topTags={memoryTopTags}
		memories={filtered}
		activeTag={tagFilter}
		onselectTag={(tag) => (tagFilter = tagFilter === tag ? '' : tag)}
	/>

	<div class="min-w-0 flex-1">
		<div class="mb-5 flex flex-wrap items-end justify-between gap-4">
			<div>
				<h1 class="flex items-center gap-2 text-2xl font-bold">
					기억 보관소
					<Info class="h-4 w-4 text-text-muted" />
				</h1>
				<p class="mt-1 text-sm text-text-muted">
					{activeCharacter?.name ?? '캐릭터'}와의 모든 기억이 시간순으로 정리됩니다
				</p>
			</div>
			<div class="flex flex-wrap items-center gap-2">
				<select
					bind:value={characterId}
					class="h-9 rounded-xl border border-[#333847] bg-[#1a1c26] px-3 text-sm outline-none focus:border-[#8c5cfa]"
				>
					{#each characters as c}
						<option value={c.id}>{c.name}</option>
					{/each}
				</select>
				<Button size="sm" variant="secondary">
					<Plus class="h-4 w-4" />
					새 기억 저장
				</Button>
			</div>
		</div>

		<div class="mb-5 grid grid-cols-2 gap-3 lg:grid-cols-4">
			<StatCard label="총 기억" value={memoryStats.total}>
				{#snippet icon()}<Brain class="h-4 w-4" />{/snippet}
			</StatCard>
			<StatCard label="중요 기억" value={memoryStats.important}>
				{#snippet icon()}<Heart class="h-4 w-4 text-[#f26699]" />{/snippet}
			</StatCard>
			<StatCard label="함께한 시간" value="{memoryStats.daysTogether}일">
				{#snippet icon()}<Calendar class="h-4 w-4" />{/snippet}
			</StatCard>
			<StatCard label="스토리 분량" value={memoryStats.storyVolume}>
				{#snippet icon()}<BookOpen class="h-4 w-4" />{/snippet}
			</StatCard>
		</div>

		<div class="mb-4 flex flex-wrap items-center gap-3 border-b border-[#333847] pb-4">
			<div class="flex gap-1 rounded-lg border border-[#333847] bg-[#1a1c26] p-1">
				<button
					type="button"
					class="rounded-md px-3 py-1.5 text-xs font-medium transition {viewMode === 'timeline'
						? 'bg-[#8c5cfa]/25 text-[#c4b5fd]'
						: 'text-text-muted hover:text-text-primary'}"
					onclick={() => (viewMode = 'timeline')}
				>
					타임라인 뷰
				</button>
				<button
					type="button"
					class="rounded-md px-3 py-1.5 text-xs font-medium transition {viewMode === 'card'
						? 'bg-[#8c5cfa]/25 text-[#c4b5fd]'
						: 'text-text-muted hover:text-text-primary'}"
					onclick={() => (viewMode = 'card')}
				>
					카드 뷰
				</button>
			</div>
			<div class="max-w-sm flex-1">
				<SearchBar bind:value={query} placeholder="기억 검색..." />
			</div>
			<select
				bind:value={importanceFilter}
				class="h-9 rounded-xl border border-[#333847] bg-[#1a1c26] px-3 text-sm outline-none"
			>
				<option value="all">전체 중요도</option>
				<option value="high">중요</option>
				<option value="medium">보통</option>
				<option value="low">일반</option>
			</select>
			<label class="flex cursor-pointer items-center gap-2 text-xs text-text-secondary">
				<input type="checkbox" bind:checked={importantOnly} class="accent-[#8c5cfa]" />
				중요 기억만
			</label>
			{#if tagFilter}
				<button
					type="button"
					class="text-xs text-[#8c5cfa] hover:underline"
					onclick={() => (tagFilter = '')}
				>
					#{tagFilter} 해제
				</button>
			{/if}
		</div>

		{#if viewMode === 'timeline'}
			<div class="relative space-y-4">
				<div
					class="absolute left-4 top-0 h-full w-px bg-gradient-to-b from-[#8c5cfa]/50 via-[#333847] to-transparent"
				></div>
				{#each filtered as memory}
					<div class="relative pl-10">
						<div
							class="absolute left-2.5 top-8 z-10 h-3 w-3 -translate-x-1/2 rounded-full border-2 {memory.importance ===
							'high'
								? 'border-[#f59e0b] bg-[#f59e0b]'
								: 'border-[#8c5cfa] bg-[#1a1c26]'}"
						></div>
						<p class="mb-1.5 pl-1 text-[10px] font-medium text-text-muted">{memory.date}</p>
						<MemoryCard
							{memory}
							selected={selectedId === memory.id}
							onclick={() => (selectedId = memory.id)}
						/>
					</div>
				{:else}
					<p class="py-16 text-center text-sm text-text-muted">조건에 맞는 기억이 없습니다.</p>
				{/each}
			</div>
		{:else}
			<div class="grid gap-4 sm:grid-cols-2">
				{#each filtered as memory}
					<MemoryCard
						{memory}
						compact
						selected={selectedId === memory.id}
						onclick={() => (selectedId = memory.id)}
					/>
				{:else}
					<p class="col-span-2 py-16 text-center text-sm text-text-muted">조건에 맞는 기억이 없습니다.</p>
				{/each}
			</div>
		{/if}
	</div>

	<aside class="hidden w-80 shrink-0 xl:block">
		<div class="sticky top-6">
			<p class="mb-3 text-xs font-semibold text-text-muted">선택된 기억 상세</p>
			<MockPanel class="!p-0 overflow-hidden">
				<MemoryDetailPanel memory={selected} />
			</MockPanel>
		</div>
	</aside>
</div>

<div class="mt-6 xl:hidden">
	<p class="mb-3 text-xs font-semibold text-text-muted">선택된 기억 상세</p>
	<MockPanel class="!p-0 overflow-hidden">
		<MemoryDetailPanel memory={selected} />
	</MockPanel>
</div>
