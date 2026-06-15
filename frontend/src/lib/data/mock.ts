export type Character = {
	id: string;
	name: string;
	title: string;
	world: string;
	worldId?: string;
	tags: string[];
	genre?: string[];
	likes: number;
	views: number;
	description: string;
	personality: string[];
	occupation: string;
	race: string;
	age?: number;
	gender?: string;
	quote?: string;
	memorySummary?: string;
	avatar: string;
	cover: string;
};

export type World = {
	id: string;
	name: string;
	genre: string[];
	characterCount: number;
	cover: string;
};

export type ChatMessage = {
	id: string;
	role: 'user' | 'character' | 'narration' | 'system';
	content: string;
	timestamp?: string;
	/** 스트리밍 중인 캐릭터 응답 */
	isStreaming?: boolean;
	/** 감정 변화 인라인 피드백 (예: 애정 +3) */
	emotionDelta?: string;
	/** 선물·행동 등 인터랙션 유형 */
	interactionType?: 'action' | 'expression' | 'gift' | 'record';
};

export type Memory = {
	id: string;
	title: string;
	summary: string;
	detail?: string;
	emotion: string;
	date: string;
	importance: 'high' | 'medium' | 'low';
	tags?: string[];
	quote?: string;
	location?: string;
	thumbnail?: string;
	characterId?: string;
	dday?: number;
	stats?: { affection?: number; trust?: number; respect?: number };
};

export type UserProfile = {
	name: string;
	level: number;
	xp: number;
	xpMax: number;
	avatar: string;
	stats: {
		charactersCreated: number;
		worldsCreated: number;
		totalChats: number;
		savedMemories: number;
	};
};

export const memoryStats = {
	total: 142,
	important: 34,
	daysTogether: 128,
	storyVolume: '382K'
};

export const userProfile: UserProfile = {
	name: 'Creator',
	level: 28,
	xp: 65,
	xpMax: 100,
	avatar: 'https://api.dicebear.com/9.x/notionists/svg?seed=creator&backgroundColor=6366f1',
	stats: {
		charactersCreated: 12,
		worldsCreated: 3,
		totalChats: 248,
		savedMemories: 142
	}
};

export type MemoryFragment = {
	id: string;
	title: string;
	date: string;
	delta: string;
	importance: 'high' | 'medium' | 'low';
	thumbnail?: string;
};

export type EmotionAxis = {
	key: string;
	label: string;
	value: number;
	color: string;
};

export const characters: Character[] = [
	{
		id: 'elia',
		name: '엘리아',
		title: '아르카디아 왕국의 공주',
		world: '아르카디아 연대기',
		worldId: 'arcadia',
		tags: ['여성', '2세', '왕족', '츤데레', '기사'],
		genre: ['판타지', '로맨스'],
		likes: 98,
		views: 12400,
		description:
			'차가운 외면과 따뜻한 내면을 가진 아르카디아 왕국의 공주. 달빛 아래 성에서 홀로 시간을 보내는 것을 좋아한다.',
		personality: ['차분함', '지적', '호기심', '고독'],
		occupation: '공주',
		race: '인간',
		age: 21,
		gender: '여성',
		quote: '"밤하늘을 함께 바라볼 수 있다면, 왕궁의 고독도 견딜 수 있을 것 같아요."',
		memorySummary: '달빛 아래의 대화, 왕궁 정원에서의 첫 만남, 비밀의 도서관 탐험',
		avatar: 'https://api.dicebear.com/9.x/notionists/svg?seed=elia&backgroundColor=6366f1',
		cover: 'https://api.dicebear.com/9.x/shapes/svg?seed=elia-world&backgroundColor=312e81'
	},
	{
		id: 'kael',
		name: '카엘',
		title: '은하 연합의 파일럿',
		world: '은하 연합 연대기',
		tags: ['남성', 'SF', '전투'],
		likes: 92,
		views: 9800,
		description: '냉철한 판단력을 가진 은하 연합 최연소 파일럿. 동료를 위해 목숨을 걸 수 있는 용기를 지녔다.',
		personality: ['냉정', '책임감', '유머'],
		occupation: '파일럿',
		race: '인간',
		avatar: 'https://api.dicebear.com/9.x/notionists/svg?seed=kael&backgroundColor=4f46e5',
		cover: 'https://api.dicebear.com/9.x/shapes/svg?seed=kael-world&backgroundColor=1e293b'
	},
	{
		id: 'luna',
		name: '루나',
		title: '달빛 숲의 수호자',
		world: '달빛 숲의 전설',
		tags: ['여성', '판타지', '엘프'],
		likes: 95,
		views: 11200,
		description: '고대 숲을 지키는 엘프 수호자. 자연과 교감하며 잃어버린 기억을 찾고 있다.',
		personality: ['신비로움', '온화', '결단력'],
		occupation: '수호자',
		race: '엘프',
		avatar: 'https://api.dicebear.com/9.x/notionists/svg?seed=luna&backgroundColor=8b5cf6',
		cover: 'https://api.dicebear.com/9.x/shapes/svg?seed=luna-world&backgroundColor=4338ca'
	},
	{
		id: 'rex',
		name: '렉스',
		title: '네온 시티의 해커',
		world: '네온 시티 2087',
		tags: ['남성', '사이버펑크', '해커'],
		likes: 88,
		views: 7600,
		description: '거대 기업의 비밀을 파헤치는 전설의 해커. 냉소적이지만 정의감이 있다.',
		personality: ['냉소적', '영리', '충성'],
		occupation: '해커',
		race: '사이보그',
		avatar: 'https://api.dicebear.com/9.x/notionists/svg?seed=rex&backgroundColor=06b6d4',
		cover: 'https://api.dicebear.com/9.x/shapes/svg?seed=rex-world&backgroundColor=0f172a'
	},
	{
		id: 'mira',
		name: '미라',
		title: '마법 학원의 신입',
		world: '아르카디아 연대기',
		tags: ['여성', '마법', '신입'],
		likes: 90,
		views: 8900,
		description: '마법 재능은 뛰어나지만 자신감이 부족한 신입 마법사. 엘리아와 우연히 만나게 된다.',
		personality: ['수줍음', '성실', '호기심'],
		occupation: '마법사',
		race: '인간',
		avatar: 'https://api.dicebear.com/9.x/notionists/svg?seed=mira&backgroundColor=ec4899',
		cover: 'https://api.dicebear.com/9.x/shapes/svg?seed=mira-world&backgroundColor=334155'
	},
	{
		id: 'draven',
		name: '드레이븐',
		title: '어둠의 기사단장',
		world: '어둠의 성채',
		tags: ['남성', '다크판타지', '기사'],
		likes: 85,
		views: 6500,
		description: '타락한 기사단을 이끄는 수수께끼의 인물. 과거의 죄책감에 사로잡혀 있다.',
		personality: ['냉혹', '고독', '명예'],
		occupation: '기사단장',
		race: '인간',
		avatar: 'https://api.dicebear.com/9.x/notionists/svg?seed=draven&backgroundColor=3730a3',
		cover: 'https://api.dicebear.com/9.x/shapes/svg?seed=draven-world&backgroundColor=1e293b'
	}
];

export const worlds: World[] = [
	{
		id: 'arcadia',
		name: '아르카디아 연대기',
		genre: ['판타지', '중세'],
		characterCount: 24,
		cover: 'https://api.dicebear.com/9.x/shapes/svg?seed=arcadia&backgroundColor=4338ca'
	},
	{
		id: 'galaxy',
		name: '은하 연합 연대기',
		genre: ['SF', '우주'],
		characterCount: 18,
		cover: 'https://api.dicebear.com/9.x/shapes/svg?seed=galaxy&backgroundColor=1e293b'
	},
	{
		id: 'moonforest',
		name: '달빛 숲의 전설',
		genre: ['판타지', '자연'],
		characterCount: 12,
		cover: 'https://api.dicebear.com/9.x/shapes/svg?seed=moonforest&backgroundColor=312e81'
	},
	{
		id: 'neon',
		name: '네온 시티 2087',
		genre: ['사이버펑크', '스릴러'],
		characterCount: 15,
		cover: 'https://api.dicebear.com/9.x/shapes/svg?seed=neon&backgroundColor=06b6d4'
	}
];

export const recentChats = [
	{ id: 'elia', name: '엘리아', preview: '오늘 밤 달이 참 아름답네요...', time: '2분 전' },
	{ id: 'kael', name: '카엘', preview: '다음 미션 브리핑 준비됐어.', time: '15분 전' },
	{ id: 'luna', name: '루나', preview: '숲 깊은 곳에서 이상한 기운이...', time: '1시간 전' },
	{ id: 'rex', name: '렉스', preview: '데이터 누출 흔적 찾았어.', time: '3시간 전' },
	{ id: 'mira', name: '미라', preview: '마법 시험... 떨려요.', time: '어제' }
];

export const chatMessages: ChatMessage[] = [
	{
		id: '1',
		role: 'narration',
		content: '달빛이 성의 창문을 통해 스며들었다. 엘리아는 창밖의 별빛을 바라보며 한숨을 쉬었다.'
	},
	{
		id: '2',
		role: 'character',
		content: '또 이런 밤이네요... 왕궁은 화려하지만, 때로는 이 탑이 더 편안해요.',
		timestamp: '오후 9:32'
	},
	{
		id: '3',
		role: 'user',
		content: '밤하늘이 정말 아름답네요. 같이 보면 더 좋을 것 같아요.',
		timestamp: '오후 9:33'
	},
	{
		id: '4',
		role: 'character',
		content: '...그렇게 말해주시니, 조금은 마음이 따뜻해지네요. 당신과 함께라면 이 밤이 덜 외로울 것 같아요.',
		timestamp: '오후 9:34'
	},
	{
		id: '5',
		role: 'system',
		content: '✦ 기억이 저장되었습니다 — [달빛 아래의 대화]'
	},
	{
		id: '6',
		role: 'narration',
		content: '엘리아의 눈가에 미세한 미소가 떠올랐다.'
	}
];

export const memories: Memory[] = [
	{
		id: '1',
		title: '달빛 아래의 대화',
		summary: '성 탑에서 엘리아와 밤하늘을 함께 바라보며 깊은 대화를 나눴다.',
		detail:
			'왕궁의 화려함과 달리 고요한 탑 방에서 엘리아는 처음으로 진심을 털어놓았다. 달빛이 창문을 비추는 가운데, 두 사람은 말없이 하늘을 바라보았다.',
		emotion: '애정 +15',
		date: '2026-06-14',
		importance: 'high',
		tags: ['#달빛', '#탑', '#고백'],
		quote: '"당신과 함께라면 이 밤이 덜 외로울 것 같아요."',
		location: '아르카디아 성 탑',
		characterId: 'elia',
		dday: 1,
		stats: { affection: 15, trust: 8 }
	},
	{
		id: '2',
		title: '첫 만남 — 왕궁 정원',
		summary: '정원에서 우연히 마주친 엘리아. 차가운 첫인상과 달리 호기심 어린 눈빛.',
		detail:
			'왕궁 정원의 장미 덤불 사이에서 마주친 엘리아. 처음에는 냉담했지만, 당신의 관심에 조금씩 마음을 열기 시작했다.',
		emotion: '신뢰 +10',
		date: '2026-06-10',
		importance: 'high',
		tags: ['#첫만남', '#정원', '#왕궁'],
		quote: '"…누구시죠? 이곳은 일반인이 들어올 수 없는 곳인데."',
		location: '왕궁 정원',
		characterId: 'elia',
		dday: 5,
		stats: { trust: 10, respect: 5 }
	},
	{
		id: '3',
		title: '비밀의 도서관',
		summary: '금서 구역에서 함께 고대 마법서를 발견했다.',
		detail: '금지된 구역에 함께 들어간 두 사람. 고대 마법서의 비밀을 공유하며 신뢰가 깊어졌다.',
		emotion: '존경 +8',
		date: '2026-06-08',
		importance: 'medium',
		tags: ['#도서관', '#마법', '#비밀'],
		location: '왕궁 비밀 도서관',
		characterId: 'elia',
		dday: 7,
		stats: { respect: 8, trust: 5 }
	},
	{
		id: '4',
		title: '왕실 연회',
		summary: '연회장에서 엘리아의 외로운 모습을 목격했다.',
		emotion: '애정 +5',
		date: '2026-06-05',
		importance: 'medium',
		tags: ['#연회', '#외로움'],
		characterId: 'elia',
		dday: 10,
		stats: { affection: 5 }
	},
	{
		id: '5',
		title: '비 오는 날의 약속',
		summary: '다음에 다시 만나자는 약속을 나눴다.',
		emotion: '신뢰 +12',
		date: '2026-06-01',
		importance: 'low',
		tags: ['#약속', '#비'],
		characterId: 'elia',
		dday: 14,
		stats: { trust: 12 }
	}
];

export const emotions: EmotionAxis[] = [
	{ key: 'affection', label: '애정', value: 72, color: '#ec4899' },
	{ key: 'trust', label: '신뢰', value: 65, color: '#6366f1' },
	{ key: 'respect', label: '존경', value: 58, color: '#8b5cf6' },
	{ key: 'anger', label: '분노', value: 12, color: '#ef4444' },
	{ key: 'fear', label: '공포', value: 8, color: '#94a3b8' },
	{ key: 'jealousy', label: '질투', value: 15, color: '#f59e0b' }
];

/** 30일 감정 추이 mock (애정, 신뢰, 분노) */
export const emotionTrend = Array.from({ length: 14 }, (_, i) => ({
	day: i + 1,
	affection: 55 + i * 1.2 + Math.sin(i) * 3,
	trust: 48 + i * 1.1 + Math.cos(i) * 2,
	anger: 18 - i * 0.4 + Math.sin(i * 2) * 2
}));

export const exploreGenres = [
	'전체',
	'판타지',
	'현대',
	'SF',
	'로맨스',
	'학원',
	'무협',
	'미스터리',
	'일상'
];

export const exploreTags = [
	'츤데레',
	'얀데레',
	'집착',
	'순정',
	'츤츤',
	'마법',
	'검술',
	'왕족',
	'기사',
	'엘프',
	'해커',
	'SF',
	'학원',
	'츤',
	'다정'
];

export const memoryFragments: MemoryFragment[] = [
	{
		id: 'f1',
		title: '첫 만남의 날',
		date: '2026-06-10',
		delta: '신뢰 +10',
		importance: 'high'
	},
	{
		id: 'f2',
		title: '달빛 아래의 대화',
		date: '2026-06-14',
		delta: '애정 +15',
		importance: 'high'
	},
	{
		id: 'f3',
		title: '비밀의 도서관',
		date: '2026-06-08',
		delta: '존경 +8',
		importance: 'medium'
	}
];

export function getCharacter(id: string): Character | undefined {
	return characters.find((c) => c.id === id);
}
