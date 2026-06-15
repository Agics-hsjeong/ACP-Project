<script lang="ts">
	interface Props {
		label: string;
		variant?: 'default' | 'primary' | 'accent';
		class?: string;
	}

	let { label, variant = 'default', class: className = '' }: Props = $props();

	const variants = {
		default: 'bg-bg-card/60 text-text-secondary',
		primary: 'bg-primary-500/20 text-primary-300',
		accent: 'bg-accent-pink/20 text-accent-pink'
	};
</script>

<span
	class="inline-flex items-center rounded-md px-2 py-0.5 text-xs font-medium {variants[
		variant
	]} {className}"
>
	{label}
</span>
