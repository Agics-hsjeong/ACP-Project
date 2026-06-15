<script lang="ts">
	import type { RelationType } from '$lib/data/relationship';
	import { edgeStyles, worlds } from '$lib/data/relationship';

	interface Props {
		worldId?: string;
		showCharacters?: boolean;
		showPlaces?: boolean;
		showFactions?: boolean;
		showEvents?: boolean;
		activeTypes?: RelationType[];
		onreset?: () => void;
	}

	let {
		worldId = $bindable('arcadia'),
		showCharacters = $bindable(true),
		showPlaces = $bindable(true),
		showFactions = $bindable(true),
		showEvents = $bindable(true),
		activeTypes = $bindable([
			'friend',
			'alliance',
			'enemy',
			'lover',
			'family',
			'ex_lover',
			'neutral'
		] as RelationType[]),
		onreset
	}: Props = $props();

	const typeFilters: RelationType[] = [
		'lover',
		'family',
		'friend',
		'alliance',
		'enemy',
		'ex_lover'
	];

	function toggleType(type: RelationType) {
		activeTypes = activeTypes.includes(type)
			? activeTypes.filter((t) => t !== type)
			: [...activeTypes, type];
	}

	function resetFilters() {
		activeTypes = [
			'friend',
			'alliance',
			'enemy',
			'lover',
			'family',
			'ex_lover',
			'neutral'
		];
		showCharacters = true;
		showPlaces = true;
		showFactions = true;
		showEvents = true;
		onreset?.();
	}
</script>

<aside class="hidden w-56 shrink-0 flex-col border-r border-white/10 bg-bg-surface/30 p-4 lg:flex">
	<h3 class="mb-4 text-sm font-semibold">필터</h3>

	<div class="mb-5">
		<label for="world" class="mb-1.5 block text-xs text-text-muted">세계관</label>
		<select
			id="world"
			bind:value={worldId}
			class="h-9 w-full rounded-lg border border-white/10 bg-bg-primary/60 px-2 text-sm outline-none"
		>
			{#each worlds as w}
				<option value={w.id}>{w.name}</option>
			{/each}
		</select>
	</div>

	<div class="mb-5 space-y-2">
		<p class="text-xs text-text-muted">표시 노드</p>
		<label class="flex items-center gap-2 text-sm">
			<input type="checkbox" bind:checked={showCharacters} class="rounded" />
			캐릭터
		</label>
		<label class="flex items-center gap-2 text-sm">
			<input type="checkbox" bind:checked={showPlaces} class="rounded" />
			장소
		</label>
		<label class="flex items-center gap-2 text-sm">
			<input type="checkbox" bind:checked={showFactions} class="rounded" />
			세력
		</label>
		<label class="flex items-center gap-2 text-sm">
			<input type="checkbox" bind:checked={showEvents} class="rounded" />
			이벤트
		</label>
	</div>

	<div class="mb-4 space-y-2">
		<p class="text-xs text-text-muted">관계 유형</p>
		{#each typeFilters as type}
			<label class="flex items-center gap-2 text-sm">
				<input
					type="checkbox"
					checked={activeTypes.includes(type)}
					onchange={() => toggleType(type)}
					class="rounded"
				/>
				<span class="h-2 w-2 rounded-full" style="background:{edgeStyles[type].color}"></span>
				{edgeStyles[type].label}
			</label>
		{/each}
	</div>

	<button
		class="mt-auto rounded-lg border border-white/10 py-2 text-xs text-text-muted hover:bg-white/5"
		onclick={resetFilters}
	>
		필터 초기화
	</button>
</aside>
