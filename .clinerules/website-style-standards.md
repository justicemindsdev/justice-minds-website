## Brief overview
Project-specific guidelines for the Justice Minds Forensic Intelligence website. These rules define the exact styling, structure, and flow that must be maintained across all pages. The current design is locked in and perfected—all new pages must follow this exact pattern.

## Header structure
- Full-width hero image from Supabase storage: `FINAL_JUSTICE_GUARDIAN.svg`
- Header background: `--primary-blue` (#052962)
- Bottom border: 4px solid `--accent-red` (#c70000)
- No padding or margins on hero image (full bleed design)

## Sticky navigation (Main Nav)
- Position: sticky, top: 0, z-index: 1000
- Background: `--primary-blue` with box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2)
- Border-top: 1px solid rgba(255, 255, 255, 0.1)
- Border-bottom: 4px solid `--accent-red`
- Nav items: uppercase, bold, letter-spacing 1px, padding 1rem 2.5rem
- Hover/active state: background rgba(255, 255, 255, 0.1) + red bottom border
- **CRITICAL MOBILE FIX**: Navigation must fit in one line on mobile screens
  - Mobile breakpoint: @media (max-width: 968px)
  - Reduce padding to 0.75rem 1.5rem for mobile
  - Reduce font-size to 0.85rem for mobile
  - Use flex-wrap but optimize spacing to keep single row if possible
  - Consider using overflow-x: auto with scrollable horizontal nav if needed

## Footer structure
- Background: `--primary-blue`
- Two-part design:
  1. Footer navigation bar with links (top section)
  2. Full-width footer image from Supabase: `FINAL_JUSTICE_GUARDIAN_FOORTER.svg`
- Footer nav bar:
  - Background: rgba(0, 0, 0, 0.2)
  - Border-top: 1px solid rgba(255, 255, 255, 0.1)
  - Links: centered, flex-wrap, padding 0.75rem 1.5rem
  - Text: white/semi-transparent, uppercase, 0.85rem, font-weight 600
  - **MOBILE OPTIMIZATION**: Footer nav links should fit nicely on mobile
    - Mobile padding: 0.5rem 1rem
    - Mobile font-size: 0.75rem
    - Allow wrapping but optimize for readability

## Color scheme (CSS variables)
- `--primary-blue`: #052962
- `--accent-red`: #c70000
- `--text-dark`: #121212
- `--text-grey`: #767676
- `--border-grey`: #dcdcdc
- `--bg-light`: #f6f6f6
- White background: #ffffff

## Typography
- Headers: 'Libre Baskerville', serif (Google Fonts)
- Body: 'Source Sans Pro', sans-serif (Google Fonts)
- Must include both font links in every page head
- Hero h1: 3rem (2rem on mobile)
- Section headers: 2rem with 4px blue bottom border
- Article card h2: 1.5rem

## Page structure pattern
Every new page MUST follow this exact structure:
1. `<header class="header">` with hero image
2. `<nav class="main-nav">` sticky navigation
3. `<main class="container">` with max-width 1280px, padding 3rem 2rem
4. `<footer class="footer">` with nav bar + footer image
5. All styling embedded in `<style>` tags in head

## Content grid system
- Hero section: 2-column grid (1fr 1fr), gap 2rem, becomes 1 column on mobile
- Article grid: 3 columns (repeat(3, 1fr)), gap 2rem, becomes 1 column on mobile
- Hero images: 500px height, object-fit cover
- Responsive breakpoint: 968px

## Article card components
- Kicker: red, uppercase, 0.85rem, bold, letter-spacing 0.5px
- Heading: Libre Baskerville, 1.5rem, line-height 1.3
- Excerpt: grey text, 1rem, line-height 1.6
- Read more link: red, bold, with arrow (→)
- Bottom border: 1px solid grey, padding-bottom 1.5rem

## Button styling
- Primary button: red background, white text
- Padding: 0.75rem 2rem
- Border-radius: 2px (subtle)
- Hover: darker red (#a00000), translateY(-2px)

## Mobile responsiveness requirements
- Breakpoint: 968px
- Navigation must remain functional and visible on mobile
- **Priority fix**: Ensure sticky nav fits in one line at top on mobile devices
- **Priority fix**: Ensure footer nav wraps properly and remains readable on mobile
- Grid layouts collapse to single column
- Reduce hero h1 from 3rem to 2rem
- Adjust padding and font sizes for smaller screens

## Consistency requirements
- All pages must use identical header/nav/footer structure
- All pages must use identical CSS variables and color scheme
- All pages must import the same Google Fonts
- All pages must use the same max-width container (1280px)
- All pages must follow the same spacing patterns (3rem sections, 2rem gaps)

## Asset references
- Header hero: `https://tvecnfdqakrevzaeifpk.supabase.co/storage/v1/object/public/caseworks/FINAL_JUSTICE_GUARDIAN.svg`
- Footer image: `https://tvecnfdqakrevzaeifpk.supabase.co/storage/v1/object/public/caseworks/FINAL_JUSTICE_GUARDIAN_FOORTER.svg`
- These must be consistent across all pages

## Development workflow
When creating new pages:
1. Copy the exact header structure from index.html
2. Copy the exact sticky nav structure from index.html
3. Copy the exact footer structure from index.html
4. Copy all CSS variables and base styles
5. Ensure mobile breakpoint includes nav optimization for single-line display
6. Test navigation fits properly on mobile (priority requirement)
7. Test footer nav wraps/displays properly on mobile
8. Maintain the exact color scheme and typography
9. Use the established grid patterns for content layout
10. Never deviate from the sticky nav, header, or footer patterns
