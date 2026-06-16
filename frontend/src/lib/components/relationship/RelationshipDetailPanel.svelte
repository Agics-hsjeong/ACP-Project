<script lang="ts">
	import { edgeStyles } from '$lib/data/relationship';
	import {
		getRelationshipNode,
		getRelationshipEdgesForNode,
		getEliaRelationships,
		getRelationshipHistory
	} from '$lib/stores/relationship.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import { MessageCircle } from 'lucide-svelte';

	interface Props {
		nodeId: string;
	}

	let { nodeId }: Props = $props();

	const node = $derived(getRelationshipNode(nodeId));
	const edges = $derived(getRelationshipEdgesForNode(nodeId));
	const eliaRelationships = $derived(getEliaRelationships());
	const relationshipHistory = $derived(getRelationshipHistory());
	const isElia = $derived(nodeId === 'elia');
</script>

<aside class="hidden w-80 shrink-0 flex-col border-l border-white/10 bg-bg-surface/30 xl:flex">
	{#if node}
		<div class="flex-1 overflow-y-auto p-5">
			<div class="mb-4 flex flex-col items-center text-center">
				{#if node.avatar}
					<img src={node.avatar} alt="" class="h-24 w-24 rounded-full border-2 border-primary-500/40 bg-bg-card" />
				{/if}
				<h3 class="mt-3 text-lg font-bold">{node.label}</h3>
				<p class="text-sm text-text-muted">{node.subtitle}</p>
				{#if node.tags?.length}
					<div class="mt-2 flex flex-wrap justify-center gap-1">
						{#each node.tags as tag}
							<Badge label={tag} variant="primary" />
						{/each}
					</div>
				{/if}
			</div>

			{#if isElia}
				<section class="mb-5">
					<h4 class="mb-3 text-sm font-semibold">핵심 관계</h4>
					<div class="space-y-3">
						{#each eliaRelationships as rel}
							<div>
								<div class="mb-1 flex justify-between text-xs">
									<span class="flex items-center gap-1.5">
										<span
											class="h-2 w-2 rounded-full"
											style="background:{edgeStyles[rel.type].color}"
										></span>
										{rel.name}
									</span>
									<span class="text-text-muted">{rel.score}</span>
								</div>
								<div class="h-1.5 rounded-full bg-bg-card">
									<div
										class="h-full rounded-full"
										style="width:{rel.score}%; background:{edgeStyles[rel.type].color}"
									></div>
								</div>
							</div>
						{/each}
					</div>
				</section>

				<section class="mb-5">
					<h4 class="mb-3 text-sm font-semibold">관계 히스토리</h4>
					<div class="space-y-3">
						{#each relationshipHistory as item}
							<div class="border-l-2 border-primary-500/40 pl-3">
								<p class="text-[10px] text-text-muted">{item.date}</p>
								<p class="text-sm font-medium">{item.title}</p>
								<p class="mt-0.5 text-xs text-text-secondary">{item.summary}</p>
							</div>
						{/each}
					</div>
				</section>
			{:else}
				<section class="mb-5">
					<h4 class="mb-2 text-sm font-semibold">연결 관계</h4>
					<ul class="space-y-2 text-sm">
						{#each edges as edge}
							{@const other =
								edge.source === nodeId
									? getRelationshipNode(edge.target)?.label
									: getRelationshipNode(edge.source)?.label}
							<li class="flex items-center gap-2 text-text-secondary">
								<span class="h-2 w-2 rounded-full" style="background:{edgeStyles[edge.type].color}"></span>
								{other} — {edge.label}
							</li>
						{/each}
					</ul>
				</section>
			{/if}

			{#if node.kind === 'character'}
				<Button href="/chat/{node.id}" fullWidth size="sm">
					<MessageCircle class="h-4 w-4" />
					대화 시작
				</Button>
			{/if}
		</div>
	{:else}
		<div class="flex flex-1 items-center justify-center p-6 text-center text-sm text-text-muted">
			노드를 선택하면 상세 정보가 표시됩니다
		</div>
	{/if}
</aside>
