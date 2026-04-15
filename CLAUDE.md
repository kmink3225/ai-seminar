# CLAUDE.md — Claude Code 실행 규칙

> 이 파일은 Claude Code 가 **세션 시작 시 자동으로 읽는 진입점**이다.
> 아래 규칙은 리다이렉트가 아니라 **직접 따라야 하는 행동 지시**이다.

---

## 실행 프로토콜 (반드시 순서대로)

### Phase 0: 가이드 로드 (작업 시작 전)

**파일을 읽지 않으면 작업을 시작하지 않는다.** 아래를 Read 도구로 읽는다.

1. `AGENT_GUIDE.md` — 슬래시 커맨드 라우팅 테이블 (진입점이 지정한 canonical 소스)
2. `guides/AGENT_GUIDE_CORE.md` — 항상-온 공통 규칙 (AGENT_GUIDE.md 가 로드를 지시)
3. 태스크에 해당하는 skill 가이드 (`guides/<name>.md`)

로드 체인: **이 파일 → `AGENT_GUIDE.md` → `guides/AGENT_GUIDE_CORE.md` → skill 가이드**.

동일 세션에서 이미 Read 한 파일은 재읽기 생략 가능. "알고 있다"는 이유로는 스킵하지 않는다.

### Phase 1: 탐색 (해당 시)

`/search`·`/qa`·`/code` 는 `guides/search.md` 의 Step 을 실행해 근거를 모은다. 결과를 사용자에게 1~2 줄로 보고한다.

### Phase 2: 실행

skill 가이드의 Step 을 **순서대로** 실행한다. 각 Step 시작 시 무엇을 하는지 사용자에게 보이는 텍스트로 명시한다.

```
예시:
"Step 1: references/md/ 에서 'tool use' Grep"
"Step 3: 요구사항 확정 — Python 3.11, anthropic SDK 사용"
```

Step 을 암묵적으로 건너뛰거나 여러 Step 을 한 문장으로 뭉개지 않는다.

### Phase 3: 검증 (Self-Check)

작업 보고 **전에** `guides/AGENT_GUIDE_CORE.md` §5 Self-Check 를 출력한다.

### Phase 4: 후속

- `/ingest` 후 신규 변환 파일이 있으면 분석·검색 제안
- 파일 생성 시 저장 위치 확인 후 사용자 승인
- **커밋·푸시는 사용자 명시 요청 시에만** 실행

---

## 절대 규칙 (인라인)

1. **한다 체** — `~한다/~이다/~된다`. `~합니다/~입니다` 금지.
2. **이모지 금지** — 파일·커밋 메시지 모두.
3. **수동 번호 금지** — 섹션 번호 직접 부여 금지.
4. **근거 인용** — 내부 문서 참조 시 `path:line` 형식.
5. **자동 생성물 직접 수정 금지** — `references/md/` 는 재생성으로만 갱신.
6. **이름 보존** — 기존 변수·함수·파일명 임의 변경 금지.

---

## 라우팅 / 저장 규칙 / 프로젝트 정보

`AGENT_GUIDE.md` 가 canonical 소스다. 이 파일은 **Claude Code 전용 Phase 프로토콜과 절대 규칙**만 담는다.

- 슬래시 커맨드 라우팅 → `AGENT_GUIDE.md` §슬래시 커맨드 정의
- 폴더·저장 규칙 → `guides/AGENT_GUIDE_CORE.md` §4
- Project Info → `AGENT_GUIDE.md` §Project Info
