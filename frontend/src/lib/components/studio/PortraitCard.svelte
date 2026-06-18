<script lang="ts">
	import { ImagePlus } from 'lucide-svelte';
	import Input from '$lib/components/ui/Input.svelte';

	interface Props {
		src: string;
		alt?: string;
		onchange: (url: string) => void;
	}

	let { src, alt = '', onchange }: Props = $props();
	let editing = $state(false);
	let draft = $state(src);

	$effect(() => {
		draft = src;
	});
</script>

<div class="flex flex-col">
	<div class="relative aspect-[3/4] overflow-hidden rounded-2xl border border-white/10 bg-bg-primary/40">
		<img {src} {alt} class="h-full w-full object-cover" />
		<div class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/70 to-transparent p-3 pt-10">
			<button
				type="button"
				class="flex w-full items-center justify-center gap-1.5 rounded-lg bg-white/10 py-2 text-xs text-text-primary backdrop-blur-sm hover:bg-white/15"
				onclick={() => (editing = !editing)}
			>
				<ImagePlus class="h-3.5 w-3.5" />
				이미지 변경
			</button>
		</div>
	</div>
	{#if editing}
		<div class="mt-3 space-y-2">
			<Input label="이미지 URL" bind:value={draft} />
			<div class="flex gap-2">
				<button
					type="button"
					class="flex-1 rounded-lg bg-primary-600/80 py-2 text-xs font-medium text-white hover:bg-primary-600"
					onclick={() => {
						onchange(draft);
						editing = false;
					}}
				>
					적용
				</button>
				<button
					type="button"
					class="rounded-lg border border-white/10 px-3 py-2 text-xs text-text-muted hover:bg-white/5"
					onclick={() => {
						draft = src;
						editing = false;
					}}
				>
					취소
				</button>
			</div>
		</div>
	{/if}
</div>
