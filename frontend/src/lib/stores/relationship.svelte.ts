import { apiHealth } from '$lib/api/client';
import { fetchRelationshipGraph, fetchRelationshipHistory, type GraphEdge, type GraphNode } from '$lib/api/relationship';
import { getCatalogWorlds } from '$lib/stores/catalog.svelte';

let graph = $state<{ world: string; center: string; nodes: GraphNode[]; edges: GraphEdge[] } | null>(null);
let history = $state<Array<{ id?: number; title: string; date: string; summary: string; delta: string }>>([]);
let loading = $state(false);

export async function initRelationship(params: { world?: string; center?: string } = {}) {
	if (!(await apiHealth())) return;
	loading = true;
	try {
		const [nextGraph, nextHistory] = await Promise.all([
			fetchRelationshipGraph(params),
			fetchRelationshipHistory(params)
		]);
		graph = nextGraph;
		history = nextHistory;
		return nextGraph;
	} catch (err) {
		console.error('Relationship API load failed:', err);
		return null;
	} finally {
		loading = false;
	}
}

export function getRelationshipGraph() {
	const worlds = getCatalogWorlds().map((w) => ({ id: w.id, name: w.name }));
	return { ...(graph ?? { world: 'arcadia', center: 'elia', nodes: [], edges: [] }), worlds };
}

export function getRelationshipHistory() {
	return history;
}

export function getEliaRelationships() {
	const g = getRelationshipGraph();
	const center = g.center || 'elia';
	const nodesById = new Map(g.nodes.map((n) => [n.id, n]));
	return g.edges
		.filter((e) => e.source === center || e.target === center)
		.map((e) => {
			const otherId = e.source === center ? e.target : e.source;
			const other = nodesById.get(otherId);
			return {
				characterId: otherId,
				name: other?.label ?? otherId,
				type: e.type,
				score: e.weight ?? 50
			};
		});
}

export function getRelationshipNode(id: string) {
	return getRelationshipGraph().nodes.find((n) => n.id === id);
}

export function getRelationshipEdgesForNode(nodeId: string) {
	return getRelationshipGraph().edges.filter((e) => e.source === nodeId || e.target === nodeId);
}

