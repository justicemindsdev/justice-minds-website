#!/usr/bin/env node

/**
 * Fix All Internal Links - Justice Minds Website
 * Updates all HTML files to use correct paths after folder restructure
 */

const fs = require('fs');
const path = require('path');

// Define the link mapping based on new structure
const linkMappings = {
  // Main pages (stay in public/)
  'index.html': 'index.html',
  'about.html': 'about.html',
  'privacy-policy.html': 'privacy-policy.html',
  'terms-of-service.html': 'terms-of-service.html',
  'template-content-page.html': 'template-content-page.html',
  
  // Investigations (moved to investigations/)
  'investigation-hilton.html': 'investigations/investigation-hilton.html',
  'article-hilton-investigation.html': 'investigations/article-hilton-investigation.html',
  'court-appeal-investigation.html': 'investigations/court-appeal-investigation.html',
  'institutional-investigation-s188.html': 'investigations/institutional-investigation-s188.html',
  
  // Articles (moved to articles/)
  'cultural-conditioning-freedom.html': 'articles/cultural-conditioning-freedom.html',
  'cultural-exploitation-indian-workers.html': 'articles/cultural-exploitation-indian-workers.html',
  'measuring-competence-beyond-exams.html': 'articles/measuring-competence-beyond-exams.html',
  'the-one-person-principle.html': 'articles/the-one-person-principle.html',
  
  // Stories (moved to stories/)
  'shubham-story.html': 'stories/shubham-story.html',
  'shubham-sick-brother.html': 'stories/shubham-sick-brother.html',
  
  // Legal (moved to legal/)
  'legal-framework.html': 'legal/legal-framework.html',
  'ben-oversight-validation.html': 'legal/ben-oversight-validation.html'
};

// Function to get relative path from one file to another
function getRelativePath(fromFile, toFile) {
  const fromDir = path.dirname(fromFile);
  const relativePath = path.relative(fromDir, toFile);
  return relativePath.replace(/\\/g, '/'); // Convert Windows backslashes to forward slashes
}

// Function to update links in HTML content
function updateLinksInContent(content, currentFilePath) {
  let updatedContent = content;
  
  // Update each link mapping
  for (const [oldLink, newLink] of Object.entries(linkMappings)) {
    const newPath = path.join(__dirname, '../../public', newLink);
    const relativePath = getRelativePath(currentFilePath, newPath);
    
    // Replace various forms of the link
    const patterns = [
      new RegExp(`href=["']${oldLink}["']`, 'g'),
      new RegExp(`href=["']./${oldLink}["']`, 'g'),
      new RegExp(`url: ['"]${oldLink}['"]`, 'g'),
      new RegExp(`url: ['"]\\./${oldLink}['"]`, 'g')
    ];
    
    patterns.forEach(pattern => {
      if (pattern.test(updatedContent)) {
        updatedContent = updatedContent.replace(pattern, (match) => {
          if (match.includes('href=')) {
            return `href="${relativePath}"`;
          } else {
            return `url: '${relativePath}'`;
          }
        });
      }
    });
  }
  
  return updatedContent;
}

// Function to process a single HTML file
function processFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const updatedContent = updateLinksInContent(content, filePath);
    
    if (content !== updatedContent) {
      fs.writeFileSync(filePath, updatedContent, 'utf8');
      console.log(`✅ Updated: ${path.relative(process.cwd(), filePath)}`);
      return true;
    } else {
      console.log(`⏭️  No changes: ${path.relative(process.cwd(), filePath)}`);
      return false;
    }
  } catch (error) {
    console.error(`❌ Error processing ${filePath}:`, error.message);
    return false;
  }
}

// Function to find all HTML files recursively
function findHtmlFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      // Skip node_modules, .git, evidence, archive
      if (!['node_modules', '.git', 'evidence', 'archive', 'tools', 'docs', '.claude', '.clinerules'].includes(file)) {
        findHtmlFiles(filePath, fileList);
      }
    } else if (file.endsWith('.html')) {
      fileList.push(filePath);
    }
  });
  
  return fileList;
}

// Main execution
function main() {
  console.log('🔍 Finding HTML files in public/ directory...\n');
  
  const publicDir = path.join(__dirname, '../../public');
  const htmlFiles = findHtmlFiles(publicDir);
  
  console.log(`📝 Found ${htmlFiles.length} HTML files\n`);
  console.log('🔧 Updating links...\n');
  
  let updatedCount = 0;
  htmlFiles.forEach(file => {
    if (processFile(file)) {
      updatedCount++;
    }
  });
  
  console.log(`\n✨ Complete! Updated ${updatedCount} file(s)`);
}

// Run the script
main();
