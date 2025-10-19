# Justice Minds Forensic Intelligence Website

A Guardian-style investigative journalism website exposing systemic exploitation of international workers in the UK.

## 📁 Optimized Project Structure

```
justice-minds-website/
├── public/                              # Public-facing website (deploy this)
│   ├── index.html                       # Homepage
│   ├── about.html
│   ├── privacy-policy.html
│   ├── terms-of-service.html
│   ├── template-content-page.html
│   │
│   ├── assets/                          # All static assets
│   │   ├── css/                         # Stylesheets (to be extracted)
│   │   ├── js/                          # JavaScript
│   │   ├── images/                      # Images
│   │   │   ├── logos/
│   │   │   ├── heroes/
│   │   │   └── icons/
│   │   └── svg/                         # SVG assets
│   │       ├── FINAL_JUSTICE_HERO.svg
│   │       ├── both_web_phone.svg
│   │       ├── Password_desktop.svg
│   │       ├── mobile_password.svg
│   │       └── emotional_debt.png
│   │
│   ├── investigations/                   # Investigation articles
│   │   ├── article-hilton-investigation.html
│   │   ├── court-appeal-investigation.html
│   │   └── institutional-investigation-s188.html
│   │
│   ├── articles/                        # Opinion & analysis articles
│   │   ├── cultural-conditioning-freedom.html
│   │   ├── cultural-exploitation-indian-workers.html
│   │   ├── measuring-competence-beyond-exams.html
│   │   └── the-one-person-principle.html
│   │
│   ├── stories/                         # Personal testimonies
│   │   ├── shubham-story.html
│   │   └── shubham-sick-brother.html
│   │
│   └── legal/                           # Legal framework pages
│       ├── legal-framework.html
│       └── ben-oversight-validation.html
│
├── evidence/                            # Forensic evidence (NOT deployed)
│   ├── audio/
│   │   └── section188-violations/
│   │       ├── violation-01/
│   │       ├── violation-02/
│   │       └── ...
│   │
│   └── court-statistics/                # Court data and analysis
│       ├── data/                        # CSV files
│       ├── documents/                   # PDF evidence
│       ├── reports/                     # HTML reports
│       └── images/                      # Charts and screenshots
│
├── tools/                               # Automation scripts
│   ├── audio-processing/
│   │   ├── download_audio.py
│   │   ├── extract_grain_transcripts.py
│   │   ├── organize_violations.py
│   │   ├── reorganize_existing_audio.py
│   │   └── create_dual_structure.py
│   │
│   ├── validation/
│   │   ├── validate-website-links.js
│   │   └── install-link-checker.sh
│   │
│   └── deployment/
│       └── setup-env.sh
│
├── docs/                                # Documentation
│   ├── DEPLOYMENT_GUIDE.md
│   ├── WEBSITE_LAUNCH_CHECKLIST.md
│   ├── WEBSITE_VALIDATION_PLAN.md
│   └── VALIDATION_RESULTS_SUMMARY.md
│
├── archive/                             # Old versions/backups
│   └── backup-site/
│
├── .gitignore                           # Git ignore rules
├── CNAME                                # Custom domain config
├── vercel.json                          # Vercel deployment config
├── package.json                         # Node dependencies
├── RESTRUCTURE_PLAN.md                  # Restructure documentation
└── README.md                            # This file
```

## 🎯 Structure Benefits

### 1. Clear Separation
- **public/** = Everything deployed to production (the actual website)
- **evidence/** = Sensitive forensic materials (NOT deployed, in .gitignore)
- **tools/** = Automation and development scripts
- **docs/** = Project documentation
- **archive/** = Old versions for reference

### 2. Better Organization
- HTML files grouped by content type (investigations, articles, stories, legal)
- Assets properly organized (CSS, JS, images, SVG)
- Evidence categorized by type (audio, court stats)
- Scripts organized by function (audio processing, validation, deployment)

### 3. Security
- Evidence folder clearly marked and ignored by git
- Sensitive data separated from public content
- Temporary files excluded from version control

### 4. Scalability
- Room to grow within each category
- Clear place for new content types
- Easy to understand for new team members

## 🎨 Design System

### Color Palette
- **Primary Blue**: `#052962` - Header background, authority
- **Accent Red**: `#c70000` - Kickers, links, emphasis
- **Text Dark**: `#121212` - Main body text
- **Text Grey**: `#767676` - Secondary text, metadata
- **Border Grey**: `#dcdcdc` - Dividers, borders
- **Background Light**: `#f6f6f6` - Subtle backgrounds

### Typography
- **Headlines**: Libre Baskerville (serif) - Authority and gravitas
- **Body**: Source Sans Pro (sans-serif) - Clean readability
- **Hierarchy**:
  - Hero title: 3.5rem (article pages), 3rem (homepage)
  - Section headers: 2rem
  - Article titles: 1.5rem
  - Body text: 1.125rem
  - Metadata: 0.95rem

## 🚀 Deployment

### Vercel (Recommended)
The site is configured for Vercel deployment. Simply connect your repository and Vercel will automatically deploy from the repository root. The `vercel.json` configuration handles URL routing.

### Local Testing
```bash
# Simply open the public/index.html file in your browser
open public/index.html

# Or use a local server
cd public
python -m http.server 8000
# Visit http://localhost:8000
```

### Build Process
No build process required - this is a static HTML/CSS website.

## 📝 Content Guidelines

### Writing Style
- **Forensic precision**: Use specific data, timestamps, recordings
- **Human empathy**: Center victim voices and experiences
- **Systemic critique**: Pattern recognition across institutions
- **Guardian tone**: Serious, authoritative, but accessible
- **Evidence-based**: Every claim backed by citation

### Article Structure
1. Opening scene or quote
2. Context and background
3. Systematic analysis
4. Human impact
5. Legal/institutional implications
6. Path forward
7. References

## 🛠️ Development Tools

### Audio Processing
Tools for extracting and organizing forensic audio evidence:
```bash
cd tools/audio-processing
python download_audio.py          # Download from Grain API
python extract_grain_transcripts.py  # Extract transcripts
python organize_violations.py     # Organize by violation type
```

### Link Validation
```bash
cd tools/validation
./install-link-checker.sh         # Install dependencies
node validate-website-links.js    # Check all links
```

### Environment Setup
```bash
cd tools/deployment
./setup-env.sh                    # Set up development environment
```

## 🏢 Company Information

**Justice Minds Forensic Intelligence Ltd**
- Company Number: 16331423
- ICO Certified: ZB896365
- Status: Parliamentary Acknowledged Investigative Body
- Founded: 2023

## 📱 Responsive Design

### Breakpoints
- **Desktop**: 1280px max-width container
- **Tablet**: < 968px - Single column layouts
- **Mobile**: < 768px - Reduced font sizes, stacked grids

### Browser Support
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## 🔗 External Assets

### Logos (SVG)
- Header: Hosted on Supabase storage
- Footer: Hosted on Supabase storage

### Fonts
- Google Fonts: Libre Baskerville, Source Sans Pro

## 🔒 Security Notes

- **Evidence folder** is excluded from git via `.gitignore`
- Temporary MP4 files are not tracked
- No sensitive credentials in version control
- All API keys should be in environment variables

## 📚 Documentation

- **DEPLOYMENT_GUIDE.md**: Detailed deployment instructions
- **WEBSITE_LAUNCH_CHECKLIST.md**: Pre-launch checklist
- **WEBSITE_VALIDATION_PLAN.md**: Testing and validation plan
- **VALIDATION_RESULTS_SUMMARY.md**: Latest validation results
- **RESTRUCTURE_PLAN.md**: Details on the folder reorganization

## 🔄 Recent Changes

### Latest Restructure (October 2025)
- ✅ Organized all HTML files into logical subdirectories
- ✅ Created proper assets structure
- ✅ Separated evidence from public content
- ✅ Moved scripts to tools directory
- ✅ Consolidated documentation
- ✅ Updated .gitignore for security
- ✅ Archived old backup site

## 📄 License

© 2025 Justice Minds Forensic Intelligence Ltd. All rights reserved.

## 📧 Contact

For press inquiries, evidence submission, or legal consultation:
- **Company No**: 16331423
- **ICO**: ZB896365

---

**Built with**: HTML5, CSS3, and a commitment to exposing systemic injustice.

**Last Updated**: October 2025
