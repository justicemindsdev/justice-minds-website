#!/usr/bin/env node

/**
 * Fix Anchor Links to index.html
 * Updates index.html#anchor links to use proper relative paths
 */

const fs = require('fs');
const path = require('path');

function fixAnchorLinksInFile(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    const relativePath = path.relative(process.cwd(), filePath);
    
    // Determine depth from public/ directory
    const depth = filePath.split(path.sep).filter(p => p !== 'public').length - filePath.split(path.sep).indexOf('public') - 1;
    
    // Calculate relative path to index.html based on depth
    let relativeIndexPath = '';
    if (depth === 0) {
      // File is in public/ root
      relativeIndexPath = 'index.html';
    } else {
      // File is in subdirectory
      relativeIndexPath = '../'.repeat(depth) + 'index.html';
    }
    
    // Replace all index.html#anchor patterns
    const anchorPattern = /href=["']index\.html(#[^"']+)["']/g;
    const matches = content.match(anchorPattern);
    
    if (matches && matches.length > 0) {
      content = content.replace(anchorPattern, `href="${relativeIndexPath}$1"`);
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`✅ Fixed ${matches.length} anchor link(s) in: ${relativePath}`);
      return true;
    } else {
      console.log(`⏭️  No anchor links to fix in: ${relativePath}`);
      return false;
    }
  } catch (error) {
    console.error(`❌ Error processing ${filePath}:`, error.message);
    return false;
  }
}

function findHtmlFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      if (!['node_modules', '.git', 'evidence', 'archive', 'tools', 'docs', '.claude', '.clinerules'].includes(file)) {
        findHtmlFiles(filePath, fileList);
      }
    } else if (file.endsWith('.html')) {
      fileList.push(filePath);
    }
  });
  
  return fileList;
}

function main() {
  console.log('🔧 Fixing anchor links to index.html...\n');
  
  const publicDir = path.join(__dirname, '../../public');
  const htmlFiles = findHtmlFiles(publicDir);
  
  let fixedCount = 0;
  htmlFiles.forEach(file => {
    if (fixAnchorLinksInFile(file)) {
      fixedCount++;
    }
  });
  
  console.log(`\n✨ Complete! Fixed anchor links in ${fixedCount} file(s)`);
}

main();
