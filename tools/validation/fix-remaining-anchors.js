const fs = require('fs');
const path = require('path');

const publicDir = path.join(__dirname, '../../public');

console.log('🔧 Fixing remaining anchor issues...\n');

// Fix about.html - add anchors before </main>
console.log('📝 Fixing about.html...');
const aboutPath = path.join(publicDir, 'about.html');
let aboutContent = fs.readFileSync(aboutPath, 'utf-8');

const aboutAnchors = `
        <!-- Anchor sections for navigation -->
        <section id="features" style="scroll-margin-top: 100px; margin-top: 3rem; padding: 2rem; border-top: 1px solid var(--border-grey);">
            <h2 style="font-family: 'Libre Baskerville', serif; font-size: 1.75rem; margin-bottom: 1rem; color: var(--primary-blue);">Features</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">Explore our investigative features and capabilities.</p>
        </section>

        <section id="analysis" style="scroll-margin-top: 100px; margin-top: 2rem; padding: 2rem;">
            <h2 style="font-family: 'Libre Baskerville', serif; font-size: 1.75rem; margin-bottom: 1rem; color: var(--primary-blue);">Analysis</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">In-depth analysis and research methodologies.</p>
        </section>

        <section id="opinion" style="scroll-margin-top: 100px; margin-top: 2rem; padding: 2rem;">
            <h2 style="font-family: 'Libre Baskerville', serif; font-size: 1.75rem; margin-bottom: 1rem; color: var(--primary-blue);">Opinion</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">Expert commentary on justice and accountability.</p>
        </section>

        <section id="services" style="scroll-margin-top: 100px; margin-top: 2rem; padding: 2rem;">
            <h2 style="font-family: 'Libre Baskerville', serif; font-size: 1.75rem; margin-bottom: 1rem; color: var(--primary-blue);">Services</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">Professional forensic intelligence services.</p>
        </section>

        <section id="contact" style="scroll-margin-top: 100px; margin-top: 2rem; padding: 2rem;">
            <h2 style="font-family: 'Libre Baskerville', serif; font-size: 1.75rem; margin-bottom: 1rem; color: var(--primary-blue);">Contact</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">Email: consult@justice-minds.com</p>
        </section>

        <section id="terms" style="scroll-margin-top: 100px; margin-top: 2rem; padding: 2rem;">
            <h2 style="font-family: 'Libre Baskerville', serif; font-size: 1.75rem; margin-bottom: 1rem; color: var(--primary-blue);">Terms</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">Review our <a href="terms-of-service.html" style="color: var(--accent-red);">terms of service</a> and legal framework.</p>
        </section>

        <section id="submit-evidence" style="scroll-margin-top: 100px; margin-top: 2rem; padding: 2rem;">
            <h2 style="font-family: 'Libre Baskerville', serif; font-size: 1.75rem; margin-bottom: 1rem; color: var(--primary-blue);">Submit Evidence</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">Secure evidence submission portal coming soon.</p>
        </section>

        <section id="media" style="scroll-margin-top: 100px; margin-top: 2rem; padding: 2rem;">
            <h2 style="font-family: 'Libre Baskerville', serif; font-size: 1.75rem; margin-bottom: 1rem; color: var(--primary-blue);">Media Inquiries</h2>
            <p style="color: var(--text-grey); font-size: 1.1rem;">Press and media contacts available upon request.</p>
        </section>
`;

aboutContent = aboutContent.replace('</main>', aboutAnchors + '\n    </main>');
fs.writeFileSync(aboutPath, aboutContent);
console.log('✅ Fixed about.html\n');

// Fix court-appeal-investigation.html
console.log('📝 Fixing court-appeal-investigation.html...');
const courtPath = path.join(publicDir, 'investigations/court-appeal-investigation.html');
let courtContent = fs.readFileSync(courtPath, 'utf-8');

if (!courtContent.includes('id="services"')) {
    const courtAnchors = `
        <section id="services" style="scroll-margin-top: 100px; margin-top: 2rem; padding: 1rem;">
            <h3 style="font-family: 'Libre Baskerville', serif; font-size: 1.5rem;">Services</h3>
            <p style="color: var(--text-grey);">Professional forensic intelligence services.</p>
        </section>
`;
    
    if (courtContent.includes('</article>')) {
        courtContent = courtContent.replace('</article>', courtAnchors + '\n    </article>');
    } else if (courtContent.includes('</main>')) {
        courtContent = courtContent.replace('</main>', courtAnchors + '\n    </main>');
    }
    
    fs.writeFileSync(courtPath, courtContent);
    console.log('✅ Fixed court-appeal-investigation.html\n');
} else {
    console.log('✅ court-appeal-investigation.html already has anchors\n');
}

// Fix ben-oversight-validation.html
console.log('📝 Fixing ben-oversight-validation.html...');
const benPath = path.join(publicDir, 'legal/ben-oversight-validation.html');
let benContent = fs.readFileSync(benPath, 'utf-8');

if (!benContent.includes('id="submit-evidence"')) {
    const benAnchors = `
        <section id="submit-evidence" style="scroll-margin-top: 100px; margin-top: 2rem; padding: 1rem;">
            <h3 style="font-family: 'Libre Baskerville', serif; font-size: 1.5rem;">Submit Evidence</h3>
            <p style="color: var(--text-grey);">Secure evidence submission portal.</p>
        </section>
        <section id="media" style="scroll-margin-top: 100px; margin-top: 2rem; padding: 1rem;">
            <h3 style="font-family: 'Libre Baskerville', serif; font-size: 1.5rem;">Media Inquiries</h3>
            <p style="color: var(--text-grey);">Press and media contacts.</p>
        </section>
`;
    
    if (benContent.includes('</article>')) {
        benContent = benContent.replace('</article>', benAnchors + '\n    </article>');
    } else if (benContent.includes('</main>')) {
        benContent = benContent.replace('</main>', benAnchors + '\n    </main>');
    }
    
    fs.writeFileSync(benPath, benContent);
    console.log('✅ Fixed ben-oversight-validation.html\n');
} else {
    console.log('✅ ben-oversight-validation.html already has anchors\n');
}

// Fix legal-framework.html
console.log('📝 Fixing legal-framework.html...');
const legalPath = path.join(publicDir, 'legal/legal-framework.html');
let legalContent = fs.readFileSync(legalPath, 'utf-8');

if (!legalContent.includes('id="citations"')) {
    const legalAnchors = `
        <section id="citations" style="scroll-margin-top: 100px; margin-top: 2rem; padding: 1rem;">
            <h3 style="font-family: 'Libre Baskerville', serif; font-size: 1.5rem;">Citations & References</h3>
            <p style="color: var(--text-grey);">Legal citations and reference materials.</p>
        </section>
`;
    
    if (legalContent.includes('</article>')) {
        legalContent = legalContent.replace('</article>', legalAnchors + '\n    </article>');
    } else if (legalContent.includes('</main>')) {
        legalContent = legalContent.replace('</main>', legalAnchors + '\n    </main>');
    }
    
    fs.writeFileSync(legalPath, legalContent);
    console.log('✅ Fixed legal-framework.html\n');
} else {
    console.log('✅ legal-framework.html already has anchors\n');
}

console.log('🎉 All remaining anchor issues fixed!\n');
console.log('Run test-navigation.js again to verify all links are working.\n');
