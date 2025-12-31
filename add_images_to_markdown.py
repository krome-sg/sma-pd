#!/usr/bin/env python3
"""
Script to add image references back into markdown files based on the image mapping.
This script reads the image mapping JSON and adds markdown image syntax to the
corresponding markdown files.
"""

import json
import os
import re
from urllib.parse import urlparse, parse_qs

MAPPING_FILE = "image_mapping_pages_to_images.json"
POSTS_DIR = "posts"
IMG_DIR = "img"

def extract_filename_from_url(url):
    """
    Extract the filename from a URL, keeping query parameters if present.
    The downloaded images have query parameters in their filenames.
    Example: https://example.com/image.jpg?format=original -> image.jpg?format=original
    """
    # Keep query parameters as they're part of the downloaded filename
    parsed = urlparse(url)
    path = parsed.path
    filename = os.path.basename(path)
    if parsed.query:
        filename = f"{filename}?{parsed.query}"
    return filename


def get_local_image_path(local_filename):
    """
    Convert a local filename to a markdown image path.
    Properly URL-encodes the path for markdown.
    """
    from urllib.parse import quote
    # URL encode the filename, but preserve the path structure
    # Split on ? to handle query parameters separately
    if '?' in local_filename:
        base, query = local_filename.split('?', 1)
        encoded_base = quote(base, safe='')
        encoded_filename = f"{encoded_base}?{query}"
    else:
        encoded_filename = quote(local_filename, safe='')
    
    # Use relative path from posts directory
    return f"../img/{encoded_filename}"


def add_images_to_markdown(post_name, image_data, markdown_content):
    """
    Add image references to markdown content.
    Images are added at the end of the content in a gallery section.
    image_data is a list of tuples: (image_url, local_filename)
    """
    if not image_data:
        return markdown_content
    
    # Check if images section already exists
    if "## Images" in markdown_content or "## Gallery" in markdown_content:
        # Don't add duplicate section
        return markdown_content
    
    # Add images section at the end
    image_section = "\n\n## Images\n\n"
    
    for img_url, local_filename in image_data:
        local_path = get_local_image_path(local_filename)
        # Create markdown image syntax
        # Use filename (without query and extension) as alt text
        clean_filename = local_filename.split('?')[0]
        alt_text = os.path.splitext(clean_filename)[0].replace("-", " ").replace("_", " ").replace("+", " ").title()
        image_section += f"![{alt_text}]({local_path})\n\n"
    
    return markdown_content.rstrip() + image_section


def update_markdown_file(filepath, image_data):
    """
    Update a markdown file with image references.
    image_data is a list of tuples: (image_url, local_filename)
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Add images to content
        updated_content = add_images_to_markdown(
            os.path.splitext(os.path.basename(filepath))[0],
            image_data,
            content
        )
        
        # Write back
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(updated_content)
        
        return True
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False


def verify_images_exist(images):
    """
    Check which images actually exist in the img directory.
    Returns a list of tuples: (image_url, local_filename)
    """
    existing_images = []
    for img_url in images:
        filename_with_query = extract_filename_from_url(img_url)
        img_path = os.path.join(IMG_DIR, filename_with_query)
        
        # Also check without query parameter (in case some were cleaned)
        filename_no_query = filename_with_query.split('?')[0]
        img_path_no_query = os.path.join(IMG_DIR, filename_no_query)
        
        if os.path.exists(img_path):
            existing_images.append((img_url, filename_with_query))
        elif os.path.exists(img_path_no_query):
            existing_images.append((img_url, filename_no_query))
        else:
            print(f"  Warning: Image not found locally: {filename_with_query}")
    return existing_images


def main():
    print("Loading image mapping...")
    
    # Load the mapping
    if not os.path.exists(MAPPING_FILE):
        print(f"Error: Mapping file not found: {MAPPING_FILE}")
        print("Please run map_images_to_pages.py first.")
        return
    
    with open(MAPPING_FILE, "r") as f:
        page_images = json.load(f)
    
    print(f"Loaded mapping for {len(page_images)} pages")
    print(f"\nProcessing markdown files in {POSTS_DIR}/...")
    
    updated_count = 0
    skipped_count = 0
    not_found_count = 0
    
    # Process each page in the mapping
    for post_name, data in page_images.items():
        markdown_file = os.path.join(POSTS_DIR, f"{post_name}.md")
        
        if not os.path.exists(markdown_file):
            print(f"  Skipping {post_name}: markdown file not found")
            not_found_count += 1
            continue
        
        images = data.get("images", [])
        if not images:
            skipped_count += 1
            continue
        
        # Verify images exist locally (returns list of (url, filename) tuples)
        existing_images = verify_images_exist(images)
        
        if existing_images:
            print(f"  Updating {post_name}.md with {len(existing_images)} images")
            if update_markdown_file(markdown_file, existing_images):
                updated_count += 1
            else:
                print(f"    Failed to update {post_name}.md")
        else:
            print(f"  Skipping {post_name}.md: no images found locally")
            skipped_count += 1
    
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"Markdown files updated: {updated_count}")
    print(f"Markdown files skipped: {skipped_count}")
    print(f"Markdown files not found: {not_found_count}")
    print(f"\nImages have been added to markdown files in the 'Images' section.")


if __name__ == "__main__":
    main()

