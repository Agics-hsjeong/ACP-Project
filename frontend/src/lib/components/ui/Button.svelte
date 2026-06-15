<script lang="ts">
	import type { Snippet } from 'svelte';
	import type { HTMLAnchorAttributes, HTMLButtonAttributes } from 'svelte/elements';

	type Variant = 'primary' | 'secondary' | 'ghost' | 'social-google' | 'social-apple' | 'social-discord';
	type Size = 'sm' | 'md' | 'lg';

	type Props = {
		variant?: Variant;
		size?: Size;
		fullWidth?: boolean;
		href?: string;
		class?: string;
		children: Snippet;
	} & (
		| (HTMLButtonAttributes & { href?: undefined })
		| (HTMLAnchorAttributes & { href: string })
	);

	let {
		variant = 'primary',
		size = 'md',
		fullWidth = false,
		href,
		class: className = '',
		children,
		...rest
	}: Props = $props();

	const variants: Record<Variant, string> = {
		primary: 'gradient-primary text-white hover:opacity-90 shadow-md',
		secondary: 'glass text-text-primary hover:bg-bg-card/80',
		ghost: 'bg-transparent text-text-secondary hover:text-text-primary hover:bg-white/5',
		'social-google': 'bg-white text-gray-900 hover:bg-gray-100',
		'social-apple': 'bg-black text-white border border-white/20 hover:bg-gray-900',
		'social-discord': 'bg-[#5865F2] text-white hover:bg-[#4752C4]'
	};

	const sizes: Record<Size, string> = {
		sm: 'h-9 px-4 text-sm rounded-lg',
		md: 'h-11 px-5 text-sm rounded-xl',
		lg: 'h-13 px-6 text-base rounded-xl'
	};

	const classes = $derived(
		[
			'inline-flex items-center justify-center gap-2 font-medium transition-all disabled:opacity-50 disabled:pointer-events-none',
			variants[variant],
			sizes[size],
			fullWidth ? 'w-full' : '',
			className
		].join(' ')
	);
</script>

{#if href}
	<a {href} class={classes} {...rest as HTMLAnchorAttributes}>
		{@render children()}
	</a>
{:else}
	<button class={classes} {...rest as HTMLButtonAttributes}>
		{@render children()}
	</button>
{/if}
