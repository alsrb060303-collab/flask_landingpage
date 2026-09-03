# -*- coding: utf-8 -*-
"""
사이트의 모든 텍스트가 모여 있는 파일.

여기만 고치면 사이트 전체가 바뀐다. HTML 은 건드릴 필요 없다.
값이 "" (빈 문자열) 이거나 [] (빈 목록) 인 항목은 화면에 "채워 넣을 자리" 로 표시된다.
"""

# ---------------------------------------------------------------------------
# 회사 기본 정보  ── 여기부터 채우면 사이트 전체에 반영된다
# ---------------------------------------------------------------------------

COMPANY = {
    "name_ko": "유니브",
    "name_en": "UNIV",
    "legal_name_ko": "유니브",
    "legal_name_en": "UNIV",
    "ceo": "김민규",
    "ceo_en": "Kim Min-gyu",
    "founded": "2026-09-01",
    "founded_year": "2026",
    "address_ko": "강원특별자치도 춘천시 안마산로 244",
    "address_en": "244 Anmasan-ro, Chuncheon-si, Gangwon State, Republic of Korea",
    "phone": "010-2591-0559",
    "phone_href": "tel:+821025910559",
    "email": "alsrb060303@gmail.com",
    "site_url": "https://univ-security.co.kr",   # TODO: 실제 도메인으로 교체
    "biz_no": "",                                 # TODO: 사업자등록번호
    "github": "",                                 # TODO: 있으면 입력
    "linkedin": "",                               # TODO: 있으면 입력
}


# ---------------------------------------------------------------------------
# 서비스
# ---------------------------------------------------------------------------

SERVICE_ORDER = ["api-pentest", "network-pentest", "red-team", "ai-scanner"]

SERVICES = {
    # -----------------------------------------------------------------------
    "api-pentest": {
        "slug": "api-pentest",
        "image": "service-api.jpg",
        "icon": """<path d="M9 6.5 4.5 12 9 17.5"/><path d="m15 6.5 4.5 5.5-4.5 5.5"/>""",
        "ko": {
            "name": "API 모의해킹",
            "tagline": "문서에 없는 엔드포인트까지 찾아냅니다",
            "summary": "REST · GraphQL · gRPC 를 대상으로 인증·인가 우회, 객체 수준 권한 결함, "
                       "대량 데이터 노출을 실제 공격 기법으로 검증합니다. "
                       "OWASP API Security Top 10 을 기준선으로 삼되, 거기서 멈추지 않습니다.",
            "targets": [
                "REST / GraphQL / gRPC / WebSocket API",
                "모바일 앱·SPA 백엔드 API",
                "파트너 연동용 외부 공개 API",
                "내부 마이크로서비스 간 통신 API",
            ],
            "checks": [
                ("BOLA / IDOR", "객체 수준 인가 결함 — 다른 사용자의 자원에 접근 가능한지"),
                ("인증 우회", "JWT 서명 검증 결함, 토큰 재사용, 세션 고정, OAuth 흐름 조작"),
                ("기능 수준 인가", "관리자 전용 기능에 일반 계정으로 도달 가능한지"),
                ("대량 데이터 노출", "응답에 불필요하게 포함된 내부 필드·개인정보"),
                ("비즈니스 로직", "결제·포인트·쿠폰 등 금액이 오가는 흐름의 순서 조작"),
                ("자원 소모 공격", "속도 제한 부재, 페이지네이션 남용, GraphQL 중첩 질의"),
                ("주입 공격", "SQL/NoSQL/명령어/템플릿 주입, 역직렬화 결함"),
                ("SSRF", "서버 측 요청 위조를 통한 내부망·클라우드 메타데이터 접근"),
                ("섀도우 API", "문서화되지 않은 구버전·테스트 엔드포인트 탐색"),
            ],
            "process": [
                ("01", "범위 정의", "대상 엔드포인트, 테스트 계정 등급, 제외 항목, 테스트 시간대를 문서로 확정합니다."),
                ("02", "정찰 및 표면 수집", "API 명세, 클라이언트 번들, 트래픽 캡처를 분석해 문서에 없는 엔드포인트까지 목록화합니다."),
                ("03", "자동 스캔", "자체 AI 점검 툴로 전체 표면을 빠르게 훑어 의심 지점을 우선순위화합니다."),
                ("04", "수동 심층 진단", "자동화가 판단할 수 없는 인가 결함과 비즈니스 로직을 전문가가 직접 파고듭니다."),
                ("05", "익스플로잇 검증", "실제 악용 가능성을 재현 가능한 PoC 로 증명합니다. 추측으로 보고하지 않습니다."),
                ("06", "보고 및 재점검", "리포트 전달 후 조치 결과를 무상으로 재검증합니다."),
            ],
            "deliverables": [
                "경영진 요약 — 위험도와 사업 영향 중심의 1~2쪽 요약",
                "기술 상세 리포트 — 취약점별 재현 절차, PoC, 증적 화면",
                "CVSS v3.1 기반 심각도 산정 및 조치 우선순위",
                "코드·설정 수준의 구체적 조치 가이드",
                "조치 후 재점검 확인서",
            ],
            "standards": ["OWASP API Security Top 10", "OWASP WSTG", "PTES", "NIST SP 800-115"],
        },
        "en": {
            "name": "API Penetration Testing",
            "tagline": "We find the endpoints your documentation forgot",
            "summary": "We test REST, GraphQL and gRPC surfaces for broken authorization, "
                       "authentication bypass and excessive data exposure using real attack "
                       "techniques. The OWASP API Security Top 10 is our baseline, not our ceiling.",
            "targets": [
                "REST / GraphQL / gRPC / WebSocket APIs",
                "Backends serving mobile apps and SPAs",
                "Public partner-facing APIs",
                "Internal service-to-service APIs",
            ],
            "checks": [
                ("BOLA / IDOR", "Object-level authorization flaws that expose other users' data"),
                ("Authentication bypass", "JWT verification flaws, token replay, session fixation, OAuth abuse"),
                ("Function-level authorization", "Admin-only functionality reachable by ordinary accounts"),
                ("Excessive data exposure", "Internal fields and personal data leaking through responses"),
                ("Business logic", "Order manipulation in payment, point and coupon flows"),
                ("Resource consumption", "Missing rate limits, pagination abuse, deeply nested GraphQL queries"),
                ("Injection", "SQL/NoSQL/command/template injection and unsafe deserialization"),
                ("SSRF", "Server-side request forgery into internal networks and cloud metadata"),
                ("Shadow APIs", "Undocumented legacy and staging endpoints"),
            ],
            "process": [
                ("01", "Scoping", "We agree in writing on endpoints, account tiers, exclusions and testing windows."),
                ("02", "Reconnaissance", "Specs, client bundles and captured traffic are analysed to enumerate every reachable endpoint."),
                ("03", "Automated sweep", "Our own AI-assisted scanner covers the full surface fast and ranks suspicious areas."),
                ("04", "Manual deep dive", "Our engineers attack the authorization and business-logic flaws automation cannot judge."),
                ("05", "Exploit validation", "Every finding ships with a reproducible proof of concept. We do not report guesses."),
                ("06", "Report and retest", "After remediation we verify the fixes at no additional cost."),
            ],
            "deliverables": [
                "Executive summary — one to two pages on risk and business impact",
                "Technical report — reproduction steps, PoC and evidence per finding",
                "CVSS v3.1 severity ratings and a prioritized remediation order",
                "Concrete fixes at the code and configuration level",
                "Retest confirmation letter",
            ],
            "standards": ["OWASP API Security Top 10", "OWASP WSTG", "PTES", "NIST SP 800-115"],
        },
    },
    # -----------------------------------------------------------------------
    "network-pentest": {
        "slug": "network-pentest",
        "image": "service-network.jpg",
        "icon": """<circle cx="12" cy="5" r="2.2"/><circle cx="5" cy="18" r="2.2"/>"""
                """<circle cx="19" cy="18" r="2.2"/><path d="M12 7.2v4.3m0 0L6.6 16m5.4-4.5L17.4 16"/>""",
        "ko": {
            "name": "네트워크 모의해킹",
            "tagline": "경계는 이미 무너져 있다고 가정합니다",
            "summary": "외부 노출 자산부터 내부 도메인 장악까지, 실제 침입 경로를 단계별로 검증합니다. "
                       "포트 목록을 나열하는 스캔 리포트가 아니라, 여기서 저기까지 어떻게 갈 수 있는지를 보여드립니다.",
            "targets": [
                "인터넷 노출 자산 (방화벽, VPN, 메일, 원격접속)",
                "내부망 (Active Directory, 파일 서버, 업무 시스템)",
                "무선 네트워크 (WPA2/3-Enterprise, 게스트망 분리)",
                "클라우드 네트워크 (VPC, 보안그룹, 하이브리드 연결)",
            ],
            "checks": [
                ("외부 표면 식별", "잊혀진 서버, 만료된 인증서, 노출된 관리 인터페이스"),
                ("초기 침투", "취약 서비스 익스플로잇, 자격증명 스터핑, 기본 계정"),
                ("자격증명 탈취", "LLMNR/NBT-NS 포이즈닝, Kerberoasting, 평문 자격증명 수집"),
                ("권한 상승", "로컬 관리자 → 도메인 관리자 경로 추적"),
                ("횡적 이동", "SMB/WMI/WinRM 을 통한 확산 경로 검증"),
                ("망 분리 검증", "업무망·개발망·DMZ 간 실제 통제 여부"),
                ("탐지 우회", "EDR·백신 하에서의 실행 가능성 확인"),
                ("데이터 반출", "실제 반출 시나리오 시연 및 DLP 통제 검증"),
            ],
            "process": [
                ("01", "범위 정의", "대상 IP 대역, 테스트 방식(블랙/그레이/화이트박스), 위험 행위 금지선을 합의합니다."),
                ("02", "자산 식별", "노출 자산을 능동·수동으로 수집하고 실제 서비스 여부를 확인합니다."),
                ("03", "취약점 분석", "자동 스캔 결과를 전문가가 검증해 오탐을 걷어냅니다."),
                ("04", "침투 시도", "확인된 경로로 실제 침투하고, 성공 시 내부 확산 경로를 추적합니다."),
                ("05", "영향도 평가", "장악 가능한 자산 범위와 접근 가능한 데이터를 산정합니다."),
                ("06", "복구 및 보고", "테스트 중 생성한 계정·아티팩트를 모두 제거하고 리포트를 전달합니다."),
            ],
            "deliverables": [
                "침투 경로 다이어그램 — 진입점부터 최종 도달 지점까지",
                "취약점별 상세 리포트와 증적",
                "CVSS 기반 심각도 및 조치 우선순위",
                "네트워크 구조 개선 권고안",
                "조치 후 재점검 확인서",
            ],
            "standards": ["PTES", "NIST SP 800-115", "MITRE ATT&CK", "OSSTMM"],
        },
        "en": {
            "name": "Network Penetration Testing",
            "tagline": "We assume the perimeter has already fallen",
            "summary": "From internet-facing assets to full domain compromise, we validate real "
                       "intrusion paths step by step. Not a list of open ports — a map of how an "
                       "attacker gets from the edge to your crown jewels.",
            "targets": [
                "Internet-facing assets (firewalls, VPN, mail, remote access)",
                "Internal networks (Active Directory, file servers, business systems)",
                "Wireless networks (WPA2/3-Enterprise, guest segmentation)",
                "Cloud networks (VPC, security groups, hybrid links)",
            ],
            "checks": [
                ("Attack surface discovery", "Forgotten hosts, expired certificates, exposed admin interfaces"),
                ("Initial access", "Vulnerable service exploitation, credential stuffing, default accounts"),
                ("Credential theft", "LLMNR/NBT-NS poisoning, Kerberoasting, cleartext credential harvesting"),
                ("Privilege escalation", "Tracing the path from local admin to domain admin"),
                ("Lateral movement", "Spread via SMB, WMI and WinRM"),
                ("Segmentation testing", "Whether office, development and DMZ boundaries actually hold"),
                ("Detection evasion", "Whether payloads run under your EDR and antivirus"),
                ("Data exfiltration", "Demonstrated exfiltration paths and DLP effectiveness"),
            ],
            "process": [
                ("01", "Scoping", "IP ranges, black/grey/white-box approach and prohibited actions are agreed up front."),
                ("02", "Asset discovery", "Active and passive enumeration of everything actually reachable."),
                ("03", "Vulnerability analysis", "Scanner output is validated by hand so false positives never reach you."),
                ("04", "Exploitation", "Confirmed paths are exploited and internal spread is traced."),
                ("05", "Impact assessment", "We quantify what could be seized and which data becomes reachable."),
                ("06", "Cleanup and reporting", "Every account and artifact we created is removed before we hand over the report."),
            ],
            "deliverables": [
                "Attack path diagram — entry point to final objective",
                "Detailed findings with evidence",
                "CVSS severity ratings and remediation priority",
                "Network architecture recommendations",
                "Retest confirmation letter",
            ],
            "standards": ["PTES", "NIST SP 800-115", "MITRE ATT&CK", "OSSTMM"],
        },
    },
    # -----------------------------------------------------------------------
    "red-team": {
        "slug": "red-team",
        "image": "service-redteam.jpg",
        "icon": """<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.2"/>"""
                """<circle cx="12" cy="12" r="0.9" fill="currentColor" stroke="none"/>""",
        "ko": {
            "name": "레드팀 침투 시나리오",
            "tagline": "취약점이 아니라 대응 능력을 시험합니다",
            "summary": "특정 목표(고객 DB 반출, 결제 시스템 장악 등)를 정해두고, 탐지되지 않는 것을 "
                       "전제로 실제 공격자처럼 움직입니다. 모의해킹이 '문이 열려 있는가'를 묻는다면 "
                       "레드팀은 '누군가 들어왔을 때 알아챌 수 있는가'를 묻습니다.",
            "targets": [
                "보안 관제(SOC)·EDR 을 이미 운영 중인 조직",
                "모의해킹을 여러 차례 수행해 온 조직",
                "침해사고 대응 절차의 실효성을 검증하려는 조직",
                "금융·의료 등 규제 산업의 위기 대응 훈련",
            ],
            "checks": [
                ("정찰", "공개 정보·임직원 노출 정보 수집(OSINT), 공격 표면 정밀 분석"),
                ("초기 침투", "스피어 피싱, 노출 자산 취약점, 유출 자격증명 활용"),
                ("거점 확보", "탐지되지 않는 지속성 확보 및 C2 통신 채널 구성"),
                ("권한 상승", "목표 도달에 필요한 최소 권한 경로 선택"),
                ("횡적 이동", "정상 관리 도구를 활용한 은밀한 확산 (LotL)"),
                ("목표 달성", "사전 합의된 목표 자산 도달 및 증적 확보"),
                ("탐지 측정", "각 단계에서 방어팀이 탐지·차단한 시점 기록"),
                ("퍼플팀 세션", "공격 타임라인과 로그를 나란히 놓고 탐지 규칙을 함께 개선"),
            ],
            "process": [
                ("01", "목표 합의", "무엇을 지켜야 하는지에서 출발합니다. 도달 목표와 금지선을 경영진과 확정합니다."),
                ("02", "정찰", "공격자가 볼 수 있는 모든 정보를 외부 시선에서 수집합니다."),
                ("03", "무기화", "해당 환경에 맞춘 도구와 시나리오를 준비합니다."),
                ("04", "작전 수행", "수 주에 걸쳐 은밀하게 목표를 향해 진행합니다."),
                ("05", "탐지 타임라인 대조", "우리의 행동 기록과 방어팀의 로그를 시간순으로 대조합니다."),
                ("06", "퍼플팀 워크숍", "탐지되지 않은 구간의 원인을 분석하고 탐지 규칙을 함께 만듭니다."),
            ],
            "deliverables": [
                "공격 타임라인 — 모든 행위의 시각·명령어·산출물 기록",
                "MITRE ATT&CK 매핑 — 사용한 전술·기법 전체 목록",
                "탐지 갭 분석 — 탐지된 것, 탐지되지 않은 것, 그 이유",
                "탐지 규칙 개선안 (SIEM 쿼리 포함)",
                "경영진 브리핑 및 퍼플팀 워크숍",
            ],
            "standards": ["MITRE ATT&CK", "TIBER-EU", "CBEST", "Unified Kill Chain"],
        },
        "en": {
            "name": "Red Team Operations",
            "tagline": "We test your response, not your patch level",
            "summary": "We agree on an objective — exfiltrating a customer database, taking over a "
                       "payment system — and then move like a real adversary, assuming we must not be "
                       "caught. A pentest asks whether the door is open. A red team asks whether you "
                       "notice when someone walks through it.",
            "targets": [
                "Organisations already running a SOC and EDR",
                "Organisations that have run several penetration tests",
                "Teams validating their incident response procedures",
                "Regulated industries running crisis exercises",
            ],
            "checks": [
                ("Reconnaissance", "OSINT on the organisation and its people, precise attack-surface mapping"),
                ("Initial access", "Spear phishing, exposed-asset exploitation, leaked credentials"),
                ("Foothold", "Undetected persistence and covert C2 channels"),
                ("Privilege escalation", "The minimum privilege path required to reach the objective"),
                ("Lateral movement", "Quiet spread using legitimate admin tooling (living off the land)"),
                ("Objective", "Reaching the agreed target asset and capturing evidence"),
                ("Detection measurement", "Recording exactly when the blue team saw or stopped each step"),
                ("Purple team session", "Comparing our timeline against your logs to improve detections together"),
            ],
            "process": [
                ("01", "Objective setting", "We start from what must be protected, and fix targets and prohibitions with the executive team."),
                ("02", "Reconnaissance", "Everything an attacker could see, gathered from the outside."),
                ("03", "Weaponisation", "Tooling and scenarios tailored to your environment."),
                ("04", "Operation", "Weeks of quiet, deliberate movement toward the objective."),
                ("05", "Timeline correlation", "Our action log is aligned against your detection log, minute by minute."),
                ("06", "Purple team workshop", "We analyse the blind spots together and write the detections that close them."),
            ],
            "deliverables": [
                "Attack timeline — every action with timestamp, command and artifact",
                "Full MITRE ATT&CK mapping of tactics and techniques used",
                "Detection gap analysis — what was caught, what was not, and why",
                "Detection engineering recommendations, including SIEM queries",
                "Executive briefing and purple team workshop",
            ],
            "standards": ["MITRE ATT&CK", "TIBER-EU", "CBEST", "Unified Kill Chain"],
        },
    },
    # -----------------------------------------------------------------------
    "ai-scanner": {
        "slug": "ai-scanner",
        "image": "service-ai.jpg",
        "icon": """<rect x="4.5" y="4.5" width="15" height="15" rx="3.5"/>"""
                """<path d="M9.2 9.2h5.6v5.6H9.2z"/><path d="M12 2.6v1.9M12 19.5v1.9M2.6 12h1.9M19.5 12h1.9"/>""",
        "ko": {
            "name": "AI 취약점 점검 툴",
            "tagline": "AI 가 넓게 훑고, 전문가가 깊게 파고듭니다",
            "summary": "자체 개발한 AI 기반 점검 엔진으로 코드와 트래픽을 대규모로 분석해 의심 지점을 "
                       "찾아내고, 그 결과를 전문가가 직접 검증합니다. 오탐 가득한 스캐너 결과를 "
                       "그대로 전달하지 않습니다. 사람이 확인한 것만 리포트에 올라갑니다.",
            "targets": [
                "지속적인 점검이 필요한 대규모 코드베이스",
                "배포 주기가 빨라 수동 점검이 따라가지 못하는 조직",
                "CI/CD 파이프라인에 보안 검증을 넣으려는 개발팀",
                "LLM·AI 기능을 도입한 서비스 (프롬프트 주입 등 신규 위협 대응)",
            ],
            "checks": [
                ("코드 취약점 탐지", "AI 기반 정적 분석으로 패턴 규칙이 놓치는 결함까지 탐색"),
                ("오탐 자동 선별", "실제 도달 가능한 실행 경로인지 판정해 노이즈를 제거"),
                ("의존성 위험 분석", "사용 중인 오픈소스의 알려진 취약점과 실제 영향 범위"),
                ("설정 오류 점검", "클라우드·컨테이너·인프라 코드의 위험 설정"),
                ("시크릿 노출", "저장소·빌드 로그에 남은 키와 자격증명"),
                ("LLM 보안", "프롬프트 주입, 시스템 프롬프트 유출, 과도한 권한 위임"),
                ("전문가 검증", "AI 가 올린 후보를 사람이 재현해 확정 — 이 단계가 핵심입니다"),
            ],
            "process": [
                ("01", "환경 연동", "저장소 또는 대상 시스템을 읽기 전용으로 연동합니다."),
                ("02", "AI 전수 분석", "전체 표면을 대규모로 분석해 위험 후보를 추출합니다."),
                ("03", "도달 가능성 판정", "실행 경로 분석으로 실제 악용 가능한 것만 남깁니다."),
                ("04", "전문가 검증", "남은 후보를 사람이 직접 재현합니다. 재현되지 않으면 보고하지 않습니다."),
                ("05", "리포트 및 연동", "결과를 전달하고 필요 시 CI/CD 파이프라인에 점검을 상시화합니다."),
            ],
            "deliverables": [
                "검증 완료된 취약점 목록 — 오탐 제거 후",
                "취약점별 재현 절차 및 수정 코드 제안",
                "의존성·설정 위험 목록",
                "CI/CD 연동 가이드 (선택)",
                "정기 재점검 리포트 (계약 시)",
            ],
            "standards": ["OWASP Top 10", "OWASP LLM Top 10", "CWE Top 25", "SLSA"],
        },
        "en": {
            "name": "AI-Assisted Vulnerability Scanning",
            "tagline": "AI scans wide. Experts dig deep.",
            "summary": "Our in-house AI engine analyses code and traffic at scale to surface suspicious "
                       "areas, and our engineers verify every one of them by hand. We do not forward raw "
                       "scanner output. If a human could not reproduce it, it does not go in the report.",
            "targets": [
                "Large codebases that need continuous assessment",
                "Teams shipping faster than manual review can follow",
                "Development teams embedding security into CI/CD",
                "Products built on LLMs, facing prompt injection and related threats",
            ],
            "checks": [
                ("Code vulnerability detection", "AI static analysis that catches what pattern rules miss"),
                ("Automated false-positive triage", "Reachability analysis removes the noise before you see it"),
                ("Dependency risk", "Known vulnerabilities in your open-source stack and their real impact"),
                ("Misconfiguration", "Risky cloud, container and infrastructure-as-code settings"),
                ("Secret exposure", "Keys and credentials left in repositories and build logs"),
                ("LLM security", "Prompt injection, system prompt leakage, over-permissioned agents"),
                ("Expert validation", "A human reproduces every candidate the AI raises — this step is the product"),
            ],
            "process": [
                ("01", "Integration", "Read-only access to the repository or target system."),
                ("02", "AI-wide analysis", "The full surface is analysed at scale and risk candidates extracted."),
                ("03", "Reachability triage", "Execution-path analysis keeps only what is genuinely exploitable."),
                ("04", "Expert validation", "Our engineers reproduce what remains. If it cannot be reproduced, it is not reported."),
                ("05", "Report and pipeline", "Findings are delivered, and checks can be made continuous in your CI/CD."),
            ],
            "deliverables": [
                "Validated findings only — false positives already removed",
                "Reproduction steps and suggested fixes per finding",
                "Dependency and configuration risk inventory",
                "CI/CD integration guide (optional)",
                "Recurring assessment reports (under contract)",
            ],
            "standards": ["OWASP Top 10", "OWASP LLM Top 10", "CWE Top 25", "SLSA"],
        },
    },
}


# ---------------------------------------------------------------------------
# 화면 문구
# ---------------------------------------------------------------------------

CONTENT = {
    # =======================================================================
    "ko": {
        "locale": "ko_KR",
        "lang_label": "한국어",
        "switch_label": "EN",
        "switch_aria": "Switch to English",
        "nav": [
            ("services", "서비스"),
            ("about", "회사소개"),
            ("insights", "인사이트"),
            ("careers", "채용"),
            ("contact", "문의"),
        ],
        "cta_nav": "상담 신청",
        "meta": {
            "index": ("유니브 | 모의해킹 · 레드팀 · AI 보안 전문기업",
                      "유니브는 API·네트워크 모의해킹, 레드팀 침투 시나리오, AI 기반 취약점 점검을 수행하는 사이버 보안 전문기업입니다."),
            "services": ("서비스 | 유니브",
                         "API·네트워크 모의해킹, 레드팀 침투 시나리오, AI 취약점 점검 툴 — 유니브의 보안 서비스."),
            "about": ("회사소개 | 유니브",
                      "공격자의 관점에서 방어를 설계하는 보안 전문기업 유니브를 소개합니다."),
            "insights": ("인사이트 | 유니브",
                         "유니브의 보안 리서치, 취약점 분석, 기술 노트."),
            "careers": ("채용 | 유니브",
                        "유니브와 함께할 보안 엔지니어를 찾습니다."),
            "contact": ("문의 | 유니브",
                        "보안 진단 상담 및 견적 문의."),
            "security": ("취약점 제보 | 유니브",
                         "유니브 웹사이트 및 서비스의 보안 취약점 제보 정책."),
        },

        # ---- 홈 --------------------------------------------------------
        "hero": {
            "eyebrow": "Penetration Testing · Red Team · AI Security",
            "title_lines": ["AI가 넓게 훑고,", "전문가가 깊게 파고듭니다"],
            "typed": ["API 모의해킹", "네트워크 침투 진단", "레드팀 시나리오", "AI 취약점 점검"],
            "typed_prefix": "지금 검증 중 —",
            "desc": "자동화가 놓치는 지점은 사람이 파고들고, 사람이 감당할 수 없는 규모는 AI가 훑습니다.\n유니브는 두 가지를 모두 하는 보안 전문기업입니다.",
            "primary": "보안 진단 문의",
            "secondary": "서비스 살펴보기",
            "scroll": "아래로 스크롤",
        },
        "stats_title": "숫자로 보는 유니브",
        "stats_note": "실적이 쌓이는 대로 갱신합니다.",
        "stats": [
            {"key": "projects", "value": "", "suffix": "+", "label": "수행 프로젝트"},
            {"key": "cve", "value": "", "suffix": "", "label": "발견 및 신고 CVE"},
            {"key": "certs", "value": "", "suffix": "", "label": "보유 자격증"},
            {"key": "founded", "value": "2026", "suffix": "", "label": "설립연도"},
        ],
        "home_services": {
            "eyebrow": "Services",
            "title": "우리가 하는 일",
            "desc": "네 가지 서비스, 하나의 원칙 — 재현되지 않는 것은 보고하지 않습니다.",
            "more": "자세히 보기",
            "all": "전체 서비스 보기",
        },
        "why": {
            "eyebrow": "Why UNIV",
            "title": "스캐너 리포트를 대신 전달하지 않습니다",
            "items": [
                ("전부 사람이 검증합니다",
                 "AI가 찾은 후보라도 전문가가 직접 재현해야 리포트에 올라갑니다. 오탐을 정리하는 일까지가 저희 몫입니다."),
                ("최신 공격 기법을 씁니다",
                 "체크리스트를 채우는 진단이 아니라, 실제 공격자가 지금 쓰는 기법으로 검증합니다."),
                ("고칠 수 있게 씁니다",
                 "\"입력값 검증이 미흡함\"이 아니라, 어느 파일 어느 줄을 어떻게 바꿔야 하는지 씁니다."),
                ("조치 후 재점검은 무상입니다",
                 "리포트 전달로 끝나지 않습니다. 조치가 실제로 유효한지 다시 확인해 드립니다."),
            ],
        },
        "method": {
            "eyebrow": "Methodology",
            "title": "국제 표준 위에서 움직입니다",
            "desc": "자체 방식이 아니라 검증된 공개 표준을 기준선으로 삼습니다. 그래야 결과를 비교하고 추적할 수 있습니다.",
            "items": [
                ("PTES", "Penetration Testing Execution Standard — 진단 전 과정의 수행 기준"),
                ("OWASP", "WSTG · API Security Top 10 · LLM Top 10 — 애플리케이션 점검 항목 기준"),
                ("MITRE ATT&CK", "레드팀 전술·기법 매핑 및 탐지 갭 분석 기준"),
                ("NIST SP 800-115", "정보보안 시험·평가 기술 가이드"),
            ],
        },
        "clients": {
            "title": "함께한 고객사",
            "note": "고객사 로고를 static/images/ 에 client-01.png ~ client-06.png 로 넣으면 표시됩니다.",
        },
        "cta": {
            "title": "먼저 찾는 쪽이 되시겠습니까",
            "desc": "공격자가 찾기 전에 저희가 먼저 찾겠습니다. 범위와 일정부터 함께 정리해 드립니다.",
            "primary": "상담 신청하기",
            "secondary": "취약점 제보",
        },

        # ---- 서비스 ----------------------------------------------------
        "services_page": {
            "eyebrow": "Services",
            "title": "보안 서비스",
            "desc": "조직의 상황에 따라 필요한 진단은 다릅니다. 어떤 것이 맞는지 모르겠다면 상담 단계에서 함께 정리해 드립니다.",
        },
        "svc": {
            "targets": "이런 조직에 필요합니다",
            "checks": "점검 항목",
            "process": "진행 프로세스",
            "deliverables": "산출물",
            "standards": "적용 표준",
            "duration": "소요 기간",
            "duration_value": "",
            "price": "비용",
            "price_value": "",
            "tbd": "협의 후 안내",
            "back": "전체 서비스",
            "cta": "이 서비스 문의하기",
            "next": "다음 서비스",
        },

        # ---- 회사소개 --------------------------------------------------
        "about_page": {
            "eyebrow": "About UNIV",
            "title": "공격자의 관점에서\n방어를 설계합니다",
            "lead": "유니브는 2026년 9월, 춘천에서 시작한 사이버 보안 전문기업입니다. "
                    "API·네트워크 모의해킹과 레드팀 침투 시나리오를 수행하고, "
                    "자체 개발한 AI 점검 엔진으로 그 과정을 확장합니다.",
            "body": [
                "보안 진단 리포트 대부분은 읽히지 않습니다. 자동 스캐너가 뱉은 수백 건의 항목 중 "
                "무엇이 진짜 위험한지 판단하는 몫이 고객에게 떠넘겨지기 때문입니다.",
                "유니브는 그 판단까지를 저희 일로 봅니다. AI가 전체 표면을 넓게 훑어 후보를 모으고, "
                "전문가가 하나씩 재현해 실제로 악용 가능한 것만 남깁니다. "
                "리포트에 남은 항목은 전부 사람이 직접 확인한 것입니다.",
                "그래서 저희 리포트는 짧습니다. 대신 그 안의 모든 항목은 재현 가능하고, 고칠 수 있습니다.",
            ],
            "principles_title": "일하는 원칙",
            "principles": [
                ("재현되지 않으면 보고하지 않는다", "추측성 지적은 신뢰를 갉아먹습니다. PoC 없이는 리포트에 오르지 않습니다."),
                ("고객보다 먼저 이해한다", "무엇을 지켜야 하는지 모르면 무엇을 공격할지도 정할 수 없습니다."),
                ("합의된 선을 넘지 않는다", "서비스 중단, 데이터 파괴, 합의되지 않은 대상은 절대 건드리지 않습니다."),
                ("배운 것을 공개한다", "산업 전체가 안전해지는 것이 결국 고객을 지키는 길입니다."),
            ],
            "ceo_title": "대표",
            "ceo_role": "대표이사 / 보안 컨설턴트",
            "ceo_message": "",          # TODO: 대표 인사말
            "ceo_bio": "",              # TODO: 대표 약력
            "team_title": "팀",
            "team_note": "팀원 정보를 채워 넣을 자리입니다. content.py 의 TEAM 을 수정하세요.",
            "certs_title": "자격 및 인증",
            "certs_note": "보유 자격증·기업 인증을 채워 넣을 자리입니다.",
            "history_title": "연혁",
            "history": [
                ("2026.09", "유니브 설립"),
            ],
            "history_note": "연혁이 쌓이는 대로 추가됩니다.",
            "info_title": "회사 정보",
            "info_labels": {
                "legal": "상호",
                "ceo": "대표자",
                "founded": "설립일",
                "address": "주소",
                "phone": "전화",
                "email": "이메일",
                "biz": "사업자등록번호",
            },
        },

        # ---- 인사이트 --------------------------------------------------
        "insights_page": {
            "eyebrow": "Insights",
            "title": "보안 리서치와 기술 노트",
            "desc": "취약점 분석, 공격 기법 연구, 진단 과정에서 얻은 것들을 정리해 공개합니다.",
            "empty_title": "첫 글을 준비하고 있습니다",
            "empty_desc": "발행되는 대로 이곳에 올라옵니다. content.py 의 INSIGHTS 목록에 글을 추가하면 자동으로 표시됩니다.",
            "read": "읽기",
        },

        # ---- 채용 ------------------------------------------------------
        "careers_page": {
            "eyebrow": "Careers",
            "title": "함께 파고들 사람을 찾습니다",
            "desc": "자격증보다 무엇을 직접 깨봤는지를 봅니다. CTF 기록, 버그바운티 리포트, 분석 글 — 형식은 자유입니다.",
            "values_title": "이런 분과 일하고 싶습니다",
            "values": [
                ("끝까지 파는 사람", "\"안 되는 것 같다\"에서 멈추지 않고 왜 안 되는지까지 확인하는 사람"),
                ("쓸 줄 아는 사람", "찾아낸 것을 상대가 고칠 수 있게 설명할 수 있는 사람"),
                ("선을 지키는 사람", "할 수 있는 것과 해도 되는 것을 구분하는 사람"),
            ],
            "openings_title": "채용 중인 포지션",
            "empty_title": "현재 공개 채용 중인 포지션이 없습니다",
            "empty_desc": "그래도 관심이 있다면 언제든 연락 주세요. 상시로 이력을 받고 있습니다.",
            "apply": "지원하기",
            "open_apply": "상시 지원 메일 보내기",
        },

        # ---- 문의 ------------------------------------------------------
        "contact_page": {
            "eyebrow": "Contact",
            "title": "무엇을 지켜야 하는지부터\n이야기해 주세요",
            "desc": "범위가 정해지지 않아도 괜찮습니다. 어떤 진단이 필요한지 함께 정리하는 것부터 시작합니다.",
            "form_title": "상담 요청",
            "form_note": "아래를 작성하면 메일 앱이 열리고 내용이 자동으로 채워집니다. 전송 버튼만 누르시면 됩니다.",
            "fields": {
                "company": "회사명",
                "name": "담당자명",
                "email": "회신 받을 이메일",
                "phone": "연락처 (선택)",
                "service": "관심 서비스",
                "message": "문의 내용",
                "message_ph": "대상 시스템, 대략적인 규모, 희망 일정 등을 적어 주시면 더 정확히 안내드릴 수 있습니다.",
                "select": "선택해 주세요",
                "other": "아직 모르겠습니다 / 상담 필요",
            },
            "submit": "메일 작성하기",
            "direct_title": "바로 연락하기",
            "hours_label": "상담 가능 시간",
            "hours": "평일 10:00 – 19:00 (KST)",
            "response_label": "회신",
            "response": "영업일 기준 1일 이내",
            "map_note": "지도 이미지를 넣을 자리입니다.",
        },

        # ---- 취약점 제보 -----------------------------------------------
        "security_page": {
            "eyebrow": "Vulnerability Disclosure",
            "title": "취약점을 발견하셨나요",
            "desc": "유니브의 웹사이트나 서비스에서 보안 취약점을 발견하셨다면 알려 주세요. "
                    "선의의 제보자에 대해서는 법적 조치를 취하지 않습니다.",
            "scope_title": "제보 범위",
            "scope_in": ["유니브 공식 웹사이트 및 하위 도메인", "유니브가 공개한 도구 및 저장소"],
            "scope_out": ["제3자 서비스에 대한 취약점", "서비스 거부(DoS) 및 부하 테스트",
                          "물리적 침입 및 사회공학 기법", "자동 스캐너 결과만 첨부된 제보"],
            "in_label": "포함",
            "out_label": "제외",
            "rules_title": "지켜 주셔야 할 것",
            "rules": [
                "타인의 데이터에 접근하거나 변경하지 마세요.",
                "서비스 가용성을 해치는 행위는 하지 마세요.",
                "확인에 필요한 최소한의 범위에서만 검증해 주세요.",
                "조치가 완료될 때까지 공개하지 말아 주세요.",
            ],
            "how_title": "제보 방법",
            "how_desc": "아래 메일로 재현 절차와 영향도를 함께 보내 주세요. 접수 후 3영업일 이내에 회신드립니다.",
            "timeline_title": "처리 절차",
            "timeline": [
                ("접수", "3영업일 이내 접수 확인 회신"),
                ("검증", "재현 및 영향도 평가"),
                ("조치", "심각도에 따른 우선순위로 수정"),
                ("공개", "제보자와 협의 후 공개 시점 결정"),
            ],
            "report": "취약점 제보하기",
            "txt_note": "이 정책은 security.txt 로도 공시되어 있습니다.",
        },

        # ---- 공통 ------------------------------------------------------
        "footer": {
            "tagline": "AI가 넓게 훑고, 전문가가 깊게 파고듭니다.",
            "nav_title": "서비스",
            "company_title": "회사",
            "contact_title": "연락처",
            "security_link": "취약점 제보",
            "rights": "All rights reserved.",
        },
        "img_slot": {
            "title": "이미지를 넣어 주세요",
            "hint": "static/images/ 에 아래 이름으로 저장하면 자동 반영됩니다",
        },
        "empty_slot": "채워 넣을 자리",
        "not_found": {
            "title": "페이지를 찾을 수 없습니다",
            "desc": "주소가 바뀌었거나 삭제된 페이지입니다.",
            "home": "홈으로 돌아가기",
        },
    },

    # =======================================================================
    "en": {
        "locale": "en_US",
        "lang_label": "English",
        "switch_label": "KO",
        "switch_aria": "한국어로 전환",
        "nav": [
            ("services", "Services"),
            ("about", "About"),
            ("insights", "Insights"),
            ("careers", "Careers"),
            ("contact", "Contact"),
        ],
        "cta_nav": "Get in touch",
        "meta": {
            "index": ("UNIV | Penetration Testing · Red Team · AI Security",
                      "UNIV is a cyber security firm delivering API and network penetration testing, red team operations and AI-assisted vulnerability assessment."),
            "services": ("Services | UNIV",
                         "API and network penetration testing, red team operations and AI-assisted vulnerability scanning."),
            "about": ("About | UNIV",
                      "UNIV designs defence from the attacker's point of view."),
            "insights": ("Insights | UNIV",
                         "Security research, vulnerability analysis and technical notes from UNIV."),
            "careers": ("Careers | UNIV",
                        "We are looking for security engineers to join UNIV."),
            "contact": ("Contact | UNIV",
                        "Talk to us about a security assessment."),
            "security": ("Vulnerability Disclosure | UNIV",
                         "How to report a security vulnerability in UNIV's website or services."),
        },

        "hero": {
            "eyebrow": "Penetration Testing · Red Team · AI Security",
            "title_lines": ["AI scans wide.", "Experts dig deep."],
            "typed": ["API penetration testing", "Network intrusion assessment", "Red team operations", "AI vulnerability scanning"],
            "typed_prefix": "Currently testing —",
            "desc": "Where automation stops, our engineers keep going. Where humans cannot scale, our AI does.\nUNIV is a security firm built to do both.",
            "primary": "Request an assessment",
            "secondary": "Explore services",
            "scroll": "Scroll",
        },
        "stats_title": "UNIV in numbers",
        "stats_note": "Updated as our track record grows.",
        "stats": [
            {"key": "projects", "value": "", "suffix": "+", "label": "Projects delivered"},
            {"key": "cve", "value": "", "suffix": "", "label": "CVEs discovered"},
            {"key": "certs", "value": "", "suffix": "", "label": "Certifications held"},
            {"key": "founded", "value": "2026", "suffix": "", "label": "Founded"},
        ],
        "home_services": {
            "eyebrow": "Services",
            "title": "What we do",
            "desc": "Four services, one rule — if it cannot be reproduced, it is not reported.",
            "more": "Learn more",
            "all": "All services",
        },
        "why": {
            "eyebrow": "Why UNIV",
            "title": "We don't forward scanner output",
            "items": [
                ("Every finding is human-verified",
                 "Even when our AI raises it, an engineer reproduces it before it reaches your report. Clearing the noise is our job, not yours."),
                ("Current attacker tradecraft",
                 "Not a checklist walkthrough — the techniques adversaries are actually using right now."),
                ("Written to be fixed",
                 "Not \"insufficient input validation\", but which file, which line, and what to change."),
                ("Retesting is included",
                 "The report is not the end. We verify that your fix actually holds."),
            ],
        },
        "method": {
            "eyebrow": "Methodology",
            "title": "Built on public standards",
            "desc": "We work from recognised open standards rather than a proprietary method, so results stay comparable and auditable.",
            "items": [
                ("PTES", "Penetration Testing Execution Standard — how the engagement is run"),
                ("OWASP", "WSTG, API Security Top 10 and LLM Top 10 — what gets tested"),
                ("MITRE ATT&CK", "Tactic and technique mapping, and detection gap analysis"),
                ("NIST SP 800-115", "Technical guide to information security testing and assessment"),
            ],
        },
        "clients": {
            "title": "Clients",
            "note": "Drop client logos into static/images/ as client-01.png through client-06.png to display them.",
        },
        "cta": {
            "title": "Find it before they do",
            "desc": "We will find it before an attacker does. Let's start by defining the scope together.",
            "primary": "Start a conversation",
            "secondary": "Report a vulnerability",
        },

        "services_page": {
            "eyebrow": "Services",
            "title": "Security services",
            "desc": "The right assessment depends on where your organisation stands. If you are not sure, we will work it out together in the first conversation.",
        },
        "svc": {
            "targets": "Who this is for",
            "checks": "What we test",
            "process": "How it runs",
            "deliverables": "What you receive",
            "standards": "Standards applied",
            "duration": "Duration",
            "duration_value": "",
            "price": "Pricing",
            "price_value": "",
            "tbd": "Scoped per engagement",
            "back": "All services",
            "cta": "Enquire about this service",
            "next": "Next service",
        },

        "about_page": {
            "eyebrow": "About UNIV",
            "title": "We design defence\nfrom the attacker's seat",
            "lead": "UNIV is a cyber security firm founded in September 2026 in Chuncheon, Korea. "
                    "We run API and network penetration tests and red team operations, and scale that "
                    "work with an AI assessment engine we built ourselves.",
            "body": [
                "Most security reports go unread. Hundreds of scanner findings arrive, and the job of "
                "deciding which ones actually matter is quietly handed back to the client.",
                "We treat that judgement as our work. Our AI covers the full surface and gathers "
                "candidates; our engineers reproduce them one by one and keep only what is genuinely "
                "exploitable. Everything left in the report was confirmed by a person.",
                "That makes our reports short. It also makes every line in them reproducible and fixable.",
            ],
            "principles_title": "How we work",
            "principles": [
                ("No proof, no finding", "Speculative findings erode trust. Nothing enters the report without a proof of concept."),
                ("Understand before attacking", "If we don't know what must be protected, we can't decide what to attack."),
                ("Never cross the agreed line", "No service disruption, no data destruction, nothing outside the agreed scope."),
                ("Publish what we learn", "A safer industry is ultimately what keeps our clients safe."),
            ],
            "ceo_title": "Leadership",
            "ceo_role": "CEO / Security Consultant",
            "ceo_message": "",
            "ceo_bio": "",
            "team_title": "Team",
            "team_note": "Placeholder for team members. Edit TEAM in content.py.",
            "certs_title": "Certifications",
            "certs_note": "Placeholder for individual and corporate certifications.",
            "history_title": "Milestones",
            "history": [
                ("2026.09", "UNIV founded"),
            ],
            "history_note": "Milestones will be added as they happen.",
            "info_title": "Company information",
            "info_labels": {
                "legal": "Legal name",
                "ceo": "CEO",
                "founded": "Founded",
                "address": "Address",
                "phone": "Phone",
                "email": "Email",
                "biz": "Business reg. no.",
            },
        },

        "insights_page": {
            "eyebrow": "Insights",
            "title": "Research and technical notes",
            "desc": "Vulnerability analysis, offensive technique research, and lessons from our engagements.",
            "empty_title": "Our first post is on the way",
            "empty_desc": "Posts will appear here as they are published. Add entries to INSIGHTS in content.py.",
            "read": "Read",
        },

        "careers_page": {
            "eyebrow": "Careers",
            "title": "We're looking for people who dig",
            "desc": "We care less about certificates than about what you have actually broken. CTF write-ups, bug bounty reports, analysis posts — any format works.",
            "values_title": "Who we work well with",
            "values": [
                ("People who don't stop at \"it seems not to work\"", "They find out why it doesn't."),
                ("People who can write", "Findings are only useful if the other side can act on them."),
                ("People who respect the line", "Knowing what you can do is not the same as knowing what you may do."),
            ],
            "openings_title": "Open positions",
            "empty_title": "No open positions right now",
            "empty_desc": "Reach out anyway — we accept speculative applications year-round.",
            "apply": "Apply",
            "open_apply": "Send a speculative application",
        },

        "contact_page": {
            "eyebrow": "Contact",
            "title": "Start with what\nyou need to protect",
            "desc": "You don't need a defined scope. Working out which assessment you actually need is where we start.",
            "form_title": "Request a consultation",
            "form_note": "Filling this in opens your mail app with everything pre-filled. You only need to hit send.",
            "fields": {
                "company": "Company",
                "name": "Your name",
                "email": "Email for our reply",
                "phone": "Phone (optional)",
                "service": "Service of interest",
                "message": "Message",
                "message_ph": "Target systems, rough scale and preferred timing help us give you a more precise answer.",
                "select": "Please select",
                "other": "Not sure yet / need advice",
            },
            "submit": "Compose email",
            "direct_title": "Reach us directly",
            "hours_label": "Consultation hours",
            "hours": "Weekdays 10:00 – 19:00 (KST)",
            "response_label": "Response time",
            "response": "Within one business day",
            "map_note": "Placeholder for a map image.",
        },

        "security_page": {
            "eyebrow": "Vulnerability Disclosure",
            "title": "Found a vulnerability?",
            "desc": "If you have found a security issue in our website or services, please tell us. "
                    "We will not pursue legal action against good-faith researchers.",
            "scope_title": "Scope",
            "scope_in": ["UNIV's official website and subdomains", "Tools and repositories published by UNIV"],
            "scope_out": ["Vulnerabilities in third-party services", "Denial of service and load testing",
                          "Physical intrusion and social engineering", "Reports consisting only of scanner output"],
            "in_label": "In scope",
            "out_label": "Out of scope",
            "rules_title": "Ground rules",
            "rules": [
                "Do not access or modify other people's data.",
                "Do not degrade service availability.",
                "Test only as far as needed to confirm the issue.",
                "Please hold disclosure until remediation is complete.",
            ],
            "how_title": "How to report",
            "how_desc": "Email us reproduction steps and impact. We acknowledge every report within three business days.",
            "timeline_title": "Our process",
            "timeline": [
                ("Received", "Acknowledgement within three business days"),
                ("Validated", "Reproduction and impact assessment"),
                ("Remediated", "Fixed in order of severity"),
                ("Disclosed", "Timing agreed with the reporter"),
            ],
            "report": "Report a vulnerability",
            "txt_note": "This policy is also published at /.well-known/security.txt.",
        },

        "footer": {
            "tagline": "AI scans wide. Experts dig deep.",
            "nav_title": "Services",
            "company_title": "Company",
            "contact_title": "Contact",
            "security_link": "Report a vulnerability",
            "rights": "All rights reserved.",
        },
        "img_slot": {
            "title": "Add an image",
            "hint": "Save a file with this name in static/images/ and it appears automatically",
        },
        "empty_slot": "Placeholder",
        "not_found": {
            "title": "Page not found",
            "desc": "This page has moved or no longer exists.",
            "home": "Back to home",
        },
    },
}


# ---------------------------------------------------------------------------
# 아래는 "틀만 있고 비어 있는" 목록들 ── 채우면 해당 섹션이 자동으로 살아난다
# ---------------------------------------------------------------------------

# 팀원.  예:
# {"name": "홍길동", "name_en": "Gildong Hong", "role": "보안 엔지니어",
#  "role_en": "Security Engineer", "image": "team-01.jpg",
#  "certs": ["OSCP"], "bio": "...", "bio_en": "..."}
TEAM = []

# 보유 자격증 / 기업 인증.  예:
# {"name": "OSCP", "issuer": "OffSec", "count": 2}
CERTIFICATIONS = []

# 인사이트 글.  예:
# {"slug": "...", "date": "2026-10-01", "category": "Research",
#  "title": "...", "title_en": "...", "excerpt": "...", "excerpt_en": "...",
#  "image": "insight-01.jpg", "url": "#"}
INSIGHTS = []

# 채용 공고.  예:
# {"title": "모의해킹 엔지니어", "title_en": "Penetration Tester",
#  "type": "정규직", "type_en": "Full-time", "location": "춘천 / 원격",
#  "location_en": "Chuncheon / Remote", "summary": "...", "summary_en": "..."}
OPENINGS = []

# 고객사 로고 파일명 (static/images/ 기준)
CLIENT_LOGOS = [f"client-{i:02d}.png" for i in range(1, 7)]
