<script lang="ts">
	import type { Memory } from '$lib/data/mock';
	import Badge from '$lib/components/ui/Badge.svelte';

	interface Props {
		memory: Memory;
		selected?: boolean;
		onclick?: () => void;
	}

	let { memory, selected = false, onclick }: Props = $props();
</script>

<button
	type="button"
	class="w-full rounded-2xl border p-4 text-left transition {selected
		? 'border-primary-500/50 bg-primary-500/10'
		: 'border-white/10 bg-bg-surface/60 hover:border-white/20'}"
	{onclick}
>
	<div class="flex gap-4">
		<div class="h-20 w-16 shrink-0 overflow-hidden rounded-xl bg-bg-card">
			<img
				src={memory.thumbnail ?? `https://api.dicebear.com/9.x/shapes/svg?seed=${memory.id}`}
				alt=""
				class="h-full w-full object-cover"
			/>
		</div>
		<div class="min-w-0 flex-1">
			<div class="flex items-start justify-between gap-2">
				<div>
					<p class="text-xs text-text-muted">
						{memory.date}
						{#if memory.dday}(D-{memory.dday}){/if}
					</p>
					<h3 class="mt-0.5 font-semibold leading-tight">{memory.title}</h3>
				</div>
				<Badge
					label={memory.importance === 'high' ? '중요' : memory.importance === 'medium' ? '보통' : '일반'}
					variant={memory.importance === 'high' ? 'accent' : 'default'}
				/>
			</div>
			<p class="mt-2 line-clamp-2 text-sm text-text-secondary">{memory.summary}</p>
			{#if memory.tags?.length}
				<div class="mt-2 flex flex-wrap gap-1">
					{#each memory.tags.slice(0, 3) as tag}
						<span class="text-[10px] text-primary-300">{tag}</span>
					{/each}
				</div>
			{/if}
			<p class="mt-2 text-xs text-accent-green">{memory.emotion}</p>
		</div>
	</div>
</button>
