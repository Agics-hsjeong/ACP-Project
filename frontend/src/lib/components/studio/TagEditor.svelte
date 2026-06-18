<script lang="ts">
	import Badge from '$lib/components/ui/Badge.svelte';
	import { Plus, X } from 'lucide-svelte';

	interface Props {
		tags: string[];
		onchange: (tags: string[]) => void;
		placeholder?: string;
	}

	let { tags, onchange, placeholder = '태그 입력 후 Enter' }: Props = $props();
	let draft = $state('');

	function commit() {
		const value = draft.trim().replace(/^#/, '');
		if (!value || tags.includes(value)) {
			draft = '';
			return;
		}
		onchange([...tags, value]);
		draft = '';
	}

	function remove(tag: string) {
		onchange(tags.filter((t) => t !== tag));
	}
</script>

<div class="space-y-3">
	<div class="flex flex-wrap gap-2">
		{#each tags as tag}
			<span class="inline-flex items-center gap-1">
				<Badge label={`#${tag}`} variant="primary" />
				<button
					type="button"
					class="rounded p-0.5 text-text-muted hover:text-accent-red"
					onclick={() => remove(tag)}
					aria-label="태그 삭제"
				>
					<X class="h-3 w-3" />
				</button>
			</span>
		{/each}
	</div>
	<div class="flex gap-2">
		<input
			bind:value={draft}
			{placeholder}
			class="h-9 flex-1 rounded-lg border border-white/10 bg-bg-primary/60 px-3 text-sm outline-none focus:border-primary-500"
			onkeydown={(e) => {
				if (e.key === 'Enter') {
					e.preventDefault();
					commit();
				}
			}}
		/>
		<button
			type="button"
			class="flex h-9 items-center gap-1 rounded-lg border border-white/10 bg-bg-primary/60 px-3 text-xs text-text-secondary hover:bg-white/5"
			onclick={commit}
		>
			<Plus class="h-3.5 w-3.5" /> 추가
		</button>
	</div>
</div>
