<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import { Sparkles, Shield, Brain, Globe } from 'lucide-svelte';

	let tab = $state<'email' | 'phone'>('email');
	let showPassword = $state(false);
</script>

<svelte:head>
	<title>로그인 — AI Character Playground</title>
</svelte:head>

<div class="relative min-h-screen">
	<img src="/images/login-bg.png" alt="" class="absolute inset-0 h-full w-full object-cover" />
	<div class="absolute inset-0 bg-bg-primary/75 backdrop-blur-[2px]"></div>

	<header class="relative z-10 flex items-center justify-between px-8 py-5">
		<a href="/landing" class="flex items-center gap-2">
			<Sparkles class="h-5 w-5 text-primary-400" />
			<span class="font-semibold">AI Character Playground</span>
		</a>
		<button class="rounded-lg border border-white/20 px-3 py-1.5 text-sm text-text-secondary">
			🌐 한국어 ▾
		</button>
	</header>

	<main class="relative z-10 mx-auto grid max-w-6xl items-start gap-12 px-8 py-8 lg:grid-cols-2 lg:py-12">
		<div class="pt-8">
			<h1 class="text-3xl font-bold leading-snug md:text-4xl">
				AI와 함께하는<br />무한한 이야기의 세계
			</h1>
			<p class="mt-4 max-w-md text-text-secondary">
				상상 속 인물들이 살아 숨 쉬는 공간, 당신만의 이야기를 지금 시작하세요.
			</p>
		</div>

		<div class="glass rounded-2xl p-8 shadow-xl">
			<h2 class="text-2xl font-bold">로그인</h2>
			<p class="mt-1 text-sm text-text-muted">AI Character Playground에 오신 것을 환영합니다</p>

			<div class="mt-6 flex rounded-xl bg-bg-primary/50 p-1">
				<button
					class="flex-1 rounded-lg py-2 text-sm transition {tab === 'email'
						? 'bg-primary-600 text-white'
						: 'text-text-muted'}"
					onclick={() => (tab = 'email')}
				>
					이메일 로그인
				</button>
				<button
					class="flex-1 rounded-lg py-2 text-sm transition {tab === 'phone'
						? 'bg-primary-600 text-white'
						: 'text-text-muted'}"
					onclick={() => (tab = 'phone')}
				>
					휴대폰 로그인
				</button>
			</div>

			<form class="mt-6 space-y-4" onsubmit={(e) => e.preventDefault()}>
				{#if tab === 'email'}
					<Input label="이메일" type="email" placeholder="이메일 주소를 입력하세요" />
					<div class="relative">
						<Input
							label="비밀번호"
							type={showPassword ? 'text' : 'password'}
							placeholder="비밀번호를 입력하세요"
						/>
						<button
							type="button"
							class="absolute right-3 top-9 text-xs text-text-muted"
							onclick={() => (showPassword = !showPassword)}
						>
							{showPassword ? '숨기기' : '보기'}
						</button>
					</div>
				{:else}
					<Input label="휴대폰 번호" type="tel" placeholder="010-0000-0000" />
					<Input label="인증번호" placeholder="인증번호 6자리" />
				{/if}

				<div class="flex items-center justify-between text-sm">
					<label class="flex items-center gap-2 text-text-secondary">
						<input type="checkbox" class="rounded border-white/20" />
						로그인 상태 유지
					</label>
					<span class="cursor-pointer text-primary-400 hover:underline">비밀번호 찾기</span>
				</div>

				<Button href="/home" fullWidth size="lg">로그인</Button>
			</form>

			<div class="my-6 flex items-center gap-3 text-xs text-text-muted">
				<span class="h-px flex-1 bg-white/10"></span>
				또는
				<span class="h-px flex-1 bg-white/10"></span>
			</div>

			<div class="space-y-2">
				<Button variant="social-google" fullWidth>Google로 계속하기</Button>
				<Button variant="social-apple" fullWidth>Apple로 계속하기</Button>
				<Button variant="social-discord" fullWidth>Discord로 계속하기</Button>
			</div>

			<p class="mt-6 text-center text-sm text-text-muted">
				계정이 없으신가요?
				<span class="cursor-pointer text-primary-400 hover:underline">회원가입</span>
			</p>
		</div>
	</main>

	<footer class="relative z-10 border-t border-white/10 px-8 py-10">
		<div class="mx-auto grid max-w-6xl gap-8 md:grid-cols-2">
			<div>
				<p class="text-lg italic text-text-secondary">"모든 이야기는 인연에서 시작된다."</p>
				<div class="mt-3 flex gap-2">
					{#each [0, 1, 2, 3] as i}
						<span class="h-2 w-2 rounded-full {i === 0 ? 'bg-primary-500' : 'bg-white/20'}"></span>
					{/each}
				</div>
			</div>
			<div class="grid gap-4 sm:grid-cols-3">
				{#each [
					{ icon: Shield, title: '안전한 데이터 보호', desc: '엔드투엔드 암호화로 대화를 보호합니다.' },
					{ icon: Brain, title: '지속적 메모리 시스템', desc: 'AI가 당신과의 순간을 기억합니다.' },
					{ icon: Globe, title: '무한한 상상력', desc: '세계관과 캐릭터를 자유롭게 창작하세요.' }
				] as feature}
					<div class="text-center">
						<feature.icon class="mx-auto h-6 w-6 text-primary-400" />
						<p class="mt-2 text-sm font-medium">{feature.title}</p>
						<p class="mt-1 text-xs text-text-muted">{feature.desc}</p>
					</div>
				{/each}
			</div>
		</div>
		<p class="mt-8 text-center text-xs text-text-muted">
			© 2024 AI Character Playground. All rights reserved. · 이용약관 | 개인정보처리방침 | 고객센터
		</p>
	</footer>
</div>
