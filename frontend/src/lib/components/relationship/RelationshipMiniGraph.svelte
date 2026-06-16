<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import * as d3 from 'd3';
	import { edgeStyles } from '$lib/data/relationship';
	import { getRelationshipGraph } from '$lib/stores/catalog.svelte';

	interface Props {
		centerId?: string;
	}

	let { centerId = 'elia' }: Props = $props();

	let container: HTMLDivElement | undefined = $state();

	const width = 240;
	const height = 160;

	onMount(() => {
		if (!browser || !container) return;

		const { nodes: graphNodes, edges: graphEdges } = getRelationshipGraph();
		const center = graphNodes.find((n) => n.id === centerId) ?? graphNodes[0];
		if (!center) return;
		const connectedIds = new Set<string>([center.id]);
		const localEdges = graphEdges.filter((e) => {
			if (e.source === center.id || e.target === center.id) {
				connectedIds.add(e.source);
				connectedIds.add(e.target);
				return true;
			}
			return false;
		});
		const localNodes = graphNodes.filter((n) => connectedIds.has(n.id)).slice(0, 6);

		type SimNode = (typeof localNodes)[0] & d3.SimulationNodeDatum;
		type SimLink = d3.SimulationLinkDatum<SimNode> & { type: string };

		const simNodes: SimNode[] = localNodes.map((n) => ({
			...n,
			x: n.id === center.id ? width / 2 : width / 2 + (Math.random() - 0.5) * 80,
			y: n.id === center.id ? height / 2 : height / 2 + (Math.random() - 0.5) * 60
		}));

		const nodeById = new Map(simNodes.map((n) => [n.id, n]));
		const simLinks: SimLink[] = localEdges
			.filter((e) => nodeById.has(e.source) && nodeById.has(e.target))
			.map((e) => ({ ...e, source: nodeById.get(e.source)!, target: nodeById.get(e.target)! }));

		const svg = d3
			.select(container)
			.append('svg')
			.attr('viewBox', `0 0 ${width} ${height}`)
			.attr('class', 'h-full w-full');

		const g = svg.append('g');

		const link = g
			.selectAll('line')
			.data(simLinks)
			.join('line')
			.attr('stroke', (d) => edgeStyles[d.type as keyof typeof edgeStyles]?.color ?? '#94a3b8')
			.attr('stroke-width', 1.5)
			.attr('stroke-opacity', 0.6);

		const node = g
			.selectAll('g')
			.data(simNodes)
			.join('g')
			.attr('cursor', 'pointer');

		node
			.append('circle')
			.attr('r', (d) => (d.id === center.id ? 14 : 10))
			.attr('fill', (d) => (d.id === center.id ? '#6366f1' : '#334155'))
			.attr('stroke', (d) => (d.id === center.id ? '#a5b4fc' : '#475569'))
			.attr('stroke-width', 1.5);

		node
			.append('text')
			.text((d) => d.label.slice(0, 2))
			.attr('text-anchor', 'middle')
			.attr('dy', 3)
			.attr('font-size', 8)
			.attr('fill', '#e2e8f0');

		const simulation = d3
			.forceSimulation(simNodes)
			.force(
				'link',
				d3.forceLink(simLinks).id((d) => (d as SimNode).id).distance(50)
			)
			.force('charge', d3.forceManyBody().strength(-120))
			.force('center', d3.forceCenter(width / 2, height / 2))
			.force('collision', d3.forceCollide().radius(18));

		simulation.on('tick', () => {
			link
				.attr('x1', (d) => (d.source as SimNode).x ?? 0)
				.attr('y1', (d) => (d.source as SimNode).y ?? 0)
				.attr('x2', (d) => (d.target as SimNode).x ?? 0)
				.attr('y2', (d) => (d.target as SimNode).y ?? 0);
			node.attr('transform', (d) => `translate(${d.x ?? 0},${d.y ?? 0})`);
		});

		return () => {
			simulation.stop();
			svg.remove();
		};
	});
</script>

<div
	bind:this={container}
	class="h-40 w-full rounded-xl border border-white/10 bg-bg-primary/40"
	role="img"
	aria-label="관계 미니맵"
></div>
