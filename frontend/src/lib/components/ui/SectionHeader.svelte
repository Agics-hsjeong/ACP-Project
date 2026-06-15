<script lang="ts">
	interface Props {
		title: string;
		href?: string;
	}

	let { title, href }: Props = $props();
</script>

<div class="mb-4 flex items-center justify-between">
	<h2 class="text-lg font-semibold">{title}</h2>
	{#if href}
		<a {href} class="text-sm text-primary-400 hover:underline">전체 보기</a>
	{/if}
</div>
