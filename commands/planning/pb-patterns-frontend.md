---
name: "pb-patterns-frontend"
title: "Frontend Architecture Patterns"
category: "planning"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-design-language', 'pb-a11y', 'pb-patterns-async', 'pb-patterns-api', 'pb-testing']
last_reviewed: "2026-02-09"
last_evolved: ""
version: "1.0.0"
version_notes: "v2.10.0 baseline"
breaking_changes: []
---
# Frontend Architecture Patterns

Patterns for building scalable, maintainable user interfaces. Mobile-first and theme-aware by default.

**Trade-offs exist:** Frontend complexity compounds quickly. Use `/pb-preamble` thinking (challenge the need for each abstraction) and `/pb-design-rules` thinking (Clarity in component boundaries, Simplicity in state management, Resilience through graceful degradation).

Question whether that library is necessary. Challenge whether that abstraction earns its complexity. Understand the constraints before adding patterns.

**Resource Hint:** sonnet — Frontend pattern reference; implementation-level UI architecture decisions.

## When to Use

- Designing component architecture for a new frontend project
- Choosing state management, styling, or rendering patterns
- Reviewing frontend code against scalability and maintainability principles

---

## Philosophy

### Mobile-First is Not Optional

**Mobile-first means:**
- Start with the smallest viewport, enhance upward
- Simplest layout is the default; complexity is opt-in
- Touch targets before hover states
- Performance budget starts tight, not loose

**Why mobile-first:**
```css
/* [NO] Desktop-first: Start complex, override to simple */
.sidebar {
  display: flex;
  width: 300px;
}
@media (max-width: 768px) {
  .sidebar {
    display: none;  /* Undoing work */
  }
}

/* [YES] Mobile-first: Start simple, enhance to complex */
.sidebar {
  display: none;  /* Simple default */
}
@media (min-width: 768px) {
  .sidebar {
    display: flex;
    width: 300px;  /* Enhancement */
  }
}
```

The second approach:
- Faster on mobile (no CSS to override)
- Progressive enhancement (features are additive)
- Forces prioritization (what matters on small screens?)

### Theme-Aware is Foundational

Design systems that support theming from day one:

```css
/* [NO] Hardcoded colors scattered everywhere */
.button {
  background: #3b82f6;
  color: white;
}

/* [YES] Design tokens enable theming */
.button {
  background: var(--color-primary);
  color: var(--color-on-primary);
}
```

Theme-awareness enables:
- Dark/light mode without refactoring
- Brand customization for white-label
- Accessibility adjustments (high contrast)
- Future design evolution

See `/pb-design-language` for project-specific token systems.

---

## Component Patterns

### Atomic Design (Component Hierarchy)

Organize components by composition level:

```
Atoms       → Basic building blocks (Button, Input, Icon)
Molecules   → Simple combinations (SearchField = Input + Button)
Organisms   → Complex sections (Header = Logo + Nav + SearchField)
Templates   → Page layouts (empty of content)
Pages       → Templates filled with real content
```

**Key insight:** Components at lower levels should know NOTHING about higher levels.

```typescript
// [NO] Atom that knows about the page
function Button({ onClick, pageContext }) {
  const label = pageContext.isCheckout ? 'Buy Now' : 'Submit';
  return <button onClick={onClick}>{label}</button>;
}

// [YES] Atom that is context-agnostic
function Button({ onClick, children }) {
  return <button onClick={onClick}>{children}</button>;
}

// Page provides context
function CheckoutPage() {
  return <Button onClick={handleCheckout}>Buy Now</Button>;
}
```

### Compound Components

For components with related pieces that share implicit state:

```typescript
// [NO] Prop drilling and configuration overload
<Tabs
  tabs={[
    { label: 'Overview', content: <Overview /> },
    { label: 'Details', content: <Details /> },
  ]}
  activeTab={0}
  onTabChange={setActiveTab}
/>

// [YES] Compound pattern - flexible, readable
<Tabs>
  <Tabs.List>
    <Tabs.Tab>Overview</Tabs.Tab>
    <Tabs.Tab>Details</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panels>
    <Tabs.Panel><Overview /></Tabs.Panel>
    <Tabs.Panel><Details /></Tabs.Panel>
  </Tabs.Panels>
</Tabs>
```

**Compound components:**
- Share state via Context internally
- Expose flexible composition externally
- Self-document their structure

**Use when:** Component has multiple related parts (Tabs, Accordion, Dropdown, Modal)

### Container/Presentational Split

Separate data fetching from rendering:

```typescript
// Presentational: Pure rendering, no data fetching
function UserCard({ name, avatar, onEdit }) {
  return (
    <article className="user-card">
      <img src={avatar} alt="" />
      <h2>{name}</h2>
      <button onClick={onEdit}>Edit</button>
    </article>
  );
}

// Container: Data fetching and state
function UserCardContainer({ userId }) {
  const { data: user, isLoading } = useUser(userId);
  const { mutate: updateUser } = useUpdateUser();

  if (isLoading) return <UserCardSkeleton />;

  return (
    <UserCard
      name={user.name}
      avatar={user.avatar}
      onEdit={() => updateUser(userId)}
    />
  );
}
```

**Benefits:**
- Presentational components are easy to test and Storybook
- Containers can be swapped (different data sources)
- Clear responsibility boundaries

**Modern evolution:** Hooks blur this line. The principle (separate concerns) still applies even if the boundary is within a single component.

---

## State Management

### State Location Decision Tree

```
Is this state used by only ONE component?
├─ Yes → Local state (useState)
└─ No → Is it used by SIBLINGS or PARENT?
    ├─ Yes → Lift state to common ancestor
    └─ No → Is it DEEPLY nested (prop drilling)?
        ├─ Yes → Context or state library
        └─ No → Is it SERVER state (fetched data)?
            ├─ Yes → Data fetching library (React Query, SWR)
            └─ No → Is it URL state (search, filters)?
                ├─ Yes → URL parameters
                └─ No → Global state library (if truly global)
```

### Server State vs Client State

**Server state:** Data from backend (users, products, orders)
- Use: React Query, SWR, Apollo
- Characteristics: Async, cacheable, can be stale

**Client state:** UI state (modals, selections, form inputs)
- Use: useState, useReducer, Context, Zustand
- Characteristics: Sync, ephemeral, always fresh

```typescript
// [NO] Treating server state like client state
const [users, setUsers] = useState([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);

useEffect(() => {
  setLoading(true);
  fetchUsers()
    .then(setUsers)
    .catch(setError)
    .finally(() => setLoading(false));
}, []);

// [YES] Dedicated server state management
const { data: users, isLoading, error } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers,
});
```

**Benefits of server state libraries:**
- Automatic caching and invalidation
- Background refetching
- Optimistic updates
- Request deduplication
- Loading/error states handled

### URL State

State that should survive refresh or be shareable:

```typescript
// [NO] Filters in local state (lost on refresh)
const [filters, setFilters] = useState({ category: 'all', sort: 'newest' });

// [YES] Filters in URL (shareable, survives refresh)
function useFilters() {
  const [searchParams, setSearchParams] = useSearchParams();

  const filters = {
    category: searchParams.get('category') || 'all',
    sort: searchParams.get('sort') || 'newest',
  };

  const setFilters = (newFilters) => {
    setSearchParams(new URLSearchParams(newFilters));
  };

  return [filters, setFilters];
}
```

**URL state candidates:**
- Search queries
- Filters and sorting
- Pagination
- Selected items (for sharing)
- Modal/drawer open state (debatable)

---

## UI States

Every component that fetches data or performs async operations needs three states: loading, error, and empty. Handle all three explicitly.

### Loading States

```typescript
// [NO] Boolean loading with no visual feedback
if (loading) return null;

// [YES] Skeleton that matches content shape
if (isLoading) return <UserCardSkeleton />;

// [YES] Progressive loading for lists
function UserList({ users, isLoading }) {
  if (isLoading && users.length === 0) {
    return <UserListSkeleton count={5} />;
  }

  return (
    <>
      {users.map(user => <UserCard key={user.id} user={user} />)}
      {isLoading && <LoadingSpinner />} {/* Loading more */}
    </>
  );
}
```

**Loading patterns:**
- **Skeletons:** Match content shape, use for initial load
- **Spinners:** Use for actions (button click, form submit)
- **Progress bars:** Use for known-duration operations (uploads)
- **Optimistic UI:** Show expected result immediately, rollback on error

### Error States

```typescript
// [NO] Silent failure
if (error) return null;

// [YES] Actionable error with retry
function DataDisplay({ data, error, refetch }) {
  if (error) {
    return (
      <ErrorCard>
        <p>Failed to load data. Please try again.</p>
        <Button onClick={refetch}>Retry</Button>
      </ErrorCard>
    );
  }
  return <DataContent data={data} />;
}

// [YES] Error boundary for unexpected errors
<ErrorBoundary fallback={<ErrorFallback />}>
  <UserProfile />
</ErrorBoundary>
```

**Error patterns:**
- **Inline errors:** For form fields, local failures
- **Error cards:** For section-level failures with retry
- **Error boundaries:** For unexpected crashes (React)
- **Toast notifications:** For background operation failures

### Empty States

```typescript
// [NO] Just nothing
if (items.length === 0) return null;

// [YES] Contextual empty state with action
function ProjectList({ projects, onCreateProject }) {
  if (projects.length === 0) {
    return (
      <EmptyState
        icon={<FolderIcon />}
        title="No projects yet"
        description="Create your first project to get started."
        action={<Button onClick={onCreateProject}>Create Project</Button>}
      />
    );
  }
  return <ProjectGrid projects={projects} />;
}
```

**Empty state types:**
- **First-use:** No data yet, guide user to create
- **No results:** Search/filter returned nothing, suggest clearing filters
- **Filtered empty:** Data exists but filter excludes all, show "clear filters"
- **Error empty:** Failed to load, show retry option

---

## Form Patterns

Forms are where users interact most. Get the patterns right for validation, layout, and multi-step flows.

### Form Layout

```typescript
// Stacked (mobile-first, default)
<form className="space-y-4">
  <FormField label="Email" name="email" />
  <FormField label="Password" name="password" />
  <Button type="submit">Sign In</Button>
</form>

// Inline (for simple, related fields)
<form className="flex gap-2">
  <Input placeholder="Search..." />
  <Button type="submit">Search</Button>
</form>

// Multi-column (desktop enhancement)
<form className="grid grid-cols-1 md:grid-cols-2 gap-4">
  <FormField label="First Name" name="firstName" />
  <FormField label="Last Name" name="lastName" />
  <FormField label="Email" name="email" className="md:col-span-2" />
</form>
```

### Validation Patterns

```typescript
// [NO] Only validate on submit (frustrating)
// [NO] Validate on every keystroke (annoying)

// [YES] Validate on blur + submit
function FormField({ name, validate }) {
  const [touched, setTouched] = useState(false);
  const [value, setValue] = useState('');
  const error = touched ? validate(value) : null;

  return (
    <div>
      <input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onBlur={() => setTouched(true)}
        aria-invalid={!!error}
        aria-describedby={error ? `${name}-error` : undefined}
      />
      {error && <span id={`${name}-error`} role="alert">{error}</span>}
    </div>
  );
}

// [YES] Real-time validation for specific fields (username availability)
function UsernameField() {
  const [username, setUsername] = useState('');
  const { data: available, isLoading } = useUsernameCheck(username);

  return (
    <div>
      <input value={username} onChange={(e) => setUsername(e.target.value)} />
      {isLoading && <span>Checking...</span>}
      {available === false && <span>Username taken</span>}
      {available === true && <span>Available!</span>}
    </div>
  );
}
```

**Validation timing:**
- **On blur:** Most fields (email, password, text)
- **On change (debounced):** Async validation (username check)
- **On submit:** Final validation, scroll to first error

### Multi-Step Forms

```typescript
function MultiStepForm() {
  const [step, setStep] = useState(1);
  const [data, setData] = useState({});

  const updateData = (stepData) => {
    setData(prev => ({ ...prev, ...stepData }));
  };

  return (
    <div>
      {/* Progress indicator */}
      <StepIndicator current={step} total={3} />

      {/* Step content */}
      {step === 1 && <PersonalInfo data={data} onNext={(d) => { updateData(d); setStep(2); }} />}
      {step === 2 && <AccountSetup data={data} onNext={(d) => { updateData(d); setStep(3); }} onBack={() => setStep(1)} />}
      {step === 3 && <Review data={data} onSubmit={handleSubmit} onBack={() => setStep(2)} />}
    </div>
  );
}
```

**Multi-step principles:**
- Show progress (step 2 of 3)
- Allow going back without losing data
- Validate each step before proceeding
- Show summary before final submit
- Save progress for long forms (localStorage or server)

### Form State Management

```typescript
// Simple forms: Local state
const [email, setEmail] = useState('');

// Complex forms: useReducer or form library
// React Hook Form example
const { register, handleSubmit, formState: { errors } } = useForm();

// Form state decision:
// - 1-3 fields → useState
// - 4-10 fields → useReducer or form library
// - 10+ fields or complex validation → Form library (React Hook Form, Formik)
```

---

## Performance Patterns

### Code Splitting

Load code when needed, not upfront:

```typescript
// [NO] Everything in main bundle
import { Dashboard } from './Dashboard';
import { Settings } from './Settings';
import { Analytics } from './Analytics';

// [YES] Route-based code splitting
const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));
const Analytics = lazy(() => import('./Analytics'));

function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/analytics" element={<Analytics />} />
      </Routes>
    </Suspense>
  );
}
```

**Split on:**
- Routes (always)
- Heavy libraries (charts, editors, maps)
- Below-the-fold content
- Conditionally rendered features

### Lazy Loading Images

```typescript
// Native lazy loading (modern browsers)
<img src={src} alt={alt} loading="lazy" />

// With responsive images
<img
  src={src}
  srcSet={`${src}?w=400 400w, ${src}?w=800 800w`}
  sizes="(max-width: 600px) 400px, 800px"
  alt={alt}
  loading="lazy"
/>
```

### Memoization (Use Sparingly)

```typescript
// [NO] Premature memoization
const MemoizedButton = memo(Button); // Button is already fast

// [YES] Memoization for expensive renders
const MemoizedChart = memo(Chart); // Chart is genuinely expensive

// [YES] Memoization to prevent unnecessary re-renders
const MemoizedListItem = memo(ListItem, (prev, next) => {
  return prev.id === next.id && prev.selected === next.selected;
});
```

**Memoize when:**
- Component is expensive to render
- Component receives same props often
- Profiler shows it's a bottleneck

**Don't memoize when:**
- "Just in case"
- Component is simple
- Props change frequently anyway

### Bundle Analysis

Regularly audit bundle size:

```bash
# webpack-bundle-analyzer
npx webpack-bundle-analyzer stats.json

# vite
npx vite-bundle-visualizer

# Next.js
ANALYZE=true npm run build
```

**Budget guidance:**
- Main bundle: < 200KB gzipped
- Initial JS: < 100KB for fast Time to Interactive
- Largest chunk: < 100KB (for good caching)

---

## Theming Patterns

### Design Tokens

Design decisions as variables:

```css
:root {
  /* Color tokens */
  --color-primary: #3b82f6;
  --color-primary-hover: #2563eb;
  --color-on-primary: #ffffff;

  /* Semantic tokens */
  --color-surface: #ffffff;
  --color-on-surface: #1f2937;
  --color-error: #ef4444;

  /* Spacing scale */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;
  --space-8: 2rem;

  /* Typography scale */
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;

  /* Motion */
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --easing-default: cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Dark Mode Implementation

```css
/* Light mode (default) */
:root {
  --color-surface: #ffffff;
  --color-on-surface: #1f2937;
  --color-primary: #3b82f6;
}

/* Dark mode */
:root[data-theme="dark"] {
  --color-surface: #1f2937;
  --color-on-surface: #f9fafb;
  --color-primary: #60a5fa;
}

/* System preference */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --color-surface: #1f2937;
    --color-on-surface: #f9fafb;
    --color-primary: #60a5fa;
  }
}
```

```typescript
// Theme toggle hook
function useTheme() {
  const [theme, setTheme] = useState(() => {
    if (typeof window === 'undefined') return 'system';
    return localStorage.getItem('theme') || 'system';
  });

  useEffect(() => {
    const root = document.documentElement;

    if (theme === 'system') {
      root.removeAttribute('data-theme');
    } else {
      root.setAttribute('data-theme', theme);
    }

    localStorage.setItem('theme', theme);
  }, [theme]);

  return [theme, setTheme];
}
```

### Skinnable Interfaces

For white-label or heavily customizable products:

```css
/* Base component - uses semantic tokens only */
.card {
  background: var(--card-background, var(--color-surface));
  border: 1px solid var(--card-border, var(--color-border));
  border-radius: var(--card-radius, var(--radius-md));
  box-shadow: var(--card-shadow, var(--shadow-sm));
}

/* Brand A overrides */
[data-brand="brand-a"] {
  --card-radius: 0;
  --card-shadow: none;
  --card-border: 2px solid var(--color-primary);
}

/* Brand B overrides */
[data-brand="brand-b"] {
  --card-radius: var(--radius-xl);
  --card-shadow: var(--shadow-lg);
  --card-border: none;
}
```

See `/pb-design-language` for creating project-specific token systems.

---

## Responsive Patterns

### Mobile-First Breakpoints

```css
/* Mobile-first breakpoint scale */
:root {
  /* Breakpoints (min-width) */
  --breakpoint-sm: 640px;   /* Large phones */
  --breakpoint-md: 768px;   /* Tablets */
  --breakpoint-lg: 1024px;  /* Small laptops */
  --breakpoint-xl: 1280px;  /* Desktops */
  --breakpoint-2xl: 1536px; /* Large screens */
}

/* Usage: Always min-width, mobile-first */
.grid {
  display: grid;
  grid-template-columns: 1fr; /* Mobile: single column */
}

@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr); /* Tablet: 2 columns */
  }
}

@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr); /* Desktop: 3 columns */
  }
}
```

### Fluid Typography

Scale typography smoothly between breakpoints:

```css
/* Fluid type scale using clamp() */
:root {
  --text-base: clamp(1rem, 0.5vw + 0.875rem, 1.125rem);
  --text-lg: clamp(1.125rem, 0.75vw + 1rem, 1.5rem);
  --text-xl: clamp(1.25rem, 1vw + 1rem, 2rem);
  --text-2xl: clamp(1.5rem, 2vw + 1rem, 3rem);
}

/* Usage */
h1 {
  font-size: var(--text-2xl);
}
```

**clamp() formula:** `clamp(min, preferred, max)`
- `min`: Smallest size (mobile floor)
- `preferred`: Fluid calculation based on viewport
- `max`: Largest size (desktop ceiling)

### Container Queries

Style based on container size, not viewport:

```css
/* Define container */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Style based on container */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: auto 1fr;
  }
}
```

**Use for:** Components that exist in different contexts (sidebar vs main content).

---

## Anti-Patterns

### Props Explosion

```typescript
// [NO] Too many props
<Button
  size="lg"
  variant="primary"
  isLoading={false}
  isDisabled={false}
  leftIcon={<Icon />}
  rightIcon={null}
  onClick={handleClick}
  onHover={handleHover}
  tooltip="Click me"
  ariaLabel="Submit form"
  className="custom-button"
  style={{ marginTop: 10 }}
/>

// [YES] Composition over configuration
<Button size="lg" variant="primary" onClick={handleClick}>
  <Icon /> Submit
</Button>
```

### Premature Abstraction

```typescript
// [NO] Abstracting after one use
// utils/formatUserName.ts
export function formatUserName(first, last) {
  return `${first} ${last}`;
}

// [YES] Inline until pattern emerges
const fullName = `${user.first} ${user.last}`;

// Abstract when you see the SAME pattern THREE times
```

### God Components

```typescript
// [NO] Component does everything
function UserDashboard() {
  // 500 lines of data fetching, state, rendering, effects
}

// [YES] Composition of focused components
function UserDashboard() {
  return (
    <DashboardLayout>
      <UserHeader />
      <UserStats />
      <RecentActivity />
      <QuickActions />
    </DashboardLayout>
  );
}
```

### Over-Engineering State

```typescript
// [NO] Redux for a todo list
const todoSlice = createSlice({
  name: 'todos',
  initialState: { items: [], filter: 'all' },
  reducers: {
    addTodo: (state, action) => { /* ... */ },
    toggleTodo: (state, action) => { /* ... */ },
    setFilter: (state, action) => { /* ... */ },
  },
});

// [YES] Local state for simple features
function TodoList() {
  const [todos, setTodos] = useState([]);
  const [filter, setFilter] = useState('all');
  // Simple, testable, deletable
}
```

---

## Accessibility Integration

Frontend patterns MUST be accessible by default. See `/pb-a11y` for comprehensive guidance.

**Quick checklist for components:**

- [ ] Semantic HTML used (button not div, etc.)
- [ ] Keyboard navigable (Tab, Enter, Escape)
- [ ] Focus visible and logical
- [ ] ARIA only when semantic HTML insufficient
- [ ] Color not sole indicator
- [ ] Touch targets 44x44px minimum

---

## Related Commands

- `/pb-design-language` — Project-specific design token systems
- `/pb-a11y` — Accessibility deep-dive
- `/pb-patterns-async` — Data fetching patterns
- `/pb-patterns-api` — API design patterns
- `/pb-testing` — Component testing patterns

---

## Design Rules Applied

| Rule | Application |
|------|-------------|
| **Clarity** | Component boundaries are explicit; no hidden state |
| **Simplicity** | Mobile-first forces prioritization; no premature abstraction |
| **Composition** | Compound components, composition over props explosion |
| **Resilience** | Error boundaries, graceful degradation, loading states |
| **Extensibility** | Design tokens enable theming without code changes |

---

**Last Updated:** 2026-01-19
**Version:** 1.0
