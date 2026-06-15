<script lang="ts">
	import type { EmotionAxis } from '$lib/data/mock';

	interface Props {
		emotions: EmotionAxis[];
		size?: number;
	}

	let { emotions, size = 220 }: Props = $props();
</script>

<svg viewBox="0 0 200 200" width={size} height={size} class="mx-auto">
	{#each Array(5) as _, ring}
		<circle
			cx="100"
			cy="100"
			r={20 + ring * 16}
			fill="none"
			stroke="rgba(255,255,255,0.1)"
			stroke-width="1"
		/>
	{/each}
	<polygon
		points={emotions
			.map((e, j) => {
				const a = (j / emotions.length) * Math.PI * 2 - Math.PI / 2;
				const rad = (e.value / 100) * 80;
				return `${100 + Math.cos(a) * rad},${100 + Math.sin(a) * rad}`;
			})
			.join(' ')}
		fill="rgba(99,102,241,0.25)"
		stroke="#6366f1"
		stroke-width="2"
	/>
	{#each emotions as emo, i}
		{@const angle = (i / emotions.length) * Math.PI * 2 - Math.PI / 2}
		<text
			x={100 + Math.cos(angle) * 94}
			y={100 + Math.sin(angle) * 94}
			text-anchor="middle"
			dominant-baseline="middle"
			fill="#94a3b8"
			font-size="8"
		>
			{emo.label}
		</text>
	{/each}
</svg>
