<script lang="ts">
	import type { Memory } from '$lib/data/mock';
	import Badge from '$lib/components/ui/Badge.svelte';

	interface Props {
		memory: Memory;
		selected?: boolean;
		onclick?: () => void;
		compact?: boolean;
	}

	let { memory, selected = false, onclick, compact = false }: Props = $props();

	const importanceLabel =
		memory.importance === 'high' ? '중요' : memory.importance === 'medium' ? '보통' : '일반';
</script>

<button
	type="button"
	class="w-full rounded-xl border text-left transition {selected
		? 'border-[#8c5cfa]/50 bg-[#8c5cfa]/10'
		: 'border-[#333847] bg-[#1a1c26] hover:border-[#8c5cfa]/30'} {compact ? 'p-3' : 'p-0 overflow-hidden'}"
	{onclick}
>
	{#if compact}
		<p class="text-xs font-semibold">{memory.title}</p>
		<p class="mt-1 line-clamp-2 text-[11px] text-text-muted">{memory.summary}</p>
	{:else}
		<div class="flex gap-0 sm:gap-4">
			<div class="w-36 shrink-0 overflow-hidden sm:w-44">
				<img
					src={memory.thumbnail ?? `https://api.dicebear.com/9.x/shapes/svg?seed=${memory.id}`}
					alt=""
					class="h-full min-h-[140px] w-full object-cover"
				/>
			</div>
			<div class="flex min-w-0 flex-1 flex-col p-4 pl-0 sm:pl-0">
				<div class="flex items-start justify-between gap-2">
					<div class="min-w-0">
						<p class="text-[10px] text-text-muted">
							{memory.date}
							{#if memory.dday}
								· D-{memory.dday}
							{/if}
						</p>
						<Badge
							label={importanceLabel}
							variant={memory.importance === 'high' ? 'accent' : 'default'}
						/>
						<h3 class="mt-1 text-base font-bold leading-tight">{memory.title}</h3>
					</div>
					<p class="shrink-0 text-xs font-medium text-accent-green">{memory.emotion}</p>
				</div>
				<p class="mt-2 line-clamp-2 text-sm text-text-secondary">{memory.summary}</p>
				{#if memory.tags?.length}
					<div class="mt-2 flex flex-wrap gap-1.5">
						{#each memory.tags.slice(0, 4) as tag}
							<span class="text-[10px] text-primary-300">#{tag.replace(/^#/, '')}</span>
						{/each}
					</div>
				{/if}
				{#if memory.quote}
					<p class="mt-2 line-clamp-1 text-xs italic text-text-muted">{memory.quote}</p>
				{/if}
			</div>
		</div>
	{/if}
</button>
