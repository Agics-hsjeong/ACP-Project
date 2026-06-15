<script lang="ts">
	import {
		sendInteraction,
		actionPresets,
		expressionPresets,
		giftPresets,
		type InteractionType
	} from '$lib/stores/chat.svelte';
	import { Bookmark, Gift, Smile, Swords, X } from 'lucide-svelte';

	interface Props {
		characterId: string;
		characterName: string;
		disabled?: boolean;
	}

	let { characterId, characterName, disabled = false }: Props = $props();

	let openPanel = $state<InteractionType | null>(null);
	let recordTitle = $state('');

	const buttons: { type: InteractionType; label: string; icon: typeof Swords }[] = [
		{ type: 'action', label: '행동', icon: Swords },
		{ type: 'expression', label: '표정', icon: Smile },
		{ type: 'gift', label: '선물', icon: Gift },
		{ type: 'record', label: '기록', icon: Bookmark }
	];

	function toggle(type: InteractionType) {
		openPanel = openPanel === type ? null : type;
		recordTitle = '';
	}

	function selectAction(text: string) {
		sendInteraction(characterId, characterName, 'action', text);
		openPanel = null;
	}

	function selectExpression(text: string) {
		sendInteraction(characterId, characterName, 'expression', text);
		openPanel = null;
	}

	function selectGift(id: string) {
		sendInteraction(characterId, characterName, 'gift', id);
		openPanel = null;
	}

	function saveRecord() {
		if (!recordTitle.trim()) return;
		sendInteraction(characterId, characterName, 'record', recordTitle.trim());
		openPanel = null;
		recordTitle = '';
	}
</script>

<div class="relative">
	<div class="flex flex-wrap justify-center gap-2">
		{#each buttons as btn}
			<button
				type="button"
				{disabled}
				onclick={() => toggle(btn.type)}
				class="flex items-center gap-1.5 rounded-xl border px-3 py-2 text-xs transition disabled:opacity-40 {openPanel ===
				btn.type
					? 'border-primary-500 bg-primary-600/20 text-primary-300'
					: 'border-white/10 bg-bg-primary/40 text-text-secondary hover:border-white/20 hover:text-text-primary'}"
			>
				<btn.icon class="h-3.5 w-3.5" />
				{btn.label}
			</button>
		{/each}
	</div>

	{#if openPanel}
		<div
			class="absolute bottom-full left-1/2 z-20 mb-2 w-[min(100%,320px)] -translate-x-1/2 rounded-2xl border border-white/10 bg-bg-surface/95 p-4 shadow-xl backdrop-blur-md"
		>
			<div class="mb-3 flex items-center justify-between">
				<p class="text-sm font-semibold">
					{buttons.find((b) => b.type === openPanel)?.label}
				</p>
				<button
					type="button"
					class="rounded-lg p-1 text-text-muted hover:bg-white/5"
					onclick={() => (openPanel = null)}
					aria-label="닫기"
				>
					<X class="h-4 w-4" />
				</button>
			</div>

			{#if openPanel === 'action'}
				<div class="flex flex-wrap gap-2">
					{#each actionPresets as action}
						<button
							type="button"
							class="rounded-lg border border-white/10 bg-bg-primary/60 px-3 py-2 text-xs hover:border-primary-500/50 hover:bg-primary-600/10"
							onclick={() => selectAction(action)}
						>
							{action}
						</button>
					{/each}
				</div>
			{:else if openPanel === 'expression'}
				<div class="grid grid-cols-3 gap-2 sm:grid-cols-5">
					{#each expressionPresets as expr}
						<button
							type="button"
							class="flex flex-col items-center gap-1 rounded-xl border border-white/10 bg-bg-primary/60 p-3 text-xs hover:border-primary-500/50"
							onclick={() => selectExpression(expr.text)}
						>
							<span class="text-xl">{expr.emoji}</span>
							{expr.label}
						</button>
					{/each}
				</div>
			{:else if openPanel === 'gift'}
				<div class="space-y-2">
					{#each giftPresets as gift}
						<button
							type="button"
							class="flex w-full items-center justify-between rounded-xl border border-white/10 bg-bg-primary/60 px-4 py-3 text-sm hover:border-primary-500/50"
							onclick={() => selectGift(gift.id)}
						>
							<span>🎁 {gift.name}</span>
							<span class="text-xs text-accent-green">
								{gift.delta.label} +{gift.delta.value}
							</span>
						</button>
					{/each}
				</div>
			{:else if openPanel === 'record'}
				<div class="space-y-3">
					<input
						bind:value={recordTitle}
						placeholder="기억 제목 (예: 달빛 아래의 대화)"
						class="h-10 w-full rounded-xl border border-white/10 bg-bg-primary/60 px-3 text-sm outline-none focus:border-primary-500"
					/>
					<button
						type="button"
						class="w-full rounded-xl bg-primary-600 py-2.5 text-sm font-medium hover:opacity-90 disabled:opacity-40"
						disabled={!recordTitle.trim()}
						onclick={saveRecord}
					>
						기억 저장
					</button>
				</div>
			{/if}
		</div>
	{/if}
</div>
