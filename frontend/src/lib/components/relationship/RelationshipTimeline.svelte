<script lang="ts">
	import type { RelationshipHistoryItem } from '$lib/data/relationship';

	interface Props {
		items: RelationshipHistoryItem[];
	}

	let { items }: Props = $props();
</script>

<div class="rounded-2xl border border-white/10 bg-bg-surface/50 p-5">
	<h3 class="mb-4 text-sm font-semibold">관계 히스토리</h3>
	<div class="space-y-4">
		{#each items as item (item.id)}
			<div class="relative border-l-2 border-primary-500/40 pl-4">
				<p class="text-[10px] text-text-muted">{item.date}</p>
				<p class="text-sm font-medium">{item.title}</p>
				<p class="mt-0.5 text-xs text-text-secondary">{item.summary}</p>
			</div>
		{/each}
	</div>
</div>
