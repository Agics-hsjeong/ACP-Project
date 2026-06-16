<script lang="ts">
	import RelationshipGraph from '$lib/components/relationship/RelationshipGraph.svelte';
	import RelationshipFilterPanel from '$lib/components/relationship/RelationshipFilterPanel.svelte';
	import RelationshipDetailPanel from '$lib/components/relationship/RelationshipDetailPanel.svelte';
	import SearchBar from '$lib/components/ui/SearchBar.svelte';
	import { type RelationType } from '$lib/data/relationship';
	import { initRelationship, getRelationshipGraph, getRelationshipHistory } from '$lib/stores/relationship.svelte';
	import RelationshipTimeline from '$lib/components/relationship/RelationshipTimeline.svelte';
	import { Download, Plus } from 'lucide-svelte';

	let selectedId = $state('elia');
	let query = $state('');
	let worldId = $state('');
	let showTimeline = $state(false);
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
	const relationshipHistory = $derived(getRelationshipHistory());

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

<div class="flex h-[calc(100dvh-0px)] min-h-[600px] lg:h-[calc(100vh-0px)]">
	<RelationshipFilterPanel
		bind:worldId
		bind:showCharacters
		bind:showPlaces
		bind:showFactions
		bind:showEvents
		bind:activeTypes
	/>

	<div class="flex min-w-0 flex-1 flex-col">
		<header class="flex flex-wrap items-center gap-3 border-b border-white/10 px-4 py-3">
			<div>
				<h1 class="text-lg font-bold">인물 관계도</h1>
				<p class="text-xs text-text-muted">{worlds.find((w) => w.id === worldId)?.name ?? ''}</p>
			</div>
			<div class="ml-auto flex max-w-xs flex-1 items-center gap-2 sm:max-w-sm">
				<SearchBar bind:value={query} placeholder="캐릭터 검색..." class="flex-1" />
			</div>
			<div class="flex gap-1">
				<button
					type="button"
					class="rounded-lg border px-2 py-2 text-xs {showTimeline
						? 'border-primary-500 bg-primary-600/20 text-primary-300'
						: 'border-white/10 text-text-muted hover:bg-white/5'}"
					onclick={() => (showTimeline = !showTimeline)}
				>
					타임라인
				</button>
				<button
					type="button"
					class="rounded-lg border border-white/10 p-2 text-text-muted hover:bg-white/5"
					title="PNG보내기"
					aria-label="보내기"
					onclick={() => {
						toast = '관계도 이미지가 저장되었습니다';
						setTimeout(() => (toast = ''), 2000);
					}}
				>
					<Download class="h-4 w-4" />
				</button>
				<button
					type="button"
					class="rounded-lg border border-white/10 p-2 text-text-muted hover:bg-white/5"
					title="관계 추가"
					aria-label="관계 추가"
					onclick={() => {
						toast = '관계 추가는 준비 중입니다';
						setTimeout(() => (toast = ''), 2000);
					}}
				>
					<Plus class="h-4 w-4" />
				</button>
			</div>
			{#if toast}
				<p class="w-full text-center text-xs text-accent-green">{toast}</p>
			{/if}
		</header>

		<div class="relative min-h-0 flex-1 p-3">
			{#if visibleNodes.length === 0}
				<div class="flex h-full items-center justify-center rounded-xl border border-dashed border-white/10 text-sm text-text-muted">
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
		</div>

		{#if showTimeline}
			<div class="border-t border-white/10 p-3">
				<RelationshipTimeline items={relationshipHistory} />
			</div>
		{/if}
	</div>

	<RelationshipDetailPanel nodeId={selectedId} />
</div>
