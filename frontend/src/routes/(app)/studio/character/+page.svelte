<script lang="ts">
	import { onMount } from 'svelte';
	import CharacterListPanel from '$lib/components/studio/CharacterListPanel.svelte';
	import PersonalitySliders from '$lib/components/studio/PersonalitySliders.svelte';
	import StudioPanel from '$lib/components/studio/StudioPanel.svelte';
	import StudioTabBar from '$lib/components/studio/StudioTabBar.svelte';
	import PortraitCard from '$lib/components/studio/PortraitCard.svelte';
	import TagEditor from '$lib/components/studio/TagEditor.svelte';
	import ChatLineEditor from '$lib/components/studio/ChatLineEditor.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import {
		characterStudioTabs,
		defaultCharacterStudioMeta,
		type StudioTab,
		type StudioCharacter
	} from '$lib/data/studio';
	import { characterToStudioForm, studioFormToCharacterPatch } from '$lib/studio/character';
	import {
		getStudioCharacters,
		getStudioWorlds,
		initStudio,
		saveStudioCharacter,
		addStudioCharacter
	} from '$lib/stores/studio.svelte';
	import { initCatalog } from '$lib/stores/catalog.svelte';
	import { Check, ChevronRight, Eye, GitBranch, Plus, Trash2, Users } from 'lucide-svelte';

	const characters = $derived(getStudioCharacters());
	const worlds = $derived(getStudioWorlds());

	let selectedId = $state('');
	let activeTab = $state<StudioTab>('basic');
	let saved = $state(true);
	let saving = $state(false);
	let toast = $state('');
	let form = $state<StudioCharacter | null>(null);
	let memorySummary = $state('');

	const character = $derived(characters.find((c) => c.id === selectedId) ?? null);
	const worldPeers = $derived(
		characters.filter((c) => c.id !== selectedId && c.worldId === form?.worldId)
	);
	const breadcrumb = $derived(
		form?.name ? `캐릭터 스튜디오 › ${form.name}` : '캐릭터 스튜디오 › 새 캐릭터 만들기'
	);

	$effect(() => {
		if (!selectedId && characters.length) selectedId = characters[0].id;
	});

	$effect(() => {
		if (!character) {
			form = null;
			return;
		}
		form = characterToStudioForm(character);
		memorySummary = character.memorySummary ?? '';
		saved = true;
	});

	onMount(() => {
		void initStudio();
	});

	function markDirty() {
		saved = false;
	}

	function updateTrait(key: string, value: number) {
		if (!form) return;
		form = {
			...form,
			traits: form.traits.map((t) => (t.key === key ? { ...t, value } : t))
		};
		markDirty();
	}

	function updateWorld(id: string) {
		if (!form) return;
		const world = worlds.find((w) => w.id === id);
		form = { ...form, worldId: id, worldName: world?.name ?? form.worldName, affiliation: world?.name ?? '' };
		markDirty();
	}

	function addForbidden() {
		if (!form) return;
		form = { ...form, forbidden: [...form.forbidden, ''] };
		markDirty();
	}

	function removeForbidden(index: number) {
		if (!form) return;
		form = { ...form, forbidden: form.forbidden.filter((_, i) => i !== index) };
		markDirty();
	}

	const backgroundPreview = $derived.by(() => {
		if (!form) return '';
		const b = form.background;
		return [b.origin, b.goal, b.trauma, b.hidden].filter(Boolean).join('\n\n');
	});

	async function handleSave() {
		if (!character || !form) return;
		saving = true;
		toast = '';
		try {
			await saveStudioCharacter(character.id, studioFormToCharacterPatch(form, character, memorySummary));
			saved = true;
			toast = '저장되었습니다';
			setTimeout(() => (toast = ''), 2000);
		} catch (err) {
			toast = err instanceof Error ? err.message : '저장에 실패했습니다';
		} finally {
			saving = false;
		}
	}

	async function handleCreate() {
		const id = `char_${Date.now().toString(36)}`;
		const worldId = worlds[0]?.id ?? 'arcadia';
		const defaults = defaultCharacterStudioMeta();
		saving = true;
		toast = '';
		try {
			const created = await addStudioCharacter({
				id,
				name: '새 캐릭터',
				title: '새 캐릭터',
				world_id: worldId,
				description: '캐릭터 소개를 입력하세요.',
				tags: [],
				occupation: '',
				race: '인간',
				avatar: `https://api.dicebear.com/9.x/notionists/svg?seed=${id}`,
				cover: `https://api.dicebear.com/9.x/shapes/svg?seed=${id}-cover`,
				studio_meta: {
					alias: '새 캐릭터',
					traits: defaults.traits,
					background: defaults.background,
					few_shots: defaults.fewShots,
					forbidden: defaults.forbidden,
					speech_preview: defaults.speechPreview,
					speech_style: defaults.speechStyle,
					memory_rules: defaults.memoryRules
				}
			});
			selectedId = created.id;
			saved = true;
			void initCatalog(true);
			toast = '새 캐릭터가 생성되었습니다';
			setTimeout(() => (toast = ''), 2000);
		} catch (err) {
			toast = err instanceof Error ? err.message : '생성에 실패했습니다';
		} finally {
			saving = false;
		}
	}
</script>

<svelte:head>
	<title>캐릭터 스튜디오 — ACP</title>
</svelte:head>

<div class="flex min-h-0 flex-1 flex-col">
	<header class="shrink-0 border-b border-white/10 px-4 py-3 lg:px-6">
		<div class="flex flex-wrap items-center gap-3">
			<div class="min-w-0 flex-1">
				<p class="flex items-center gap-1 text-[11px] text-text-muted">
					<span>창작 스튜디오</span>
					<ChevronRight class="h-3 w-3" />
					<span class="text-text-secondary">{breadcrumb}</span>
				</p>
				<h1 class="mt-0.5 truncate text-lg font-bold">{form?.name ?? '캐릭터 선택'}</h1>
			</div>
			<div class="flex flex-wrap items-center gap-2">
				{#if saved}
					<span class="flex items-center gap-1 text-xs text-accent-green">
						<Check class="h-3.5 w-3.5" /> 저장됨
					</span>
				{/if}
				<Button
					variant="secondary"
					class="gap-2"
					href={character ? `/characters/${character.id}` : undefined}
					disabled={!character}
				>
					<Eye class="h-4 w-4" /> 미리보기
				</Button>
				<Button onclick={handleSave} disabled={saving || !form}>
					{saving ? '저장 중…' : '저장'}
				</Button>
			</div>
		</div>
		{#if toast}
			<p class="mt-2 text-center text-xs text-text-muted">{toast}</p>
		{/if}
	</header>

	<div class="grid min-h-0 flex-1 lg:grid-cols-[auto_1fr]">
		<CharacterListPanel
			{characters}
			{selectedId}
			onselect={(id) => {
				selectedId = id;
				saved = true;
			}}
			oncreate={handleCreate}
		/>

		<section class="flex min-w-0 flex-col overflow-hidden">
			{#if form}
				<div class="shrink-0 border-b border-white/10 px-4 py-3 lg:px-6">
					<StudioTabBar tabs={characterStudioTabs} active={activeTab} onchange={(id) => (activeTab = id)} />
				</div>

				<div class="min-h-0 flex-1 overflow-y-auto p-4 lg:p-6" oninput={markDirty} onchange={markDirty}>
					{#if activeTab === 'basic'}
						<div class="grid gap-4 xl:grid-cols-[220px_1fr_1fr]">
							<PortraitCard
								src={form.avatar}
								alt={form.name}
								onchange={(url) => {
									form!.avatar = url;
									markDirty();
								}}
							/>
							<StudioPanel title="기본 정보">
								<div class="grid gap-3 sm:grid-cols-2">
									<Input label="이름" bind:value={form.name} />
									<Input label="별칭 / 호칭" bind:value={form.alias} />
									<Input label="나이" type="number" bind:value={form.age} />
									<Input label="성별" bind:value={form.gender} />
									<Input label="종족" bind:value={form.race} />
									<Input label="직업" bind:value={form.occupation} />
									<div class="sm:col-span-2">
										<label for="char-world" class="text-sm text-text-secondary">소속 세계관</label>
										<select
											id="char-world"
											value={form.worldId}
											class="mt-1.5 h-11 w-full rounded-xl border border-white/10 bg-bg-primary/60 px-4 text-sm outline-none focus:border-primary-500"
											onchange={(e) => updateWorld((e.currentTarget as HTMLSelectElement).value)}
										>
											{#each worlds as w}
												<option value={w.id}>{w.name}</option>
											{/each}
										</select>
									</div>
									<div class="sm:col-span-2">
										<label for="char-intro" class="text-sm text-text-secondary">한 줄 소개</label>
										<textarea
											id="char-intro"
											bind:value={form.shortIntro}
											rows="3"
											class="mt-1.5 w-full rounded-xl border border-white/10 bg-bg-primary/60 px-4 py-3 text-sm outline-none focus:border-primary-500"
										></textarea>
									</div>
								</div>
							</StudioPanel>
							<StudioPanel title="태그 & 성향">
								<TagEditor
									tags={form.tags}
									onchange={(tags) => {
										form!.tags = tags;
										markDirty();
									}}
								/>
								<div class="mt-5 border-t border-white/5 pt-4">
									<PersonalitySliders traits={form.traits} onchange={updateTrait} />
								</div>
							</StudioPanel>
						</div>

						<div class="mt-4 grid gap-4 lg:grid-cols-3">
							<StudioPanel title="상세 배경">
								<p class="line-clamp-6 whitespace-pre-wrap text-sm leading-relaxed text-text-secondary">
									{backgroundPreview || '성격·배경 탭에서 출신, 목표, 트라우마, 비밀을 작성하세요.'}
								</p>
								<button
									type="button"
									class="mt-3 text-xs text-primary-400 hover:underline"
									onclick={() => (activeTab = 'personality')}
								>
									배경 편집하기 →
								</button>
							</StudioPanel>
							<StudioPanel title="Few-shot 예시">
								<div class="space-y-2">
									{#each form.fewShots.slice(0, 4) as line}
										<div
											class="rounded-lg px-3 py-2 text-xs {line.role === 'user'
												? 'ml-4 bg-primary-600/15 text-text-secondary'
												: 'mr-4 bg-bg-primary/50 text-text-primary'}"
										>
											<span class="text-[10px] text-text-muted">{line.role === 'user' ? '유저' : '캐릭터'}</span>
											<p class="mt-0.5">{line.content || '…'}</p>
										</div>
									{:else}
										<p class="text-xs text-text-muted">말투·스타일 탭에서 예시를 추가하세요.</p>
									{/each}
								</div>
								<button
									type="button"
									class="mt-3 text-xs text-primary-400 hover:underline"
									onclick={() => (activeTab = 'speech')}
								>
									예시 편집하기 →
								</button>
							</StudioPanel>
							<StudioPanel title="금지 사항">
								<ul class="space-y-1.5 text-sm text-text-secondary">
									{#each form.forbidden.filter(Boolean).slice(0, 5) as rule}
										<li class="flex gap-2">
											<span class="text-accent-red">×</span>
											<span>{rule}</span>
										</li>
									{:else}
										<li class="text-xs text-text-muted">금지 규칙이 없습니다.</li>
									{/each}
								</ul>
								<button
									type="button"
									class="mt-3 text-xs text-primary-400 hover:underline"
									onclick={() => (activeTab = 'speech')}
								>
									규칙 편집하기 →
								</button>
							</StudioPanel>
						</div>
					{:else if activeTab === 'personality'}
						<div class="grid gap-4 lg:grid-cols-2">
							<StudioPanel title="성격 슬라이더">
								<PersonalitySliders traits={form.traits} onchange={updateTrait} />
								<p class="mt-4 text-xs text-text-muted">
									슬라이더 값은 AI 대화 시 성격 톤과 반응 강도에 반영됩니다.
								</p>
							</StudioPanel>
							<StudioPanel title="배경 스토리">
								<div class="space-y-4">
									{#each [
										{ key: 'origin', label: '출신 / 배경', rows: 4 },
										{ key: 'goal', label: '목표', rows: 3 },
										{ key: 'trauma', label: '트라우마', rows: 3 },
										{ key: 'hidden', label: '숨겨진 비밀', rows: 3 }
									] as field}
										<div>
											<label class="text-sm text-text-secondary" for={field.key}>{field.label}</label>
											<textarea
												id={field.key}
												bind:value={form.background[field.key as keyof typeof form.background]}
												rows={field.rows}
												class="mt-1.5 w-full rounded-xl border border-white/10 bg-bg-primary/60 px-4 py-3 text-sm outline-none focus:border-primary-500"
											></textarea>
										</div>
									{/each}
								</div>
							</StudioPanel>
						</div>
					{:else if activeTab === 'speech'}
						<div class="grid gap-4 lg:grid-cols-2">
							<StudioPanel title="말투 스타일">
								<div class="space-y-3">
									<Input label="어조 (예: 차분하고 정중함)" bind:value={form.speechStyle.tone} />
									<Input label="말버릇 / 패턴" bind:value={form.speechStyle.pattern} />
									<Input label="호칭 / 존댓말 규칙" bind:value={form.speechStyle.honorific} />
								</div>
							</StudioPanel>
							<StudioPanel title="말투 미리보기">
								<div class="space-y-2">
									{#each form.speechPreview as line}
										<div
											class="rounded-lg px-3 py-2 text-sm {line.role === 'user'
												? 'ml-6 bg-primary-600/20'
												: 'mr-6 bg-bg-primary/60'}"
										>
											{line.content || '…'}
										</div>
									{/each}
								</div>
							</StudioPanel>
						</div>
						<div class="mt-4 grid gap-4 lg:grid-cols-2">
							<StudioPanel title="Few-shot 대화 예시">
								<ChatLineEditor
									lines={form.fewShots}
									title="예시"
									onchange={(lines) => {
										form!.fewShots = lines;
										markDirty();
									}}
								/>
							</StudioPanel>
							<StudioPanel title="금지 규칙">
								<div class="mb-3 flex justify-end">
									<Button size="sm" variant="secondary" onclick={addForbidden}>
										<Plus class="h-4 w-4" /> 규칙 추가
									</Button>
								</div>
								<div class="space-y-2">
									{#each form.forbidden as rule, i}
										<div class="flex items-center gap-2">
											<Input
												class="flex-1"
												value={rule}
												placeholder="캐릭터가 하지 말아야 할 행동"
												oninput={(e) => {
													form!.forbidden[i] = (e.currentTarget as HTMLInputElement).value;
													markDirty();
												}}
											/>
											<button
												type="button"
												class="rounded p-2 text-text-muted hover:text-accent-red"
												onclick={() => removeForbidden(i)}
												aria-label="삭제"
											>
												<Trash2 class="h-4 w-4" />
											</button>
										</div>
									{/each}
								</div>
							</StudioPanel>
						</div>
						<div class="mt-4">
							<StudioPanel title="미리보기 대화 편집">
								<ChatLineEditor
									lines={form.speechPreview}
									title="대화"
									onchange={(lines) => {
										form!.speechPreview = lines;
										markDirty();
									}}
								/>
							</StudioPanel>
						</div>
					{:else if activeTab === 'memory'}
						<div class="grid gap-4 lg:grid-cols-2">
							<StudioPanel title="에피소드 기억 요약">
								<p class="mb-3 text-xs text-text-muted">
									캐릭터가 기억해야 할 핵심 설정과 대화 중 저장할 에피소드 기준을 정의합니다.
								</p>
								<textarea
									bind:value={memorySummary}
									rows="10"
									class="w-full rounded-xl border border-white/10 bg-bg-primary/60 px-4 py-3 text-sm outline-none focus:border-primary-500"
									placeholder="예: 왕궁 정원에서의 첫 만남, 달빛 아래 고백, 약속한 별빛 산책..."
								></textarea>
							</StudioPanel>
							<StudioPanel title="기억 규칙">
								<div class="space-y-3">
									<div>
										<label class="text-sm text-text-secondary" for="mem-priority">우선 기억</label>
										<textarea
											id="mem-priority"
											bind:value={form.memoryRules.priority}
											rows="3"
											class="mt-1.5 w-full rounded-xl border border-white/10 bg-bg-primary/60 px-4 py-3 text-sm outline-none focus:border-primary-500"
											placeholder="반드시 기억해야 할 사건·인물·약속"
										></textarea>
									</div>
									<div>
										<label class="text-sm text-text-secondary" for="mem-retention">보존 기준</label>
										<textarea
											id="mem-retention"
											bind:value={form.memoryRules.retention}
											rows="3"
											class="mt-1.5 w-full rounded-xl border border-white/10 bg-bg-primary/60 px-4 py-3 text-sm outline-none focus:border-primary-500"
											placeholder="중요도·감정 강도에 따른 기억 유지 규칙"
										></textarea>
									</div>
									<div>
										<label class="text-sm text-text-secondary" for="mem-triggers">저장 트리거</label>
										<textarea
											id="mem-triggers"
											bind:value={form.memoryRules.triggers}
											rows="3"
											class="mt-1.5 w-full rounded-xl border border-white/10 bg-bg-primary/60 px-4 py-3 text-sm outline-none focus:border-primary-500"
											placeholder="기억이 생성되는 조건 (첫 키스, 비밀 고백 등)"
										></textarea>
									</div>
								</div>
							</StudioPanel>
						</div>
					{:else if activeTab === 'relationship'}
						<div class="grid gap-4 lg:grid-cols-2">
							<StudioPanel title="같은 세계관 캐릭터">
								<div class="mb-3 flex items-center gap-2 text-xs text-text-muted">
									<Users class="h-4 w-4" />
									{form.worldName} · {worldPeers.length}명
								</div>
								<div class="space-y-2">
									{#each worldPeers as peer}
										<a
											href="/studio/character"
											class="flex items-center gap-3 rounded-xl border border-white/10 bg-bg-primary/30 px-3 py-2.5 transition hover:bg-white/5"
											onclick={(e) => {
												e.preventDefault();
												selectedId = peer.id;
											}}
										>
											<img src={peer.avatar} alt="" class="h-9 w-9 rounded-full object-cover" />
											<div class="min-w-0">
												<p class="truncate text-sm font-medium">{peer.name}</p>
												<p class="truncate text-[10px] text-text-muted">{peer.title}</p>
											</div>
										</a>
									{:else}
										<p class="text-sm text-text-muted">같은 세계관의 다른 캐릭터가 없습니다.</p>
									{/each}
								</div>
							</StudioPanel>
							<StudioPanel title="관계도 연결">
								<div class="flex flex-col items-start gap-3 text-sm text-text-secondary">
									<p>
										캐릭터 간 관계 유형·친밀도·연결선은 인물 관계도에서 시각적으로 편집할 수 있습니다.
									</p>
									<Button variant="secondary" href="/relationship" class="gap-2">
										<GitBranch class="h-4 w-4" />
										인물 관계도 열기
									</Button>
								</div>
							</StudioPanel>
						</div>
					{:else}
						<div class="grid gap-4 lg:grid-cols-2">
							<StudioPanel title="프로필 미리보기">
								<div class="flex items-start gap-4">
									<img src={form.avatar} alt="" class="h-24 w-24 rounded-2xl bg-bg-card object-cover" />
									<div class="min-w-0">
										<p class="text-xl font-bold">{form.name}</p>
										<p class="text-sm text-text-muted">{form.alias} · {form.occupation || '직업 미설정'}</p>
										<p class="mt-1 text-xs text-primary-300">{form.worldName}</p>
										<div class="mt-2 flex flex-wrap gap-1.5">
											{#each form.tags as t}
												<Badge label={`#${t}`} variant="primary" />
											{/each}
										</div>
									</div>
								</div>
								<p class="mt-4 text-sm leading-relaxed text-text-secondary">{form.shortIntro}</p>
								<div class="mt-4 border-t border-white/5 pt-4">
									<p class="mb-2 text-xs font-semibold text-text-muted">성향</p>
									<PersonalitySliders traits={form.traits} readonly />
								</div>
							</StudioPanel>
							<StudioPanel title="대화 미리보기">
								<div class="space-y-2">
									{#each form.speechPreview as line}
										<div
											class="rounded-xl px-4 py-2.5 text-sm {line.role === 'user'
												? 'ml-8 bg-primary-600/20'
												: 'mr-8 bg-bg-primary/60'}"
										>
											<p class="text-[10px] text-text-muted">{line.role === 'user' ? '유저' : form.name}</p>
											<p class="mt-0.5">{line.content || '…'}</p>
										</div>
									{/each}
								</div>
								{#if form.speechStyle.tone}
									<p class="mt-4 text-xs text-text-muted">어조: {form.speechStyle.tone}</p>
								{/if}
							</StudioPanel>
						</div>
						<div class="mt-4">
							<StudioPanel title="배경 요약">
								<p class="whitespace-pre-wrap text-sm leading-relaxed text-text-secondary">{backgroundPreview}</p>
							</StudioPanel>
						</div>
					{/if}
				</div>
			{:else}
				<div class="flex flex-1 items-center justify-center p-6">
					<div class="rounded-2xl border border-white/10 bg-bg-surface/40 p-8 text-center text-sm text-text-muted">
						캐릭터 데이터를 불러오는 중…
					</div>
				</div>
			{/if}
		</section>
	</div>
</div>
