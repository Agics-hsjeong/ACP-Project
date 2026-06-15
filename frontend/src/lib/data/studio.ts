import { characters, worlds } from './mock';

export type StudioTab =
	| 'basic'
	| 'personality'
	| 'speech'
	| 'memory'
	| 'relationship'
	| 'preview';

export type PersonalityTrait = {
	key: string;
	label: string;
	value: number;
};

export type StudioCharacter = {
	id: string;
	name: string;
	alias: string;
	age: number;
	gender: string;
	race: string;
	occupation: string;
	affiliation: string;
	worldId: string;
	worldName: string;
	shortIntro: string;
	tags: string[];
	avatar: string;
	traits: PersonalityTrait[];
	background: {
		origin: string;
		goal: string;
		trauma: string;
		hidden: string;
	};
	fewShots: { role: 'user' | 'character'; content: string }[];
	forbidden: string[];
	speechPreview: { role: 'user' | 'character'; content: string }[];
};

export type WorldTab =
	| 'overview'
	| 'nation'
	| 'faction'
	| 'location'
	| 'event'
	| 'timeline'
	| 'law'
	| 'memo';

export type WorldFaction = {
	id: string;
	name: string;
	alignment: string;
	description: string;
	power: number;
	icon: string;
};

export type WorldTheme = {
	id: string;
	title: string;
	color: string;
};

export type WorldEra = {
	id: string;
	name: string;
	range: string;
	subtitle: string;
};

export type WorldLaw = {
	id: string;
	title: string;
	description: string;
	icon: string;
};

export type WorldEvent = {
	id: string;
	year: number;
	name: string;
	category: string;
	categoryColor: string;
};

const defaultTraits: PersonalityTrait[] = [
	{ key: 'extro', label: '외향성', value: 80 },
	{ key: 'rational', label: '이성', value: 30 },
	{ key: 'cold', label: '냉담함', value: 25 },
	{ key: 'caution', label: '신중함', value: 20 },
	{ key: 'humble', label: '겸손함', value: 70 }
];

export const studioCharacters: StudioCharacter[] = characters.slice(0, 6).map((c, i) => ({
	id: c.id,
	name: c.name,
	alias: c.title.split(' ').pop() ?? c.title,
	age: c.age ?? 20 + i,
	gender: c.gender ?? (c.tags.includes('여성') ? '여성' : '남성'),
	race: c.race,
	occupation: c.occupation,
	affiliation: c.world,
	worldId: c.worldId ?? 'arcadia',
	worldName: c.world,
	shortIntro: c.description,
	tags: c.tags,
	avatar: c.avatar,
	traits: defaultTraits.map((t) => ({ ...t, value: t.value + (i % 3) * 5 - 5 })),
	background: {
		origin:
			i === 0
				? '아르카디아 왕실에서 태어나 어린 시절부터 기사 수련을 받았다.'
				: `${c.name}의 고향과 유년 시절에 대한 배경 설정.`,
		goal: i === 0 ? '왕국을 수호하고 진정한 자아를 찾는 것' : '자신만의 목표를 향해 나아간다.',
		trauma: i === 0 ? '어린 시절 왕실 내 권력 다툼으로 인한 고립감' : '과거의 상처와 아픔.',
		hidden: i === 0 ? '달빛 아래에서만 드러나는 부드러운 내면' : '겉으로 드러나지 않는 비밀.'
	},
	fewShots:
		i === 0
			? [
					{ role: 'user', content: '오늘 기분이 어때요?' },
					{
						role: 'character',
						content: '…별로예요. 왕궁은 화려하지만, 때로는 이 탑이 더 편안하죠.'
					}
				]
			: [
					{ role: 'user', content: '안녕하세요.' },
					{ role: 'character', content: `안녕하세요. 저는 ${c.name}입니다.` }
				],
	forbidden: [
		'유저를 모욕하거나 비하하지 않는다',
		'갑작스러운 성격 변화를 하지 않는다',
		'설정에 없는 능력을 사용하지 않는다'
	],
	speechPreview:
		i === 0
			? [
					{ role: 'user', content: '밤하늘이 정말 아름답네요.' },
					{
						role: 'character',
						content: '…그렇게 말해주시니, 조금은 마음이 따뜻해지네요.'
					}
				]
			: [
					{ role: 'user', content: '잘 지내고 있어?' },
					{ role: 'character', content: '응, 네 덕분에 괜찮아.' }
				]
}));

export const characterStudioTabs: { id: StudioTab; label: string }[] = [
	{ id: 'basic', label: '기본 정보' },
	{ id: 'personality', label: '성격·배경' },
	{ id: 'speech', label: '말투·스타일' },
	{ id: 'memory', label: '기억 규칙' },
	{ id: 'relationship', label: '관계 설정' },
	{ id: 'preview', label: '미리보기' }
];

export const arcadiaWorld = {
	id: 'arcadia',
	name: '아르카디아 연대기',
	genre: ['하이 판타지', '마법', '중세', '정치'],
	oneLiner: '신과 인간, 마법과 과학이 충돌하는 대륙의 연대기',
	description:
		'아르카디아 대륙은 다섯 왕국과 수많은 세력이 경쟁하는 판타지 세계입니다. 고대 신들의 유산이 남아 있으며, 마법과 검술이 공존합니다. 왕실의 음모, 종교의 권력, 엘프와 드워프의 오랜 갈등이 이야기의 중심을 이룹니다.',
	mapImage:
		'https://api.dicebear.com/9.x/shapes/svg?seed=arcadia-map&backgroundColor=312e81&scale=80',
	gallery: [
		'https://api.dicebear.com/9.x/shapes/svg?seed=arc1&backgroundColor=4338ca',
		'https://api.dicebear.com/9.x/shapes/svg?seed=arc2&backgroundColor=6366f1',
		'https://api.dicebear.com/9.x/shapes/svg?seed=arc3&backgroundColor=4f46e5',
		'https://api.dicebear.com/9.x/shapes/svg?seed=arc4&backgroundColor=3730a3'
	]
};

export const worldFactions: WorldFaction[] = [
	{
		id: 'holy',
		name: '신성 제국',
		alignment: '질서 중립',
		description: '대륙 중앙을 지배하는 신성 왕국. 성기사단을 두고 있다.',
		power: 12,
		icon: '⚔️'
	},
	{
		id: 'elf',
		name: '엘프 동맹',
		alignment: '혼돈 선',
		description: '고대 숲을 수호하는 엘프 연합. 자연 마법에 능하다.',
		power: 8,
		icon: '🌿'
	},
	{
		id: 'free',
		name: '자유 연합',
		alignment: '혼돈 중립',
		description: '상인과 모험가가 모인 도시 연합. 중립을 지킨다.',
		power: 9,
		icon: '⚓'
	},
	{
		id: 'dwarf',
		name: '드워프 왕국',
		alignment: '질서 선',
		description: '산악 지대의 대장장이 왕국. 최고의 무기를 생산한다.',
		power: 7,
		icon: '⛏️'
	}
];

export const worldThemes: WorldTheme[] = [
	{ id: 't1', title: '신과 인간의 갈등', color: '#ef4444' },
	{ id: 't2', title: '마법 vs 과학', color: '#8b5cf6' },
	{ id: 't3', title: '왕실의 음모', color: '#f59e0b' },
	{ id: 't4', title: '종족 간 화해', color: '#22c55e' }
];

export const worldEras: WorldEra[] = [
	{ id: 'e1', name: '고대', range: 'BC 3000~', subtitle: '신들의 시대' },
	{ id: 'e2', name: '신화', range: 'BC 500~', subtitle: '영웅의 전설' },
	{ id: 'e3', name: '제국', range: 'AD 0~800', subtitle: '통일 왕국' },
	{ id: 'e4', name: '분열', range: 'AD 800~1200', subtitle: '다섯 왕국' },
	{ id: 'e5', name: '탐험', range: 'AD 1200~1500', subtitle: '대항해' },
	{ id: 'e6', name: '혼돈', range: 'AD 1500~', subtitle: '현재' }
];

export const worldLaws: WorldLaw[] = [
	{
		id: 'l1',
		title: '마법의 법칙',
		description: '모든 마법은 마나를 소모하며, 과도한 사용은 역효과를 낳는다.',
		icon: '✨'
	},
	{
		id: 'l2',
		title: '신의 법칙',
		description: '신들은 직접 개입하지 않으나, 신탁을 통해 세계에 영향을 미친다.',
		icon: '☀️'
	},
	{
		id: 'l3',
		title: '역사의 법칙',
		description: '과거의 사건은 현재에 반드시 영향을 미친다. 시간 역행은 불가능하다.',
		icon: '📜'
	},
	{
		id: 'l4',
		title: '생명의 법칙',
		description: '죽은 자는 되살릴 수 없으나, 영혼은 다른 차원으로 이동한다.',
		icon: '💫'
	}
];

export const worldEvents: WorldEvent[] = [
	{ id: 'ev1', year: -1200, name: '대분열 전쟁', category: '전쟁', categoryColor: '#ef4444' },
	{ id: 'ev2', year: -800, name: '신성 제국 건국', category: '정치', categoryColor: '#f59e0b' },
	{ id: 'ev3', year: -200, name: '엘프-인간 협정', category: '외교', categoryColor: '#22c55e' },
	{ id: 'ev4', year: 342, name: '마법 대학 설립', category: '탐험', categoryColor: '#6366f1' },
	{ id: 'ev5', year: 891, name: '붉은 사막 전쟁', category: '전쟁', categoryColor: '#ef4444' }
];

export const worldStudioTabs: { id: WorldTab; label: string }[] = [
	{ id: 'overview', label: '개요' },
	{ id: 'nation', label: '국가' },
	{ id: 'faction', label: '세력' },
	{ id: 'location', label: '장소' },
	{ id: 'event', label: '사건' },
	{ id: 'timeline', label: '연대표' },
	{ id: 'law', label: '절대 법칙' },
	{ id: 'memo', label: '메모' }
];

export const studioWorlds = worlds;
