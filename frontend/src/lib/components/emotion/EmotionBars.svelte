<script lang="ts">
	import type { EmotionAxis } from '$lib/data/mock';

	interface Props {
		emotions: EmotionAxis[];
		compact?: boolean;
	}

	let { emotions, compact = false }: Props = $props();
</script>

<div class={compact ? 'space-y-2' : 'space-y-3'}>
	{#each emotions as emo}
		<div>
			<div class="mb-1 flex justify-between {compact ? 'text-xs' : 'text-sm'}">
				<span>{emo.label}</span>
				<span class="text-text-muted">{emo.value}%</span>
			</div>
			<div class="{compact ? 'h-1.5' : 'h-2'} rounded-full bg-bg-card">
				<div
					class="h-full rounded-full transition-all duration-500"
					style="width: {emo.value}%; background: {emo.color}"
				></div>
			</div>
		</div>
	{/each}
</div>
