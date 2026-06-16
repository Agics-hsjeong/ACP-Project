<script lang="ts">
	import RelationshipGraph from '$lib/components/relationship/RelationshipGraph.svelte';
	import {
		getRelationshipGraph,
		getRelationshipHistory
	} from '$lib/stores/catalog.svelte';
	import RelationshipTimeline from '$lib/components/relationship/RelationshipTimeline.svelte';

	let selectedId = $state('elia');

	const graphData = $derived(getRelationshipGraph());
	const graphNodes = $derived(graphData.nodes);
	const graphEdges = $derived(graphData.edges);
	const relationshipHistory = $derived(getRelationshipHistory());

	const arcadiaNodes = $derived(
		graphNodes.filter((n) => (n.worldId ?? graphData.worlds[0]?.id) === 'arcadia' || n.isCenter)
	);
	const arcadiaEdges = $derived(
		graphEdges.filter((e) => {
			const ids = new Set(arcadiaNodes.map((n) => n.id));
			return ids.has(e.source) && ids.has(e.target);
		})
	);
</script>

<svelte:head>
	<title>관계도 — Mobile</title>
</svelte:head>

<div class="border-b border-white/10 p-4">
	<h1 class="text-lg font-bold">인물 관계도</h1>
	<p class="text-xs text-text-muted">엘리아 중심 · 핀치/버튼 줌</p>
</div>

<div class="h-[calc(100dvh-180px)] p-2">
	{#if arcadiaNodes.length}
		<RelationshipGraph
			nodes={arcadiaNodes}
			edges={arcadiaEdges}
			{selectedId}
			onselect={(id) => (selectedId = id)}
		/>
	{:else}
		<div class="flex h-full items-center justify-center text-sm text-text-muted">
			관계 데이터를 불러오는 중...
		</div>
	{/if}
</div>

{#if selectedId}
	<div class="border-t border-white/10 p-4 text-center">
		<p class="text-sm font-medium">{arcadiaNodes.find((n) => n.id === selectedId)?.label}</p>
		<a href="/mobile/chat/{selectedId}" class="mt-2 inline-block text-xs text-primary-400">
			대화 시작 →
		</a>
	</div>
{/if}

<div class="border-t border-white/10 p-4">
	<RelationshipTimeline items={relationshipHistory} />
</div>
