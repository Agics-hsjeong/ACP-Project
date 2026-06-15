<script lang="ts">
	import type { Character } from '$lib/data/mock';
	import Badge from '$lib/components/ui/Badge.svelte';
	import { Heart, Eye } from 'lucide-svelte';

	interface Props {
		character: Character;
	}

	let { character }: Props = $props();
</script>

<a
	href="/characters/{character.id}"
	class="group flex w-44 shrink-0 flex-col overflow-hidden rounded-2xl border border-white/10 bg-bg-surface/60 transition hover:-translate-y-0.5 hover:border-primary-500/40 hover:shadow-lg"
>
	<div class="relative aspect-[3/4] overflow-hidden bg-bg-card">
		<img
			src={character.avatar}
			alt={character.name}
			class="h-full w-full object-cover transition group-hover:scale-105"
		/>
	</div>
	<div class="flex flex-1 flex-col gap-2 p-3">
		<div>
			<p class="font-semibold leading-tight">{character.name}</p>
			<p class="mt-0.5 line-clamp-1 text-xs text-text-muted">{character.title}</p>
		</div>
		<div class="flex flex-wrap gap-1">
			{#each character.tags.slice(0, 3) as tag}
				<Badge label={tag.startsWith('#') ? tag : `#${tag}`} />
			{/each}
		</div>
		<div class="mt-auto flex items-center gap-3 text-xs text-text-muted">
			<span class="flex items-center gap-1 text-accent-pink">
				<Heart class="h-3 w-3" />
				{character.likes}%
			</span>
			<span class="flex items-center gap-1">
				<Eye class="h-3 w-3" />
				{(character.views / 1000).toFixed(1)}k
			</span>
		</div>
	</div>
</a>
