<script lang="ts">
	import { Plus, Trash2 } from 'lucide-svelte';
	import Button from '$lib/components/ui/Button.svelte';

	export type ChatLine = { role: 'user' | 'character'; content: string };

	interface Props {
		lines: ChatLine[];
		title?: string;
		onchange: (lines: ChatLine[]) => void;
	}

	let { lines, title = '대화', onchange }: Props = $props();

	function update(index: number, patch: Partial<ChatLine>) {
		onchange(lines.map((line, i) => (i === index ? { ...line, ...patch } : line)));
	}

	function add() {
		onchange([...lines, { role: 'user', content: '' }]);
	}

	function remove(index: number) {
		onchange(lines.filter((_, i) => i !== index));
	}
</script>

<div class="space-y-3">
	<div class="flex items-center justify-between">
		<h4 class="text-sm font-semibold">{title}</h4>
		<Button size="sm" variant="secondary" onclick={add}>
			<Plus class="h-4 w-4" /> 추가
		</Button>
	</div>
	<div class="space-y-2">
		{#each lines as line, i}
			<div class="rounded-xl border border-white/10 bg-bg-primary/30 p-3">
				<div class="mb-2 flex items-center gap-2">
					<select
						value={line.role}
						class="rounded-lg border border-white/10 bg-bg-surface/60 px-2 py-1 text-xs"
						onchange={(e) =>
							update(i, { role: (e.currentTarget as HTMLSelectElement).value as ChatLine['role'] })}
					>
						<option value="user">유저</option>
						<option value="character">캐릭터</option>
					</select>
					<button
						type="button"
						class="ml-auto rounded p-1 text-text-muted hover:text-accent-red"
						onclick={() => remove(i)}
						aria-label="삭제"
					>
						<Trash2 class="h-4 w-4" />
					</button>
				</div>
				<textarea
					value={line.content}
					rows="2"
					class="w-full rounded-lg border border-white/10 bg-bg-primary/60 px-3 py-2 text-sm outline-none focus:border-primary-500"
					oninput={(e) => update(i, { content: (e.currentTarget as HTMLTextAreaElement).value })}
				></textarea>
			</div>
		{:else}
			<p class="text-xs text-text-muted">등록된 {title}이 없습니다.</p>
		{/each}
	</div>
</div>
