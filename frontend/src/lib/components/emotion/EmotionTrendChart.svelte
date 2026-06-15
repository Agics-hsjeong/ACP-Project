<script lang="ts">
	interface Point {
		day: number;
		affection: number;
		trust: number;
		anger: number;
	}

	interface Props {
		data: Point[];
		height?: number;
	}

	let { data, height = 120 }: Props = $props();

	const w = 280;
	const pad = 20;

	const series = [
		{ key: 'affection' as const, color: '#ec4899', label: '애정' },
		{ key: 'trust' as const, color: '#6366f1', label: '신뢰' },
		{ key: 'anger' as const, color: '#ef4444', label: '분노' }
	];

	function pathFor(key: keyof Point) {
		const max = 100;
		const min = 0;
		return data
			.map((d, i) => {
				const x = pad + (i / (data.length - 1)) * (w - pad * 2);
				const y = height - pad - ((d[key] as number) - min) / (max - min) * (height - pad * 2);
				return `${i === 0 ? 'M' : 'L'}${x},${y}`;
			})
			.join(' ');
	}
</script>

<div>
	<div class="mb-2 flex gap-3">
		{#each series as s}
			<span class="flex items-center gap-1 text-[10px] text-text-muted">
				<span class="h-2 w-2 rounded-full" style="background:{s.color}"></span>
				{s.label}
			</span>
		{/each}
	</div>
	<svg viewBox="0 0 {w} {height}" class="w-full" style="max-height:{height}px">
		{#each series as s}
			<path d={pathFor(s.key)} fill="none" stroke={s.color} stroke-width="2" stroke-linecap="round" />
		{/each}
	</svg>
</div>
