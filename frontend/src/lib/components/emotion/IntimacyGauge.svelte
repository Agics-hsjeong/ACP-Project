<script lang="ts">
	interface Props {
		value: number;
		label?: string;
		size?: number;
	}

	let { value, label = '친밀도', size = 120 }: Props = $props();

	const radius = 42;
	const circumference = 2 * Math.PI * radius;
	const offset = $derived(circumference - (value / 100) * circumference);
</script>

<div class="flex flex-col items-center gap-2">
	<div class="relative" style="width: {size}px; height: {size}px">
		<svg class="-rotate-90" width={size} height={size} viewBox="0 0 100 100">
			<circle cx="50" cy="50" r={radius} fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="8" />
			<circle
				cx="50"
				cy="50"
				r={radius}
				fill="none"
				stroke="url(#gauge-gradient)"
				stroke-width="8"
				stroke-linecap="round"
				stroke-dasharray={circumference}
				stroke-dashoffset={offset}
				class="transition-all duration-700"
			/>
			<defs>
				<linearGradient id="gauge-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
					<stop offset="0%" stop-color="#6366f1" />
					<stop offset="100%" stop-color="#ec4899" />
				</linearGradient>
			</defs>
		</svg>
		<div class="absolute inset-0 flex flex-col items-center justify-center">
			<span class="text-2xl font-bold">{value}</span>
		</div>
	</div>
	<p class="text-xs text-text-muted">{label}</p>
</div>
