// 타입 정의 전용 파일 (실데이터 전환 후)

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
	studioMeta?: Record<string, unknown>;
};

export type World = {
	id: string;
	name: string;
	genre: string[];
	characterCount: number;
	cover: string;
	studioMeta?: Record<string, unknown>;
};

export type ChatMessage = {
	id: string;
	role: 'user' | 'character' | 'narration' | 'system';
	content: string;
	timestamp?: string;
	isStreaming?: boolean;
	emotionDelta?: string;
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

export type CharacterScenario = {
	id: string;
	title: string;
	description: string;
};

