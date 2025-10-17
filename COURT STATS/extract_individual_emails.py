#!/usr/bin/env python3
"""
Extract individual email records from all CSV data sources
Creates a comprehensive listing with columns:
INSTITTUE | NAME | EMAIL | ROLE | NAME_EXTRACTED | SECTOR | FIRST CONTACT | 
LAST CONTACT | SUBJECT | TOTAL ALL | SENT | RECIEVED | FILES SENT | 
FILES RECIEVED | ALL FILES | OPENS | CLICKS | DATE
"""

import csv
import re
from collections import defaultdict
from datetime import datetime

def extract_organization_from_domain(domain):
    """Extract clean organization name from email domain using AI pattern matching"""
    if not domain:
        return domain
    
    domain_lower = domain.lower()
    
    # Known government domains mapping
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
        'fco.gov.uk': 'Foreign Office',
        'mod.gov.uk': 'Ministry of Defence',
        'nhs.uk': 'National Health Service',
        'nhs.net': 'NHS',
        'nhsbt.nhs.uk': 'NHS Blood and Transplant',
    }
    
    # Check exact matches first
    if domain_lower in gov_domains:
        return gov_domains[domain_lower]
    
    # Check if domain ends with known government domains
    for known_domain, org_name in gov_domains.items():
        if domain_lower.endswith(known_domain):
            return org_name
    
    # Extract subdomain patterns for police forces
    if 'police.uk' in domain_lower or 'pnn.police.uk' in domain_lower:
        parts = domain_lower.split('.')
        if len(parts) > 2:
            force_name = parts[0].replace('-', ' ').title()
            return f"{force_name} Police"
        return "UK Police Force"
    
    # Academic institutions
    if domain_lower.endswith('.ac.uk'):
        parts = domain_lower.split('.')
        if len(parts) >= 3:
            uni_name = parts[0].replace('-', ' ').upper()
            return f"{uni_name} University"
    
    # Clean up common domain patterns
    domain_clean = domain_lower
    # Remove common TLDs
    domain_clean = domain_clean.replace('.co.uk', '').replace('.com', '').replace('.org.uk', '').replace('.org', '').replace('.gov.uk', '')
    # Remove www
    domain_clean = domain_clean.replace('www.', '')
    # Replace hyphens and underscores with spaces
    domain_clean = domain_clean.replace('-', ' ').replace('_', ' ')
    # Title case
    domain_clean = domain_clean.title()
    
    return domain_clean if domain_clean else domain

def detect_role_from_email(email, institute):
    """AI-powered role detection based on email domain and institute patterns"""
    email_lower = email.lower()
    institute_lower = institute.lower() if institute else ''
    
    # Extract domain for analysis
    domain = email.split('@')[1] if '@' in email else ''
    domain_lower = domain.lower()
    
    # Parliament - very specific detection
    if 'parliament.uk' in domain_lower:
        return 'MP (Member of Parliament)'
    
    # Government ministers and officials
    if '.gov.uk' in domain_lower:
        # Specific ministries
        if 'homeoffice' in domain_lower:
            return 'Home Office Official'
        elif 'justice' in domain_lower or 'moj' in domain_lower:
            return 'Ministry of Justice Official'
        elif 'hmcts' in domain_lower:
            return 'HMCTS Official'
        elif 'cps' in domain_lower:
            return 'Crown Prosecution Service'
        elif 'dwp' in domain_lower:
            return 'DWP Official'
        elif 'hmrc' in domain_lower:
            return 'HMRC Official'
        else:
            return 'Government Official'
    
    # Judiciary
    if 'judiciary' in domain_lower or ('judge' in institute_lower):
        if 'lord' in institute_lower or 'lady' in institute_lower:
            return 'Senior Judge'
        return 'Judge/Judicial Officer'
    
    # Legal tribunals and courts
    if any(term in domain_lower or term in institute_lower for term in ['tribunal', 'court']):
        return 'Legal/Court Official'
    
    # Police forces
    if 'police' in domain_lower or 'pnn.police.uk' in domain_lower:
        if 'chief' in institute_lower or 'commissioner' in institute_lower:
            return 'Senior Police Officer'
        return 'Police Officer'
    
    # Healthcare
    if 'nhs' in domain_lower or 'health' in domain_lower:
        if 'doctor' in institute_lower or 'dr' in institute_lower:
            return 'Medical Professional'
        return 'Healthcare Professional'
    
    # Legal professionals
    if any(term in domain_lower or term in institute_lower for term in ['solicitor', 'barrister', 'legal', 'law']):
        return 'Legal Professional'
    
    # Regulatory and oversight
    if any(term in domain_lower or term in institute_lower for term in ['ombudsman', 'ico', 'regulator']):
        return 'Regulatory/Oversight'
    
    # Media
    if any(term in domain_lower for term in ['bbc.co.uk', 'bbc.com', 'guardian', 'telegraph', 'times', 'itv', 'channel4', 'sky']):
        return 'Media/Journalist'
    
    # Academic
    if '.ac.uk' in domain_lower:
        if 'professor' in institute_lower or 'prof' in institute_lower or 'dr' in institute_lower:
            return 'Academic (Professor/Researcher)'
        return 'Academic'
    
    # Private sector based on common domains
    if any(term in domain_lower for term in ['.com', '.co.uk', '.net']) and not any(gov in domain_lower for gov in ['.gov.uk', '.nhs', 'parliament']):
        return 'Private Sector'
    
    return 'Other'

def detect_sector(email, institute, role):
    """Classify into sector categories"""
    email_lower = email.lower()
    institute_lower = institute.lower() if institute else ''
    role_lower = role.lower()
    
    # Parliament/Political
    if 'mp' in role_lower or 'parliament' in email_lower or 'parliament' in institute_lower:
        return 'Parliament'
    
    # Government
    if 'government' in role_lower or '.gov.uk' in email_lower:
        if any(dept in institute_lower for dept in ['home office', 'justice', 'dwp', 'hmrc']):
            return 'Government - Home Office/Justice'
        return 'Government'
    
    # Judiciary
    if 'judge' in role_lower or 'judicial' in role_lower or any(term in institute_lower for term in ['court', 'tribunal', 'judiciary']):
        return 'Judiciary'
    
    # Law Enforcement
    if 'police' in email_lower or 'police' in institute_lower or 'law enforcement' in role_lower:
        return 'Law Enforcement'
    
    # Legal
    if 'legal' in role_lower or any(term in institute_lower for term in ['solicitor', 'barrister', 'law firm']):
        return 'Legal Sector'
    
    # Healthcare
    if 'healthcare' in role_lower or 'nhs' in email_lower or 'nhs' in institute_lower:
        return 'Healthcare'
    
    # Oversight/Regulatory
    if 'ombudsman' in role_lower or 'oversight' in role_lower:
        return 'Oversight/Regulatory'
    
    # Media
    if 'media' in role_lower or 'journalist' in role_lower:
        return 'Media'
    
    # Academic
    if 'academic' in role_lower or '.ac.uk' in email_lower:
        return 'Academic'
    
    return 'Other'

def extract_name_from_text(name_field, email):
    """Extract and normalize names from text"""
    if not name_field or name_field == 'Unknown':
        # Try to extract from email
        local_part = email.split('@')[0]
        # Replace dots and underscores with spaces
        name_guess = local_part.replace('.', ' ').replace('_', ' ').replace('-', ' ')
        # Title case
        return name_guess.title()
    
    # Clean up name field
    name = name_field.strip()
    
    # Remove common prefixes/suffixes
    name = re.sub(r'\b(Mr|Mrs|Ms|Dr|Prof|Sir|Lord|Lady)\b\.?\s*', '', name, flags=re.IGNORECASE)
    
    # Split by pipe if multiple names
    if '|' in name:
        names = [n.strip() for n in name.split('|')]
        # Return first non-empty name
        for n in names:
            if n and n != 'Unknown':
                return n
    
    return name if name else 'Unknown'

def parse_date(date_str):
    """Parse various date formats to a standard format"""
    if not date_str or date_str == "Not read yet":
        return ""
    
    # Try different date formats
    formats = [
        "%Y/%m/%d %H:%M",
        "%b %d, %Y, %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%b %d, %Y, %H:%M:%S",
        "%b %d,%Y,%H:%M:%S",
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d %H:%M")
        except:
            continue
    
    return date_str

def extract_emails_from_list(email_string):
    """Extract individual emails from comma-separated string"""
    if not email_string:
        return []
    
    # Split by comma and clean
    emails = [e.strip() for e in email_string.split(',')]
    # Filter valid emails
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    return [e for e in emails if email_pattern.match(e)]

def process_data_sheet1(filename):
    """Process DATA - Sheet1.csv"""
    records = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            org = row.get('Organisaton', '').strip()
            name = row.get('Name', '').strip()
            sent = row.get('Sent Email Count', '0')
            received = row.get('Received Email Count', '0')
            threads = row.get('Email Thread Count', '0')
            total = row.get('Total Email Count', '0')
            files = row.get('File Count', '0')
            first_date = parse_date(row.get('Date of First Email', ''))
            last_date = parse_date(row.get('Date of Last Interaction', ''))
            email_list = row.get('Email Addresses included', '')
            
            # Extract individual emails
            emails = extract_emails_from_list(email_list)
            
            for email in emails:
                records.append({
                    'INSTITTUE': org or 'Unknown',
                    'NAME': name or 'Unknown',
                    'EMAIL': email,
                    'ROLE': '',
                    'FIRST CONTACT': first_date,
                    'LAST CONTACT': last_date,
                    'SUBJECT': '',
                    'TOTAL ALL': total,
                    'SENT': sent,
                    'RECIEVED': received,
                    'FILES SENT': '',
                    'FILES RECIEVED': '',
                    'ALL FILES': files,
                    'OPENS': '',
                    'CLICKS': '',
                    'DATE': last_date
                })
    
    return records

def process_mailsuite_tracks(filename):
    """Process mailsuite_tracks CSV"""
    records = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            recipient = row.get('Recipient', '').strip()
            subject = row.get('Subject', '').strip()
            last_opened = row.get('Last Opened', '')
            opens = row.get('Opens', '0')
            clicks = row.get('Clicks', '0')
            pdf_views = row.get('PDF views', '0')
            sent_date = row.get('Sent', '')
            
            # Extract individual recipients
            recipients = extract_emails_from_list(recipient)
            
            # Parse date
            sent_parsed = parse_date(sent_date)
            last_opened_parsed = parse_date(last_opened)
            
            for email in recipients:
                records.append({
                    'INSTITTUE': email.split('@')[1] if '@' in email else 'Unknown',
                    'NAME': recipient.split(',')[0] if ',' in recipient else recipient,
                    'EMAIL': email,
                    'ROLE': '',
                    'FIRST CONTACT': sent_parsed,
                    'LAST CONTACT': last_opened_parsed if last_opened_parsed else sent_parsed,
                    'SUBJECT': subject,
                    'TOTAL ALL': '1',
                    'SENT': '1',
                    'RECIEVED': '0',
                    'FILES SENT': pdf_views,
                    'FILES RECIEVED': '0',
                    'ALL FILES': pdf_views,
                    'OPENS': opens,
                    'CLICKS': clicks,
                    'DATE': sent_parsed
                })
    
    return records

def process_consult_mailsuite(filename):
    """Process CONSULT_MAILSUITE CSV"""
    records = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            recipient = row.get('Recipient', '').strip()
            subject = row.get('Subject', '').strip()
            last_opened = row.get('Last Opened', '')
            opens = row.get('Opens', '0')
            clicks = row.get('Clicks', '0')
            pdf_views = row.get('PDF views', '0')
            year = row.get('Year', '')
            time = row.get('Time', '')
            
            # Combine year and time for date
            sent_date = f"{year} {time}" if year and time else ''
            
            # Extract individual recipients
            recipients = extract_emails_from_list(recipient)
            
            # Parse dates
            sent_parsed = parse_date(sent_date)
            last_opened_parsed = parse_date(last_opened)
            
            for email in recipients:
                records.append({
                    'INSTITTUE': email.split('@')[1] if '@' in email else 'Unknown',
                    'NAME': recipient.split(',')[0] if ',' in recipient else recipient,
                    'EMAIL': email,
                    'ROLE': '',
                    'FIRST CONTACT': sent_parsed,
                    'LAST CONTACT': last_opened_parsed if last_opened_parsed else sent_parsed,
                    'SUBJECT': subject,
                    'TOTAL ALL': '1',
                    'SENT': '1',
                    'RECIEVED': '0',
                    'FILES SENT': pdf_views if pdf_views else '0',
                    'FILES RECIEVED': '0',
                    'ALL FILES': pdf_views if pdf_views else '0',
                    'OPENS': opens if opens else '0',
                    'CLICKS': clicks if clicks else '0',
                    'DATE': sent_parsed
                })
    
    return records

def merge_and_deduplicate(records):
    """Merge records by email and aggregate data"""
    email_data = defaultdict(lambda: {
        'INSTITTUE': set(),
        'NAME': set(),
        'ROLE': '',
        'NAME_EXTRACTED': '',
        'SECTOR': '',
        'FIRST CONTACT': None,
        'LAST CONTACT': None,
        'SUBJECT': [],
        'TOTAL ALL': 0,
        'SENT': 0,
        'RECIEVED': 0,
        'FILES SENT': 0,
        'FILES RECIEVED': 0,
        'ALL FILES': 0,
        'OPENS': 0,
        'CLICKS': 0,
        'DATE': None
    })
    
    for record in records:
        email = record['EMAIL']
        data = email_data[email]
        
        # Add institute (filter out "Unknown" if we have a real institute)
        institute = record['INSTITTUE']
        if institute and institute != 'Unknown':
            data['INSTITTUE'].add(institute)
        elif not data['INSTITTUE']:
            # If no institute yet, extract from email domain
            if '@' in email:
                domain = email.split('@')[1]
                data['INSTITTUE'].add(domain)
        
        # Add name (filter out "Unknown" if we have a real name)
        name = record['NAME']
        if name and name != 'Unknown':
            data['NAME'].add(name)
        
        # Track earliest and latest dates
        if record['FIRST CONTACT']:
            if not data['FIRST CONTACT'] or record['FIRST CONTACT'] < data['FIRST CONTACT']:
                data['FIRST CONTACT'] = record['FIRST CONTACT']
        
        if record['LAST CONTACT']:
            if not data['LAST CONTACT'] or record['LAST CONTACT'] > data['LAST CONTACT']:
                data['LAST CONTACT'] = record['LAST CONTACT']
                data['DATE'] = record['LAST CONTACT']
        
        # Add subjects
        if record['SUBJECT']:
            data['SUBJECT'].append(record['SUBJECT'])
        
        # Aggregate counts - handle non-numeric values
        def safe_int(value):
            """Safely convert to int, return 0 for invalid values"""
            if not value or value == '':
                return 0
            try:
                return int(float(value))
            except (ValueError, TypeError):
                return 0
        
        data['TOTAL ALL'] += safe_int(record['TOTAL ALL'])
        data['SENT'] += safe_int(record['SENT'])
        data['RECIEVED'] += safe_int(record['RECIEVED'])
        data['FILES SENT'] += safe_int(record['FILES SENT'])
        data['FILES RECIEVED'] += safe_int(record['FILES RECIEVED'])
        data['ALL FILES'] += safe_int(record['ALL FILES'])
        data['OPENS'] += safe_int(record['OPENS'])
        data['CLICKS'] += safe_int(record['CLICKS'])
    
    # Convert to list of records with AI-powered role and name detection
    result = []
    for email, data in sorted(email_data.items()):
        # Get domain from email
        domain = email.split('@')[1] if '@' in email else 'Unknown'
        
        # Filter out "Unknown" from institutes and get the best one
        institutes = [i for i in data['INSTITTUE'] if i and i != 'Unknown']
        
        # If we have an explicit institute name, use it
        if institutes:
            # Prefer organization names over domains
            institute_raw = institutes[0]
            # Check if it's just a domain or an actual organization name
            if '.' in institute_raw and institute_raw == domain:
                # It's just a domain, extract organization name
                institute = extract_organization_from_domain(domain)
            else:
                # It's an actual organization name
                institute = institute_raw
        else:
            # Extract organization from email domain
            institute = extract_organization_from_domain(domain)
        
        # Filter out "Unknown" from names
        names = [n for n in data['NAME'] if n and n != 'Unknown']
        name_raw = names[0] if names else 'Unknown'
        
        # AI-powered role detection (pass the cleaned institute name)
        role = detect_role_from_email(email, institute)
        
        # Extract and normalize name
        name_extracted = extract_name_from_text(name_raw, email)
        
        # Detect sector
        sector = detect_sector(email, institute, role)
        
        result.append({
            'INSTITTUE': institute,
            'NAME': name_raw,
            'EMAIL': email,
            'ROLE': role,
            'NAME_EXTRACTED': name_extracted,
            'SECTOR': sector,
            'FIRST CONTACT': data['FIRST CONTACT'] or '',
            'LAST CONTACT': data['LAST CONTACT'] or '',
            'SUBJECT': ' | '.join(data['SUBJECT'][:5]) if data['SUBJECT'] else '',  # Limit to 5 subjects
            'TOTAL ALL': str(data['TOTAL ALL']),
            'SENT': str(data['SENT']),
            'RECIEVED': str(data['RECIEVED']),
            'FILES SENT': str(data['FILES SENT']),
            'FILES RECIEVED': str(data['FILES RECIEVED']),
            'ALL FILES': str(data['ALL FILES']),
            'OPENS': str(data['OPENS']),
            'CLICKS': str(data['CLICKS']),
            'DATE': data['DATE'] or ''
        })
    
    return result

def main():
    print("=" * 70)
    print("AI-POWERED EMAIL ANALYTICS - Justice Minds Contact Database")
    print("=" * 70)
    
    print("\n[1/4] Processing DATA - Sheet1.csv...")
    records1 = process_data_sheet1('DATA - Sheet1.csv')
    print(f"  ✓ Extracted {len(records1)} email records")
    
    print("\n[2/4] Processing mailsuite_tracks_1760668937.csv...")
    records2 = process_mailsuite_tracks('mailsuite_tracks_1760668937.csv')
    print(f"  ✓ Extracted {len(records2)} email records")
    
    print("\n[3/4] Processing CONSULT_MAILSUITE.csv...")
    records3 = process_consult_mailsuite('CONSULT_MAILSUITE.csv')
    print(f"  ✓ Extracted {len(records3)} email records")
    
    # Combine all records
    all_records = records1 + records2 + records3
    print(f"\n  📊 Total raw email records: {len(all_records)}")
    
    # Merge and deduplicate with AI analysis
    print("\n[4/4] AI Analysis: Merging, deduplicating, and enriching data...")
    print("  • Extracting organization names from domains")
    print("  • Detecting roles and sectors")
    print("  • Normalizing contact names")
    print("  • Aggregating engagement metrics")
    
    final_records = merge_and_deduplicate(all_records)
    print(f"\n  ✓ Processed {len(final_records)} unique contacts")
    
    # Calculate statistics
    sectors = {}
    roles = {}
    for record in final_records:
        sector = record['SECTOR']
        role = record['ROLE']
        sectors[sector] = sectors.get(sector, 0) + 1
        roles[role] = roles.get(role, 0) + 1
    
    print(f"\n📈 ANALYSIS SUMMARY:")
    print(f"  • Unique Contacts: {len(final_records)}")
    print(f"  • Sectors Identified: {len(sectors)}")
    print(f"  • Roles Classified: {len(roles)}")
    print(f"\n  Top Sectors:")
    for sector, count in sorted(sectors.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"    - {sector}: {count} contacts")
    print(f"\n  Top Roles:")
    for role, count in sorted(roles.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"    - {role}: {count} contacts")
    
    # Write to CSV
    output_file = 'INDIVIDUAL-EMAILS-COMPLETE.csv'
    print(f"\nWriting to {output_file}...")
    
    fieldnames = [
        'INSTITTUE', 'NAME', 'EMAIL', 'ROLE', 'NAME_EXTRACTED', 'SECTOR',
        'FIRST CONTACT', 'LAST CONTACT', 'SUBJECT', 'TOTAL ALL', 'SENT', 'RECIEVED',
        'FILES SENT', 'FILES RECIEVED', 'ALL FILES', 'OPENS', 'CLICKS', 'DATE'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_records)
    
    print(f"\n✓ Successfully created {output_file}")
    print(f"✓ Total unique emails: {len(final_records)}")

if __name__ == '__main__':
    main()
