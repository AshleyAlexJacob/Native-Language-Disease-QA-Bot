---
name: Clinical Precision
colors:
  surface: '#f8f9fa'
  surface-dim: '#d9dadb'
  surface-bright: '#f8f9fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f5'
  surface-container: '#edeeef'
  surface-container-high: '#e7e8e9'
  surface-container-highest: '#e1e3e4'
  on-surface: '#191c1d'
  on-surface-variant: '#3e4949'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f2'
  outline: '#6e7979'
  outline-variant: '#bdc9c8'
  surface-tint: '#006a6a'
  primary: '#006565'
  on-primary: '#ffffff'
  primary-container: '#008080'
  on-primary-container: '#e3fffe'
  inverse-primary: '#76d6d5'
  secondary: '#5c5f60'
  on-secondary: '#ffffff'
  secondary-container: '#e1e3e4'
  on-secondary-container: '#626566'
  tertiary: '#8b4823'
  on-tertiary: '#ffffff'
  tertiary-container: '#a96039'
  on-tertiary-container: '#fff9f7'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#93f2f2'
  primary-fixed-dim: '#76d6d5'
  on-primary-fixed: '#002020'
  on-primary-fixed-variant: '#004f4f'
  secondary-fixed: '#e1e3e4'
  secondary-fixed-dim: '#c5c7c8'
  on-secondary-fixed: '#191c1d'
  on-secondary-fixed-variant: '#444748'
  tertiary-fixed: '#ffdbcb'
  tertiary-fixed-dim: '#ffb692'
  on-tertiary-fixed: '#341100'
  on-tertiary-fixed-variant: '#733512'
  background: '#f8f9fa'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
typography:
  display-lg:
    fontFamily: Manrope
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.4'
    letterSpacing: -0.01em
  body-base:
    fontFamily: Manrope
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: '0'
  label-sm:
    fontFamily: Manrope
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.2'
    letterSpacing: 0.01em
  caption:
    fontFamily: Manrope
    fontSize: 12px
    fontWeight: '400'
    lineHeight: '1.4'
    letterSpacing: '0'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 24px
  lg: 48px
  xl: 80px
  gutter: 24px
  margin: 32px
---

## Brand & Style

The design system is anchored in the concept of "Clinical Precision." It balances the rigorous, data-driven nature of medical AI with a warm, approachable interface that reduces user anxiety. The style is **Minimalist and Corporate/Modern**, prioritizing clarity and speed of cognition above all else. 

The visual language utilizes high-density whitespace to create a "breathable" environment, essential for a healthcare context where information can often feel overwhelming. The aesthetic is sterile but not cold, professional but not intimidating, ensuring that every interaction feels reliable and scientifically sound.

## Colors

The palette is intentionally restrained to maintain high accessibility and a clinical feel. 

- **Primary Teal (#008080):** Used exclusively for primary calls-to-action, active states, and critical highlights. It represents health and vitality.
- **Deep Slate (#1A1D1E):** Used for primary text and headings. This high-contrast dark gray ensures maximum legibility for medical data.
- **Pure White (#FFFFFF):** The foundational background color to maximize light and space.
- **Cool Gray (#6B7280):** Utilized for secondary text, metadata, and borders to create a clear visual hierarchy.
- **Success/Error:** Use standard semantic greens and reds, but desaturated slightly to match the professional teal tone.

## Typography

The design system utilizes **Manrope** for its balance of geometric modernism and humanistic warmth. It is a highly legible typeface that performs exceptionally well for both large-scale medical dashboards and dense patient records.

Headers should be set with tighter letter-spacing and heavier weights to anchor the page. Body text utilizes a generous 1.6x line height to ensure reading comfort during long sessions. Use "Deep Slate" for all primary content and "Cool Gray" for tertiary information or labels.

## Layout & Spacing

This design system follows a **Fixed Grid** approach for desktop applications to ensure data visualization remains consistent and readable. A 12-column system is used with a 24px gutter. 

Spacing follows a strict 8px linear scale. For medical interfaces, "Whitespace is a tool"—use the `lg` (48px) and `xl` (80px) units to separate distinct clinical sections, preventing the UI from feeling cluttered. Content containers should typically have a maximum width of 1280px to maintain optimal line lengths for data reading.

## Elevation & Depth

Hierarchy is established through **Ambient Shadows** and tonal layering. The design avoids heavy borders, favoring soft shadows to define elevation.

- **Level 0 (Flat):** The main application background (Pure White).
- **Level 1 (Subtle):** Cards and content modules. Use a highly diffused shadow: `0px 4px 20px rgba(0, 0, 0, 0.04)`.
- **Level 2 (Active):** Modals, dropdowns, and floating tooltips. Use a deeper shadow: `0px 10px 30px rgba(0, 0, 0, 0.08)`.

Use thin, low-contrast borders (`1px solid #E5E7EB`) for input fields and table structures where shadows might cause too much visual noise.

## Shapes

The design system employs a **Rounded** shape language to soften the clinical aesthetic and make the AI interactions feel more "human." 

A base radius of **8px** (0.5rem) is used for standard components like buttons and input fields. Larger containers, such as dashboard cards or modal overlays, should use a **12px** radius. This consistency in rounding helps unify disparate data modules into a cohesive visual experience.

## Components

### Buttons
Primary buttons use the Teal accent with white text. They should have ample internal padding (12px vertical, 24px horizontal) to appear prominent and "touch-friendly." Secondary buttons are ghost-style with a subtle gray border and dark gray text.

### Cards
Cards are the primary container for patient data and AI insights. They must have a 12px corner radius, a subtle Level 1 shadow, and at least 24px of internal padding to maintain the "breathable" look.

### Input Fields
Inputs use a white background with a 1px Cool Gray border. On focus, the border transitions to Primary Teal with a subtle 2px teal outer glow (0.15 opacity). Labels should always be visible above the field in the `label-sm` style.

### Chips & Tags
Used for medical status (e.g., "Stable," "Critical"). Chips use a pill-shape (full rounding) and very light tints of semantic colors (e.g., light teal background with dark teal text) to avoid distracting from the primary CTA.

### Additional Components
- **Data Tables:** High-density but with clear row separation using 1px horizontal lines only.
- **AI Insight Banners:** Subtle teal-tinted background blocks used to highlight AI-generated suggestions or warnings.