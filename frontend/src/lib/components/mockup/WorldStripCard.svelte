<script lang="ts">
	import type { World } from '$lib/data/mock';

	interface Props {
		world: World;
	}

	let { world }: Props = $props();
</script>

<a
	href="/explore?world={world.id}"
	class="group flex w-56 shrink-0 items-center gap-3 overflow-hidden rounded-xl border border-mock-border bg-mock-panel p-2.5 transition hover:border-mock-accent/50"
>
	<div class="h-14 w-20 shrink-0 overflow-hidden rounded-lg bg-mock-bg">
		<img
			src={world.cover}
			alt={world.name}
			class="h-full w-full object-cover transition group-hover:scale-105"
		/>
	</div>
	<div class="min-w-0 flex-1">
		<p class="truncate text-sm font-semibold text-text-primary">{world.name}</p>
		<p class="mt-0.5 truncate text-[11px] text-text-muted">
			{world.genre.slice(0, 2).join(' · ')}
		</p>
	</div>
</a>
