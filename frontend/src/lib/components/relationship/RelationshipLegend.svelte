<script lang="ts">
	import { edgeStyles } from '$lib/data/relationship';

	const items = Object.entries(edgeStyles).map(([type, style]) => ({
		type,
		label: style.label,
		color: style.color
	}));
</script>

<div class="flex flex-wrap items-center gap-3 rounded-xl border border-white/10 bg-bg-surface/40 px-4 py-2.5">
	<span class="text-[10px] font-medium text-text-muted">범례</span>
	{#each items as item}
		<span class="flex items-center gap-1.5 text-[10px] text-text-secondary">
			<span class="h-2 w-2 rounded-full" style="background: {item.color}"></span>
			{item.label}
		</span>
	{/each}
</div>
