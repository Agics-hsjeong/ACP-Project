# ACP Frontend

AI Character Playground 웹 퍼블리싱 (SvelteKit + Tailwind CSS v4)

## 스택

- **SvelteKit** 2.x · **Svelte** 5 · **TypeScript**
- **Tailwind CSS** v4 (DESIGN_SYSTEM 토큰)
- **lucide-svelte** 아이콘

기획 문서: `01. 기획/` · UI 목업: `02. UI 디자인/mockup/`

## 실행

### Docker (권장)

프로젝트 루트에서:

```bash
docker compose up --build
```

브라우저: http://localhost:28433 (Nginx → frontend)

`frontend`는 Docker 내부 네트워크만 노출합니다. 외부 접근은 **Nginx** 를 통합니다.  
로컬 기본 포트 `28433` (80/8080 등 충돌 회피). 배포 시 `docker-compose.yml`에서 `80:80` 등으로 변경.

### 로컬 개발

```bash
cd frontend
npm install
npm run dev
```

브라우저: http://localhost:5173

## 라우트 (Phase 1 퍼블)

| 경로 | Screen | 설명 |
|------|--------|------|
| `/landing` | 01 | 랜딩 |
| `/login` | 02 | 로그인 |
| `/home` | 03 | 홈 (간소) |
| `/explore` | 04 | 캐릭터 탐색 |
| `/characters/[id]` | 05 | 캐릭터 상세 |
| `/chat/[id]` | 06 | RP 채팅 |
| `/memory` | 07 | 기억 보관소 |
| `/emotion` | 09 | 감정 분석 (간소) |
| `/mypage` | — | 마이페이지 (Creator) |
| `/mobile` | 12 | Mobile 8폰 쇼케이스 |

### Mobile (Screen 12) — `/mobile/*`

| 경로 | 화면 |
|------|------|
| `/mobile` | 8폰 그리드 쇼케이스 |
| `/mobile/home` | M01 홈 |
| `/mobile/explore` | M02 탐색 |
| `/mobile/chat/[id]` | M03 채팅 |
| `/mobile/relationship` | M04 관계도 |

Phase 2+ placeholder: `/studio/*`
| `/mobile/memory` | M05 기억 |
| `/mobile/emotion` | M06 감정 |
| `/mobile/characters/[id]` | M07 프로필 |
| `/mobile/profile` | M08 마이페이지 |

| `/relationship` | 08 | 인물 관계도 (D3 그래프) |

## 구조

```text
src/
  lib/
    components/   # UI, layout, cards, chat
    data/mock.ts  # 목업 데이터
  routes/
    landing/ login/
    (app)/        # AppShell (SideNav + TopBar)
```
