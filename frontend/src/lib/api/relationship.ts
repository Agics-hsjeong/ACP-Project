import { apiFetch } from './client';

export type RelationType =
	| 'friend'
	| 'alliance'
	| 'enemy'
	| 'lover'
	| 'family'
	| 'ex_lover'
	| 'neutral';

export type GraphNode = {
	id: string;
	label: string;
	kind: 'character' | 'location' | 'faction' | 'event';
	avatar?: string;
	subtitle?: string;
	tags?: string[];
	worldId?: string;
	isCenter?: boolean;
};

export type GraphEdge = {
	id: string;
	source: string;
	target: string;
	type: RelationType;
	label: string;
	weight?: number;
};

export async function fetchRelationshipGraph(params: { world?: string; center?: string }) {
	const search = new URLSearchParams();
	if (params.world) search.set('world', params.world);
	if (params.center) search.set('center', params.center);
	const qs = search.toString();
	return apiFetch<{ world: string; center: string; nodes: GraphNode[]; edges: GraphEdge[] }>(
		`/relationship/graph/${qs ? `?${qs}` : ''}`
	);
}

export async function fetchRelationshipHistory(params: { world?: string; center?: string }) {
	const search = new URLSearchParams();
	if (params.world) search.set('world', params.world);
	if (params.center) search.set('center', params.center);
	const qs = search.toString();
	return apiFetch<
		Array<{ id: number; world_id: string; center_id: string; title: string; date: string; summary: string; delta: string }>
	>(`/relationship/history/${qs ? `?${qs}` : ''}`);
}

