<script lang="ts">
	import { getUser } from '$lib/stores/auth.svelte';
	import {
		getMemoryFragments,
		getUserProfileStats,
		getCatalogMemoryStats
	} from '$lib/stores/catalog.svelte';
	import { getEmotions, getIntimacy } from '$lib/stores/emotion.svelte';
	import { getEliaRelationships } from '$lib/stores/relationship.svelte';
	import MockPanel from '$lib/components/mockup/MockPanel.svelte';
	import RelationshipMiniGraph from '$lib/components/relationship/RelationshipMiniGraph.svelte';
	import { edgeStyles } from '$lib/data/relationship';
	import type { EmotionAxis } from '$lib/data/mock';
	import {
		Compass,
		MessageCircle,
		Brain,
		GitBranch,
		Heart,
		Palette
	} from 'lucide-svelte';

	const user = $derived(getUser());
	const stats = $derived(getUserProfileStats());
	const memoryStats = $derived(getCatalogMemoryStats());
	const emotions = $derived(getEmotions());
	const intimacy = $derived(getIntimacy());
	const memories = $derived(getMemoryFragments());
	const relationships = $derived(getEliaRelationships());

	const level = $derived(Math.min(99, 12 + stats.totalChats * 2 + stats.savedMemories));
	const xp = $derived((stats.savedMemories * 7 + stats.totalChats * 3) % 100);

	const mockEmotionColors: Record<string, string> = {
		affection: 'var(--color-emo-affection)',
		trust: 'var(--color-emo-trust)',
		respect: 'var(--color-emo-respect)',
		anger: 'var(--color-emo-anger)',
		jealousy: 'var(--color-emo-jealousy)',
		fear: 'var(--color-emo-fear)'
	};

	const displayEmotions = $derived(
		emotions.map((e) => ({
			...e,
			color: mockEmotionColors[e.key] ?? e.color
		})) as EmotionAxis[]
	);

	const relationSummary = $derived.by(() => {
		const counts = new Map<string, number>();
		for (const r of relationships) {
			const label = edgeStyles[r.type]?.label ?? r.type;
			counts.set(label, (counts.get(label) ?? 0) + 1);
		}
		return [...counts.entries()].map(([label, count]) => ({ label, count }));
	});

	const quickLinks = [
		{ href: '/explore', label: '캐릭터 탐색', icon: Compass },
		{ href: '/chat/elia', label: '새 대화', icon: MessageCircle },
		{ href: '/memory', label: '기억 보관소', icon: Brain },
		{ href: '/relationship', label: '관계도', icon: GitBranch },
		{ href: '/emotion', label: '감정 분석', icon: Heart },
		{ href: '/studio/character', label: '캐릭터 제작', icon: Palette }
	];
</script>

<aside class="sticky top-6 flex w-[400px] shrink-0 flex-col gap-4 self-start">
	<MockPanel>
		<div class="flex items-center gap-3">
			<img
				src={user?.picture ||
					`https://api.dicebear.com/9.x/notionists/svg?seed=${user?.email || 'creator'}`}
				alt=""
				class="h-14 w-14 rounded-full border-2 border-mock-accent/40 bg-mock-bg"
			/>
			<div class="min-w-0 flex-1">
				<p class="truncate font-semibold">{user?.name || 'Creator'}</p>
				<p class="text-xs text-mock-accent">Lv. {level}</p>
			</div>
		</div>
		<div class="mt-3">
			<div class="mb-1 flex justify-between text-[10px] text-text-muted">
				<span>경험치</span>
				<span>{xp}%</span>
			</div>
			<div class="h-1.5 overflow-hidden rounded-full bg-mock-track">
				<div class="h-full rounded-full bg-mock-accent" style="width: {xp}%"></div>
			</div>
		</div>
	</MockPanel>

	<MockPanel title="관계 요약">
		{#if relationships.length}
			<div class="mb-3 flex flex-wrap gap-2">
				{#each relationSummary as item}
					<span class="rounded-full border border-mock-border bg-mock-bg/60 px-2.5 py-1 text-[10px] text-text-secondary">
						{item.label} {item.count}
					</span>
				{/each}
			</div>
			<RelationshipMiniGraph centerId="elia" />
		{:else}
			<p class="text-xs text-text-muted">아직 관계 데이터가 없습니다.</p>
		{/if}
		<a href="/relationship" class="mt-2 block text-center text-[10px] text-mock-accent hover:underline">
			관계도 보기 →
		</a>
	</MockPanel>

	<MockPanel title="감정 상태 요약">
		<div class="mb-4 flex items-center justify-between rounded-lg border border-mock-border bg-mock-bg/50 px-3 py-2">
			<span class="text-xs text-text-muted">친밀도</span>
			<span class="text-lg font-bold text-mock-accent">{intimacy}%</span>
		</div>
		{#if displayEmotions.length}
			<div class="space-y-2.5">
				{#each displayEmotions as emo}
					<div>
						<div class="mb-1 flex justify-between text-xs">
							<span>{emo.label}</span>
							<span class="text-text-muted">{emo.value}%</span>
						</div>
						<div class="h-1.5 rounded-full bg-mock-track">
							<div
								class="h-full rounded-full transition-all duration-500"
								style="width: {emo.value}%; background: {emo.color}"
							></div>
						</div>
					</div>
				{/each}
			</div>
		{:else}
			<p class="text-xs text-text-muted">감정 데이터를 불러오는 중…</p>
		{/if}
	</MockPanel>

	<MockPanel title="최근 기억">
		<div class="space-y-2">
			{#each memories as mem}
				<a
					href="/memory"
					class="flex items-start gap-2 rounded-lg border border-mock-border bg-mock-bg/40 px-2.5 py-2 transition hover:border-mock-accent/40"
				>
					<span class="mt-0.5 h-2 w-2 shrink-0 rounded-full bg-mock-accent"></span>
					<div class="min-w-0">
						<p class="truncate text-xs font-medium">{mem.title}</p>
						<p class="text-[10px] text-text-muted">{mem.delta} · {mem.date}</p>
					</div>
				</a>
			{:else}
				<p class="text-xs text-text-muted">저장된 기억이 없습니다.</p>
			{/each}
		</div>
	</MockPanel>

	<MockPanel title="바로가기">
		<div class="grid grid-cols-3 gap-2">
			{#each quickLinks as link}
				<a
					href={link.href}
					class="flex flex-col items-center gap-1.5 rounded-xl border border-mock-border bg-mock-bg/40 p-2.5 text-center transition hover:border-mock-accent/40 hover:bg-mock-accent/5"
				>
					<link.icon class="h-4 w-4 text-mock-accent" />
					<span class="text-[9px] leading-tight text-text-muted">{link.label}</span>
				</a>
			{/each}
		</div>
	</MockPanel>

	<MockPanel class="border-mock-accent/30 bg-mock-accent/5">
		<p class="text-sm font-semibold text-mock-accent">Premium Plan</p>
		<p class="mt-1 text-xs text-text-muted">무제한 대화 · 고급 기억 엔진 · 창작 도구</p>
		<p class="mt-2 text-[10px] text-text-muted">함께한 기간 {memoryStats.daysTogether}일</p>
		<a href="/mypage" class="mt-3 inline-block text-xs text-mock-accent hover:underline">플랜 업그레이드 →</a>
	</MockPanel>
</aside>
