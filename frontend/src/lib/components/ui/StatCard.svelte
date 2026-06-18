<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		label: string;
		value: string | number;
		icon?: Snippet;
		hint?: string;
	}

	let { label, value, icon, hint }: Props = $props();
</script>

<div class="rounded-xl border border-[#333847] bg-[#1a1c26] p-4">
	<div class="flex items-start justify-between gap-2">
		<p class="text-xs text-text-muted">{label}</p>
		{#if icon}
			<span class="text-text-muted">{@render icon()}</span>
		{/if}
	</div>
	<p class="mt-2 text-2xl font-bold tracking-tight">{value}</p>
	{#if hint}
		<p class="mt-1 text-[10px] text-text-muted">{hint}</p>
	{/if}
</div>
