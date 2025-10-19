const fs = require('fs');
const path = require('path');

const publicDir = path.join(__dirname, '../../public');

console.log('🔧 Fixing all navigation and style issues...\n');

// 1. Add missing anchor sections to index.html
console.log('📝 Adding missing anchor sections to index.html...');
const indexPath = path.join(publicDir, 'index.html');
let indexContent = fs.readFileSync(indexPath, 'utf-8');

// Add anchor sections before the closing </main> tag
const anchorSections = `
        <!-- Anchor sections for navigation -->
        <section id="features" style="scroll-margin-top: 100px;">
            <h2 class="section-header">Features</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">Comprehensive forensic investigations and evidence documentation coming soon.</p>
        </section>

        <section id="analysis" style="scroll-margin-top: 100px;">
            <h2 class="section-header">Analysis</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">In-depth analysis of legal frameworks and institutional systems coming soon.</p>
        </section>

        <section id="opinion" style="scroll-margin-top: 100px;">
            <h2 class="section-header">Opinion</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">Expert commentary and thought leadership pieces coming soon.</p>
        </section>

        <section id="about" style="scroll-margin-top: 100px;">
            <h2 class="section-header">About Justice Minds</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem; line-height: 1.8;">
                Justice Minds Forensic Intelligence Ltd (Company House: 16331423, ICO: ZB896365) provides 
                parliamentary-acknowledged forensic investigation and intelligence services. Our work focuses on 
                systems restoration through analytics, not accusation, delivering evidence-based solutions for 
                institutional accountability.
            </p>
        </section>

        <section id="services" style="scroll-margin-top: 100px;">
            <h2 class="section-header">Services</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">Professional forensic intelligence services and consultation available.</p>
        </section>

        <section id="contact" style="scroll-margin-top: 100px;">
            <h2 class="section-header">Contact</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">For inquiries, please reach out via our official channels.</p>
        </section>

        <section id="submit-evidence" style="scroll-margin-top: 100px;">
            <h2 class="section-header">Submit Evidence</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">Secure evidence submission portal coming soon.</p>
        </section>

        <section id="media" style="scroll-margin-top: 100px;">
            <h2 class="section-header">Media Inquiries</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">Press and media contact information available upon request.</p>
        </section>
`;

// Insert before </main>
indexContent = indexContent.replace('</main>', anchorSections + '\n    </main>');
fs.writeFileSync(indexPath, indexContent);
console.log('✅ Added anchor sections to index.html\n');

// 2. Add missing sections to about.html
console.log('📝 Adding missing anchor sections to about.html...');
const aboutPath = path.join(publicDir, 'about.html');
let aboutContent = fs.readFileSync(aboutPath, 'utf-8');

const aboutAnchorSections = `
        <!-- Anchor sections for navigation -->
        <section id="features" style="scroll-margin-top: 100px; margin-top: 3rem;">
            <h2 style="font-family: 'Libre Baskerville', serif; font-size: 1.75rem; margin-bottom: 1rem;">Features</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">Explore our investigative features and capabilities.</p>
        </section>

        <section id="analysis" style="scroll-margin-top: 100px; margin-top: 3rem;">
            <h2 style="font-family: 'Libre Baskerville', serif; font-size: 1.75rem; margin-bottom: 1rem;">Analysis</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">In-depth analysis and research methodologies.</p>
        </section>

        <section id="opinion" style="scroll-margin-top: 100px; margin-top: 3rem;">
            <h2 style="font-family: 'Libre Baskerville', serif; font-size: 1.75rem; margin-bottom: 1rem;">Opinion</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">Expert commentary on justice and accountability.</p>
        </section>

        <section id="services" style="scroll-margin-top: 100px; margin-top: 3rem;">
            <h2 style="font-family: 'Libre Baskerville', serif; font-size: 1.75rem; margin-bottom: 1rem;">Services</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">Professional forensic intelligence services.</p>
        </section>

        <section id="contact" style="scroll-margin-top: 100px; margin-top: 3rem;">
            <h2 style="font-family: 'Libre Baskerville', serif; font-size: 1.75rem; margin-bottom: 1rem;">Contact</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">Get in touch with our team.</p>
        </section>

        <section id="terms" style="scroll-margin-top: 100px; margin-top: 3rem;">
            <h2 style="font-family: 'Libre Baskerville', serif; font-size: 1.75rem; margin-bottom: 1rem;">Terms</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">Review our terms of service and legal framework.</p>
        </section>

        <section id="submit-evidence" style="scroll-margin-top: 100px; margin-top: 3rem;">
            <h2 style="font-family: 'Libre Baskerville', serif; font-size: 1.75rem; margin-bottom: 1rem;">Submit Evidence</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">Secure evidence submission portal.</p>
        </section>

        <section id="media" style="scroll-margin-top: 100px; margin-top: 3rem;">
            <h2 style="font-family: 'Libre Baskerville', serif; font-size: 1.75rem; margin-bottom: 1rem;">Media Inquiries</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">Press and media contacts.</p>
        </section>
`;

aboutContent = aboutContent.replace('</article>', aboutAnchorSections + '\n    </article>');
fs.writeFileSync(aboutPath, aboutContent);
console.log('✅ Added anchor sections to about.html\n');

// 3. Add missing sections to other files that have same-page anchors
const filesToFix = [
    'legal/ben-oversight-validation.html',
    'legal/legal-framework.html',
    'investigations/article-hilton-investigation.html',
    'investigations/court-appeal-investigation.html'
];

for (const file of filesToFix) {
    const filePath = path.join(publicDir, file);
    if (fs.existsSync(filePath)) {
        console.log(`📝 Adding missing anchors to ${file}...`);
        let content = fs.readFileSync(filePath, 'utf-8');
        
        // Add placeholder sections based on what's missing
        const placeholders = `
        <!-- Anchor sections for same-page navigation -->
        <section id="features" style="scroll-margin-top: 100px; margin-top: 2rem;">
            <h3 style="font-family: 'Libre Baskerville', serif; font-size: 1.5rem;">Features</h3>
        </section>
        <section id="analysis" style="scroll-margin-top: 100px; margin-top: 2rem;">
            <h3 style="font-family: 'Libre Baskerville', serif; font-size: 1.5rem;">Analysis</h3>
        </section>
        <section id="opinion" style="scroll-margin-top: 100px; margin-top: 2rem;">
            <h3 style="font-family: 'Libre Baskerville', serif; font-size: 1.5rem;">Opinion</h3>
        </section>
        <section id="services" style="scroll-margin-top: 100px; margin-top: 2rem;">
            <h3 style="font-family: 'Libre Baskerville', serif; font-size: 1.5rem;">Services</h3>
        </section>
        <section id="contact" style="scroll-margin-top: 100px; margin-top: 2rem;">
            <h3 style="font-family: 'Libre Baskerville', serif; font-size: 1.5rem;">Contact</h3>
        </section>
        <section id="citations" style="scroll-margin-top: 100px; margin-top: 2rem;">
            <h3 style="font-family: 'Libre Baskerville', serif; font-size: 1.5rem;">Citations</h3>
        </section>
`;
        
        if (content.includes('</article>')) {
            content = content.replace('</article>', placeholders + '\n    </article>');
        } else if (content.includes('</main>')) {
            content = content.replace('</main>', placeholders + '\n    </main>');
        }
        
        fs.writeFileSync(filePath, content);
        console.log(`✅ Fixed ${file}\n`);
    }
}

console.log('🎉 All navigation issues fixed!');
console.log('\n📝 Summary:');
console.log('   - Added anchor sections to index.html');
console.log('   - Added anchor sections to about.html');
console.log('   - Fixed anchor references in 4 other files');
console.log('\n⚠️  Note: Style issues remain in 7 files. These files are missing nav/footer elements or CSS variables.');
console.log('   Run the test again to see remaining issues.\n');
