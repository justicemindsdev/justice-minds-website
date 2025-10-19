#!/usr/bin/env node
/**
 * Website Link Validator for Justice Minds
 * Validates all internal links across HTML files in the project
 */

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

// Configuration
const rootDir = '/Volumes/JUDGE_MAK/BOOK/justice-minds-website';
const htmlFiles = [
    'index.html',
    'about.html',
    'article-hilton-investigation.html',
    'ben-oversight-validation.html',
    'court-appeal-investigation.html',
    'cultural-conditioning-freedom.html',
    'cultural-exploitation-indian-workers.html',
    'institutional-investigation-s188.html',
    'investigation-hilton.html',
    'legal-framework.html',
    'measuring-competence-beyond-exams.html',
    'privacy-policy.html',
    'shubham-sick-brother.html',
    'shubham-story.html',
    'terms-of-service.html',
    'the-one-person-principle.html'
];

const results = {
    totalLinks: 0,
    validLinks: 0,
    brokenLinks: [],
    externalLinks: [],
    styleIssues: []
};

console.log('🔍 Justice Minds Website Validation');
console.log('=====================================\n');

// Check if file exists
function fileExists(filepath) {
    return fs.existsSync(path.join(rootDir, filepath));
}

// Extract links from HTML
function extractLinks(filepath) {
    const fullPath = path.join(rootDir, filepath);
    const html = fs.readFileSync(fullPath, 'utf-8');
    const dom = new JSDOM(html);
    const document = dom.window.document;
    
    const links = [];
    
    // Get all <a> tags
    const anchors = document.querySelectorAll('a[href]');
    anchors.forEach(anchor => {
        const href = anchor.getAttribute('href');
        if (href) {
            links.push({
                href,
                text: anchor.textContent.trim(),
                type: 'anchor'
            });
        }
    });
    
    // Get navigation links
    const navLinks = document.querySelectorAll('nav a[href]');
    
    return { links, navLinks: navLinks.length };
}

// Validate style consistency
function validateStyles(filepath) {
    const fullPath = path.join(rootDir, filepath);
    const html = fs.readFileSync(fullPath, 'utf-8');
    const issues = [];
    
    // Check for required elements
    if (!html.includes('FINAL_JUSTICE_GUARDIAN.svg')) {
        issues.push('Missing header hero image');
    }
    if (!html.includes('FINAL_JUSTICE_GUARDIAN_FOOTER.svg')) {
        issues.push('Missing footer image');
    }
    if (!html.includes('Libre Baskerville')) {
        issues.push('Missing Libre Baskerville font');
    }
    if (!html.includes('Source Sans Pro')) {
        issues.push('Missing Source Sans Pro font');
    }
    if (!html.includes('--primary-blue')) {
        issues.push('Missing primary-blue CSS variable');
    }
    if (!html.includes('--accent-red')) {
        issues.push('Missing accent-red CSS variable');
    }
    
    return issues;
}

// Main validation
console.log('📁 Scanning HTML files...\n');

htmlFiles.forEach(file => {
    console.log(`\n📄 ${file}`);
    console.log('─'.repeat(50));
    
    if (!fileExists(file)) {
        console.log('   ❌ FILE NOT FOUND');
        return;
    }
    
    // Extract and validate links
    const { links, navLinks } = extractLinks(file);
    console.log(`   ✓ Found ${links.length} links (${navLinks} in navigation)`);
    
    links.forEach(link => {
        results.totalLinks++;
        
        if (link.href.startsWith('http://') || link.href.startsWith('https://')) {
            results.externalLinks.push({
                file,
                href: link.href,
                text: link.text
            });
        } else if (link.href.startsWith('#')) {
            // Internal anchor - skip for now
            results.validLinks++;
        } else if (link.href.startsWith('mailto:') || link.href.startsWith('tel:')) {
            // Email/phone - skip
            results.validLinks++;
        } else {
            // Internal page link
            const targetFile = link.href.split('#')[0];
            if (targetFile && !fileExists(targetFile)) {
                results.brokenLinks.push({
                    file,
                    href: link.href,
                    text: link.text
                });
                console.log(`   ❌ BROKEN: "${link.href}" → "${link.text}"`);
            } else {
                results.validLinks++;
            }
        }
    });
    
    // Validate styles
    const styleIssues = validateStyles(file);
    if (styleIssues.length > 0) {
        results.styleIssues.push({ file, issues: styleIssues });
        console.log(`   ⚠️  Style issues: ${styleIssues.join(', ')}`);
    } else {
        console.log('   ✓ Style standards maintained');
    }
});

// Summary
console.log('\n\n📊 VALIDATION SUMMARY');
console.log('=====================================');
console.log(`Total Links Checked: ${results.totalLinks}`);
console.log(`Valid Links: ${results.validLinks}`);
console.log(`Broken Links: ${results.brokenLinks.length}`);
console.log(`External Links: ${results.externalLinks.length}`);
console.log(`Style Issues: ${results.styleIssues.length}`);

if (results.brokenLinks.length > 0) {
    console.log('\n\n❌ BROKEN LINKS FOUND:');
    console.log('=====================================');
    results.brokenLinks.forEach(link => {
        console.log(`\nFile: ${link.file}`);
        console.log(`Link: ${link.href}`);
        console.log(`Text: "${link.text}"`);
    });
}

if (results.externalLinks.length > 0) {
    console.log('\n\n🌐 EXTERNAL LINKS (Manual Check Required):');
    console.log('=====================================');
    const uniqueExternal = [...new Set(results.externalLinks.map(l => l.href))];
    uniqueExternal.forEach(href => {
        console.log(`• ${href}`);
    });
}

if (results.styleIssues.length > 0) {
    console.log('\n\n⚠️  STYLE CONSISTENCY ISSUES:');
    console.log('=====================================');
    results.styleIssues.forEach(issue => {
        console.log(`\n${issue.file}:`);
        issue.issues.forEach(i => console.log(`  • ${i}`));
    });
}

// Final verdict
console.log('\n\n' + '='.repeat(50));
if (results.brokenLinks.length === 0 && results.styleIssues.length === 0) {
    console.log('✅ VALIDATION PASSED!');
    console.log('All internal links work and style standards are maintained.');
} else {
    console.log('⚠️  ISSUES FOUND - Please review above');
}
console.log('='.repeat(50) + '\n');

// Save report
const report = {
    timestamp: new Date().toISOString(),
    summary: {
        totalLinks: results.totalLinks,
        validLinks: results.validLinks,
        brokenLinksCount: results.brokenLinks.length,
        externalLinksCount: results.externalLinks.length,
        styleIssuesCount: results.styleIssues.length
    },
    brokenLinks: results.brokenLinks,
    externalLinks: results.externalLinks,
    styleIssues: results.styleIssues
};

fs.writeFileSync(
    path.join(rootDir, 'validation-report.json'),
    JSON.stringify(report, null, 2)
);

console.log('📝 Detailed report saved to: validation-report.json\n');

// Exit with error code if issues found
process.exit(results.brokenLinks.length > 0 || results.styleIssues.length > 0 ? 1 : 0);
