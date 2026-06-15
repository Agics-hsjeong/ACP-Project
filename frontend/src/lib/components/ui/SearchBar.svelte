<script lang="ts">
	import { Search } from 'lucide-svelte';

	interface Props {
		placeholder?: string;
		value?: string;
		class?: string;
	}

	let {
		placeholder = '캐릭터, 세계관, 키워드 검색...',
		value = $bindable(''),
		class: className = ''
	}: Props = $props();
</script>

<div class="relative {className}">
	<Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-text-muted" />
	<input
		type="search"
		bind:value
		{placeholder}
		class="h-11 w-full rounded-xl border border-white/10 bg-bg-surface/80 pl-10 pr-4 text-sm text-text-primary placeholder:text-text-muted outline-none transition focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20"
	/>
</div>
