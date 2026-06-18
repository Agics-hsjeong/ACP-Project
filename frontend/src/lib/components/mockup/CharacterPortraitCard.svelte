<script lang="ts">
	import type { Character } from '$lib/data/mock';

	interface Props {
		character: Character;
	}

	let { character }: Props = $props();
</script>

<a
	href="/characters/{character.id}"
	class="group flex w-[164px] shrink-0 flex-col overflow-hidden rounded-xl border border-mock-border bg-mock-panel transition hover:border-mock-accent/50 hover:shadow-lg hover:shadow-mock-accent/5"
>
	<div class="aspect-[3/4] overflow-hidden bg-mock-bg">
		<img
			src={character.avatar}
			alt={character.name}
			class="h-full w-full object-cover transition duration-300 group-hover:scale-105"
		/>
	</div>
	<div class="border-t border-mock-border px-2.5 py-2.5">
		<p class="truncate text-sm font-semibold text-text-primary">{character.name}</p>
		<p class="mt-0.5 truncate text-[11px] text-text-muted">{character.world}</p>
	</div>
</a>
