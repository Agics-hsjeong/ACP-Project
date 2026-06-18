<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		class?: string;
		padding?: boolean;
		title?: string;
		children: Snippet;
	}

	let { class: className = '', padding = true, title, children }: Props = $props();
</script>

<div
	class="rounded-xl border border-[#333847] bg-[#1a1c26] {padding ? 'p-4' : ''} {className}"
>
	{#if title}
		<h3 class="mb-3 text-sm font-semibold text-text-primary">{title}</h3>
	{/if}
	{@render children()}
</div>
