#!/usr/bin/env python3
"""
Create Master Contact List with AI-Powered Analysis
Extracts ALL unique emails from ALL sources, then enriches with metrics
"""

import csv
import re
from collections import defaultdict
from datetime import datetime

def extract_organization_from_domain(domain):
    """AI: Extract clean organization name from email domain"""
    if not domain:
        return "Unknown"
    
    domain_lower = domain.lower()
    
    # Known government domains
    gov_domains = {
        'parliament.uk': 'UK Parliament',
        'homeoffice.gov.uk': 'Home Office',
        'justice.gov.uk': 'Ministry of Justice',
        'hmcts.gov.uk': 'HM Courts & Tribunals Service',
        'cps.gov.uk': 'Crown Prosecution Service',
        'sfo.gov.uk': 'Serious Fraud Office',
        'ico.org.uk': 'Information Commissioner\'s Office',
        'judiciary.uk': 'The Judiciary',
        'dwp.gov.uk': 'Department for Work and Pensions',
        'hmrc.gov.uk': 'HM Revenue & Customs',
        'nhs.uk': 'National Health Service',
        'nhs.net': 'NHS',
        'liverpool.gov.uk': 'Liverpool City Council',
        'westminster.gov.uk': 'Westminster City Council',
    }
    
    # Exact match
    if domain_lower in gov_domains:
        return gov_domains[domain_lower]
    
    # Partial match
    for known, name in gov_domains.items():
        if domain_lower.endswith(known):
            return name
    
    # Police
    if 'police' in domain_lower:
        parts = domain_lower.split('.')
        if 'merseyside' in domain_lower:
            return "Merseyside Police"
        elif 'sussex' in domain_lower:
            return "Sussex Police"
        elif len(parts) > 2:
            return f"{parts[0].replace('-', ' ').title()} Police"
        return "UK Police Force"
    
    # Academic
    if domain_lower.endswith('.ac.uk') or 'law.ac.uk' in domain_lower:
        if 'law.ac.uk' in domain_lower:
            return "University of Law"
        parts = domain_lower.split('.')
        if len(parts) >= 3:
            return f"{parts[0].upper()} University"
    
    # Schools
    if '.sch.uk' in domain_lower:
        parts = domain_lower.split('.')
        if len(parts) >= 3:
            return f"{parts[0].replace('-', ' ').title()} School"
    
    # Known organizations
    known_orgs = {
        'alderhey.nhs.uk': 'Alder Hey Children\'s Hospital',
        'maryseacolehouse.com': 'Mary Seacole House',
        'healthwatchliverpool.co.uk': 'Healthwatch Liverpool',
        'healthwatchcentralwestlondon.org': 'Healthwatch Central West London',
        'torus.co.uk': 'Torus Housing',
        'liverpoolmh.co.uk': 'Liverpool Mutual Homes',
        'advocacyproject.org.uk': 'The Advocacy Project',
        'listeningplace.org.uk': 'The Listening Place',
        'pohwer.net': 'Pohwer',
        'hestia.org': 'Hestia',
        'westminstercab.org.uk': 'Westminster Citizens Advice Bureau',
        'survivorsuk.org': 'Survivors UK',
        'merseycare.nhs.uk': 'Merseycare NHS Foundation Trust',
        'westlondon.nhs.uk': 'West London NHS Trust',
        'benmaklondon.com': 'Justice Minds',
        'attorneysyndicate.com': 'Attorney Syndicate',
        'mailtrack.io': 'Mailtrack',
        'bbc.co.uk': 'BBC',
    }
    
    for domain_key, org_name in known_orgs.items():
        if domain_key in domain_lower:
            return org_name
    
    # Clean domain name
    clean = domain_lower.replace('.co.uk', '').replace('.com', '').replace('.org', '').replace('.gov.uk', '').replace('.nhs.uk', '').replace('.nhs.net', '')
    clean = clean.replace('www.', '').replace('-', ' ').replace('_', ' ').title()
    
    return clean if clean else domain

def detect_role_from_email(email, institute):
    """AI: Detect role from email domain and institute"""
    email_lower = email.lower()
    institute_lower = institute.lower() if institute else ''
    
    # Parliament
    if 'parliament.uk' in email_lower:
        return 'MP (Member of Parliament)'
    
    # Government
    if '.gov.uk' in email_lower:
        if 'homeoffice' in email_lower:
            return 'Home Office Official'
        elif 'justice' in email_lower or 'hmcts' in email_lower:
            return 'Ministry of Justice Official'
        elif 'cps' in email_lower:
            return 'Crown Prosecution Service'
        elif 'liverpool.gov.uk' in email_lower:
            return 'Liverpool Council Official'
        elif 'westminster.gov.uk' in email_lower:
            return 'Westminster Council Official'
        return 'Government Official'
    
    # Judiciary
    if 'judiciary' in email_lower or 'judge' in institute_lower:
        return 'Judge/Judicial Officer'
    
    # Police
    if 'police' in email_lower:
        return 'Police Officer'
    
    # NHS/Healthcare
    if 'nhs' in email_lower or 'health' in institute_lower:
        return 'Healthcare Professional'
    
    # Legal
    if any(term in email_lower or term in institute_lower for term in ['solicitor', 'barrister', 'legal', 'law.ac.uk']):
        return 'Legal Professional'
    
    # Media
    if any(term in email_lower for term in ['bbc', 'guardian', 'telegraph', 'times']):
        return 'Media/Journalist'
    
    # Academic
    if '.ac.uk' in email_lower:
        return 'Academic/Student'
    
    # Advocacy/Support
    if any(term in email_lower or term in institute_lower for term in ['advocacy', 'support', 'advice', 'healthwatch']):
        return 'Advocacy/Support Services'
    
    # Housing
    if 'torus' in email_lower or 'housing' in institute_lower:
        return 'Housing Services'
    
    # Regulatory
    if 'ombudsman' in email_lower or 'ico' in email_lower or 'cqc' in email_lower:
        return 'Regulatory/Oversight'
    
    return 'Other'

def detect_sector(email, role):
    """AI: Classify into sectors"""
    role_lower = role.lower()
    email_lower = email.lower()
    
    if 'mp' in role_lower or 'parliament' in email_lower:
        return 'Parliament'
    if 'government' in role_lower or 'council' in role_lower or '.gov.uk' in email_lower:
        return 'Government/Local Authority'
    if 'judge' in role_lower or 'judicial' in role_lower:
        return 'Judiciary'
    if 'police' in role_lower:
        return 'Law Enforcement'
    if 'legal' in role_lower:
        return 'Legal Sector'
    if 'healthcare' in role_lower or 'nhs' in email_lower:
        return 'Healthcare'
    if 'regulatory' in role_lower or 'oversight' in role_lower:
        return 'Oversight/Regulatory'
    if 'media' in role_lower:
        return 'Media'
    if 'academic' in role_lower or 'student' in role_lower:
        return 'Academic'
    if 'advocacy' in role_lower or 'support' in role_lower:
        return 'Advocacy/Support Services'
    if 'housing' in role_lower:
        return 'Housing'
    
    return 'Other'

def extract_name_from_email(email):
    """AI: Extract name from email address"""
    local = email.split('@')[0]
    name = local.replace('.', ' ').replace('_', ' ').replace('-', ' ')
    return name.title()

def extract_emails_from_string(text):
    """Extract all valid email addresses from text"""
    if not text:
        return []
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    return email_pattern.findall(str(text).lower())

def safe_int(value):
    """Safely convert to int"""
    if not value or value == '':
        return 0
    try:
        if isinstance(value, str) and ':' in value:
            return 0
        return int(float(value))
    except (ValueError, TypeError):
        return 0

def parse_date(date_str):
    """Parse various date formats"""
    if not date_str or date_str == "Not read yet":
        return ""
    
    formats = [
        "%Y/%m/%d %H:%M",
        "%b %d, %Y, %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%b %d, %Y, %H:%M:%S",
        "%b %d,%Y,%H:%M:%S",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d %H:%M")
        except:
            continue
    return date_str

print("=" * 80)
print("MASTER CONTACT DATABASE CREATION - AI-Powered Analysis")
print("=" * 80)

# Step 1: Collect ALL unique emails from ALL sources
print("\n[Step 1] Collecting all unique email addresses...")
all_emails = set()

email_data = defaultdict(lambda: {
    'institutes': set(),
    'names': set(),
    'emails_sent': 0,
    'emails_received': 0,
    'total_emails': 0,
    'files': 0,
    'opens': 0,
    'clicks': 0,
    'first_contact': None,
    'last_contact': None,
    'subjects': []
})

# Read DATA - Sheet1.csv
print("  Reading DATA - Sheet1.csv...")
try:
    with open('DATA - Sheet1.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            email_list = row.get('Email Addresses included', '')
            emails = extract_emails_from_string(email_list)
            all_emails.update(emails)
            
            org = row.get('Organisaton', '') or row.get('Organisation', '')
            name = row.get('Name', '')
            
            for email in emails:
                if org:
                    email_data[email]['institutes'].add(org)
                if name:
                    email_data[email]['names'].add(name)
                
                email_data[email]['total_emails'] += safe_int(row.get('Total Email Count', 0))
                email_data[email]['emails_sent'] += safe_int(row.get('Sent Email Count', 0))
                email_data[email]['emails_received'] += safe_int(row.get('Received Email Count', 0))
                email_data[email]['files'] += safe_int(row.get('File Count', 0))
                
                first = parse_date(row.get('Date of First Email', ''))
                last = parse_date(row.get('Date of Last Interaction', ''))
                if first:
                    if not email_data[email]['first_contact'] or first < email_data[email]['first_contact']:
                        email_data[email]['first_contact'] = first
                if last:
                    if not email_data[email]['last_contact'] or last > email_data[email]['last_contact']:
                        email_data[email]['last_contact'] = last
    print(f"    ✓ Found {len(all_emails)} emails in DATA - Sheet1.csv")
except FileNotFoundError:
    print("    ⚠ File not found, skipping")
except Exception as e:
    print(f"    ⚠ Error: {str(e)}")

# Read mailsuite_tracks_1760668937.csv
print("  Reading mailsuite_tracks_1760668937.csv...")
try:
    with open('mailsuite_tracks_1760668937.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            recipient = row.get('Recipient', '')
            emails = extract_emails_from_string(recipient)
            all_emails.update(emails)
            
            for email in emails:
                email_data[email]['opens'] += safe_int(row.get('Opens', 0))
                email_data[email]['clicks'] += safe_int(row.get('Clicks', 0))
                email_data[email]['files'] += safe_int(row.get('PDF views', 0))
                
                subject = row.get('Subject', '')
                if subject and subject not in email_data[email]['subjects']:
                    email_data[email]['subjects'].append(subject)
                
                date = parse_date(row.get('Sent', ''))
                if date:
                    if not email_data[email]['first_contact'] or date < email_data[email]['first_contact']:
                        email_data[email]['first_contact'] = date
                    if not email_data[email]['last_contact'] or date > email_data[email]['last_contact']:
                        email_data[email]['last_contact'] = date
    print(f"    ✓ Found {len(all_emails)} emails total")
except FileNotFoundError:
    print("    ⚠ File not found, skipping")
except Exception as e:
    print(f"    ⚠ Error: {str(e)}")

# Read CONSULT_MAILSUITE.csv
print("  Reading CONSULT_MAILSUITE.csv...")
try:
    with open('CONSULT_MAILSUITE.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            recipient = row.get('Recipient', '')
            emails = extract_emails_from_string(recipient)
            all_emails.update(emails)
            
            for email in emails:
                email_data[email]['opens'] += safe_int(row.get('Opens', 0))
                email_data[email]['clicks'] += safe_int(row.get('Clicks', 0))
                email_data[email]['files'] += safe_int(row.get('PDF views', 0))
                
                subject = row.get('Subject', '')
                if subject and subject not in email_data[email]['subjects']:
                    email_data[email]['subjects'].append(subject)
    print(f"    ✓ Found {len(all_emails)} emails total")
except FileNotFoundError:
    print("    ⚠ File not found, skipping")
except Exception as e:
    print(f"    ⚠ Error: {str(e)}")

print(f"\n  📧 Total unique email addresses found: {len(all_emails)}")

# Step 2: Enrich each email with AI-powered analysis
print("\n[Step 2] Enriching contacts with AI-powered analysis...")

master_contacts = []
for email in sorted(all_emails):
    domain = email.split('@')[1] if '@' in email else ''
    data = email_data[email]
    
    # Extract or infer organization
    if data['institutes']:
        institute = '; '.join(sorted(data['institutes']))
    else:
        institute = extract_organization_from_domain(domain)
    
    # Extract or infer name
    if data['names']:
        name = '; '.join(sorted(data['names']))
    else:
        name = extract_name_from_email(email)
    
    # Detect role and sector
    role = detect_role_from_email(email, institute)
    sector = detect_sector(email, role)
    
    # Calculate engagement rate
    total_interactions = data['opens'] + data['clicks']
    engagement_rate = 0
    if data['total_emails'] > 0:
        engagement_rate = round((total_interactions / data['total_emails']) * 100, 1)
    
    # Compile subjects
    subjects = '; '.join(data['subjects'][:5]) if data['subjects'] else ''
    
    master_contacts.append({
        'EMAIL': email,
        'NAME': name,
        'INSTITUTE': institute,
        'ROLE': role,
        'SECTOR': sector,
        'DOMAIN': domain,
        'FIRST_CONTACT': data['first_contact'] or '',
        'LAST_CONTACT': data['last_contact'] or '',
        'TOTAL_EMAILS': data['total_emails'],
        'EMAILS_SENT': data['emails_sent'],
        'EMAILS_RECEIVED': data['emails_received'],
        'FILES': data['files'],
        'OPENS': data['opens'],
        'CLICKS': data['clicks'],
        'ENGAGEMENT_RATE': engagement_rate,
        'SUBJECTS': subjects
    })

print(f"  ✅ Enriched {len(master_contacts)} contacts")

# Step 3: Write to CSV
print("\n[Step 3] Writing to MASTER-CONTACTS-DATABASE.csv...")

output_file = 'MASTER-CONTACTS-DATABASE.csv'
fieldnames = [
    'EMAIL', 'NAME', 'INSTITUTE', 'ROLE', 'SECTOR', 'DOMAIN',
    'FIRST_CONTACT', 'LAST_CONTACT', 'TOTAL_EMAILS', 'EMAILS_SENT', 'EMAILS_RECEIVED',
    'FILES', 'OPENS', 'CLICKS', 'ENGAGEMENT_RATE', 'SUBJECTS'
]

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(master_contacts)

print(f"\n" + "=" * 80)
print(f"✅ SUCCESS! Created {output_file}")
print(f"✅ Total unique contacts: {len(master_contacts)}")
print("=" * 80)

# Step 4: Create summary by institute
print("\n[Step 4] Creating institute summary...")

institute_summary = defaultdict(lambda: {
    'contacts': 0,
    'total_emails': 0,
    'sector': set()
})

for contact in master_contacts:
    institute = contact['INSTITUTE']
    institute_summary[institute]['contacts'] += 1
    institute_summary[institute]['total_emails'] += contact['TOTAL_EMAILS']
    institute_summary[institute]['sector'].add(contact['SECTOR'])

# Write institute summary
summary_output = 'MASTER-INSTITUTES-SUMMARY.csv'
with open(summary_output, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['INSTITUTE', 'TOTAL_CONTACTS', 'TOTAL_EMAILS', 'SECTORS'])
    
    for institute in sorted(institute_summary.keys()):
        data = institute_summary[institute]
        sectors = '; '.join(sorted(data['sector']))
        writer.writerow([
            institute,
            data['contacts'],
            data['total_emails'],
            sectors
        ])

print(f"✅ Created {summary_output}")
print(f"✅ Total unique institutes: {len(institute_summary)}")
print("=" * 80)
