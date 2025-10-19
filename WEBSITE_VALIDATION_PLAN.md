# Website Validation & Testing Plan
## Justice Minds Forensic Intelligence Website

### Executive Summary
This document outlines a comprehensive strategy for validating all links, navigation flow, styling consistency, and functionality across the Justice Minds website.

---

## Current Website Inventory

### HTML Pages (17 total)
1. **index.html** - Homepage
2. **about.html** - About page
3. **article-hilton-investigation.html** - Article page
4. **ben-oversight-validation.html** - Article page
5. **court-appeal-investigation.html** - Article page
6. **cultural-conditioning-freedom.html** - Article page
7. **cultural-exploitation-indian-workers.html** - Article page
8. **institutional-investigation-s188.html** - Article page
9. **investigation-hilton.html** - Article page
10. **legal-framework.html** - Article page
11. **measuring-competence-beyond-exams.html** - Article page
12. **privacy-policy.html** - Legal page
13. **shubham-sick-brother.html** - Article page
14. **shubham-story.html** - Article page
15. **terms-of-service.html** - Legal page
16. **the-one-person-principle.html** - Article page
17. **template-content-page.html** - Template

---

## Recommended MCP Server Solution

### Option 1: Use Existing Firecrawl MCP Server (Already Installed) ✅
**Your Firecrawl server can already help with:**
- Crawling entire website to map all pages
- Extracting all links from each page
- Validating navigation paths
- Checking for broken links

### Option 2: Add Dedicated Broken Link Checker MCP Server (Recommended Addition)
**Repository:** https://github.com/davinoishi/broken-link-checker-mcp

**Installation Steps:**
```bash
# Clone the repository
cd ~/Documents
git clone https://github.com/davinoishi/broken-link-checker-mcp.git
cd broken-link-checker-mcp
npm install
```

**Add to MCP Settings** (`~/Library/Application Support/Claude/claude_desktop_config.json` or Cline MCP settings):
```json
{
  "broken-link-checker": {
    "command": "node",
    "args": ["/Users/infiniteintelligence/Documents/broken-link-checker-mcp/index.js"],
    "disabled": false,
    "autoApprove": []
  }
}
```

**Available Tools:**
1. `check_page_links` - Check all links on a single HTML page
   - Parameters: url (required), excludeExternalLinks (optional), honorRobotExclusions (optional)
2. `check_site` - Recursively crawl and check all links across entire website
   - Parameters: url (required), excludeExternalLinks (optional), honorRobotExclusions (optional), maxSocketsPerHost (optional)

**Why This Server:**
- Specifically designed for link validation
- Checks internal and external links with detailed reporting
- Shows HTTP status codes and broken reasons
- Can exclude external links or respect robots.txt
- Provides summary stats (total links, broken, working)
- Works alongside your existing Firecrawl server

---

## Comprehensive Testing Strategy

### Phase 1: Initial Link Mapping
**Tools:** Firecrawl MCP Server
**Actions:**
- [ ] Crawl entire website starting from index.html
- [ ] Generate complete sitemap of all pages
- [ ] Extract all internal links from each page
- [ ] Extract all external links from each page
- [ ] Document navigation structure

### Phase 2: Link Validation
**Tools:** Broken Link Checker MCP Server + Manual Testing
**Actions:**
- [ ] Check all internal page links (forwards)
- [ ] Check all navigation menu links
- [ ] Check all footer links
- [ ] Check all article card links
- [ ] Check all "Read more" links
- [ ] Verify external links (Supabase images, etc.)
- [ ] Test breadcrumb navigation (if present)
- [ ] Validate legal page links (Terms, Privacy)

### Phase 3: Navigation Flow Testing
**Test Each Path:**
- [ ] Homepage → Article pages → Back to homepage
- [ ] Homepage → About page → Back to homepage
- [ ] Article page → Related article → Back navigation
- [ ] Any page → Footer links → Target pages
- [ ] Any page → Header nav → Target pages

### Phase 4: Style Consistency Validation
**According to .clinerules/website-style-standards.md:**
- [ ] Verify header structure on all pages (FINAL_JUSTICE_GUARDIAN.svg)
- [ ] Check sticky navigation on all pages (consistent behavior)
- [ ] Validate footer on all pages (nav bar + FINAL_JUSTICE_GUARDIAN_FOOTER.svg)
- [ ] Confirm color scheme consistency (--primary-blue, --accent-red)
- [ ] Check typography consistency (Libre Baskerville, Source Sans Pro)
- [ ] Verify mobile responsiveness on all pages (968px breakpoint)
- [ ] Test sticky nav mobile optimization (single line requirement)
- [ ] Test footer nav mobile wrapping

### Phase 5: Resource Validation
**Check All Assets:**
- [ ] Hero image: FINAL_JUSTICE_GUARDIAN.svg (Supabase)
- [ ] Footer image: FINAL_JUSTICE_GUARDIAN_FOOTER.svg (Supabase)
- [ ] Other SVG files: both_web_phone.svg, FINAL_JUSTICE_HERO.svg
- [ ] PNG files: emotional_debt.png, Password_desktop.svg, mobile_password.svg
- [ ] Google Fonts loading (Libre Baskerville, Source Sans Pro)

### Phase 6: Cross-Page Consistency Check
**Validate Across All Pages:**
- [ ] Header structure matches standard
- [ ] Navigation menu items identical
- [ ] Footer structure matches standard
- [ ] CSS variables consistent
- [ ] Color scheme identical
- [ ] Typography standards followed
- [ ] Button styling consistent
- [ ] Grid systems match standard

---

## Testing Workflow

### Step 1: Install Broken Link Checker
```bash
# Navigate to your preferred directory
cd ~/Documents

# Clone the repository
git clone https://github.com/davinoishi/broken-link-checker-mcp.git

# Install dependencies
cd broken-link-checker-mcp
npm install
```

### Step 2: Update MCP Settings
Add to your Cline MCP settings file (`~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`):

```json
{
  "mcpServers": {
    "broken-link-checker": {
      "command": "node",
      "args": ["/Users/infiniteintelligence/Documents/broken-link-checker-mcp/index.js"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

Then restart VSCode for changes to take effect.

### Step 3: Run Automated Link Check
Use the broken-link-checker MCP server tools:

**Option A: Check Single Page**
```
check_page_links with url: file:///Volumes/JUDGE_MAK/BOOK/justice-minds-website/index.html
```

**Option B: Check Entire Site (After Deploying)**
```
check_site with url: https://your-deployed-site.com
```

This will:
1. Scan all links on the specified page(s)
2. Report broken links with HTTP status codes
3. Provide summary (total, broken, working links)
4. Show detailed information about each broken link

### Step 4: Manual Style Validation
For each page:
1. Open in browser
2. Verify header/nav/footer match standard
3. Check color scheme and typography
4. Test responsive behavior at 968px
5. Click through navigation
6. Document any inconsistencies

### Step 5: Navigation Path Testing
Test all common user journeys:
- Landing on homepage → browsing articles → returning
- Direct article access → navigation → other sections
- Footer link usage → target pages → navigation back
- Mobile navigation flow

---

## Expected Results

### What Should Work:
✅ All internal links resolve correctly
✅ All navigation paths work forwards and backwards
✅ Header/footer consistent across all pages
✅ Style standards maintained on every page
✅ Mobile responsiveness working correctly
✅ Supabase assets loading properly
✅ Google Fonts loading correctly
✅ Article cards linking to correct pages

### Red Flags to Watch For:
❌ 404 errors on any internal links
❌ Broken image links (especially Supabase assets)
❌ Inconsistent header/footer structure
❌ Color scheme variations
❌ Typography inconsistencies
❌ Mobile navigation breaking into multiple lines
❌ Missing sticky nav behavior
❌ Footer nav wrapping incorrectly on mobile

---

## Maintenance Checklist

### After Any Page Changes:
- [ ] Run broken link checker
- [ ] Verify style standards maintained
- [ ] Test navigation to/from modified page
- [ ] Check mobile responsiveness
- [ ] Validate asset loading

### Weekly Validation:
- [ ] Full site crawl with Firecrawl
- [ ] Complete link check
- [ ] Spot-check random pages for style consistency
- [ ] Test external links (Supabase, Google Fonts)

---

## Emergency Fix Protocol

If issues found:
1. **Broken Link:** Update href in source file
2. **Style Inconsistency:** Reference .clinerules/website-style-standards.md
3. **Missing Asset:** Check Supabase storage URL
4. **Navigation Error:** Verify sticky nav structure
5. **Mobile Issue:** Test at 968px breakpoint, adjust padding/font-size

---

## Tools Summary

### Already Installed (Use These First):
1. **Firecrawl MCP Server** - Website crawling and mapping
2. **Browser DevTools** - Manual inspection
3. **VSCode** - Code editing and fixes

### Recommended Addition:
1. **Broken Link Checker MCP Server** - Automated link validation

### Manual Tools:
1. Browser (Chrome/Firefox) - Visual inspection
2. Mobile device or emulator - Mobile testing
3. Browser DevTools Responsive Mode - Breakpoint testing

---

## Next Steps

1. ✅ Review this plan
2. ⬜ Install broken-link-checker MCP server
3. ⬜ Run Phase 1: Initial Link Mapping
4. ⬜ Run Phase 2: Link Validation
5. ⬜ Execute Phase 3: Navigation Flow Testing
6. ⬜ Complete Phase 4: Style Consistency Validation
7. ⬜ Verify Phase 5: Resource Validation
8. ⬜ Finalize Phase 6: Cross-Page Consistency
9. ⬜ Document findings
10. ⬜ Fix any issues discovered
11. ⬜ Re-test after fixes
12. ⬜ Mark website as validated ✓

---

**Created:** January 18, 2025
**Website:** Justice Minds Forensic Intelligence
**Purpose:** Comprehensive validation before launch/streamlining
