import type { Character, World } from '$lib/data/mock';
import type { PersonalityTrait, StudioCharacter } from '$lib/data/studio';
import { defaultCharacterStudioMeta, defaultWorldStudioMeta } from '$lib/data/studio';

export function characterToStudioForm(c: Character): StudioCharacter {
	const meta = (c.studioMeta ?? {}) as Record<string, unknown>;
	const defaults = defaultCharacterStudioMeta();
	const traits = (meta.traits as PersonalityTrait[]) ?? defaults.traits;
	const background = (meta.background as StudioCharacter['background']) ?? defaults.background;
	const speechStyle =
		(meta.speech_style as StudioCharacter['speechStyle']) ??
		(meta.speechStyle as StudioCharacter['speechStyle']) ??
		defaults.speechStyle;
	const memoryRules =
		(meta.memory_rules as StudioCharacter['memoryRules']) ??
		(meta.memoryRules as StudioCharacter['memoryRules']) ??
		defaults.memoryRules;

	return {
		id: c.id,
		name: c.name,
		alias: String(meta.alias ?? c.title.split(' ').pop() ?? ''),
		age: c.age ?? 20,
		gender: c.gender ?? '',
		race: c.race,
		occupation: c.occupation,
		affiliation: c.world,
		worldId: c.worldId ?? 'arcadia',
		worldName: c.world,
		shortIntro: c.description,
		tags: c.tags,
		avatar: c.avatar,
		traits: traits.map((t) => ({ ...t })),
		background: { ...background },
		fewShots: ((meta.few_shots ?? meta.fewShots) as StudioCharacter['fewShots']) ?? [],
		forbidden: (meta.forbidden as string[]) ?? defaults.forbidden,
		speechPreview:
			((meta.speech_preview ?? meta.speechPreview) as StudioCharacter['speechPreview']) ??
			defaults.speechPreview,
		speechStyle: { ...speechStyle },
		memoryRules: { ...memoryRules }
	};
}

export function studioFormToCharacterPatch(
	form: StudioCharacter,
	base: Character,
	memorySummary = ''
) {
	return {
		name: form.name,
		title: form.alias || form.name,
		world_id: form.worldId,
		description: form.shortIntro,
		tags: form.tags,
		occupation: form.occupation,
		race: form.race,
		age: form.age,
		gender: form.gender,
		quote: base.quote,
		memory_summary: memorySummary || base.memorySummary || '',
		avatar: form.avatar,
		cover: base.cover,
		personality: base.personality,
		genre: base.genre,
		studio_meta: {
			alias: form.alias,
			traits: form.traits,
			background: form.background,
			few_shots: form.fewShots,
			forbidden: form.forbidden,
			speech_preview: form.speechPreview,
			speech_style: form.speechStyle,
			memory_rules: form.memoryRules
		}
	};
}

export function worldStudioMeta(world: World) {
	return (world.studioMeta ?? {}) as Record<string, unknown>;
}

export function parseWorldStudioMeta(raw: Record<string, unknown>) {
	const defaults = defaultWorldStudioMeta();
	return {
		one_liner: String(raw.one_liner ?? defaults.one_liner),
		description: String(raw.description ?? defaults.description),
		era_setting: String(raw.era_setting ?? defaults.era_setting),
		tech_level: String(raw.tech_level ?? defaults.tech_level),
		magic_system: String(raw.magic_system ?? defaults.magic_system),
		atmosphere: String(raw.atmosphere ?? defaults.atmosphere),
		map_image: String(raw.map_image ?? defaults.map_image),
		gallery: (raw.gallery as string[]) ?? defaults.gallery,
		themes: (raw.themes as typeof defaults.themes) ?? defaults.themes,
		eras: (raw.eras as typeof defaults.eras) ?? defaults.eras,
		factions: (raw.factions as typeof defaults.factions) ?? defaults.factions,
		nations: (raw.nations as typeof defaults.nations) ?? defaults.nations,
		locations: (raw.locations as typeof defaults.locations) ?? defaults.locations,
		cultures: (raw.cultures as typeof defaults.cultures) ?? defaults.cultures,
		events:
			((raw.events as Array<Record<string, unknown>>) ?? []).map((ev) => ({
				id: String(ev.id ?? ''),
				year: Number(ev.year ?? 0),
				name: String(ev.name ?? ''),
				category: String(ev.category ?? ''),
				categoryColor: String(ev.categoryColor ?? ev.category_color ?? '#6366f1')
			})) ?? defaults.events,
		laws: (raw.laws as typeof defaults.laws) ?? defaults.laws,
		memos:
			((raw.memos as Array<Record<string, unknown>>) ?? []).map((m) => ({
				id: String(m.id ?? ''),
				title: String(m.title ?? ''),
				content: String(m.content ?? ''),
				updatedAt: String(m.updatedAt ?? m.updated_at ?? '')
			})) ?? defaults.memos
	};
}
