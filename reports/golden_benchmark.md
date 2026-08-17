# Lab 17 Golden Set Report

- Implementation: `student`
- Kind: `golden`
- Cases: **20**
- Passed: **20/20**
- Evidence hit rate: **100.0%**
- Average retrieval latency: **1014.0 ms**
- Average token reduction vs full source context: **6.3%**
- Golden bonus: **10/10** (100% required)

| Case | Layer | Pass | Latency ms | Retrieved tokens | Token reduction | Missing / Error |
| --- | --- | --- | ---: | ---: | ---: | --- |
| G01 | short_term | PASS | 0.8 | 227 | 0.0% |  |
| G02 | short_term | PASS | 0.1 | 133 | 0.0% |  |
| G08 | long_term | PASS | 1647.2 | 829 | 0.0% |  |
| G09 | long_term | PASS | 1456.6 | 1363 | 0.0% |  |
| G12 | semantic | PASS | 314.8 | 418 | 8.9% |  |
| G14 | semantic | PASS | 251.1 | 270 | 30.2% |  |
| G15 | semantic | PASS | 248.6 | 270 | 41.2% |  |
| G19 | mixed | PASS | 1675.5 | 581 | 0.0% |  |
| G03 | long_term | PASS | 1796.6 | 1334 | 0.0% |  |
| G04 | long_term | PASS | 1350.0 | 1341 | 0.0% |  |
| G05 | long_term | PASS | 1624.4 | 1341 | 0.0% |  |
| G10 | episodic | PASS | 270.9 | 579 | 0.0% |  |
| G11 | episodic | PASS | 322.7 | 610 | 0.0% |  |
| G13 | semantic | PASS | 258.9 | 416 | 26.4% |  |
| G16 | mixed | PASS | 1794.9 | 581 | 0.0% |  |
| G18 | mixed | PASS | 541.2 | 500 | 11.5% |  |
| G20 | mixed | PASS | 2144.0 | 831 | 0.0% |  |
| G06 | long_term | PASS | 1419.4 | 1351 | 0.0% |  |
| G07 | long_term | PASS | 1428.1 | 1356 | 0.0% |  |
| G17 | mixed | PASS | 1733.8 | 581 | 8.1% |  |

## Evidence excerpts

### G01 - short_term

`<SESSION_SUMMARY> user: Constraint HOLD-ALPHA-0900: standup is 09:00 sharp and must not be forgotten. | assistant: Noted standup constraint. | user: Constraint HOLD-BETA-STAGING: writes go to staging DB only. | assistant: Noted staging constraint. | user: Filler A about button padding. | assistant: Filler A. | user: Filler B about color tokens. | assistant: Filler B. | user: Filler C about copy tone. | assistant: Filler C. </SESSION_SUMMARY> <DURABLE_NOTES> - user: Constraint HOLD-ALPHA-0900: standup is 09:00 sharp and must not be forgotten. - assistant: Noted standup constraint. - user: Constraint HOLD-BETA-STAGING: writes go to staging DB only. - assistant: Noted staging constraint. </DURA`

### G02 - short_term

`<RECENT_TURNS> user: Ten du an ca nhan cua toi la ORCHID-27. Toi thich Python va khong thich Java. Khi giai thich code, hay dung vi du ngan. assistant: Da hieu: demo ca nhan ORCHID-27, uu tien Python, tranh Java, vi du ngan. user: Toi dang hoc async/await va hay nham coroutine voi Task. Neu sau nay gap chu de nay, hay giai thich bang timeline. assistant: Toi se uu tien timeline khi giai thich coroutine va Task. user: TODO: hoan thanh benchmark report truoc thu Sau luc 16:00. Day la open loop LAB-REPORT-1600. </RECENT_TURNS>`

### G08 - long_term

`<USER_SUMMARY> Lan's project is LOTUS-88. They prioritize Java and Spring Boot and do not use Python for the backend. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2026-08-17 05:02:29     Source: message     Content: [user] {   "user_id": "lan-lab17",   "first_name": "Lan",   "last_name": "Tran",   "user_alias": "Evaluation User" }: Minh la Lan, minh dang muon them retry cho phan goi payment trong san pham cua minh va minh muon vi du code hop voi dung stack ma minh dang dung chu dung dua cho minh vi du cua ngon ngu khac. Ban gy y gium minh: dua theo backend ma minh da chon cho san pham cua minh, minh nen viet retry paym`

### G09 - long_term

`<USER_SUMMARY> Minh Nguyen is working on a personal project named ORCHID-27, for which Python is used. For the company project BLUEBIRD-42, TypeScript with NestJS is mandatory for the backend, and Python is not to be used for this specific project.  Minh Nguyen prefers Python and dislikes Java. When explaining code, Minh prefers short examples. When explaining the topic of async/await and the confusion between coroutine and Task, Minh Nguyen requests that the explanation be provided as a timeline. The assistant will prioritize a timeline when explaining coroutine and Task. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2`

### G12 - semantic

`EPISODE: {"id":"kb-payment-retry","entity":"Payment API Retry Policy","summary":"For POST /payments, every retryable request MUST send the same Idempotency-Key. Retry only HTTP 429 or transient 5xx errors, use exponential-backoff, and stop after max-3-retries. Marker: PAYMENT-RULE-3.","source":"internal-api-guideline-v3","updated_at":"2026-08-10T00:00:00Z"} metadata= EPISODE: For POST /payments, every retryable request MUST send the same Idempotency-Key. Retry only HTTP 429 or transient 5xx errors, use exponential-backoff, and stop after max-3-retries. Marker: PAYMENT-RULE-3. metadata= EPISODE: {"id":"kb-memory-privacy","entity":"Agent Memory Privacy Rule","summary":"Do not persist personal `

### G14 - semantic

`EPISODE: {"id":"kb-memory-privacy","entity":"Agent Memory Privacy Rule","summary":"Do not persist personal data without explicit opt-in. A deletion request must remove user-scoped memory and be verified across every store. Marker: DELETE-VERIFY-ALL.","source":"memory-governance-policy","updated_at":"2026-08-12T00:00:00Z"} metadata= EPISODE: Do not persist personal data without explicit opt-in. A deletion request must remove user-scoped memory and be verified across every store. Marker: DELETE-VERIFY-ALL. metadata= EPISODE: {"id":"kb-context-budget","entity":"Memory Context Budget","summary":"Reserve bounded context for memory. This lab uses short-term 10 percent, long-term 4 percent, episodi`

### G15 - semantic

`EPISODE: {"id":"kb-memory-privacy","entity":"Agent Memory Privacy Rule","summary":"Do not persist personal data without explicit opt-in. A deletion request must remove user-scoped memory and be verified across every store. Marker: DELETE-VERIFY-ALL.","source":"memory-governance-policy","updated_at":"2026-08-12T00:00:00Z"} metadata= EPISODE: Do not persist personal data without explicit opt-in. A deletion request must remove user-scoped memory and be verified across every store. Marker: DELETE-VERIFY-ALL. metadata= EPISODE: {"id":"kb-context-budget","entity":"Memory Context Budget","summary":"Reserve bounded context for memory. This lab uses short-term 10 percent, long-term 4 percent, episodi`

### G19 - mixed

`<LONG_TERM> <USER_SUMMARY> Lan's project is LOTUS-88. They prioritize Java and Spring Boot and do not use Python for the backend. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2026-08-01 11:00:00     Source: message     Content: [user] {   "user_id": "lan-lab17",   "first_name": "Lan",   "last_name": "Tran",   "user_alias": "Lan Tran" }: Toi la Lan. Du an cua toi la LOTUS-88. Toi uu tien Java va Spring Boot, va khong dung Python trong vi du backend.   - Created At: 2026-08-01 11:00:20     Source: message     Content: Lab Assistant (assistant): Da hieu: LOTUS-88, Java + Spring Boot cho backend examples. </EPISODES>  <FAC`

### G03 - long_term

`<USER_SUMMARY> Minh Nguyen is working on a personal project named ORCHID-27, for which Python is used. For the company project BLUEBIRD-42, TypeScript with NestJS is mandatory for the backend, and Python is not to be used for this specific project.  Minh Nguyen prefers Python and dislikes Java. When explaining code, Minh prefers short examples. When explaining the topic of async/await and the confusion between coroutine and Task, Minh Nguyen requests that the explanation be provided as a timeline. The assistant will prioritize a timeline when explaining coroutine and Task. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2`

### G04 - long_term

`<USER_SUMMARY> Minh Nguyen is working on a personal project named ORCHID-27, for which Python is used. For the company project BLUEBIRD-42, TypeScript with NestJS is mandatory for the backend, and Python is not to be used for this specific project.  Minh Nguyen prefers Python and dislikes Java. When explaining code, Minh prefers short examples. When explaining the topic of async/await and the confusion between coroutine and Task, Minh Nguyen requests that the explanation be provided as a timeline. The assistant will prioritize a timeline when explaining coroutine and Task. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2`

### G05 - long_term

`<USER_SUMMARY> Minh Nguyen is working on a personal project named ORCHID-27, for which Python is used. For the company project BLUEBIRD-42, TypeScript with NestJS is mandatory for the backend, and Python is not to be used for this specific project.  Minh Nguyen prefers Python and dislikes Java. When explaining code, Minh prefers short examples. When explaining the topic of async/await and the confusion between coroutine and Task, Minh Nguyen requests that the explanation be provided as a timeline. The assistant will prioritize a timeline when explaining coroutine and Task. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2`

### G10 - episodic

`EPISODE: Cach hieu qua la reuse aiohttp ClientSession va dat concurrency=20. Reflection: loi chinh la connection churn, khong phai timeout threshold. Ma su co ASYNC-FIX-20. EPISODE: Da ghi nhan trajectory: increase timeout khong hieu qua; ClientSession + concurrency=20 giai quyet connection churn. EPISODE: Toi nay minh muon viet cho tron ven cai retry payment ma vua dung so thich stack ca nhan cua minh, vua theo dung policy thanh toan chinh thuc, vua tranh dam lai dung cai su co asyn EPISODE: Minh dang ngoi mot minh viet cho xong cai ham retry cho POST payment de toi nay demo, va minh muon no vua dung dung ngon ngu ma minh thich khi lam viec ca nhan, vua bam sat dung po EPISODE: Minh dang vi`

### G11 - episodic

`EPISODE: Cach hieu qua la reuse aiohttp ClientSession va dat concurrency=20. Reflection: loi chinh la connection churn, khong phai timeout threshold. Ma su co ASYNC-FIX-20. EPISODE: Da ghi nhan trajectory: increase timeout khong hieu qua; ClientSession + concurrency=20 giai quyet connection churn. EPISODE: Minh dang setup lai moi truong dev cho mot buoi ngoi code mot minh cuoi tuan nay, kieu khong co ai chung nhom, chi lam project rieng cua minh cho vui thoi. Truoc khi minh chon temp EPISODE: Minh dang viet mot cai note tong ket ngan de tuan sau trinh bay cho ca nhom nghe ve cach minh phan biet giua viec ca nhan va viec o cong ty, vi may ban trong nhom hay bi lan lon. D EPISODE: Tuan nay min`

### G13 - semantic

`EPISODE: {"id":"kb-async-http","entity":"Async HTTP Incident Playbook","summary":"When async HTTP calls time out, inspect connection pooling, downstream saturation and concurrency before increasing timeout. Reuse a long-lived client session where possible. Marker: CONN-POOL-FIRST.","source":"incident-playbook-2026","updated_at":"2026-08-11T00:00:00Z"} metadata= EPISODE: When async HTTP calls time out, inspect connection pooling, downstream saturation and concurrency before increasing timeout. Reuse a long-lived client session where possible. Marker: CONN-POOL-FIRST. metadata= EPISODE: {"id":"kb-memory-privacy","entity":"Agent Memory Privacy Rule","summary":"Do not persist personal data witho`

### G16 - mixed

`<LONG_TERM> <USER_SUMMARY> Minh Nguyen is working on a personal project named ORCHID-27, for which Python is used. For the company project BLUEBIRD-42, TypeScript with NestJS is mandatory for the backend, and Python is not to be used for this specific project.  Minh Nguyen prefers Python and dislikes Java. When explaining code, Minh prefers short examples. When explaining the topic of async/await and the confusion between coroutine and Task, Minh Nguyen requests that the explanation be provided as a timeline. The assistant will prioritize a timeline when explaining coroutine and Task. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - C`

### G18 - mixed

`<EPISODIC> EPISODE: Cach hieu qua la reuse aiohttp ClientSession va dat concurrency=20. Reflection: loi chinh la connection churn, khong phai timeout threshold. Ma su co ASYNC-FIX-20. EPISODE: Toi nay minh muon viet cho tron ven cai retry payment ma vua dung so thich stack ca nhan cua minh, vua theo dung policy thanh toan chinh thuc, vua tranh dam lai dung cai su co asyn EPISODE: Tuan nay minh moi bi keo vao cai du an ben cong ty va sep hoi lien tuc ve chuyen chuan hoa backend, ma minh thi hoi mo ho vi truoc gio minh xai nhieu thu khac nhau cho project rien EPISODE: Tuan nay minh phai them chuc nang retry payment vao dung cai backend cua du an ben cong ty chu khong phai project ca nhan, nen `

### G20 - mixed

`<LONG_TERM> <USER_SUMMARY> Minh Nguyen is working on a personal project named ORCHID-27, for which Python is used. For the company project BLUEBIRD-42, TypeScript with NestJS is mandatory for the backend, and Python is not to be used for this specific project.  Minh Nguyen prefers Python and dislikes Java. When explaining code, Minh prefers short examples. When explaining the topic of async/await and the confusion between coroutine and Task, Minh Nguyen requests that the explanation be provided as a timeline. The assistant will prioritize a timeline when explaining coroutine and Task. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - C`

### G06 - long_term

`<USER_SUMMARY> Minh Nguyen is working on a personal project named ORCHID-27, for which Python is used. For the company project BLUEBIRD-42, TypeScript with NestJS is mandatory for the backend, and Python is not to be used for this specific project.  Minh Nguyen prefers Python and dislikes Java. When explaining code, Minh prefers short examples. When explaining the topic of async/await and the confusion between coroutine and Task, Minh Nguyen requests that the explanation be provided as a timeline. The assistant will prioritize a timeline when explaining coroutine and Task. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2`

### G07 - long_term

`<USER_SUMMARY> Minh Nguyen is working on a personal project named ORCHID-27, for which Python is used. For the company project BLUEBIRD-42, TypeScript with NestJS is mandatory for the backend, and Python is not to be used for this specific project.  Minh Nguyen prefers Python and dislikes Java. When explaining code, Minh prefers short examples. When explaining the topic of async/await and the confusion between coroutine and Task, Minh Nguyen requests that the explanation be provided as a timeline. The assistant will prioritize a timeline when explaining coroutine and Task. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2`

### G17 - mixed

`<LONG_TERM> <USER_SUMMARY> Minh Nguyen is working on a personal project named ORCHID-27, for which Python is used. For the company project BLUEBIRD-42, TypeScript with NestJS is mandatory for the backend, and Python is not to be used for this specific project.  Minh Nguyen prefers Python and dislikes Java. When explaining code, Minh prefers short examples. When explaining the topic of async/await and the confusion between coroutine and Task, Minh Nguyen requests that the explanation be provided as a timeline. The assistant will prioritize a timeline when explaining coroutine and Task. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - C`
