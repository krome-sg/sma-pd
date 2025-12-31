#!/usr/bin/env python3
import xml.etree.ElementTree as ET

tree = ET.parse('squarespace.xml')
root = tree.getroot()

namespace = {
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'wp': 'http://wordpress.org/export/1.2/'
}

# Categorize pages
categories = {
    'Home': [],
    'Funded Programmes': [],
    'Corporate Training': [],
    'Masterclasses': [],
    'Workshops': [],
    'Forms': [],
    'Other': []
}

for item in root.findall('./channel/item'):
    link_elem = item.find('link')
    title_elem = item.find('title')
    post_type = item.find('{%s}post_type' % namespace['wp'])
    
    if link_elem is not None and title_elem is not None:
        link = link_elem.text or ''
        title = title_elem.text or 'Untitled'
        ptype = post_type.text if post_type is not None else 'page'
        
        if ptype != 'attachment' and link:
            # Escape for Mermaid - replace & with &amp; but keep &amp; as is first
            title_escaped = title.replace('&amp;', '&AMP;').replace('&', '&amp;').replace('&AMP;', '&amp;')
            title_escaped = title_escaped.replace('"', '&quot;')
            
            if link == '/home' or (link.startswith('/home') and link not in ['/homepage-desktop-slider', '/homepage-mobile-slider']):
                categories['Home'].append((link, title_escaped))
            elif link == '/funded-programmes' or link.startswith('/sgus') or link.startswith('/sms') or link.startswith('/bsm') or link.startswith('/ftv') or link.startswith('/ctw') or link.startswith('/rsd') or link.startswith('/nmt') or link.startswith('/apa') or link.startswith('/sfdw-courses') or link.startswith('/sgunited-courses') or any(x in link for x in ['broadcast', 'creative-writing', 'business-management', 'film-tv', 'radio-sound', 'advertising', 'new-media']):
                categories['Funded Programmes'].append((link, title_escaped))
            elif '/corporate' in link.lower():
                categories['Corporate Training'].append((link, title_escaped))
            elif 'masterclass' in link.lower() or link.startswith('/mcs'):
                categories['Masterclasses'].append((link, title_escaped))
            elif link.startswith('/wks') or link == '/workshops-seminars':
                categories['Workshops'].append((link, title_escaped))
            elif '-form' in link or link == '/funding-information' or (link != '/form-template' and link != '/form-template-msg' and 'form' in link.lower()):
                categories['Forms'].append((link, title_escaped))
            else:
                categories['Other'].append((link, title_escaped))

# Generate Mermaid
print('flowchart TD')
print('    Root["SMA Professional Development<br/>pd.mediaacademy.sg<br/>━━━━━━━━━━━━━━━━━━━━<br/>129 Total Pages"]')
print('')
print('    Root --> Home["🏠 Home"]')
print('    Root --> Funded["📚 Funded Programmes"]')
print('    Root --> Corporate["💼 Corporate Training"]')
print('    Root --> Masterclasses["🎓 Masterclasses"]')
print('    Root --> Workshops["📋 Workshops & Seminars"]')
print('    Root --> Forms["📝 Forms & Enquiries"]')
print('    Root --> Other["📄 Other Pages"]')
print('')

# Home pages
for i, (link, title) in enumerate(sorted(categories['Home']), 1):
    node_id = f'Home{i}'
    print(f'    Home --> {node_id}["{title}"]')

# Funded Programmes - organize by subcategory
funded_subs = {
    'WSQ': [],
    'SGUS': [],
    'SFM': [],
    'BSM': [],
    'FTV': [],
    'CTW': [],
    'RSD': [],
    'NMT': [],
    'APA': [],
    'SFDW': [],
    'Main': []
}

for link, title in categories['Funded Programmes']:
    if link == '/funded-programmes':
        funded_subs['Main'].append((link, title))
    elif link.startswith('/sgus') or link.startswith('/sgunited'):
        funded_subs['SGUS'].append((link, title))
    elif link.startswith('/sms'):
        funded_subs['SFM'].append((link, title))
    elif link.startswith('/bsm'):
        funded_subs['BSM'].append((link, title))
    elif link.startswith('/ftv'):
        funded_subs['FTV'].append((link, title))
    elif link.startswith('/ctw'):
        funded_subs['CTW'].append((link, title))
    elif link.startswith('/rsd'):
        funded_subs['RSD'].append((link, title))
    elif link.startswith('/nmt'):
        funded_subs['NMT'].append((link, title))
    elif link.startswith('/apa'):
        funded_subs['APA'].append((link, title))
    elif link.startswith('/sfdw'):
        funded_subs['SFDW'].append((link, title))
    else:
        funded_subs['WSQ'].append((link, title))

print('')
print('    Funded --> FundedMain["Funded Programmes Main"]')
print('    Funded --> WSQCat["WSQ Framework"]')
print('    Funded --> SGUSCat["SGUS Programme"]')
print('    Funded --> SFMCat["SFM Courses"]')
print('    Funded --> BSMCat["Business Management"]')
print('    Funded --> FTVCat["Film &amp; TV"]')
print('    Funded --> CTWCat["Creative Writing"]')
print('    Funded --> RSDCat["Radio &amp; Sound"]')
print('    Funded --> NMTCat["New Media Tech"]')
print('    Funded --> APACat["APA Courses"]')
print('    Funded --> SFDWCat["SFDW Courses"]')
print('')

# Print all funded pages
for subcat, pages in funded_subs.items():
    if not pages:
        continue
    cat_var = subcat + 'Cat' if subcat != 'Main' else 'FundedMain'
    for i, (link, title) in enumerate(sorted(pages), 1):
        node_id = f'{subcat}{i}'
        print(f'    {cat_var} --> {node_id}["{title}"]')

# Corporate Training
print('')
for i, (link, title) in enumerate(sorted(categories['Corporate Training']), 1):
    node_id = f'Corp{i}'
    print(f'    Corporate --> {node_id}["{title}"]')

# Masterclasses
print('')
for i, (link, title) in enumerate(sorted(categories['Masterclasses']), 1):
    node_id = f'MC{i}'
    print(f'    Masterclasses --> {node_id}["{title}"]')

# Workshops
print('')
for i, (link, title) in enumerate(sorted(categories['Workshops']), 1):
    node_id = f'Wks{i}'
    print(f'    Workshops --> {node_id}["{title}"]')

# Forms
print('')
for i, (link, title) in enumerate(sorted(categories['Forms']), 1):
    node_id = f'Form{i}'
    print(f'    Forms --> {node_id}["{title}"]')

# Other
print('')
for i, (link, title) in enumerate(sorted(categories['Other']), 1):
    node_id = f'Other{i}'
    print(f'    Other --> {node_id}["{title}"]')

