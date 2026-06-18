<script lang="ts" generics="T extends string">
	interface Tab {
		id: T;
		label: string;
	}

	interface Props {
		tabs: Tab[];
		active: T;
		onchange: (id: T) => void;
	}

	let { tabs, active, onchange }: Props = $props();
</script>

<nav class="flex flex-wrap gap-1 border-b border-white/10 pb-1">
	{#each tabs as tab}
		<button
			type="button"
			class="rounded-lg px-3 py-2 text-xs font-medium transition {active === tab.id
				? 'bg-primary-600/25 text-primary-200 ring-1 ring-primary-500/30'
				: 'text-text-muted hover:bg-white/5 hover:text-text-primary'}"
			onclick={() => onchange(tab.id)}
		>
			{tab.label}
		</button>
	{/each}
</nav>
