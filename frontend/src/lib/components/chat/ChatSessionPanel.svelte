<script lang="ts">
	import { page } from '$app/stores';
	import { Plus } from 'lucide-svelte';
	import { getCatalogRecentChats, getMemoryFragments } from '$lib/stores/catalog.svelte';

	interface Props {
		activeId?: string;
	}

	let { activeId }: Props = $props();

	const recentChats = $derived(getCatalogRecentChats());
	const memoryFragments = $derived(getMemoryFragments());
</script>

<aside class="hidden w-72 shrink-0 flex-col border-r border-[#333847] bg-[#0a0a14] lg:flex">
	<div class="p-4">
		<a
			href="/explore"
			class="flex w-full items-center justify-center gap-2 rounded-xl bg-[#8c5cfa] px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-[#7a4de0]"
		>
			<Plus class="h-4 w-4" />
			새 대화 시작
		</a>
	</div>

	<div class="flex-1 overflow-y-auto px-3 pb-4">
		<p class="mb-2 px-2 text-xs font-medium text-text-muted">대화 세션</p>
		<div class="space-y-0.5">
			{#each recentChats as chat}
				<a
					href="/chat/{chat.id}"
					class="flex items-start gap-3 rounded-xl px-2 py-2.5 transition {(activeId ?? $page.params.id) ===
					chat.id
						? 'bg-[#8c5cfa]/15'
						: 'hover:bg-white/5'}"
				>
					<img
						src={chat.avatar || `https://api.dicebear.com/9.x/notionists/svg?seed=${chat.id}`}
						alt=""
						class="mt-0.5 h-9 w-9 shrink-0 rounded-full bg-[#262933]"
					/>
					<div class="min-w-0 flex-1">
						<p class="truncate text-sm font-medium">{chat.name}</p>
						<p class="truncate text-[11px] text-text-muted">{chat.preview}</p>
					</div>
					<span class="shrink-0 pt-0.5 text-[10px] text-text-muted">{chat.time}</span>
				</a>
			{/each}
		</div>

		<p class="mb-2 mt-6 px-2 text-xs font-medium text-text-muted">기억 조각</p>
		<div class="space-y-2">
			{#each memoryFragments as frag}
				<a
					href="/memory"
					class="flex gap-2.5 rounded-xl border border-[#333847] bg-[#1a1c26] p-2.5 transition hover:border-[#8c5cfa]/40"
				>
					<img
						src={frag.thumbnail ?? `https://api.dicebear.com/9.x/shapes/svg?seed=${frag.id}`}
						alt=""
						class="h-12 w-10 shrink-0 rounded-lg object-cover"
					/>
					<div class="min-w-0 flex-1">
						<p class="truncate text-xs font-medium">{frag.title}</p>
						<p class="mt-0.5 text-[10px] text-text-muted">{frag.date}</p>
						<p class="mt-0.5 text-[10px] text-[#33b266]">{frag.delta}</p>
					</div>
				</a>
			{/each}
		</div>
	</div>
</aside>
