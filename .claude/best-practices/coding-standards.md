# TinyFish Engineering — Code Quality Principles

Standards for writing maintainable, legible code — for humans and coding agents alike. Exceptions exist; apply judgment.

---

## 1. Don't Repeat Yourself (DRY)

If logic appears more than once, it belongs in a shared function, constant, or module. Duplication creates drift — two copies of the same logic will eventually diverge.

```ts
// ✗ rate limit check copy-pasted across routes
if (account.plan === 'pro' || account.monthlyRequests > 10_000) {
  applyHighThroughputLimits(req);
}
// ... in another handler ...
if (account.plan === 'pro' || account.monthlyRequests > 10_000) {
  applyHighThroughputLimits(req);
}

// ✓ single source of truth
const isPowerUser = (account: Account) =>
  account.plan === 'pro' || account.monthlyRequests > 10_000;
```

This applies to strings, config values, types, and logic — not just functions.

**Exception: don't over-apply DRY to trivial one-liners.** If the "duplication" is a simple conditional that takes two lines and carries no real logic, extracting it into a named function adds indirection without adding clarity.

```ts
// ✗ a helper that exists solely to save two lines — the name adds no meaning
function maybeOpen(path: string, shouldOpen: boolean) {
  if (shouldOpen) openInBrowser(path);
}

// ✓ just write it inline — it's obvious, and there's nothing to drift
if (args.open) openInBrowser(outputPath);
if (args.open) openInBrowser(outputPath); // repeated in cmd_full — that's fine
```

A good signal: if you can't give the helper a name that's more informative than reading the two lines directly, the abstraction isn't paying for itself.

---

## 2. Write Legible, Self-Documenting Code

If a block requires a comment to be understood, that's a signal to restructure. Name things for what they mean, not what they are. Code that reads like prose rarely needs explanation.

Single-letter variables and terse abbreviations are fine in coding competitions. In production they are a liability — the next reader has no implicit context, and neither does an agent.

```ts
// ✗ what is r, s, t?
const r = await fetch(u);
const s = r.status;
const t = await r.json();
const out = t.d.filter(x => x.s > 0).map(x => x.u).slice(0, n);

// ✓ readable without any comments
const response = await fetch(searchUrl);
const { data: results } = await response.json();
const activeResultUrls = results
  .filter(result => result.score > 0)
  .map(result => result.url)
  .slice(0, maxResults);
```

Name booleans as assertions (`isAllocated`, `hasCredits`, `canRunAgent`). Name functions as verbs (`fetchContent`, `allocateBrowser`, `scoreResults`). Extract complex conditions into named variables.

---

## 3. No Magic Numbers or Strings

Literals embedded in logic are opaque and brittle. Name them.

```ts
// ✗ what do these numbers mean?
if (session.browsers > 5) throw new Error('limit reached');
setTimeout(releaseBrowser, 30_000);
if (plan === 'pro_v2') { ... }

// ✓ named, findable, changeable in one place
const MAX_CONCURRENT_BROWSERS = 5;
const BROWSER_IDLE_TIMEOUT_MS = 30_000;
const PLAN = { PRO: 'pro_v2', FREE: 'free' } as const;

if (session.browsers > MAX_CONCURRENT_BROWSERS)
  throw new Error('Concurrent browser limit reached');
setTimeout(releaseBrowser, BROWSER_IDLE_TIMEOUT_MS);
```

Applies equally to plan identifiers, route paths, event names, and any literal that carries meaning beyond its raw value.

---

## 4. Guard Against Errors — Proportionally

Wrap the meaningful boundary, not every line. Chained try/catch blocks are noise. One well-placed handler with a descriptive message tells you everything you need.

```ts
// ✗ over-guarded, repetitive, obscures intent
try {
  const browser = await allocate(sessionId);
  try {
    const page = await browser.newPage();
    try { return await page.fetch(url); }
    catch (e) { throw new Error('fetch failed'); }
  } catch (e) { throw new Error('page failed'); }
} catch (e) { throw new Error('alloc failed'); }

// ✓ one boundary, descriptive message
try {
  const browser = await allocate(sessionId);
  const page = await browser.newPage();
  return await page.fetch(url);
} catch (err) {
  const msg = err instanceof Error ? err.message : String(err);
  throw new Error(`Browser fetch failed for session ${sessionId}: ${msg}`);
}
```

Don't swallow errors silently. Don't re-guard inputs already validated upstream. Let errors propagate with context attached.

---

## 5. Avoid Deep Nesting

More than 2–3 levels of indentation is usually a design problem. Deep nesting makes the happy path hard to find and raises cognitive load for every future reader.

```ts
// ✗ where does the work actually happen?
if (account) {
  if (account.isActive) {
    if (isPowerUser(account)) {
      if (session.browsersAvailable > 0) {
        runAgent(task);
      }
    }
  }
}

// ✓ guard clauses flatten the structure
if (!account?.isActive) return;
if (!isPowerUser(account)) return;
if (session.browsersAvailable === 0) return;
runAgent(task);
```

Prefer early returns and guard clauses. Extract inner blocks into named functions. Flat code is easier to test, read, and reason about.

---

## 6. Comments: Signal, Not Noise

Keep comments that explain non-obvious decisions. Remove comments that describe what the code already shows, or that document process, history, or planning.

**Keep:**
- Why a counterintuitive approach was chosen
- References to external specs, tickets, or known platform quirks
- Warnings about subtle side effects or ordering dependencies

**Remove:**
- `// Step 1: fetch content` — the code says this
- `// TODO: refactor later` — use a ticket
- `// Fixed bug where agent was hanging` — that's git's job
- Commented-out code — delete it; history is preserved in version control

---

## 7. Single Responsibility

Functions and modules should do one thing. If you can't name a function without using "and", it should be split.

```ts
// ✗ fetches, scores, AND persists — too many jobs
async function runSearchAndSave(query: string, accountId: string) {
  const raw = await searchIndex(query);
  const scored = raw.map(r => ({ ...r, score: scoreResult(r, query) }));
  const top = scored.sort((a, b) => b.score - a.score).slice(0, 10);
  await db.searches.insert({ accountId, query, results: top });
  await billing.recordUsage(accountId, 'search');
  return top;
}

// ✓ each function has one clear job
const search = (query: string) => searchIndex(query);

const rankResults = (results: Result[], query: string) =>
  results
    .map(r => ({ ...r, score: scoreResult(r, query) }))
    .sort((a, b) => b.score - a.score)
    .slice(0, 10);

async function runSearch(query: string, accountId: string) {
  const results = rankResults(await search(query), query);
  await db.searches.insert({ accountId, query, results });
  await billing.recordUsage(accountId, 'search');
  return results;
}
```

---

## 8. Consistent Abstraction Levels

A function should operate at one level of abstraction. Don't mix high-level orchestration with low-level implementation detail in the same body. Either a function calls other functions, or it does work — rarely both.

```ts
// ✗ mixes orchestration with raw header construction
async function executeAgentTask(task: AgentTask) {
  const headers = {
    'Authorization': `Bearer ${process.env.API_KEY}`,
    'X-Session-Id': task.sessionId,
    'Content-Type': 'application/json',
  };
  const res = await fetch('/api/agent/run', {
    method: 'POST', headers, body: JSON.stringify(task),
  });
  if (!res.ok) throw new Error(`Agent API error: ${res.status}`);
  const { jobId } = await res.json();
  await db.jobs.insert({ jobId, taskId: task.id, status: 'running' });
  emitEvent('agent.started', { jobId, taskId: task.id });
}

// ✓ orchestration reads like a summary; details live elsewhere
async function executeAgentTask(task: AgentTask) {
  const { jobId } = await agentApi.run(task);
  await db.jobs.insert({ jobId, taskId: task.id, status: 'running' });
  emitEvent('agent.started', { jobId, taskId: task.id });
}
```

A reader scanning the high-level function should understand the flow without parsing implementation details. Those belong one level down.

---

## 9. Fail Fast, Fail Loudly

Validate preconditions as early as possible — ideally at startup — and crash with a clear, specific message. A misconfigured service that fails at boot is caught in CI and never reaches users. The same misconfiguration discovered at runtime surfaces as a confusing error deep in a call stack, hours or days later.

```python
# ✗ missing API key is only discovered when the route is first called
from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/summarise")
async def summarise(text: str):
    client = openai.AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])  # KeyError here, in prod, under load
    return await client.chat.completions.create(...)


# ✓ missing API key crashes the process on startup — deployment fails, pager fires, no user impact
from fastapi import FastAPI
import os

app = FastAPI()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is required but not set")

client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)

@app.get("/summarise")
async def summarise(text: str):
    return await client.chat.completions.create(...)
```

The same principle applies to any required config: database URLs, feature flags that gate critical paths, credentials for downstream services. Check at startup, crash loudly, fix before shipping.

---

## 10. Explicit Over Implicit

Avoid cleverness that makes behavior hard to trace — auto-wiring, convention-over-configuration magic, dynamic dispatch based on string keys. Code should be followable linearly, without knowing hidden rules.

```ts
// ✗ which handler runs? depends on runtime string matching
registry.register('content.*', handler);
registry.register('agent.run', handler);
registry.dispatch(event.type, event); // good luck tracing this

// ✓ control flow is obvious at the call site
switch (event.type) {
  case 'content.fetched': return onContentFetched(event);
  case 'content.failed':  return onContentFailed(event);
  case 'agent.run':       return onAgentRun(event);
  default:
    throw new Error(`Unhandled event type: ${event.type}`);
}
```

Explicit dependency passing, clear return values, and obvious control flow are worth more than brevity. If a reader has to know framework conventions to understand what code does, that's implicit behavior.

---

## 11. Pure Functions & Data In / Data Out

Functions should take inputs and return outputs. Don't mutate state inside a function unless mutation is explicitly the function's stated purpose. Unexpected side effects are among the hardest bugs to trace.

```ts
// ✗ silently mutates the request object it was handed
function applyRateLimitHeaders(req: ApiRequest) {
  req.headers['X-RateLimit-Limit'] = getRateLimit(req.account);
  req.headers['X-RateLimit-Remaining'] = getRemaining(req.account);
  req.account.lastRequestAt = Date.now(); // caller's req is now permanently altered
}

// ✓ returns a new value; caller controls what happens to it
function buildRateLimitHeaders(account: Account): Record<string, string> {
  return {
    'X-RateLimit-Limit': String(getRateLimit(account)),
    'X-RateLimit-Remaining': String(getRemaining(account)),
  };
}
```

At system boundaries (API handlers, DB writes, external services), side effects are unavoidable — push them to the edges. Core logic should be pure: same inputs, same outputs, no surprises.

---

## 12. Descriptive Arguments, Legible Call Sites

Function signatures should be readable at the *call site*. Positional boolean flags and long argument lists are unreadable without an IDE tooltip. Use named options objects for anything non-obvious.

```ts
// ✗ what does true, false, true mean here?
spawnBrowser('chromium', true, false, true, 30_000);

// ✓ self-documenting at the call site
spawnBrowser('chromium', {
  headless: true,
  persistSession: false,
  blockAds: true,
  timeoutMs: 30_000,
});
```

If a function takes more than 2–3 positional parameters, reach for an options object. Boolean flag parameters almost always mean the function should be split or its arguments made explicit. Keep argument lists short enough that the function's purpose remains obvious.

---

## 13. Delete Dead Code Ruthlessly

Unused functions, unreachable branches, stale feature flags, commented-out experiments — remove them. Dead code misleads every future reader about what the system actually does. It's especially toxic for coding agents, which treat everything present as intentional.

```ts
// ✗ is this old? intentional? safe to call?
// async function legacyFetchContent(url: string) {
//   return oldContentApi.get(url);
// }

async function fetchContent(url: string, opts: FetchOptions) {
  if (FEATURE_FLAGS.USE_NEW_FETCHER) { // shipped 3 months ago
    return newFetcher.fetch(url, opts);
  }
  return oldFetcher.fetch(url, opts); // dead branch
}

// ✓ shipped means cleaned up
const fetchContent = (url: string, opts: FetchOptions) =>
  newFetcher.fetch(url, opts);
```

Version control preserves history. If code is gone and you need it back, git has it. The working codebase should reflect only what the system currently does.

---

## 14. Bias for Immutability

Default to `const`. Don't mutate function arguments. Return new objects instead of modifying existing ones. Mutation at a distance — where something changes a value it doesn't own — is one of the hardest categories of bug to trace.

```ts
// ✗ mutates the config it was handed; caller is surprised
function applyDefaults(config: AgentConfig) {
  config.timeoutMs = config.timeoutMs ?? 10_000;
  config.maxSteps = config.maxSteps ?? 50;
  config.retries = config.retries ?? 2;
  return config;
}

// ✓ caller's object is untouched; undefined values in config don't overwrite defaults
function applyDefaults(config: AgentConfig): AgentConfig {
  return {
    ...config,
    timeoutMs: config.timeoutMs ?? 10_000,
    maxSteps: config.maxSteps ?? 50,
    retries: config.retries ?? 2,
  };
}
```

Immutability isn't a dogma — in-place mutation is valid in performance-critical paths. The default posture: don't mutate what you don't own, and be explicit when you do.

---

## 15. Pull Requests: Single Purpose, Small Surface

A PR should do one thing. Not one thing and a rename. Not one thing and a file reorganisation. Not one thing and a dependency upgrade. Each of those is its own PR.

Single-purpose PRs are faster to review, less likely to conflict with parallel work, and trivial to revert precisely. A PR that mixes a feature with drive-by renames or file moves buries the meaningful change and makes the reviewer's job harder than it needs to be.

As a practical ceiling: **350 SLoC changed**, excluding generated or non-semantic files (lock files, CSS stylesheets, compiled assets). Regularly breaching that is a sign the change should be split.

A PR probably needs splitting if:
- The title requires "and" to describe it accurately
- The diff includes file moves or renames alongside logic changes
- Rolling it back would undo multiple independent decisions

When a large mechanical change is unavoidable (e.g. a codebase-wide rename), make it a dedicated PR with zero logic changes so it can be reviewed and reverted cleanly.

---

## 16. PR Titles: Be Descriptive Enough to Scan

A PR title should give a reader enough context to judge relevance without opening the diff. In a review queue, a changelog, or git log, you should be able to guess whether a change is related to a bug you're seeing or an area you're about to touch.

The bar is specificity. Both "Fixed edge case when users don't have enough credits for a run" and "Added null check to credit validation" pass — they're scannable and specific. Vague titles don't.

```
// ✗ useless on a scan
Fixed some bugs
WIP
Tweaks
PR for review

// ✓ specific enough to judge relevance at a glance
Fixed edge case where users with insufficient credits could trigger a run
Fixed browser session leak when agent task times out
Added null check to credit validation
Added per-account rate limiting for the search API
Refactored browser allocation to reduce cold-start latency
```
