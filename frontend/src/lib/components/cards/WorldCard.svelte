<script lang="ts">
	import type { World } from '$lib/data/mock';
	import Badge from '$lib/components/ui/Badge.svelte';
	import { Users } from 'lucide-svelte';

	interface Props {
		world: World;
	}

	let { world }: Props = $props();
</script>

<a
	href="/explore?world={world.id}"
	class="group flex w-56 shrink-0 flex-col overflow-hidden rounded-2xl border border-white/10 bg-bg-surface/60 transition hover:border-primary-500/40 hover:shadow-lg"
>
	<div class="aspect-video overflow-hidden bg-bg-card">
		<img src={world.cover} alt={world.name} class="h-full w-full object-cover transition group-hover:scale-105" />
	</div>
	<div class="p-4">
		<p class="font-semibold">{world.name}</p>
		<div class="mt-2 flex flex-wrap gap-1">
			{#each world.genre as g}
				<Badge label={g} variant="primary" />
			{/each}
		</div>
		<p class="mt-2 flex items-center gap-1 text-xs text-text-muted">
			<Users class="h-3 w-3" />
			{world.characterCount}명의 캐릭터
		</p>
	</div>
</a>
