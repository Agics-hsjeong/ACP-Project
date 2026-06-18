<script lang="ts">
	import MockPanel from '$lib/components/mockup/MockPanel.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import { getLoginUrl } from '$lib/auth/access';
	import { Compass, LogIn, Sparkles } from 'lucide-svelte';
</script>

<aside class="sticky top-6 flex w-[400px] shrink-0 flex-col gap-4 self-start">
	<MockPanel class="border-mock-accent/20 bg-mock-accent/5">
		<div class="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-mock-accent/15">
			<Sparkles class="h-6 w-6 text-mock-accent" />
		</div>
		<h3 class="text-lg font-semibold">지금은 둘러보기 모드입니다</h3>
		<p class="mt-2 text-sm leading-relaxed text-text-secondary">
			홈·탐색·캐릭터 상세는 로그인 없이 볼 수 있습니다. 대화, 기억, 관계도, 스튜디오는 로그인 후
			이용할 수 있어요.
		</p>
		<div class="mt-5 flex flex-col gap-2">
			<Button href={getLoginUrl('/home')} fullWidth>
				<LogIn class="h-4 w-4" />
				로그인 / 회원가입
			</Button>
			<Button variant="secondary" href="/explore" fullWidth>
				<Compass class="h-4 w-4" />
				캐릭터 더 둘러보기
			</Button>
		</div>
	</MockPanel>

	<MockPanel title="로그인 후 이용 가능">
		<ul class="space-y-2 text-xs text-text-muted">
			<li>· 캐릭터와 실시간 대화</li>
			<li>· 기억 보관소 & 감정 분석</li>
			<li>· 인물 관계도 편집</li>
			<li>· 캐릭터·세계관 스튜디오</li>
		</ul>
	</MockPanel>
</aside>
