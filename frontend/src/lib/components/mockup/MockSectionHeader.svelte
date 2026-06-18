<script lang="ts">
	interface Props {
		title: string;
		href?: string;
		moreLabel?: string;
	}

	let { title, href, moreLabel = '더 보기 >' }: Props = $props();
</script>

<div class="mb-4 flex items-center justify-between">
	<h2 class="text-base font-bold text-text-primary">{title}</h2>
	{#if href}
		<a href={href} class="text-xs text-mock-accent transition hover:text-mock-accent/80">
			{moreLabel}
		</a>
	{/if}
</div>
