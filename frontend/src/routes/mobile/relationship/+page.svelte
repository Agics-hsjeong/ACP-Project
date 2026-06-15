<script lang="ts">
	import RelationshipGraph from '$lib/components/relationship/RelationshipGraph.svelte';
	import { graphNodes, graphEdges } from '$lib/data/relationship';

	let selectedId = $state('elia');
	const centerNodes = $derived(graphNodes);
	const centerEdges = $derived(graphEdges);
</script>

<svelte:head>
	<title>관계도 — Mobile</title>
</svelte:head>

<div class="border-b border-white/10 p-4">
	<h1 class="text-lg font-bold">인물 관계도</h1>
	<p class="text-xs text-text-muted">엘리아 중심 · 핀치/버튼 줌</p>
</div>

<div class="h-[calc(100dvh-180px)] p-2">
	<RelationshipGraph
		nodes={centerNodes}
		edges={centerEdges}
		{selectedId}
		onselect={(id) => (selectedId = id)}
	/>
</div>

{#if selectedId}
	<div class="border-t border-white/10 p-4 text-center">
		<p class="text-sm font-medium">{graphNodes.find((n) => n.id === selectedId)?.label}</p>
		<a href="/mobile/chat/{selectedId}" class="mt-2 inline-block text-xs text-primary-400">
			대화 시작 →
		</a>
	</div>
{/if}
