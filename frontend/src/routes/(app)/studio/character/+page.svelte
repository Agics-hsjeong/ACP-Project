<script lang="ts">
	import CharacterListPanel from '$lib/components/studio/CharacterListPanel.svelte';
	import PersonalitySliders from '$lib/components/studio/PersonalitySliders.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import {
		studioCharacters,
		characterStudioTabs,
		type StudioTab
	} from '$lib/data/studio';
	import { graphEdges, edgeStyles } from '$lib/data/relationship';
	import { Check, Eye, Redo2, Undo2 } from 'lucide-svelte';

	let selectedId = $state('elia');
	let activeTab = $state<StudioTab>('basic');
	let saved = $state(true);

	const character = $derived(studioCharacters.find((c) => c.id === selectedId) ?? studioCharacters[0]);

	const relations = $derived(
		graphEdges
			.filter((e) => e.source === selectedId || e.target === selectedId)
			.slice(0, 5)
	);
</script>

<svelte:head>
	<title>캐릭터 스튜디오 — ACP</title>
</svelte:head>

<div class="flex h-[calc(100dvh-0px)] min-h-[600px] flex-col lg:h-[calc(100vh-0px)]">
	<header class="flex flex-wrap items-center gap-3 border-b border-white/10 px-4 py-3">
		<div>
			<p class="text-xs text-text-muted">캐릭터 스튜디오 › 새 캐릭터 만들기</p>
			<h1 class="text-lg font-bold">{character.name}</h1>
		</div>
		<div class="ml-auto flex flex-wrap items-center gap-2">
			{#if saved}
				<span class="flex items-center gap-1 text-xs text-accent-green">
					<Check class="h-3.5 w-3.5" /> 저장됨
				</span>
			{/if}
			<button type="button" class="rounded-lg p-2 text-text-muted hover:bg-white/5" aria-label="실행 취소">
				<Undo2 class="h-4 w-4" />
			</button>
			<button type="button" class="rounded-lg p-2 text-text-muted hover:bg-white/5" aria-label="다시 실행">
				<Redo2 class="h-4 w-4" />
			</button>
			<Button variant="secondary" class="gap-2">
				<Eye class="h-4 w-4" /> 미리보기
			</Button>
			<Button onclick={() => (saved = true)}>캐릭터 저장</Button>
		</div>
	</header>

	<div class="flex min-h-0 flex-1">
		<CharacterListPanel
			characters={studioCharacters}
			{selectedId}
			onselect={(id) => {
				selectedId = id;
				saved = false;
			}}
		/>

		<div class="flex min-w-0 flex-1 flex-col">
			<nav class="flex gap-1 overflow-x-auto border-b border-white/10 px-4">
				{#each characterStudioTabs as tab}
					<button
						type="button"
						onclick={() => (activeTab = tab.id)}
						class="shrink-0 border-b-2 px-4 py-3 text-sm transition {activeTab === tab.id
							? 'border-primary-500 text-primary-300'
							: 'border-transparent text-text-muted hover:text-text-primary'}"
					>
						{tab.label}
					</button>
				{/each}
			</nav>

			<div class="flex-1 overflow-y-auto p-4 lg:p-6">
				{#if activeTab === 'basic'}
					<div class="grid gap-6 xl:grid-cols-[240px_1fr_280px]">
						<div class="space-y-3">
							<div class="overflow-hidden rounded-2xl border border-white/10 bg-bg-card/40">
								<img
									src={character.avatar}
									alt={character.name}
									class="aspect-[3/4] w-full object-cover"
								/>
								<Button variant="secondary" class="w-full rounded-none border-0 border-t border-white/10">
									이미지 변경
								</Button>
							</div>
						</div>

						<div class="space-y-4">
							<div class="grid gap-4 sm:grid-cols-2">
								<Input label="이름" bind:value={character.name} />
								<Input label="이명" bind:value={character.alias} />
								<Input label="나이" type="number" bind:value={character.age} />
								<div class="flex flex-col gap-1.5">
									<label for="gender" class="text-sm text-text-secondary">성별</label>
									<select
										id="gender"
										bind:value={character.gender}
										class="h-11 rounded-xl border border-white/10 bg-bg-primary/60 px-4 text-sm outline-none focus:border-primary-500"
									>
										<option>여성</option>
										<option>남성</option>
										<option>기타</option>
									</select>
								</div>
								<Input label="종족" bind:value={character.race} />
								<Input label="직업" bind:value={character.occupation} />
								<Input label="소속" bind:value={character.affiliation} />
								<div class="flex flex-col gap-1.5">
									<label for="world" class="text-sm text-text-secondary">세계관</label>
									<select
										id="world"
										bind:value={character.worldName}
										class="h-11 rounded-xl border border-white/10 bg-bg-primary/60 px-4 text-sm outline-none focus:border-primary-500"
									>
										<option>아르카디아 연대기</option>
										<option>은하 연합 연대기</option>
										<option>달빛 숲의 전설</option>
									</select>
								</div>
							</div>
							<div class="flex flex-col gap-1.5">
								<label for="intro" class="text-sm text-text-secondary">한 줄 소개</label>
								<textarea
									id="intro"
									bind:value={character.shortIntro}
									rows="3"
									class="rounded-xl border border-white/10 bg-bg-primary/60 px-4 py-3 text-sm outline-none focus:border-primary-500"
								></textarea>
							</div>
						</div>

						<div class="space-y-6">
							<div>
								<h3 class="mb-3 text-sm font-semibold">캐릭터 태그</h3>
								<div class="flex flex-wrap gap-2">
									{#each character.tags as tag}
										<Badge label="#{tag}" variant="primary" />
									{/each}
								</div>
							</div>
							<div>
								<h3 class="mb-3 text-sm font-semibold">성격 (3~5)</h3>
								<PersonalitySliders traits={character.traits} />
							</div>
							<div class="rounded-xl border border-white/10 bg-bg-card/30 p-4">
								<h3 class="mb-3 text-sm font-semibold">말투 미리보기</h3>
								<div class="space-y-2">
									{#each character.speechPreview as msg}
										<div
											class="rounded-lg px-3 py-2 text-xs {msg.role === 'user'
												? 'ml-4 bg-primary-600/20 text-right'
												: 'mr-4 bg-bg-primary/60'}"
										>
											{msg.content}
										</div>
									{/each}
								</div>
							</div>
						</div>
					</div>

					<div class="mt-8 grid gap-4 lg:grid-cols-2">
						{#each Object.entries({ 출신: character.background.origin, '현재 목표': character.background.goal, '과거 트라우마': character.background.trauma, '숨겨진 면': character.background.hidden }) as [label, text]}
							<div class="rounded-xl border border-white/10 bg-bg-card/30 p-4">
								<h4 class="mb-2 text-xs font-medium text-text-muted">{label}</h4>
								<p class="text-sm leading-relaxed text-text-secondary">{text}</p>
							</div>
						{/each}
					</div>
				{:else if activeTab === 'personality'}
					<div class="mx-auto max-w-2xl space-y-6">
						<h2 class="text-lg font-semibold">성격 · 배경 상세</h2>
						<PersonalitySliders traits={character.traits} />
						<div class="grid gap-4">
							{#each Object.entries(character.background) as [key, value]}
								<div class="flex flex-col gap-1.5">
									<label class="text-sm text-text-secondary" for="bg-{key}">{key}</label>
									<textarea
										id="bg-{key}"
										bind:value={character.background[key as keyof typeof character.background]}
										rows="3"
										class="rounded-xl border border-white/10 bg-bg-primary/60 px-4 py-3 text-sm outline-none focus:border-primary-500"
									></textarea>
								</div>
							{/each}
						</div>
					</div>
				{:else if activeTab === 'speech'}
					<div class="grid gap-6 lg:grid-cols-2">
						<div>
							<h2 class="mb-4 text-lg font-semibold">Few-shot 예시</h2>
							<div class="space-y-3">
								{#each character.fewShots as shot, i}
									<div class="rounded-xl border border-white/10 bg-bg-card/30 p-4">
										<p class="mb-1 text-xs text-text-muted">{shot.role === 'user' ? '유저' : '캐릭터'}</p>
										<p class="text-sm">{shot.content}</p>
									</div>
								{/each}
							</div>
							<Button variant="secondary" class="mt-4">예시 추가</Button>
						</div>
						<div>
							<h2 class="mb-4 text-lg font-semibold">금지 사항</h2>
							<ul class="space-y-2">
								{#each character.forbidden as rule, i}
									<li class="flex items-start gap-2 rounded-xl border border-white/10 bg-bg-card/30 px-4 py-3 text-sm">
										<span class="text-accent-red">✕</span>
										{rule}
									</li>
								{/each}
							</ul>
							<Button variant="secondary" class="mt-4">규칙 추가</Button>
						</div>
					</div>
				{:else if activeTab === 'memory'}
					<div class="mx-auto max-w-2xl space-y-4">
						<h2 class="text-lg font-semibold">기억 규칙</h2>
						<p class="text-sm text-text-muted">
							캐릭터가 대화 중 기억해야 할 이벤트, 감정 변화, 관계 변동 규칙을 설정합니다.
						</p>
						<div class="space-y-3">
							{#each ['중요 이벤트는 자동 저장', '감정 변화 ±5 이상 시 기록', '관계 변동 시 관계도 업데이트'] as rule}
								<label class="flex items-center gap-3 rounded-xl border border-white/10 bg-bg-card/30 px-4 py-3">
									<input type="checkbox" checked class="accent-primary-500" />
									<span class="text-sm">{rule}</span>
								</label>
							{/each}
						</div>
					</div>
				{:else if activeTab === 'relationship'}
					<div class="space-y-4">
						<h2 class="text-lg font-semibold">관계 설정</h2>
						<div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
							{#each relations as edge}
								{@const other =
									edge.source === selectedId
										? graphEdges.find((e) => e.id === edge.id)?.target
										: edge.source}
								{@const style = edgeStyles[edge.type]}
								<div class="rounded-xl border border-white/10 bg-bg-card/30 p-4">
									<div class="mb-2 flex items-center gap-2">
										<span
											class="h-2 w-2 rounded-full"
											style="background: {style.color}"
										></span>
										<span class="text-sm font-medium">{style.label}</span>
									</div>
									<p class="text-xs text-text-muted">{edge.label}</p>
								</div>
							{/each}
						</div>
						<Button variant="secondary" href="/relationship">관계도에서 편집</Button>
					</div>
				{:else}
					<div class="mx-auto max-w-lg space-y-4 text-center">
						<img
							src={character.avatar}
							alt=""
							class="mx-auto h-32 w-32 rounded-full border-4 border-primary-500/30"
						/>
						<h2 class="text-xl font-bold">{character.name}</h2>
						<p class="text-sm text-text-muted">{character.alias} · {character.occupation}</p>
						<p class="text-sm leading-relaxed text-text-secondary">{character.shortIntro}</p>
						<div class="flex flex-wrap justify-center gap-2">
							{#each character.tags as tag}
								<Badge label="#{tag}" variant="primary" />
							{/each}
						</div>
					</div>
				{/if}
			</div>
		</div>
	</div>
</div>
