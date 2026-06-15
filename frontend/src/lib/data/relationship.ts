export type RelationType =
	| 'friend'
	| 'alliance'
	| 'enemy'
	| 'lover'
	| 'family'
	| 'ex_lover'
	| 'neutral';

export type NodeKind = 'character' | 'location' | 'faction' | 'event';

export type GraphNode = {
	id: string;
	label: string;
	kind: NodeKind;
	avatar?: string;
	subtitle?: string;
	tags?: string[];
	age?: number;
	gender?: string;
	race?: string;
	occupation?: string;
	worldId?: string;
	isCenter?: boolean;
};

export type GraphEdge = {
	id: string;
	source: string;
	target: string;
	type: RelationType;
	label: string;
};

export type RelationshipScore = {
	characterId: string;
	name: string;
	type: RelationType;
	score: number;
};

export type RelationshipHistoryItem = {
	id: string;
	title: string;
	date: string;
	summary: string;
};

export const edgeStyles: Record<
	RelationType,
	{ color: string; dash: string; label: string }
> = {
	friend: { color: '#22c55e', dash: '', label: '친구' },
	alliance: { color: '#3b82f6', dash: '', label: '동맹' },
	enemy: { color: '#ef4444', dash: '', label: '적대' },
	lover: { color: '#ec4899', dash: '', label: '연인' },
	family: { color: '#f59e0b', dash: '', label: '가족' },
	ex_lover: { color: '#ec4899', dash: '6 4', label: '전 연인' },
	neutral: { color: '#94a3b8', dash: '', label: '중립' }
};

export const worlds = [
	{ id: 'arcadia', name: '아르카디아 연대기' },
	{ id: 'galaxy', name: '은하 연합 연대기' },
	{ id: 'moonforest', name: '달빛 숲의 전설' }
];

export const graphNodes: GraphNode[] = [
	{
		id: 'elia',
		label: '엘리아',
		kind: 'character',
		subtitle: '아르카디아 왕국',
		tags: ['여성', '21세', '인간', '기사'],
		age: 21,
		gender: '여성',
		race: '인간',
		occupation: '공주',
		avatar: 'https://api.dicebear.com/9.x/notionists/svg?seed=elia&backgroundColor=6366f1',
		isCenter: true,
		worldId: 'arcadia'
	},
	{
		id: 'serena',
		label: '세레나',
		kind: 'character',
		subtitle: '마법사',
		avatar: 'https://api.dicebear.com/9.x/notionists/svg?seed=serena&backgroundColor=8b5cf6'
	},
	{
		id: 'kaion',
		label: '카이온',
		kind: 'character',
		subtitle: '검은 기사단',
		avatar: 'https://api.dicebear.com/9.x/notionists/svg?seed=kaion&backgroundColor=3730a3'
	},
	{
		id: 'iris',
		label: '이리스',
		kind: 'character',
		subtitle: '전 연인',
		avatar: 'https://api.dicebear.com/9.x/notionists/svg?seed=iris&backgroundColor=ec4899'
	},
	{
		id: 'harden',
		label: '하든',
		kind: 'character',
		subtitle: '왕국 대장장이',
		avatar: 'https://api.dicebear.com/9.x/notionists/svg?seed=harden&backgroundColor=475569'
	},
	{
		id: 'yuna',
		label: '유나',
		kind: 'character',
		subtitle: '시녀',
		avatar: 'https://api.dicebear.com/9.x/notionists/svg?seed=yuna&backgroundColor=f59e0b'
	},
	{
		id: 'gabriel',
		label: '가브리엘',
		kind: 'character',
		subtitle: '왕 · 아버지',
		avatar: 'https://api.dicebear.com/9.x/notionists/svg?seed=gabriel&backgroundColor=1e293b'
	},
	{
		id: 'lucas',
		label: '루카스',
		kind: 'character',
		subtitle: '왕국 기사',
		avatar: 'https://api.dicebear.com/9.x/notionists/svg?seed=lucas&backgroundColor=4f46e5'
	},
	{
		id: 'arcadia-castle',
		label: '아르카디아 성',
		kind: 'location',
		subtitle: '장소',
		avatar: 'https://api.dicebear.com/9.x/shapes/svg?seed=castle&backgroundColor=312e81',
		worldId: 'arcadia'
	},
	{
		id: 'kael',
		label: '카엘',
		kind: 'character',
		subtitle: '은하 연합',
		avatar: 'https://api.dicebear.com/9.x/notionists/svg?seed=kael&backgroundColor=4f46e5',
		isCenter: true,
		worldId: 'galaxy'
	},
	{
		id: 'nova-station',
		label: '노바 스테이션',
		kind: 'location',
		subtitle: '우주 정거장',
		avatar: 'https://api.dicebear.com/9.x/shapes/svg?seed=nova&backgroundColor=1e293b',
		worldId: 'galaxy'
	},
	{
		id: 'luna',
		label: '루나',
		kind: 'character',
		subtitle: '달빛 숲',
		avatar: 'https://api.dicebear.com/9.x/notionists/svg?seed=luna&backgroundColor=8b5cf6',
		isCenter: true,
		worldId: 'moonforest'
	}
];

export const graphEdges: GraphEdge[] = [
	{ id: 'e1', source: 'elia', target: 'lucas', type: 'friend', label: '오랜 친구' },
	{ id: 'e2', source: 'elia', target: 'serena', type: 'alliance', label: '동맹' },
	{ id: 'e3', source: 'elia', target: 'kaion', type: 'enemy', label: '적대' },
	{ id: 'e4', source: 'elia', target: 'iris', type: 'ex_lover', label: '전 연인' },
	{ id: 'e5', source: 'elia', target: 'harden', type: 'alliance', label: '협력' },
	{ id: 'e6', source: 'elia', target: 'yuna', type: 'friend', label: '친밀' },
	{ id: 'e7', source: 'elia', target: 'gabriel', type: 'family', label: '부녀' },
	{ id: 'e8', source: 'elia', target: 'arcadia-castle', type: 'neutral', label: '소속' },
	{ id: 'e9', source: 'kael', target: 'nova-station', type: 'neutral', label: '주둔' }
];

export const eliaRelationships: RelationshipScore[] = [
	{ characterId: 'lucas', name: '루카스', type: 'friend', score: 82 },
	{ characterId: 'serena', name: '세레나', type: 'alliance', score: 74 },
	{ characterId: 'yuna', name: '유나', type: 'friend', score: 68 },
	{ characterId: 'harden', name: '하든', type: 'alliance', score: 55 },
	{ characterId: 'gabriel', name: '가브리엘', type: 'family', score: 45 },
	{ characterId: 'iris', name: '이리스', type: 'ex_lover', score: 38 },
	{ characterId: 'kaion', name: '카이온', type: 'enemy', score: 15 }
];

export const relationshipHistory: RelationshipHistoryItem[] = [
	{
		id: 'rh1',
		title: '왕궁 정원에서 첫 대면',
		date: '1012.03.12',
		summary: '엘리아와 루카스가 정원에서 처음 마주쳤다.'
	},
	{
		id: 'rh2',
		title: '검은 기사단과의 대립',
		date: '1012.05.28',
		summary: '카이온과의 충돌로 신뢰가 크게 하락했다.'
	},
	{
		id: 'rh3',
		title: '달빛 아래의 화해',
		date: '1012.06.14',
		summary: '이리스와의 과거를 넘어선 새로운 인연의 시작.'
	}
];

export function getNode(id: string): GraphNode | undefined {
	return graphNodes.find((n) => n.id === id);
}

export function getEdgesForNode(nodeId: string): GraphEdge[] {
	return graphEdges.filter((e) => e.source === nodeId || e.target === nodeId);
}
