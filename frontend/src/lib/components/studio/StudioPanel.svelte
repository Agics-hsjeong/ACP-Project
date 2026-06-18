<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		title?: string;
		class?: string;
		actions?: Snippet;
		children: Snippet;
	}

	let { title, class: className = '', actions, children }: Props = $props();
</script>

<div class="rounded-2xl border border-white/10 bg-bg-surface/40 {className}">
	{#if title || actions}
		<div class="flex items-center justify-between gap-2 border-b border-white/5 px-4 py-3">
			{#if title}
				<h3 class="text-sm font-semibold text-text-primary">{title}</h3>
			{/if}
			{#if actions}
				<div class="ml-auto">{@render actions()}</div>
			{/if}
		</div>
	{/if}
	<div class="p-4">{@render children()}</div>
</div>
