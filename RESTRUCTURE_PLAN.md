# Website Restructure Plan

## Current Issues
1. ❌ 15+ HTML files in root directory
2. ❌ Mixed content: audio forensics, court statistics, backup site all at root level
3. ❌ Python scripts scattered in audio subdirectories
4. ❌ Temporary MP4 files in version control
5. ❌ No clear assets structure (CSS, images, JavaScript)
6. ❌ Documentation mixed with code
7. ❌ SVG/image files in root
8. ❌ Court statistics and backup site at root level

## Proposed Optimized Structure

```
justice-minds-website/
├── public/                              # Public-facing website (deploy this)
│   ├── index.html                       # Homepage
│   ├── about.html
│   ├── privacy-policy.html
│   ├── terms-of-service.html
│   │
│   ├── assets/                          # All static assets
│   │   ├── css/                         # Stylesheets
│   │   │   ├── main.css
│   │   │   ├── article.css
│   │   │   └── components.css
│   │   ├── js/                          # JavaScript
│   │   │   └── main.js
│   │   ├── images/                      # Images
│   │   │   ├── logos/
│   │   │   ├── heroes/
│   │   │   └── icons/
│   │   └── svg/                         # SVG assets
│   │       ├── FINAL_JUSTICE_HERO.svg
│   │       ├── both_web_phone.svg
│   │       └── Password_desktop.svg
│   │
│   ├── investigations/                   # Investigation articles
│   │   ├── hilton-investigation.html
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
│   │       ├── README.md
│   │       ├── violation-01/
│   │       ├── violation-02/
│   │       └── ...
│   │
│   ├── court-statistics/                # Court data and analysis
│   │   ├── data/                        # CSV files
│   │   │   ├── COMBINED-DATA-COMPLETE.csv
│   │   │   ├── comprehensive_obstruction_metrics.csv
│   │   │   └── ...
│   │   ├── documents/                   # PDF evidence
│   │   │   ├── CIVAPP3_form__MACKLIN.pdf
│   │   │   └── ...
│   │   ├── reports/                     # HTML reports
│   │   │   └── dashboard.html
│   │   └── images/                      # Charts and screenshots
│   │       ├── appeal_success_chart.png
│   │       └── radar_chart.png
│   │
│   └── correspondence/                  # Email evidence
│       ├── mail.com - Abel Macklin-Daly.pdf
│       └── ...
│
├── tools/                               # Automation scripts
│   ├── audio-processing/
│   │   ├── download_audio.py
│   │   ├── extract_grain_transcripts.py
│   │   ├── organize_violations.py
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
│   ├── VALIDATION_RESULTS_SUMMARY.md
│   └── design-system.md
│
├── archive/                             # Old versions/backups
│   └── backup-site/
│       ├── index.html
│       └── ...
│
├── .gitignore                           # Git ignore rules
├── CNAME                                # Custom domain config
├── vercel.json                          # Vercel deployment config
├── package.json                         # Node dependencies
├── package-lock.json
└── README.md                            # Main documentation

```

## Benefits of New Structure

### 1. Clear Separation
- **public/** = Everything that gets deployed to production
- **evidence/** = Sensitive forensic materials (NOT deployed)
- **tools/** = Automation and development scripts
- **docs/** = Project documentation
- **archive/** = Old versions for reference

### 2. Better Organization
- HTML files grouped by content type (investigations, articles, stories, legal)
- Assets properly organized (CSS, JS, images, SVG)
- Evidence categorized by type (audio, court stats, correspondence)
- Scripts organized by function (audio processing, validation, deployment)

### 3. Improved Maintainability
- Easy to find files by purpose
- Clear what gets deployed vs what stays local
- Better for team collaboration
- Follows web development best practices

### 4. Security
- Evidence folder clearly marked as NOT for deployment
- Sensitive data separated from public content
- Easy to configure .gitignore properly

### 5. Scalability
- Room to grow within each category
- Clear place for new content types
- Template system can reference organized assets
- Build process can target public/ folder

## Migration Steps

1. ✅ Create new folder structure
2. Move HTML files to appropriate subdirectories
3. Create assets folders and organize CSS/JS/images
4. Move evidence to evidence/ folder
5. Move scripts to tools/ folder
6. Move documentation to docs/ folder
7. Move backup site to archive/
8. Update all internal links in HTML files
9. Update deployment configuration
10. Test all links and assets
11. Update README with new structure

## Deployment Configuration

### Vercel
Update `vercel.json`:
```json
{
  "cleanUrls": true,
  "trailingSlash": false,
  "public": true
}
```

Point deployment to `public/` directory or move its contents to root during deployment.

### Git Ignore
Update `.gitignore`:
```
# Development
node_modules/
.DS_Store
*.log

# Evidence (sensitive)
evidence/
temp_*.mp4

# Environment
.env
.env.local
```

## Notes

- All external SVG links in HTML remain unchanged
- Google Fonts CDN links remain unchanged
- Evidence folder should be added to .gitignore if sensitive
- Internal links need updating (href paths)
- Consider using relative paths from root
