<script lang="ts">
	interface Props {
		value: number;
		label: string;
		color: string;
		trend?: number;
	}

	let { value, label, color, trend = 0 }: Props = $props();

	const rounded = $derived(Math.round(value));
	const trendUp = $derived(trend >= 0);
</script>

<div class="rounded-xl border border-[#333847] bg-[#1a1c26] p-4">
	<p class="mb-2 text-xs text-text-muted">{label}</p>
	<div class="flex items-baseline gap-2">
		<p class="text-2xl font-bold" style="color: {color}">
			{rounded}<span class="text-base font-medium text-text-muted">/100</span>
		</p>
		{#if trend !== 0}
			<span class="text-xs font-medium {trendUp ? 'text-[#33b266]' : 'text-[#f28033]'}">
				{trendUp ? '▲' : '▼'}{Math.abs(trend).toFixed(1)}
			</span>
		{/if}
	</div>
	<div class="mt-3 h-1 overflow-hidden rounded-full bg-[#262933]">
		<div class="h-full rounded-full transition-all" style="width: {value}%; background: {color}"></div>
	</div>
</div>
