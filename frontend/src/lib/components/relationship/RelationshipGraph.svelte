<script lang="ts">
	import { onMount, untrack } from 'svelte';
	import { browser } from '$app/environment';
	import * as d3 from 'd3';
	import type { GraphEdge, GraphNode } from '$lib/data/relationship';
	import { edgeStyles } from '$lib/data/relationship';

	interface Props {
		nodes: GraphNode[];
		edges: GraphEdge[];
		selectedId?: string;
		onselect?: (id: string) => void;
	}

	let { nodes, edges, selectedId = '', onselect }: Props = $props();

	let container: HTMLDivElement | undefined = $state();
	let zoomLevel = $state(100);
	let transform = $state({ x: 0, y: 0, k: 1 });

	type SimNode = GraphNode & d3.SimulationNodeDatum;
	type SimLink = d3.SimulationLinkDatum<SimNode> & { edge: GraphEdge };

	let simNodes: SimNode[] = [];
	let simLinks: SimLink[] = [];
	let graphTick = $state(0);
	let svgEl: SVGSVGElement | undefined = $state();
	let gEl: SVGGElement | undefined = $state();
	let zoomBehavior: d3.ZoomBehavior<SVGSVGElement, unknown> | null = null;
	let simulation: d3.Simulation<SimNode, SimLink> | null = null;

	const width = 900;
	const height = 560;

	function kindColor(kind: GraphNode['kind']) {
		switch (kind) {
			case 'location':
				return '#8b5cf6';
			case 'faction':
				return '#06b6d4';
			case 'event':
				return '#f59e0b';
			default:
				return '#6366f1';
		}
	}

	function rebuild() {
		if (!browser || !nodes.length) return;

		simulation?.stop();

		const center = nodes.find((n) => n.isCenter)?.id ?? nodes[0]?.id;
		simNodes = nodes.map((n) => ({
			...n,
			x: n.isCenter ? width / 2 : width / 2 + (Math.random() - 0.5) * 120,
			y: n.isCenter ? height / 2 : height / 2 + (Math.random() - 0.5) * 120
		}));

		const nodeById = new Map(simNodes.map((n) => [n.id, n]));
		simLinks = edges
			.filter((e) => nodeById.has(e.source) && nodeById.has(e.target))
			.map((e) => ({
				source: nodeById.get(e.source)!,
				target: nodeById.get(e.target)!,
				edge: e
			}));

		simulation = d3
			.forceSimulation(simNodes)
			.force(
				'link',
				d3
					.forceLink<SimNode, SimLink>(simLinks)
					.id((d) => d.id)
					.distance((l) => (l.source.id === center || l.target.id === center ? 140 : 100))
			)
			.force('charge', d3.forceManyBody().strength(-420))
			.force('center', d3.forceCenter(width / 2, height / 2))
			.force('collision', d3.forceCollide(42))
			.on('tick', () => {
				graphTick++;
			});
	}

	function zoomIn() {
		if (!svgEl || !zoomBehavior) return;
		d3.select(svgEl).transition().call(zoomBehavior.scaleBy, 1.2);
	}

	function zoomOut() {
		if (!svgEl || !zoomBehavior) return;
		d3.select(svgEl).transition().call(zoomBehavior.scaleBy, 0.8);
	}

	function resetView() {
		if (!svgEl || !zoomBehavior) return;
		d3.select(svgEl).transition().call(zoomBehavior.transform, d3.zoomIdentity);
		zoomLevel = 100;
		transform = { x: 0, y: 0, k: 1 };
	}

	const miniW = 148;
	const miniH = 104;
	const miniScale = $derived(Math.min(miniW / width, miniH / height));
	const viewport = $derived({
		x: (-transform.x / transform.k) * miniScale,
		y: (-transform.y / transform.k) * miniScale,
		w: (width / transform.k) * miniScale,
		h: (height / transform.k) * miniScale
	});

	const graphDataKey = $derived(
		`${nodes.map((n) => n.id).join(',')}|${edges.map((e) => e.id).join(',')}`
	);

	onMount(() => {
		if (!svgEl) return;

		zoomBehavior = d3
			.zoom<SVGSVGElement, unknown>()
			.scaleExtent([0.4, 2.5])
			.on('zoom', (event) => {
				if (gEl) {
					gEl.setAttribute('transform', event.transform.toString());
					zoomLevel = Math.round(event.transform.k * 100);
					transform = { x: event.transform.x, y: event.transform.y, k: event.transform.k };
				}
			});

		d3.select(svgEl).call(zoomBehavior);
	});

	$effect(() => {
		graphDataKey;
		if (!browser) return;
		untrack(() => rebuild());
	});

	function linkPath(d: SimLink) {
		const sx = (d.source as SimNode).x ?? 0;
		const sy = (d.source as SimNode).y ?? 0;
		const tx = (d.target as SimNode).x ?? 0;
		const ty = (d.target as SimNode).y ?? 0;
		return `M${sx},${sy} L${tx},${ty}`;
	}

	function linkLabelPos(d: SimLink) {
		const sx = (d.source as SimNode).x ?? 0;
		const sy = (d.source as SimNode).y ?? 0;
		const tx = (d.target as SimNode).x ?? 0;
		const ty = (d.target as SimNode).y ?? 0;
		return { x: (sx + tx) / 2, y: (sy + ty) / 2 };
	}
</script>

<div bind:this={container} class="relative h-full w-full overflow-hidden rounded-xl bg-bg-primary/40">
	<!-- Legend -->
	<div class="absolute left-3 top-3 z-10 flex flex-wrap gap-2 rounded-lg bg-bg-surface/90 px-3 py-2 text-[10px] backdrop-blur-sm">
		{#each Object.entries(edgeStyles) as [key, style]}
			{#if key !== 'neutral'}
				<span class="flex items-center gap-1 text-text-muted">
					<span class="h-0.5 w-4" style="background:{style.color}"></span>
					{style.label}
				</span>
			{/if}
		{/each}
	</div>

	<svg bind:this={svgEl} class="h-full w-full" viewBox="0 0 {width} {height}">
		<g bind:this={gEl} data-tick={graphTick}>
			{#each simLinks as link (link.edge.id)}
				{@const style = edgeStyles[link.edge.type]}
				<path
					d={linkPath(link)}
					fill="none"
					stroke={style.color}
					stroke-width="2"
					stroke-dasharray={style.dash || undefined}
					opacity="0.85"
				/>
				{@const pos = linkLabelPos(link)}
				<text
					x={pos.x}
					y={pos.y - 6}
					text-anchor="middle"
					fill={style.color}
					font-size="10"
					class="pointer-events-none select-none"
				>
					{link.edge.label}
				</text>
			{/each}

			{#each simNodes as node (node.id)}
				<g
					transform="translate({node.x ?? 0},{node.y ?? 0})"
					class="cursor-pointer"
					role="button"
					tabindex="0"
					onclick={() => onselect?.(node.id)}
					onkeydown={(e) => e.key === 'Enter' && onselect?.(node.id)}
				>
					<circle
						r="34"
						fill="#1e293b"
						stroke={selectedId === node.id ? '#818cf8' : kindColor(node.kind)}
						stroke-width={selectedId === node.id || node.isCenter ? 3 : 2}
					/>
					{#if node.avatar}
						<image
							href={node.avatar}
							x="-28"
							y="-28"
							width="56"
							height="56"
							clip-path="circle(28px at 28px 28px)"
						/>
					{/if}
					<text y="48" text-anchor="middle" fill="#f8fafc" font-size="11" font-weight="600">
						{node.label}
					</text>
				</g>
			{/each}
		</g>
	</svg>

	<div class="absolute bottom-3 left-3 flex gap-1">
		<button
			class="rounded-lg border border-white/10 bg-bg-surface/90 px-2.5 py-1.5 text-sm backdrop-blur-sm hover:bg-bg-card"
			onclick={zoomOut}
			aria-label="축소"
		>
			−
		</button>
		<button
			class="rounded-lg border border-white/10 bg-bg-surface/90 px-2.5 py-1.5 text-sm backdrop-blur-sm hover:bg-bg-card"
			onclick={zoomIn}
			aria-label="확대"
		>
			+
		</button>
		<button
			class="rounded-lg border border-white/10 bg-bg-surface/90 px-2 py-1.5 text-xs backdrop-blur-sm hover:bg-bg-card"
			onclick={resetView}
		>
			리셋
		</button>
	</div>
	<div class="absolute bottom-3 left-1/2 -translate-x-1/2 rounded-full bg-bg-surface/90 px-3 py-1 text-xs text-text-muted backdrop-blur-sm">
		{zoomLevel}%
	</div>

	<!-- Minimap -->
	<div class="absolute bottom-3 right-3 overflow-hidden rounded-lg border border-white/10 bg-bg-surface/90 backdrop-blur-sm">
		<p class="border-b border-white/10 px-2 py-1 text-[9px] text-text-muted">미니맵</p>
		<svg width={miniW} height={miniH} class="block" data-tick={graphTick}>
			{#each simLinks as link (link.edge.id)}
				<line
					x1={((link.source as SimNode).x ?? 0) * miniScale}
					y1={((link.source as SimNode).y ?? 0) * miniScale}
					x2={((link.target as SimNode).x ?? 0) * miniScale}
					y2={((link.target as SimNode).y ?? 0) * miniScale}
					stroke="#475569"
					stroke-width="1"
				/>
			{/each}
			{#each simNodes as node (node.id)}
				<circle
					cx={(node.x ?? 0) * miniScale}
					cy={(node.y ?? 0) * miniScale}
					r={node.isCenter ? 4 : 3}
					fill={selectedId === node.id ? '#818cf8' : kindColor(node.kind)}
				/>
			{/each}
			<rect
				x={viewport.x}
				y={viewport.y}
				width={viewport.w}
				height={viewport.h}
				fill="none"
				stroke="#a5b4fc"
				stroke-width="1.5"
				rx="2"
			/>
		</svg>
	</div>
</div>
