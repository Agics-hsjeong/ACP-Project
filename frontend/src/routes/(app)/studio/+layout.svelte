<script lang="ts">
	import type { Snippet } from 'svelte';
	import StudioSubNav from '$lib/components/studio/StudioSubNav.svelte';

	let { children }: { children: Snippet } = $props();
</script>

<div class="flex h-[calc(100dvh-0px)] min-h-[600px]">
	<StudioSubNav />
	<div class="flex min-w-0 flex-1 flex-col">{@render children()}</div>
</div>
