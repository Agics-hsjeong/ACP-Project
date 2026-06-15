<script lang="ts">
	import { page } from '$app/stores';
	import { Plus } from 'lucide-svelte';
	import { recentChats, memoryFragments } from '$lib/data/mock';
	import Button from '$lib/components/ui/Button.svelte';

	interface Props {
		activeId?: string;
	}

	let { activeId }: Props = $props();
</script>

<aside class="hidden w-64 shrink-0 flex-col border-r border-white/10 bg-bg-surface/30 lg:flex">
	<div class="border-b border-white/10 p-4">
		<Button href="/explore" fullWidth size="sm">
			<Plus class="h-4 w-4" />
			새 대화
		</Button>
	</div>

	<div class="flex-1 overflow-y-auto p-3">
		<p class="mb-2 px-2 text-xs font-medium text-text-muted">대화 세션</p>
		<div class="space-y-1">
			{#each recentChats as chat}
				<a
					href="/chat/{chat.id}"
					class="flex items-center gap-2 rounded-xl px-2 py-2.5 transition {(activeId ?? $page.params.id) ===
					chat.id
						? 'bg-primary-600/20 text-primary-200'
						: 'hover:bg-white/5'}"
				>
					<img
						src="https://api.dicebear.com/9.x/notionists/svg?seed={chat.id}"
						alt=""
						class="h-9 w-9 rounded-full bg-bg-card"
					/>
					<div class="min-w-0 flex-1">
						<p class="truncate text-sm font-medium">{chat.name}</p>
						<p class="truncate text-[11px] text-text-muted">{chat.preview}</p>
					</div>
					<span class="text-[10px] text-text-muted">{chat.time}</span>
				</a>
			{/each}
		</div>

		<p class="mb-2 mt-6 px-2 text-xs font-medium text-text-muted">기억 조각</p>
		<div class="space-y-2">
			{#each memoryFragments as frag}
				<a
					href="/memory"
					class="block rounded-xl border border-white/5 bg-bg-primary/40 p-3 transition hover:border-primary-500/30"
				>
					<div class="flex items-start justify-between gap-2">
						<p class="text-sm font-medium leading-tight">{frag.title}</p>
						<span
							class="shrink-0 rounded px-1.5 py-0.5 text-[10px] {frag.importance === 'high'
								? 'bg-accent-red/20 text-accent-red'
								: 'bg-bg-card text-text-muted'}"
						>
							{frag.importance === 'high' ? '중요' : '보통'}
						</span>
					</div>
					<p class="mt-1 text-[10px] text-text-muted">{frag.date}</p>
					<p class="mt-1 text-xs text-accent-green">{frag.delta}</p>
				</a>
			{/each}
		</div>
	</div>
</aside>
