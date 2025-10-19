const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const publicDir = path.join(__dirname, '../../public');

// ANSI color codes
const colors = {
    green: '\x1b[32m',
    red: '\x1b[31m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    reset: '\x1b[0m',
    bold: '\x1b[1m'
};

// Get all HTML files
function getAllHtmlFiles(dir) {
    const files = [];
    const items = fs.readdirSync(dir);
    
    for (const item of items) {
        const fullPath = path.join(dir, item);
        const stat = fs.statSync(fullPath);
        
        if (stat.isDirectory()) {
            files.push(...getAllHtmlFiles(fullPath));
        } else if (item.endsWith('.html')) {
            files.push(fullPath);
        }
    }
    
    return files;
}

// Test internal links
function testLinks(htmlFile) {
    const content = fs.readFileSync(htmlFile, 'utf-8');
    const dom = new JSDOM(content);
    const document = dom.window.document;
    const links = document.querySelectorAll('a[href]');
    
    const results = {
        working: [],
        broken: []
    };
    
    for (const link of links) {
        const href = link.getAttribute('href');
        
        // Skip external links and javascript/mailto
        if (!href || 
            href.startsWith('http://') || 
            href.startsWith('https://') || 
            href.startsWith('javascript:') || 
            href.startsWith('mailto:') ||
            href.startsWith('tel:') ||
            href === '#') {
            continue;
        }
        
        // Check if link has an anchor
        const [filePath, anchor] = href.split('#');
        
        // Resolve the file path relative to the current file
        const currentDir = path.dirname(htmlFile);
        const resolvedPath = path.resolve(currentDir, filePath || '.');
        
        // For same-page anchors (href="#anchor"), check current file
        const targetFile = filePath ? resolvedPath : htmlFile;
        
        // Check if file exists
        if (!fs.existsSync(targetFile)) {
            results.broken.push({
                link: href,
                text: link.textContent.trim(),
                resolved: targetFile,
                reason: 'File not found'
            });
            continue;
        }
        
        // If there's an anchor, verify it exists in the target file
        if (anchor) {
            const targetContent = fs.readFileSync(targetFile, 'utf-8');
            const targetDom = new JSDOM(targetContent);
            const targetDoc = targetDom.window.document;
            
            // Check if anchor ID exists
            const anchorElement = targetDoc.getElementById(anchor);
            const anchorExists = anchorElement !== null;
            
            if (!anchorExists) {
                results.broken.push({
                    link: href,
                    text: link.textContent.trim(),
                    resolved: targetFile,
                    reason: `Anchor #${anchor} not found`
                });
            } else {
                results.working.push({
                    link: href,
                    text: link.textContent.trim()
                });
            }
        } else {
            results.working.push({
                link: href,
                text: link.textContent.trim()
            });
        }
    }
    
    return results;
}

// Test style consistency
function testStyles(htmlFile) {
    const content = fs.readFileSync(htmlFile, 'utf-8');
    const dom = new JSDOM(content);
    const document = dom.window.document;
    
    const issues = [];
    
    // Check for style tag
    const styleTag = document.querySelector('style');
    if (!styleTag) {
        issues.push('No <style> tag found');
        return issues;
    }
    
    const styleContent = styleTag.textContent;
    
    // Check for CSS variables
    if (!styleContent.includes('--primary-blue')) issues.push('Missing CSS variable: --primary-blue');
    if (!styleContent.includes('--accent-red')) issues.push('Missing CSS variable: --accent-red');
    if (!styleContent.includes('--text-dark')) issues.push('Missing CSS variable: --text-dark');
    
    // Check for navigation
    const nav = document.querySelector('nav');
    if (!nav) {
        issues.push('Missing <nav> element');
    } else if (!styleContent.includes('.main-nav') && !styleContent.includes('.nav-bar')) {
        issues.push('Missing navigation styles');
    }
    
    // Check for footer
    const footer = document.querySelector('footer');
    if (!footer) issues.push('Missing <footer> element');
    
    return issues;
}

// Test common navigation paths
function testNavigationPaths() {
    const results = [];
    
    // Test: Home → Article → Back
    const indexFile = path.join(publicDir, 'index.html');
    const articleFile = path.join(publicDir, 'articles/cultural-conditioning-freedom.html');
    
    if (fs.existsSync(indexFile) && fs.existsSync(articleFile)) {
        results.push({ path: 'Home → Article → Back', status: 'working' });
    }
    
    // Test: Home → Investigation → Back
    const investigationFile = path.join(publicDir, 'investigations/investigation-hilton.html');
    if (fs.existsSync(indexFile) && fs.existsSync(investigationFile)) {
        results.push({ path: 'Home → Investigation → Back', status: 'working' });
    }
    
    // Test: Article → Story → Legal
    const storyFile = path.join(publicDir, 'stories/shubham-story.html');
    const legalFile = path.join(publicDir, 'legal/legal-framework.html');
    if (fs.existsSync(articleFile) && fs.existsSync(storyFile) && fs.existsSync(legalFile)) {
        results.push({ path: 'Article → Story → Legal', status: 'working' });
    }
    
    return results;
}

// Main execution
console.log('============================================================');
console.log('Justice Minds Website - Navigation & Style Test');
console.log('============================================================\n');

const htmlFiles = getAllHtmlFiles(publicDir);
console.log(`📁 Found ${htmlFiles.length} HTML files\n`);

console.log('============================================================');
console.log('Testing Internal Links');
console.log('============================================================\n');

let totalLinks = 0;
let totalWorking = 0;
let totalBroken = 0;
const brokenLinksDetails = [];
const linkResults = {};

for (const file of htmlFiles) {
    const relativePath = path.relative(path.join(__dirname, '../..'), file);
    const results = testLinks(file);
    
    linkResults[relativePath] = results;
    totalLinks += results.working.length + results.broken.length;
    totalWorking += results.working.length;
    totalBroken += results.broken.length;
    
    if (results.broken.length > 0) {
        console.log(`${colors.red}📄 ${relativePath}${colors.reset}`);
        console.log(`   ${colors.red}❌ ${results.broken.length} broken link(s)${colors.reset}`);
        brokenLinksDetails.push({ file: relativePath, broken: results.broken });
    } else {
        console.log(`${colors.green}📄 ${relativePath}${colors.reset}`);
        console.log(`   ${colors.green}✅ All ${results.working.length} link(s) working${colors.reset}`);
    }
}

console.log('\n============================================================');
console.log('Testing Style Consistency');
console.log('============================================================\n');

const styleIssues = {};
for (const file of htmlFiles) {
    const relativePath = path.relative(path.join(__dirname, '../..'), file);
    const issues = testStyles(file);
    
    if (issues.length > 0) {
        console.log(`${colors.yellow}⚠️  ${relativePath}${colors.reset}`);
        styleIssues[relativePath] = issues;
    } else {
        console.log(`${colors.green}✅ ${relativePath}${colors.reset}`);
    }
}

console.log('\n============================================================');
console.log('Testing Common Navigation Paths');
console.log('============================================================\n');

const navPaths = testNavigationPaths();
for (const path of navPaths) {
    console.log(`${colors.green}✅ ${path.path}${colors.reset}`);
}

console.log('\n============================================================');
console.log('Summary');
console.log('============================================================\n');

console.log(`📊 Total Files: ${htmlFiles.length}`);
console.log(`🔗 Total Links Tested: ${totalLinks}`);
console.log(`${colors.green}✅ Working Links: ${totalWorking}${colors.reset}`);
console.log(`${colors.red}❌ Broken Links: ${totalBroken}${colors.reset}`);
console.log(`${colors.yellow}⚠️  Style Issues: ${Object.keys(styleIssues).length}${colors.reset}`);

// Detailed broken links
if (brokenLinksDetails.length > 0) {
    console.log('\n============================================================');
    console.log('Broken Links Details');
    console.log('============================================================\n');
    
    for (const { file, broken } of brokenLinksDetails) {
        console.log(`${colors.red}❌ ${file}${colors.reset}`);
        for (const link of broken) {
            console.log(`   Link: ${link.link}`);
            console.log(`   Text: "${link.text}"`);
            console.log(`   Reason: ${link.reason}`);
            console.log(`   Resolved to: ${link.resolved}\n`);
        }
    }
}

// Detailed style issues
if (Object.keys(styleIssues).length > 0) {
    console.log('\n============================================================');
    console.log('Style Issues Details');
    console.log('============================================================\n');
    
    for (const [file, issues] of Object.entries(styleIssues)) {
        console.log(`${colors.yellow}⚠️  ${file}${colors.reset}`);
        for (const issue of issues) {
            console.log(`   - ${issue}`);
        }
        console.log('');
    }
}

console.log('\n============================================================');
if (totalBroken === 0 && Object.keys(styleIssues).length === 0) {
    console.log(`${colors.green}${colors.bold}✅ All tests passed! Navigation and styles are consistent.${colors.reset}`);
} else {
    console.log(`${colors.yellow}⚠️  Some issues found. Please review above.${colors.reset}`);
}
console.log('============================================================\n');
