---
name: ui-ux-grandmaster
description: >
  Unified UI/UX design intelligence for web, mobile, and desktop. Combines rigorous UX/accessibility
  and stack-aware implementation guidance, Apple-inspired fluid interaction physics, premium
  anti-generic visual taste, and project-specific DESIGN.md governance. Use when designing, building,
  reviewing, refactoring, or polishing interfaces, design systems, responsive layouts, typography,
  color, components, navigation, forms, charts, animation, gesture-driven interactions, or
  implementation details. Treat accessibility, user agency, platform behavior, and performance as
  hard constraints; treat visual taste and decorative motion as contextual layers.
---

# UI/UX Grandmaster

A unified design-director skill for producing interfaces that are usable, accessible, technically
credible, visually intentional, responsive, and physically coherent in motion.

This skill merges four concerns that must not be treated as equal-weight prompt fragments:

1. **UX intelligence** — accessibility, usability, information architecture, responsive behavior,
   components, forms, charts, performance, and stack-specific implementation.
2. **Interaction physics** — direct manipulation, interruptibility, springs, velocity, momentum,
   spatial continuity, translucent materials, and reduced-motion behavior.
3. **Visual taste** — anti-generic composition, typography character, calibrated color, hierarchy,
   asymmetry, restrained accents, and explicit anti-patterns.
4. **Project design governance** — existing `DESIGN.md`, persisted design-system documents, brand
   rules, and page-level overrides.

The goal is not to average these concerns. The goal is to **route each decision to the right layer,
resolve conflicts deliberately, and preserve one coherent source of truth.**

---

## 0. The Operating Law

When rules conflict, apply this precedence order:

1. **User safety, accessibility, and legal/product constraints**
2. **Explicit user requirements and repository/project constraints**
3. **Platform conventions and input modality**
4. **Existing project design source of truth (`DESIGN.md`, MASTER.md, brand tokens)**
5. **Usability, information architecture, and user agency**
6. **Performance and technical feasibility**
7. **Interaction physics and spatial continuity**
8. **Visual system consistency**
9. **Premium taste / anti-generic preferences**
10. **Decorative delight**

Never let a lower layer break a higher one.

Examples:

- A decorative hover effect never overrides keyboard focus visibility.
- A high-motion visual direction never overrides `prefers-reduced-motion`.
- A distinctive premium font preference does not override a native-platform requirement where the
  system font is the more coherent choice.
- A project `DESIGN.md` may override the default accent color, card radius, or hero composition, but
  it may not override minimum touch targets or readable contrast.
- A "perpetual micro-interaction" is allowed only when it communicates a live/active state and passes
  accessibility/performance constraints. Do not animate every object merely because animation exists.

**Do not resolve conflicts by averaging values. Resolve them by scope and precedence.**

---

## 1. When to Apply

Use this skill when a task changes how an interface:

- looks,
- reads,
- responds,
- moves,
- adapts,
- communicates status,
- supports input,
- or is implemented visually.

Typical tasks:

- New page, app, dashboard, portfolio, landing page, or component design
- UI review / UX audit / accessibility review
- Design-system generation or refinement
- Responsive layout fixes
- Typography, palette, spacing, hierarchy, iconography
- Forms, feedback, navigation, empty/error/loading states
- Charts and data visualization
- Gesture-driven UI, sheets, drawers, carousels, drag/drop, swipe, momentum
- Animation and motion polish
- React / Next.js / Vue / Svelte / Flutter / SwiftUI / React Native / other UI stack guidance
- Google Stitch screen-generation briefs and `DESIGN.md` generation

Skip for pure backend/API/database/DevOps work unless it directly changes user-visible behavior.

---

## 2. Never Start by Styling

Before proposing visuals, infer or inspect:

- **Product type:** SaaS, commerce, portfolio, dashboard, entertainment, tool, productivity, editorial,
  social, mobile app, desktop app, hybrid.
- **Primary user:** expertise, age/context when known, frequency of use, environment.
- **Core job:** what the user is trying to complete.
- **Primary surface:** marketing page, workflow, data-dense dashboard, content browser, form,
  editor, modal flow, native-like app.
- **Platform:** web, iOS-like web, native iOS, Android, desktop, TV, wearable, etc.
- **Input:** touch, pointer, keyboard, remote, mixed.
- **Stack:** detect from repository files; never silently assume.
- **Existing design authority:** `DESIGN.md`, design tokens, brand guide, persisted MASTER, page override.
- **Requested style:** minimal, expressive, editorial, dark, playful, clinical, cinematic, etc.
- **Risk:** destructive actions, privacy, financial/health/safety consequences, irreversible state.
- **Constraints:** deadline, library restrictions, performance budget, browser/device support.

If files are available, inspect them before generating a replacement system.

---

## 3. Source-of-Truth Resolution

Before creating or changing a design system, check in this order:

1. Project-level `DESIGN.md`
2. Persisted design system:
   - `design-system/<project-slug>/MASTER.md`
   - `design-system/<project-slug>/pages/<page-name>.md`
3. Brand tokens / theme files / component library
4. Existing implementation patterns
5. This skill's defaults

If a page override exists, it overrides the master **for that page only**.

Never overwrite an existing design source of truth merely because a newly generated recommendation is
different. Surface the conflict and preserve the existing decision unless the user explicitly asks to
replace it.

---

## 4. Design Dials

Use four 1–10 dials to make visual intent explicit:

| Dial | 1–3 | 4–7 | 8–10 |
|---|---|---|---|
| **Creativity** | quiet, Swiss, conventional | balanced personality | expressive, editorial, experimental |
| **Density** | gallery-airy | daily-app balanced | cockpit/data-dense |
| **Variance** | symmetric/predictable | controlled offsets | strongly asymmetric / varied |
| **Motion Intent** | nearly static | purposeful micro-motion | choreographed / cinematic |

### Taste Standard preset

When the user explicitly wants the premium anti-generic taste profile and gives no values:

- Creativity: `8`
- Density: `4`
- Variance: `8`
- Motion Intent: `6`

Do **not** apply this preset automatically to every product. A dense enterprise dashboard, native
settings screen, accessibility-first workflow, or highly regulated product may need substantially lower
variance or motion.

---

# PART I — UX FOUNDATION

## 5. Priority Categories

Evaluate in this order:

| Priority | Category | Impact | Minimum checks |
|---|---|---|---|
| 1 | Accessibility | Critical | contrast, semantics, keyboard, labels, focus |
| 2 | Touch & Interaction | Critical | ≥44×44px targets, spacing, feedback, non-hover path |
| 3 | Performance | High | stable layout, responsive input, efficient media |
| 4 | Style Selection | High | product fit, consistency, intentional iconography |
| 5 | Layout & Responsive | High | mobile-first, no accidental overflow, scalable containment |
| 6 | Typography & Color | Medium | readable base size, hierarchy, semantic tokens |
| 7 | Animation | Medium | meaning, continuity, reduced-motion path |
| 8 | Forms & Feedback | Medium | visible labels, inline errors, recovery |
| 9 | Navigation | High | predictable back/exit, hierarchy, deep-link awareness |
| 10 | Charts & Data | Contextual | labels, legends/tooltips, non-color encoding |

### Hard failures

Treat these as failures unless the user explicitly provides a justified exception:

- Removing visible focus indicators
- Icon-only controls with no accessible name
- Interaction available only on hover
- Body text so small that normal reading becomes difficult
- Horizontal overflow on ordinary mobile content
- Disabled pinch zoom
- Destructive action with no reasonable recovery/confirmation strategy
- Layout shift caused by unreserved media or late-loading structure
- Errors shown only at the top while the failing field is elsewhere
- Motion with no reduced-motion alternative
- Color as the only signal for important state

---

## 6. Accessibility First

Accessibility is not a polish pass.

Check:

- Semantic elements before ARIA.
- Keyboard order follows visual/logical order.
- Focus is visible and not obscured.
- Interactive elements have accessible names.
- Decorative icons are hidden from assistive tech.
- Validation is announced and associated with the field.
- Drag-only actions have an alternative when the task matters.
- Status changes that matter are communicated without relying only on color.
- Touch targets are normally at least `44×44px`.
- Contrast is sufficient for the text size and context.
- Text can scale without clipping or losing functionality.
- Motion/transparency/contrast user preferences have a meaningful fallback.

For accessibility debugging, search one observable outcome at a time rather than asking for "all
accessibility best practices."

---

## 7. User Agency & Wayfinding

Every screen should make these answers obvious:

- Where am I?
- What can I do here?
- What happens if I do it?
- What changed?
- How do I undo, cancel, go back, or leave?

Prefer:

- Specific labels over vague labels.
- Inline feedback over surprise after submission.
- Undo for reversible mistakes.
- Confirmation only for genuinely destructive or hard-to-reverse actions.
- Progressive disclosure for advanced options.
- Familiar patterns unless a tested alternative is materially better.

Simplicity is not "show fewer pixels." Simplicity is reducing uncertainty and unnecessary work.

---

## 8. Responsive Architecture

Responsive behavior is a structural requirement.

### Baseline

- Use fluid containment and sensible max-widths.
- Avoid fixed desktop widths that force mobile overflow.
- Use `clamp()` for fluid type/space when appropriate.
- Prefer CSS Grid for structural layouts.
- Avoid percentage-math hacks where Grid/Flex already model the layout.
- Use `min-height: 100dvh` for true viewport-height sections on modern mobile web.
- Keep body copy readable; do not shrink it merely to preserve desktop composition.
- Test important states, not just happy-path static screens.

### Reference viewports

When practical, verify at:

- `375px`
- `390px`
- `768px`
- `1024px`
- `1440px`

For high-variance editorial layouts, collapse deliberately rather than squeezing the desktop
composition.

---

# PART II — VISUAL INTELLIGENCE

## 9. Visual Direction Before Tokens

Define the atmosphere in plain language before picking exact values.

Describe:

- emotional tone,
- density,
- contrast,
- variance,
- material quality,
- image treatment,
- motion intensity,
- hierarchy strategy.

A good atmosphere description constrains later choices.

Bad:
> modern clean premium

Better:
> A restrained editorial interface with warm-neutral surfaces, strong typographic hierarchy,
> asymmetric whitespace, one muted accent, minimal chrome, and motion that behaves physically
> rather than theatrically.

---

## 10. Color System

For every important color specify:

**Semantic name + exact value + functional role**

Example:

- `Canvas` `#F9FAFB` — base page surface
- `Surface` `#FFFFFF` — elevated container
- `Ink` `#18181B` — primary text
- `Steel` `#71717A` — secondary text
- `Border` `rgba(226,232,240,0.5)` — low-emphasis separation

### Taste-layer defaults

When premium anti-generic mode is active:

- Prefer one dominant accent.
- Avoid accidental warm/cool neutral mixing.
- Avoid pure `#000000` when a near-black gives better material depth.
- Avoid neon outer glows and stereotypical "AI purple" gradients unless they are actually part of the
  brand or explicitly requested.
- Keep saturation controlled.
- Use semantic tokens in components instead of scattering raw hex values.

These are **taste defaults**, not universal laws. Brand identity may override them.

---

## 11. Typography Architecture

Typography must be reasoned as a system:

- family,
- weight,
- size,
- line-height,
- tracking,
- width,
- optical sizing,
- content measure.

### Physical typography rules

- Large display type usually needs tighter tracking.
- Body text usually needs more relaxed leading.
- Tracking must not be one fixed value for every size.
- Hierarchy should use weight, size, spacing, and color together.
- Respect user text scaling.
- Prefer `rem`/`em` for type-coupled spacing.
- Use `font-optical-sizing: auto` when the typeface supports it.

### Font routing

Resolve the "system font vs distinctive font" question by context:

**Prefer system/platform fonts when:**
- native familiarity matters,
- platform coherence matters,
- dense utility UI dominates,
- performance is constrained,
- the product is imitating native behavior.

**Prefer a distinctive family when:**
- brand/editorial personality is part of the product value,
- the user asks for premium/creative visual identity,
- marketing or portfolio expression matters.

In premium/creative mode, avoid defaulting automatically to `Inter`. Consider families with stronger
character such as `Geist`, `Satoshi`, `Cabinet Grotesk`, `Outfit`, or an appropriate brand typeface.

For editorial serif use, prefer a deliberate modern serif over an unconsidered browser-default serif.
Dashboards generally benefit from sans-serif UI families, with monospace reserved for code,
timestamps, IDs, tabular numbers, or deliberately technical data.

---

## 12. Layout Taste

When high-variance premium taste is active:

- Prefer intentional asymmetry over automatic centering.
- Do not default to three identical feature cards in a row.
- Use negative space, split layouts, zig-zag structures, asymmetric grids, or varied rhythm when
  content supports them.
- Do not overlap text/images merely to look "designed." Overlap must have a clear compositional reason
  and remain responsive/readable.
- Keep structural content in normal flow whenever possible.
- Use cards only when elevation/grouping communicates something. In dense interfaces, dividers,
  spacing, and typographic grouping may be better.
- Avoid generic filler chrome such as "Scroll to explore" when content itself can establish direction.

At low variance, symmetry and conventional grids are not failures. They may be exactly right.

---

## 13. Hero Logic

For marketing/editorial surfaces:

- Hero should communicate product identity and job quickly.
- One strong primary CTA is often enough.
- Avoid redundant "Learn more" secondary actions if they add no decision value.
- At high variance, consider split or asymmetric composition.
- Inline imagery inside display typography can be used as punctuation when it genuinely supports the
  content and still collapses cleanly on mobile.
- Never let visual novelty obscure the product's purpose.

For application/dashboard screens, do not force a marketing-style hero at all.

---

## 14. Components

### Buttons
- Immediate pressed feedback.
- Primary action visually clear.
- No glow merely for decoration.
- Keyboard focus distinct from hover.
- Disabled state still legible.

### Cards
- Use elevation only when hierarchy benefits.
- Avoid card-on-card-on-card nesting.
- Dense products may use borders/spacing instead.

### Inputs
- Visible label above or otherwise persistently associated.
- Helper text optional.
- Error near the field.
- Clear focus state.
- No placeholder-only labeling.

### Loading
- Prefer a loader matching the structure being loaded when practical.
- Skeletons should reflect actual layout geometry.
- Do not use a generic spinner for every loading state by reflex.

### Empty states
- Explain what is empty, why it matters, and the next useful action.
- Do not stop at "No data found."

### Error states
- State what failed.
- Preserve user input when possible.
- Give a realistic recovery action.

---

# PART III — FLUID INTERACTION PHYSICS

## 15. Core Principle

A fluid interface behaves less like a sequence of canned animations and more like a manipulable
physical system.

For touchable/gesture-driven objects:

- respond immediately,
- track input continuously,
- preserve momentum,
- remain interruptible,
- preserve spatial origin,
- soften boundaries,
- and allow reversal without visible discontinuity.

---

## 16. Kill Input Latency

- Show pressed feedback on pointer/touch down, not only after click release.
- Audit artificial delays and avoid unnecessary debounce on direct-manipulation paths.
- During drag/slide/scrub interactions, update continuously instead of waiting for completion.

Example:

```css
.button:active {
  transform: scale(0.97);
  transition: transform 100ms ease-out;
}
```

Use this only for simple press feedback. Gesture-driven motion needs a more interruptible mechanism.

---

## 17. Direct Manipulation

For drag/swipe:

- Keep the object 1:1 with the pointer after the gesture commits.
- Preserve the grab offset.
- Use Pointer Events on web.
- Use `setPointerCapture` so tracking survives pointer movement outside the element.
- Track recent position/time samples so release velocity can be estimated.
- Use a small intent threshold before committing a drag direction.

Do not snap the dragged object to its center under the pointer.

---

## 18. Interruptibility

This is a hard requirement for gesture-driven animation.

- Never lock input merely because an animation is running.
- Start a retargeted animation from the **current on-screen/presentation value**, not the stale logical
  target.
- Preserve velocity across retargeting when the animation engine supports it.
- For 2D physical motion, treat X and Y independently when their velocities differ.
- Avoid fixed keyframe choreography for objects the user must be able to grab mid-flight.

---

## 19. Spring Defaults

Think in terms of:

- **Damping ratio** — overshoot/oscillation behavior
- **Response** — perceived speed of convergence, not a fixed animation duration

Safe starting points for physical UI:

| Interaction | Damping | Response |
|---|---:|---:|
| move/reposition | `1.0` | `0.4` |
| rotation with momentum | `0.8` | `0.4` |
| drawer/sheet release | `0.8` | `0.3` |

Default most non-momentum UI toward critically damped behavior (`~1.0`, no overshoot).

Use bounce/overshoot when the preceding gesture carries momentum. Do not make ordinary menu opens
bounce just because springs exist.

### Taste preset mapping

A generic "premium spring" such as `stiffness: 100, damping: 20` may be used as an implementation
starting point where the library exposes stiffness/damping, but tune it by context. It does not
override the behavioral rules above.

---

## 20. Velocity Handoff

When a drag ends, animation should continue from the gesture's release velocity.

Some systems use absolute velocity. Systems requiring relative velocity may normalize:

```text
relativeVelocity = gestureVelocity / (targetValue - currentValue)
```

Avoid hard-cutting velocity at the drag/animation seam.

---

## 21. Momentum Projection

For flickable/snap interactions, choose the destination from the **projected endpoint**, not merely the
release coordinate.

Reference model:

```js
function project(initialVelocity, decelerationRate = 0.998) {
  return (initialVelocity / 1000) * decelerationRate / (1 - decelerationRate);
}

const projectedEndpoint = currentPosition + project(releaseVelocity);
const target = nearestSnapPoint(projectedEndpoint);
animateSpringTo(target, { velocity: releaseVelocity });
```

Use a snappier decay when the product calls for it; preserve the conceptual rule: velocity affects
where the object lands.

---

## 22. Spatial Consistency

- Enter and exit along coherent paths.
- A reversible object should return toward its origin.
- Popovers/menus should feel anchored to their trigger.
- Use a meaningful transform origin.
- Avoid transitions that imply teleportation between unrelated directions.

Motion is wayfinding.

---

## 23. Rubber-Banding

At boundaries, progressive resistance often feels better than an immediate hard stop.

Reference:

```js
function rubberband(overshoot, dimension, constant = 0.55) {
  return (overshoot * dimension * constant) /
         (dimension + constant * Math.abs(overshoot));
}
```

Use only for interactions where soft overdrag is semantically appropriate.

---

## 24. Frame-Level Performance

Prefer compositor-friendly animation:

- `transform`
- `opacity`

Be cautious animating:

- `top`
- `left`
- `width`
- `height`

Use `requestAnimationFrame` for manual per-frame work.

Do not equate 60fps with good motion. A smooth frame rate can still contain visually incoherent
position jumps, bad easing, or excessive motion.

---

## 25. Material & Depth

Translucency can communicate layered hierarchy when used with restraint.

For floating navigation, toolbars, sheets, or overlays:

- use translucent material only when the background relationship matters,
- maintain readable contrast,
- do not stack weak translucent surfaces until text becomes muddy,
- scale blur/shadow weight with surface size,
- use scrims for modal separation,
- avoid a scrim for parallel/non-blocking surfaces when it would falsely imply modality,
- provide a solid/reduced-transparency alternative.

Material should explain hierarchy, not advertise a blur filter.

---

## 26. Multimodal Feedback

When combining visual, audio, and haptic feedback:

1. **Causality:** feedback corresponds to a clear event.
2. **Harmony:** channels fire together closely enough to feel like one event.
3. **Utility:** feedback earns its place.

Reserve stronger feedback for meaningful commit, success, warning, error, snap, or state transitions.
Do not create sensory noise.

---

## 27. Reduced Motion / Transparency / Contrast

Respect independent preferences.

### Reduced motion
Replace large slides, parallax, elastic movement, and overshoot with short fades or static state
changes while preserving comprehension.

```css
@media (prefers-reduced-motion: reduce) {
  .sheet {
    transform: none !important;
    transition: opacity 200ms ease;
  }
}
```

### Reduced transparency
Use more opaque/solid surfaces and remove blur when supported.

### Increased contrast
Strengthen surface separation and text/border contrast.

Never make "reduced motion" mean "remove all feedback."

---

# PART IV — MOTION TASTE WITHOUT MOTION SLOP

## 28. Motion Routing

Use motion according to meaning:

### Always useful
- press feedback,
- state transitions,
- spatial continuity,
- loading progress,
- reordering,
- success/error confirmation,
- gesture handoff.

### Sometimes useful
- staggered reveal,
- decorative float,
- shimmer,
- subtle ambient motion.

### Usually harmful
- motion on every idle component,
- infinite movement in dense work surfaces,
- animation that delays input,
- animation that competes with reading,
- bounce with no physical cause,
- parallax that ignores reduced-motion,
- animation solely to prove animation exists.

### Perpetual micro-interactions

Interpret the premium-taste "perpetual motion" idea narrowly:

Use loops only for components that are **semantically active/live**, such as:

- status pulse,
- streaming indicator,
- loading shimmer,
- recording state,
- genuinely live visualization.

Do not put infinite motion on ordinary cards, labels, icons, and buttons by default.

---

# PART V — DATA-DRIVEN UI/UX PRO MAX ENGINE

## 29. Optional Search Engine

If the UI/UX Pro Max search assets are installed, use them rather than relying only on memory.

Search for `scripts/search.py` in this order:

1. This skill's own directory:
   `scripts/search.py`
2. Original Pro Max installation:
   `${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py`

If no script exists, continue using the embedded rules in this file and **do not claim a database
match occurred**.

### Python fallback order

1. `python`
2. `python3`
3. `py -3`

---

## 30. Query Contract

Choose the smallest mode that fits:

1. **New project/page or product-wide direction** → `--design-system`
2. **Targeted design concern** → explicit `--domain`
3. **Implementation-specific concern** → `--stack`

Use one dominant intent and roughly 2–5 meaningful query terms.

Good:
```text
keyboard focus modal
```

Bad:
```text
give me every accessibility typography color responsive animation rule for this whole application
```

If results are empty/off-topic:

1. retry once with narrower wording or explicit domain/stack;
2. if still empty, fall back to the embedded rules;
3. explicitly distinguish fallback guidance from verified search output.

Never fabricate a search result.

---

## 31. Design-System Search

When the script is available:

```bash
python "<skill-path>/scripts/search.py" \
  "<product_type> <industry> <keywords>" \
  --design-system \
  -p "Project Name"
```

Optional dials:

```bash
python "<skill-path>/scripts/search.py" \
  "<query>" \
  --design-system \
  --variance <1-10> \
  --motion <1-10> \
  --density <1-10> \
  -p "Project Name"
```

Use the generated system as evidence/recommendation, then reconcile it with existing project rules and
this skill's precedence hierarchy.

---

## 32. Domain Search

When installed, useful domains include:

| Need | Domain |
|---|---|
| Product patterns | `product` |
| Styles | `style` |
| Color | `color` |
| Typography | `typography` |
| Google Fonts | `google-fonts` |
| Charts | `chart` |
| UX | `ux` |
| Landing structure | `landing` |
| Icons | `icons` |
| GSAP | `gsap` |
| React performance | `react` |
| App/native guidance | `web` |

Example:

```bash
python "<skill-path>/scripts/search.py" "error summary validation" --domain ux
```

---

## 33. Stack Routing

Detect stack from the repository before using stack-specific guidance.

Signals include:

- `package.json`
- `pubspec.yaml`
- `Package.swift`
- `*.xcodeproj`
- `composer.json`
- React Native app markers

Supported Pro Max stacks may include:

`react`, `nextjs`, `vue`, `svelte`, `astro`, `nuxtjs`, `nuxt-ui`, `angular`, `laravel`, `swiftui`,
`react-native`, `flutter`, `jetpack-compose`, `html-tailwind`, `shadcn`, `threejs`, `javafx`, `wpf`,
`winui`, `avalonia`, `uno`, `uwp`.

Do not silently hardcode a stack.

---

# PART VI — PROJECT DESIGN GOVERNANCE

## 34. Existing `DESIGN.md`

If the project already has `DESIGN.md`:

1. Read it first.
2. Extract:
   - atmosphere,
   - dials,
   - palette,
   - typography,
   - components,
   - layout rules,
   - motion rules,
   - banned patterns.
3. Treat it as the project visual source of truth unless a higher-priority constraint conflicts.
4. Preserve terminology so implementation stays consistent.
5. Do not regenerate or rewrite it unless asked.

---

## 35. Generating a New `DESIGN.md`

When asked to create one, produce:

```markdown
# Design System: [Project]

## Configuration
- Creativity:
- Density:
- Variance:
- Motion Intent:

## 1. Product Intent & Experience Goal
## 2. Visual Theme & Atmosphere
## 3. Color Palette & Semantic Roles
## 4. Typography Architecture
## 5. Spacing, Grid & Responsive Rules
## 6. Component Styling
## 7. Navigation & Wayfinding
## 8. Forms, Feedback & States
## 9. Motion & Interaction Physics
## 10. Accessibility Requirements
## 11. Performance Constraints
## 12. Platform / Stack Notes
## 13. Anti-Patterns / Banned Patterns
## 14. Page-Specific Exceptions
```

Every important visual rule should be:

- descriptive enough for a design agent,
- concrete enough for a coding agent,
- scoped enough to avoid becoming dogma.

---

## 36. Taste Standard Reference Preset

Use only when explicitly selected or clearly appropriate.

### Dials
- Creativity `8`
- Density `4`
- Variance `8`
- Motion Intent `6`

### Light neutral palette
- Canvas White `#F9FAFB`
- Pure Surface `#FFFFFF`
- Charcoal Ink `#18181B`
- Steel Secondary `#71717A`
- Muted Slate `#94A3B8`
- Whisper Border `rgba(226,232,240,0.5)`
- Diffused Shadow `rgba(0,0,0,0.05)`

### Candidate accents — choose one
- Emerald Signal `#10B981`
- Electric Blue `#3B82F6`
- Deep Rose `#E11D48`
- Amber Warmth `#F59E0B`

### Type direction
Potential display/UI families:

- Geist
- Satoshi
- Cabinet Grotesk
- Outfit

Potential mono:

- Geist Mono
- JetBrains Mono

Do not use these merely because they appear in the preset. Product/brand context still wins.

### Reference component values
- Display tracking around `-0.025em` as a starting point
- Display leading around `1.1`
- Body leading around `1.65` for editorial/airy layouts
- Body measure around `65ch`
- Large soft card radius can reach `2.5rem` in this specific taste mode
- Strong component padding around `2rem–2.5rem` for airy premium cards

These are **preset values**, not universal defaults.

---

# PART VII — ANTI-SLOP RULES

## 37. Generic AI Tells to Challenge

Unless the project explicitly calls for them, challenge:

- neon purple/blue glow as automatic "AI" styling,
- huge gradient headline with no hierarchy,
- three identical feature cards because a template did it,
- every section centered,
- gratuitous glassmorphism,
- decorative emojis used as product icons,
- generic placeholder names such as "John Doe" / "Acme",
- suspiciously round fake metrics,
- filler marketing clichés,
- scroll instructions for users who already know how to scroll,
- custom cursors that reduce predictability,
- z-index escalation instead of proper layout/layer design,
- loading spinner used for every latency,
- stock component-library defaults left visually untouched while claiming a custom design system.

The goal is not novelty for its own sake. The goal is intentionality.

---

## 38. Copy and Data Integrity

Do not invent fake product evidence just to fill the screen.

When realistic data is needed:

- use clearly labeled sample/demo data,
- avoid fake precision that implies measurement,
- preserve the domain's plausible formats,
- do not fabricate testimonials or business claims as if real.

---

# PART VIII — WORKFLOW

## 39. New Product / Page Workflow

### Step 1 — Understand
Identify product, user, task, platform, stack, constraints, existing design authority, and dials.

### Step 2 — Protect
Lock accessibility, user agency, responsive requirements, and performance constraints.

### Step 3 — Research
If Pro Max search exists, query the smallest relevant design-system/domain/stack slice.

### Step 4 — Define direction
Write atmosphere and hierarchy before exact tokens.

### Step 5 — Establish system
Define semantic color, typography, spacing, radii, elevation, icon rules, and layout behavior.

### Step 6 — Define interactions
Specify press, hover/focus, loading, error, empty, modal, navigation, and gesture behavior.

### Step 7 — Define motion
Use spatially coherent, interruptible behavior. Add decorative motion only after functional motion works.

### Step 8 — Implement
Follow the detected stack's conventions. Keep dependencies minimal unless a library solves a real
interaction problem better than bespoke code.

### Step 9 — Test
Test keyboard, touch/pointer, small/large viewport, text scaling, reduced motion, loading, empty,
error, long content, and interruption during animation.

### Step 10 — Polish
Only after the above, tune optical details, micro-motion, visual rhythm, and delight.

---

## 40. Targeted Bug / Audit Workflow

For a focused issue:

1. State the observed problem.
2. Identify its user impact.
3. Identify the governing layer: accessibility, UX, layout, typography, motion, performance, stack.
4. Search that domain if tooling is available.
5. Fix the smallest causal issue first.
6. Re-test adjacent states.
7. Avoid unrelated aesthetic rewrites.

Do not redesign an entire product when the user asked to fix one input, modal, or breakpoint.

---

# PART IX — IMPLEMENTATION PRINCIPLES

## 41. Web Interaction

Prefer:

- semantic HTML,
- CSS layout primitives,
- Pointer Events for cross-input gesture work,
- compositor-friendly motion,
- progressive enhancement.

Use animation libraries when they provide actual value:

- interruptible springs,
- velocity handoff,
- layout/shared-element transitions,
- complex timeline choreography.

Do not add a motion dependency to animate a simple opacity change.

---

## 42. Component State Model

For interactive components, consider:

- default,
- hover when applicable,
- focus-visible,
- pressed/active,
- loading,
- selected,
- disabled,
- success,
- warning,
- error.

Visual states must not create contradictory semantics.

---

## 43. Performance Discipline

Before shipping:

- avoid unnecessary parent re-renders from decorative animation,
- isolate continuous animation work,
- reserve media dimensions,
- lazy-load non-critical media,
- keep interaction response fast,
- avoid layout thrash,
- prefer transform/opacity for motion,
- test on realistic hardware when possible.

"Premium" that drops frames on an ordinary device is not premium.

---

# PART X — OUTPUT MODES

## 44. Choose the Output That Matches the Task

### Design direction
Return:
- experience goal,
- atmosphere,
- dials,
- palette,
- typography,
- layout,
- component language,
- motion,
- anti-patterns.

### UX audit
Return:
- issue,
- evidence,
- severity,
- user impact,
- recommended change,
- validation method.

### Component spec
Return:
- anatomy,
- states,
- dimensions,
- semantics,
- keyboard/touch behavior,
- motion,
- responsive behavior.

### Motion spec
Return:
- trigger,
- start state,
- target state,
- interruption behavior,
- velocity/momentum behavior,
- reduced-motion equivalent.

### Stitch brief / `DESIGN.md`
Use semantic natural language plus exact values where useful.

### Code implementation
Respect the detected stack and existing project conventions before introducing new dependencies.

---

# PART XI — CONFLICT RESOLUTION TABLE

## 45. Common Conflicts

| Conflict | Resolution |
|---|---|
| System font vs distinctive premium font | Platform coherence wins for native/utility UI; brand expression may justify distinctive type |
| Restrained Apple motion vs perpetual micro-loops | Functional/physical motion wins; loops only for semantically live states |
| Project `DESIGN.md` vs generated Pro Max design system | Existing project source of truth wins unless user authorizes change |
| High variance vs usability | Preserve hierarchy and task clarity; reduce variance in workflow-dense surfaces |
| One accent vs brand palette | Brand may use more colors; still assign semantic roles and prevent visual noise |
| No overlap vs editorial composition | Default to clean separation; permit intentional overlap only when user/brand asks and responsiveness/readability survive |
| Skeleton vs spinner | Match loader to latency/context; skeleton for structural content, progress/spinner only when more appropriate |
| Glass material vs contrast | Legibility wins; use solid fallback or stronger material |
| Decorative motion vs performance | Performance wins |
| Visual novelty vs familiarity | Familiarity wins for critical controls and navigation |

---

# PART XII — PRE-DELIVERY GATE

## 46. Before Delivering Any UI

Do not call the interface finished until the relevant checks pass.

### Accessibility
- [ ] Keyboard path works
- [ ] Focus visible
- [ ] Accessible names present
- [ ] Contrast acceptable
- [ ] Important state not encoded only by color
- [ ] Text can scale
- [ ] Motion preference honored

### Interaction
- [ ] Press feedback is immediate
- [ ] Loading/error/success states exist where needed
- [ ] Destructive actions have recovery/confirmation strategy
- [ ] Gesture interactions remain interruptible
- [ ] Back/close behavior is predictable

### Responsive
- [ ] No accidental horizontal overflow
- [ ] Mobile structure is deliberate
- [ ] Touch targets are adequate
- [ ] Long text does not break controls
- [ ] Safe areas considered for app-like mobile UI

### Visual system
- [ ] Tokens are semantically consistent
- [ ] Hierarchy is obvious
- [ ] Typography scale/leading/tracking are coherent
- [ ] Icons are consistent
- [ ] Cards/elevation are used intentionally
- [ ] Accent usage is controlled

### Motion
- [ ] Motion communicates meaning
- [ ] Enter/exit paths are spatially coherent
- [ ] No gratuitous bounce
- [ ] Continuous motion is justified
- [ ] Reduced-motion equivalent exists

### Performance
- [ ] Layout shift controlled
- [ ] Images/media sized appropriately
- [ ] Continuous animations isolated
- [ ] No obvious layout-thrashing animation
- [ ] Perceived input response remains fast

### Integrity
- [ ] No fabricated search/database result
- [ ] No accidental overwrite of existing design authority
- [ ] No generic AI clichés added by habit
- [ ] Final implementation matches the stated design rationale

---

# Final Principle

A strong interface is not the one with the most rules, motion, asymmetry, glass, or novelty.

It is the one where:

- users understand what is happening,
- actions feel immediate and reversible,
- hierarchy survives every viewport,
- motion preserves physical and spatial logic,
- accessibility is built in,
- performance stays credible,
- visual decisions have a reason,
- and the product still has a recognizable point of view.

**Utility is the floor. Coherence is the structure. Craft is the multiplier. Delight is earned.**
