<script lang="ts">
	import { getUserProfileStats } from '$lib/stores/catalog.svelte';
	import { getUser } from '$lib/stores/auth.svelte';
	import MemoryFidelityGauge from '$lib/components/memory/MemoryFidelityGauge.svelte';
	import MemoryTagPanel from '$lib/components/memory/MemoryTagPanel.svelte';
	import MockPanel from '$lib/components/mockup/MockPanel.svelte';
	import type { Memory } from '$lib/data/mock';

	interface Props {
		fidelity: number;
		topTags: { tag: string; count: number }[];
		memories: Memory[];
		activeTag: string;
		onselectTag: (tag: string) => void;
	}

	let { fidelity, topTags, memories, activeTag, onselectTag }: Props = $props();

	const user = $derived(getUser());
	const stats = $derived(getUserProfileStats());
	const level = $derived(Math.min(99, 12 + stats.totalChats * 2 + stats.savedMemories));
	const xp = $derived((stats.savedMemories * 7 + stats.totalChats * 3) % 100);
</script>

<aside class="hidden w-56 shrink-0 space-y-3 lg:block">
	<MockPanel>
		<MemoryFidelityGauge value={fidelity} />
	</MockPanel>

	<MockPanel>
		<MemoryTagPanel tags={topTags} {memories} {activeTag} onselect={onselectTag} />
	</MockPanel>

	<MockPanel>
		<div class="flex items-center gap-3">
			<img
				src={user?.picture ||
					`https://api.dicebear.com/9.x/notionists/svg?seed=${user?.email || 'creator'}`}
				alt=""
				class="h-10 w-10 rounded-full border border-[#8c5cfa]/30"
			/>
			<div>
				<p class="text-sm font-semibold">{user?.name ?? 'Creator'}</p>
				<p class="text-xs text-[#8c5cfa]">Lv. {level}</p>
			</div>
		</div>
		<div class="mt-3">
			<div class="mb-1 flex justify-between text-[10px] text-text-muted">
				<span>XP</span>
				<span>{xp}%</span>
			</div>
			<div class="h-1.5 overflow-hidden rounded-full bg-[#262933]">
				<div class="h-full rounded-full bg-[#8c5cfa]" style="width: {xp}%"></div>
			</div>
		</div>
	</MockPanel>
</aside>
