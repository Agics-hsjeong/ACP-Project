<script lang="ts">
	import RelationshipGraph from '$lib/components/relationship/RelationshipGraph.svelte';
	import RelationshipDetailPanel from '$lib/components/relationship/RelationshipDetailPanel.svelte';
	import RelationshipLegend from '$lib/components/relationship/RelationshipLegend.svelte';
	import MockPanel from '$lib/components/mockup/MockPanel.svelte';
	import { type RelationType } from '$lib/data/relationship';
	import { initRelationship, getRelationshipGraph } from '$lib/stores/relationship.svelte';
	import { Filter, Maximize2, Shuffle } from 'lucide-svelte';

	let selectedId = $state('elia');
	let query = $state('');
	let worldId = $state('');
	let showFilter = $state(false);
	let toast = $state('');
	let showCharacters = $state(true);
	let showPlaces = $state(true);
	let showFactions = $state(true);
	let showEvents = $state(true);
	let activeTypes = $state<RelationType[]>([
		'friend',
		'alliance',
		'enemy',
		'lover',
		'family',
		'ex_lover',
		'neutral'
	]);

	const graphData = $derived(getRelationshipGraph());
	const graphNodes = $derived(graphData.nodes);
	const graphEdges = $derived(graphData.edges);
	const worlds = $derived(graphData.worlds);

	$effect(() => {
		if (!worldId && worlds.length) worldId = worlds[0].id;
	});

	$effect(() => {
		const w = worldId;
		if (!w) return;
		void initRelationship({ world: w, center: selectedId }).then((g) => {
			if (!g) return;
			if (!g.nodes.some((n) => n.id === selectedId)) {
				const first = g.nodes.find((n) => n.kind === 'character');
				if (first) selectedId = first.id;
			}
		});
	});

	const filteredNodes = $derived.by(() => {
		return graphNodes.filter((n) => {
			const nodeWorld = n.worldId ?? worlds[0]?.id;
			if (worldId && nodeWorld !== worldId) return false;
			if (n.kind === 'character' && !showCharacters) return false;
			if (n.kind === 'location' && !showPlaces) return false;
			if (n.kind === 'faction' && !showFactions) return false;
			if (n.kind === 'event' && !showEvents) return false;
			if (query && !n.label.includes(query) && !n.subtitle?.includes(query)) return false;
			return true;
		});
	});

	const filteredEdges = $derived.by(() => {
		const ids = new Set(filteredNodes.map((n) => n.id));
		return graphEdges.filter(
			(e) => activeTypes.includes(e.type) && ids.has(e.source) && ids.has(e.target)
		);
	});

	const visibleNodes = $derived.by(() => {
		const connected = new Set<string>();
		for (const e of filteredEdges) {
			connected.add(e.source);
			connected.add(e.target);
		}
		return filteredNodes.filter((n) => {
			if (n.kind === 'character') return true;
			return n.isCenter || connected.has(n.id);
		});
	});
</script>

<svelte:head>
	<title>인물 관계도 — ACP</title>
</svelte:head>

<div class="flex h-[calc(100dvh-0px)] min-h-[600px] gap-0 lg:h-[calc(100vh-0px)]">
	<div class="flex min-w-0 flex-1 flex-col">
		<header class="flex flex-wrap items-center gap-3 border-b border-[#333847] px-5 py-4">
			<h1 class="text-lg font-bold">
				인물 관계도
				<span class="text-sm font-normal text-text-muted">ⓘ</span>
			</h1>
			<p class="text-xs text-text-muted">
				{worlds.find((w) => w.id === worldId)?.name ?? ''}
			</p>
			<div class="ml-auto flex items-center gap-2">
				<button
					type="button"
					class="flex items-center gap-1.5 rounded-lg border border-[#333847] bg-[#1a1c26] px-3 py-1.5 text-xs text-text-secondary hover:bg-white/5"
					onclick={() => {
						toast = '노드가 자동 정렬되었습니다';
						setTimeout(() => (toast = ''), 2000);
					}}
				>
					<Shuffle class="h-3.5 w-3.5" />
					자동정렬
				</button>
				<button
					type="button"
					class="flex items-center gap-1.5 rounded-lg border border-[#333847] bg-[#1a1c26] px-3 py-1.5 text-xs text-text-secondary hover:bg-white/5 {showFilter
						? 'border-[#8c5cfa]/50 text-[#c4b5fd]'
						: ''}"
					onclick={() => (showFilter = !showFilter)}
				>
					<Filter class="h-3.5 w-3.5" />
					필터
				</button>
				<button
					type="button"
					class="flex items-center gap-1.5 rounded-lg border border-[#333847] bg-[#1a1c26] px-3 py-1.5 text-xs text-text-secondary hover:bg-white/5"
					onclick={() => {
						toast = '전체화면 모드는 준비 중입니다';
						setTimeout(() => (toast = ''), 2000);
					}}
				>
					<Maximize2 class="h-3.5 w-3.5" />
					전체화면
				</button>
			</div>
			{#if toast}
				<p class="w-full text-center text-xs text-[#33b266]">{toast}</p>
			{/if}
		</header>

		{#if showFilter}
			<div class="border-b border-[#333847] px-5 py-3">
				<div class="flex flex-wrap items-center gap-3">
					<select
						bind:value={worldId}
						class="h-8 rounded-lg border border-[#333847] bg-[#1a1c26] px-2 text-xs outline-none"
					>
						{#each worlds as w}
							<option value={w.id}>{w.name}</option>
						{/each}
					</select>
					<input
						bind:value={query}
						placeholder="캐릭터 검색..."
						class="h-8 flex-1 max-w-xs rounded-lg border border-[#333847] bg-[#1a1c26] px-3 text-xs outline-none focus:border-[#8c5cfa]"
					/>
					<label class="flex items-center gap-1.5 text-xs text-text-muted">
						<input type="checkbox" bind:checked={showCharacters} class="accent-[#8c5cfa]" />
						캐릭터
					</label>
					<label class="flex items-center gap-1.5 text-xs text-text-muted">
						<input type="checkbox" bind:checked={showPlaces} class="accent-[#8c5cfa]" />
						장소
					</label>
				</div>
			</div>
		{/if}

		<div class="border-b border-[#333847] px-5 py-2">
			<RelationshipLegend />
		</div>

		<div class="relative min-h-0 flex-1 p-4">
			<MockPanel padding={false} class="h-full overflow-hidden">
				{#if visibleNodes.length === 0}
					<div class="flex h-full min-h-[400px] items-center justify-center text-sm text-text-muted">
						이 세계관의 관계 데이터가 아직 없습니다
					</div>
				{:else}
					<RelationshipGraph
						nodes={visibleNodes}
						edges={filteredEdges}
						{selectedId}
						onselect={(id) => (selectedId = id)}
					/>
				{/if}
			</MockPanel>
		</div>
	</div>

	<aside class="hidden w-80 shrink-0 border-l border-[#333847] bg-[#0a0a14] xl:flex xl:flex-col">
		<div class="flex-1 overflow-y-auto p-4">
			<MockPanel class="h-full">
				<RelationshipDetailPanel nodeId={selectedId} embedded />
			</MockPanel>
		</div>
	</aside>
</div>
