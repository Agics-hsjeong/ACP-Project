<script lang="ts">
	import type { HTMLInputAttributes } from 'svelte/elements';

	interface Props extends HTMLInputAttributes {
		label?: string;
		error?: string;
	}

	let { label, error, class: className = '', id, ...rest }: Props = $props();
	const inputId = $derived(id ?? label?.replace(/\s/g, '-').toLowerCase());
</script>

<div class="flex flex-col gap-1.5">
	{#if label}
		<label for={inputId} class="text-sm text-text-secondary">{label}</label>
	{/if}
	<input
		id={inputId}
		class="h-11 w-full rounded-xl border border-white/10 bg-bg-primary/60 px-4 text-sm text-text-primary placeholder:text-text-muted outline-none transition focus:border-primary-500 focus:ring-2 focus:ring-primary-500/30 {error
			? 'border-accent-red'
			: ''} {className}"
		{...rest}
	/>
	{#if error}
		<p class="text-xs text-accent-red">{error}</p>
	{/if}
</div>
