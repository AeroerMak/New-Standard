#!/usr/bin/env python3
"""
Performance Optimization Script
Applies optimizations to all HTML pages:
- CSS preloading
- Image lazy loading
- Preconnect for external resources
"""

import re
import os
from pathlib import Path

# HTML files to optimize (excluding component files)
HTML_FILES = [
    'index.html',
    'about.html',
    'privacy-policy.html',
    'spaces-kitchen.html',
    'spaces-dining.html',
    'spaces-living.html',
    'spaces-bedroom.html',
    'collection-kitchen.html',
    'collection-dining.html',
    'collection-living.html',
    'collection-badroom.html',
    'collection-home.html',
    'collection-wallsystems.html',
    'spaces-dining-tables.html'
]

def optimize_css_loading(content):
    """Add CSS preloading"""
    # Pattern to find CSS links
    css_pattern = r'(<link type="text/css" media="all" href="css/style\.css" rel="stylesheet">)'
    
    # Replace with preload version
    replacement = '''    <!-- Preload critical CSS -->
    <link rel="preload" href="css/style.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="css/style.css"></noscript>'''
    
    content = re.sub(css_pattern, replacement, content)
    return content

def add_preconnect(content):
    """Add preconnect for external resources"""
    preconnect_tags = '''    <!-- Preconnect to external domains for faster loading -->
    <link rel="preconnect" href="https://www.googletagmanager.com">
    <link rel="preconnect" href="https://www.google-analytics.com">
    <link rel="dns-prefetch" href="https://img.icons8.com">
    
'''
    
    # Add after charset meta tag
    charset_pattern = r'(<meta charset="[^"]+">)'
    if '<link rel="preconnect"' not in content:
        content = re.sub(charset_pattern, r'\1\n' + preconnect_tags, content, count=1)
    
    return content

def add_lazy_loading_to_images(content):
    """Add lazy loading to images that don't have it"""
    # Pattern for img tags without loading attribute
    img_pattern = r'(<img\s+src="([^"]+)"\s+alt="([^"]*)")(?!\s+loading)'
    
    def add_loading(match):
        img_tag_start = match.group(1)
        # Skip if it's a logo or critical above-the-fold image
        src = match.group(2)
        if 'logo' in src.lower() or 'favicon' in src.lower():
            return img_tag_start  # Don't lazy load logos
        return img_tag_start + ' loading="lazy" decoding="async"'
    
    content = re.sub(img_pattern, add_loading, content)
    
    # Also handle images with other attributes before alt
    img_pattern2 = r'(<img\s+[^>]*src="([^"]+)"[^>]*alt="([^"]*)")(?!\s+loading)([^>]*>)'
    
    def add_loading2(match):
        img_tag = match.group(0)
        src = match.group(2)
        if 'logo' in src.lower() or 'favicon' in src.lower():
            return img_tag  # Don't lazy load logos
        if 'loading=' not in img_tag:
            return img_tag.replace('>', ' loading="lazy" decoding="async">')
        return img_tag
    
    content = re.sub(img_pattern2, add_loading2, content)
    
    return content

def optimize_scripts(content):
    """Ensure scripts have defer attribute where appropriate"""
    # Scripts that should have defer (already mostly done, but ensure consistency)
    script_pattern = r'(<script\s+src="([^"]+)")(?!\s+defer)(?!\s+async)([^>]*type="text/javascript"[^>]*>)'
    
    def add_defer(match):
        script_start = match.group(1)
        src = match.group(2)
        script_end = match.group(3)
        
        # Don't defer critical scripts
        if 'components-loader.js' in src or 'jquery.js' in src:
            return script_start + script_end
        
        # Add defer to non-critical scripts
        if 'defer' not in script_end:
            return script_start + ' defer' + script_end
        
        return match.group(0)
    
    # Only apply to non-critical scripts
    content = re.sub(script_pattern, add_defer, content)
    
    return content

def optimize_html_file(filepath):
    """Optimize a single HTML file"""
    print(f"Optimizing {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply optimizations
        content = optimize_css_loading(content)
        content = add_preconnect(content)
        content = add_lazy_loading_to_images(content)
        # Note: Script optimization commented out to avoid breaking existing functionality
        # content = optimize_scripts(content)
        
        # Only write if content changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Optimized {filepath}")
            return True
        else:
            print(f"  - No changes needed for {filepath}")
            return False
            
    except FileNotFoundError:
        print(f"  ✗ File not found: {filepath}")
        return False
    except Exception as e:
        print(f"  ✗ Error optimizing {filepath}: {e}")
        return False

def main():
    """Main optimization function"""
    base_dir = Path(__file__).parent
    
    print("=" * 60)
    print("Website Performance Optimization")
    print("=" * 60)
    print()
    
    optimized_count = 0
    
    for html_file in HTML_FILES:
        filepath = base_dir / html_file
        if filepath.exists():
            if optimize_html_file(filepath):
                optimized_count += 1
        else:
            print(f"  - Skipping {html_file} (not found)")
    
    print()
    print("=" * 60)
    print(f"Optimization complete! {optimized_count} files optimized.")
    print("=" * 60)

if __name__ == '__main__':
    main()

