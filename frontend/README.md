# ACP Frontend

AI Character Playground 웹 퍼블리싱 (SvelteKit + Tailwind CSS v4)

## 스택

- **SvelteKit** 2.x · **Svelte** 5 · **TypeScript**
- **Tailwind CSS** v4 (DESIGN_SYSTEM 토큰)
- **lucide-svelte** · **d3** (관계도)
- **adapter-node** (Docker 프로덕션)

기획: `01. 기획/` · UI 목업: Figma (`figma.config.json`)

## 실행

### Docker (권장)

```bash
docker compose up --build
```

→ http://localhost:28433

### 로컬 개발

```bash
cd frontend
npm install
npm run dev
```

→ http://localhost:5173

## 라우트

### PC (Screen 01–11)

| 경로 | Screen | 설명 |
|------|--------|------|
| `/landing` | 01 | 랜딩 · 인기 캐릭터 · 서비스 소개 |
| `/login` | 02 | 로그인 · OAuth mock · 회원가입 전환 |
| `/home` | 03 | 홈 · 추천 스토리 · 데일리 퀘스트 |
| `/explore` | 04 | 캐릭터 탐색 · 필터 · 검색 |
| `/characters/[id]` | 05 | 상세 · 즐겨찾기 · 시나리오 · 관계 요약 |
| `/chat/[id]` | 06 | RP 채팅 · 인터랙션 · 스트리밍 mock |
| `/memory` | 07 | 기억 보관소 · 충실도 · Top5 태그 |
| `/relationship` | 08 | D3 관계도 · 미니맵 · 타임라인 |
| `/emotion` | 09 | 감정 대시보드 · 이벤트 · AI 인사이트 |
| `/studio/character` | 10 | 캐릭터 스튜디오 |
| `/studio/world` | 11 | 세계관 스튜디오 (8탭) |
| `/mypage` | — | Creator 허브 |
| `/settings` | — | 계정 · 알림 · 테마 |

### Mobile (Screen 12) — `/mobile/*`

| 경로 | 화면 |
|------|------|
| `/mobile` | 8폰 쇼케이스 |
| `/mobile/home` | M01 홈 |
| `/mobile/explore` | M02 탐색 |
| `/mobile/chat/[id]` | M03 채팅 |
| `/mobile/relationship` | M04 관계도 |
| `/mobile/memory` | M05 기억 |
| `/mobile/emotion` | M06 감정 |
| `/mobile/characters/[id]` | M07 프로필 |
| `/mobile/profile` | M08 마이페이지 |

## 구조

```text
src/
  lib/
    components/   # UI, layout, cards, chat, memory, emotion, relationship, studio
    data/         # mock.ts, studio.ts, relationship.ts
    stores/       # chat, emotion, auth, favorites, search
    actions/      # autoscroll
  routes/
    landing/ login/
    (app)/        # AppShell
    mobile/       # MobileShell
```

## 데이터

현재 **mock 데이터 + localStorage**(auth, favorites) 기반입니다.  
백엔드 연동 시 `lib/api/` 레이어 추가 예정.

## 확인 URL

- PC: `/home`, `/explore`, `/chat/elia`, `/memory`, `/relationship`, `/studio/character`
- Mobile: `/mobile`, `/mobile/home`
