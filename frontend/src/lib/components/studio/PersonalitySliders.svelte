<script lang="ts">
	type PersonalityTrait = { key: string; label: string; value: number };

	interface Props {
		traits: PersonalityTrait[];
		readonly?: boolean;
	}

	let { traits, readonly = false }: Props = $props();
</script>

<div class="space-y-4">
	{#each traits as trait (trait.key)}
		<div>
			<div class="mb-1.5 flex items-center justify-between text-xs">
				<span class="text-text-secondary">{trait.label}</span>
				<span class="font-medium text-primary-300">{trait.value}%</span>
			</div>
			<div class="h-2 overflow-hidden rounded-full bg-bg-primary/80">
				<div
					class="h-full rounded-full bg-gradient-to-r from-primary-600 to-primary-400 transition-all"
					style="width: {trait.value}%"
				></div>
			</div>
			{#if !readonly}
				<input
					type="range"
					min="0"
					max="100"
					bind:value={trait.value}
					class="mt-1 w-full accent-primary-500"
				/>
			{/if}
		</div>
	{/each}
</div>
