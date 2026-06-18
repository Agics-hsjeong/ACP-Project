<script lang="ts">
	import { Bell, Mail, Search } from 'lucide-svelte';

	interface Props {
		placeholder?: string;
		value?: string;
		showIcons?: boolean;
		oninput?: (value: string) => void;
	}

	let {
		placeholder = '캐릭터, 세계관, 태그 검색…',
		value = $bindable(''),
		showIcons = true,
		oninput
	}: Props = $props();

	function handleInput(e: Event) {
		const next = (e.currentTarget as HTMLInputElement).value;
		value = next;
		oninput?.(next);
	}
</script>

<div class="mb-5 flex items-center gap-3">
	<label class="relative min-w-0 flex-1">
		<Search class="pointer-events-none absolute top-1/2 left-3.5 h-4 w-4 -translate-y-1/2 text-text-muted" />
		<input
			type="search"
			{placeholder}
			{value}
			oninput={handleInput}
			class="h-11 w-full rounded-xl border border-mock-border bg-mock-panel pr-4 pl-10 text-sm text-text-primary placeholder:text-text-muted outline-none transition focus:border-mock-accent/60 focus:ring-1 focus:ring-mock-accent/30"
		/>
	</label>
	{#if showIcons}
		<div class="flex shrink-0 items-center gap-2">
			<button
				type="button"
				class="flex h-11 w-11 items-center justify-center rounded-xl border border-mock-border bg-mock-panel text-text-muted transition hover:border-mock-accent/40 hover:text-text-secondary"
				aria-label="알림"
			>
				<Bell class="h-4 w-4" />
			</button>
			<button
				type="button"
				class="flex h-11 w-11 items-center justify-center rounded-xl border border-mock-border bg-mock-panel text-text-muted transition hover:border-mock-accent/40 hover:text-text-secondary"
				aria-label="메시지"
			>
				<Mail class="h-4 w-4" />
			</button>
		</div>
	{/if}
</div>
