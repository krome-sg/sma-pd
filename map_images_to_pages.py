#!/usr/bin/env python3
"""
Utility script to map images to pages from Squarespace XML export.
This script analyzes the XML file and creates a mapping of which images
are used on which pages.
"""

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from collections import defaultdict
import json

XML_FILE = "squarespace.xml"
IMG_URL = "images.squarespace-cdn.com"

def get_page_image_mapping(root):
    """
    Returns a dictionary mapping page/post names to lists of image URLs.
    """
    namespace = {
        "content": "http://purl.org/rss/1.0/modules/content/",
        "wp": "http://wordpress.org/export/1.2/",
    }
    
    page_images = defaultdict(list)
    
    for item in root.findall("./channel/item"):
        # Get page/post name
        post_name_element = item.find("{%s}post_name" % namespace["wp"])
        post_name = post_name_element.text if post_name_element is not None else "unknown"
        
        # Get title for reference
        title_element = item.find("title")
        title = title_element.text if title_element is not None else "unknown title"
        
        # Get post type to skip attachments
        post_type = item.find("{%s}post_type" % namespace["wp"])
        if post_type is not None and post_type.text == "attachment":
            continue
        
        images_found = []
        
        # Extract images from content:encoded
        for element in item.findall("{%s}encoded" % namespace["content"]):
            if element.text:
                soup = BeautifulSoup(element.text, "html.parser")
                for img in soup.find_all("img"):
                    src = img.get("src")
                    if src and IMG_URL in src:
                        images_found.append(src)
        
        # Extract images from link elements
        for element in item.findall("link"):
            if element.text and IMG_URL in element.text:
                images_found.append(element.text)
        
        # Extract images from wp:attachment_url
        for element in item.findall("{%s}attachment_url" % namespace["wp"]):
            if element.text and IMG_URL in element.text:
                images_found.append(element.text)
        
        if images_found:
            page_images[post_name] = {
                "title": title,
                "images": list(set(images_found))  # Remove duplicates
            }
    
    return page_images


def get_image_to_pages_mapping(root):
    """
    Returns a dictionary mapping image URLs to lists of pages that use them.
    """
    namespace = {
        "content": "http://purl.org/rss/1.0/modules/content/",
        "wp": "http://wordpress.org/export/1.2/",
    }
    
    image_to_pages = defaultdict(list)
    
    for item in root.findall("./channel/item"):
        post_name_element = item.find("{%s}post_name" % namespace["wp"])
        post_name = post_name_element.text if post_name_element is not None else "unknown"
        
        title_element = item.find("title")
        title = title_element.text if title_element is not None else "unknown title"
        
        post_type = item.find("{%s}post_type" % namespace["wp"])
        if post_type is not None and post_type.text == "attachment":
            continue
        
        images_found = []
        
        for element in item.findall("{%s}encoded" % namespace["content"]):
            if element.text:
                soup = BeautifulSoup(element.text, "html.parser")
                for img in soup.find_all("img"):
                    src = img.get("src")
                    if src and IMG_URL in src:
                        images_found.append(src)
        
        for element in item.findall("link"):
            if element.text and IMG_URL in element.text:
                images_found.append(element.text)
        
        for element in item.findall("{%s}attachment_url" % namespace["wp"]):
            if element.text and IMG_URL in element.text:
                images_found.append(element.text)
        
        for img_url in set(images_found):
            image_to_pages[img_url].append({
                "post_name": post_name,
                "title": title
            })
    
    return image_to_pages


def main():
    print("Analyzing XML file to map images to pages...")
    
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    
    # Get page -> images mapping
    page_images = get_page_image_mapping(root)
    
    # Get image -> pages mapping
    image_to_pages = get_image_to_pages_mapping(root)
    
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"Total pages with images: {len(page_images)}")
    print(f"Total unique images: {len(image_to_pages)}")
    
    # Save page -> images mapping
    output_file = "image_mapping_pages_to_images.json"
    with open(output_file, "w") as f:
        json.dump(page_images, f, indent=2)
    print(f"\nSaved page-to-images mapping to: {output_file}")
    
    # Save image -> pages mapping
    output_file2 = "image_mapping_images_to_pages.json"
    with open(output_file2, "w") as f:
        json.dump(image_to_pages, f, indent=2)
    print(f"Saved image-to-pages mapping to: {output_file2}")
    
    # Print some examples
    print(f"\n{'='*80}")
    print(f"SAMPLE: Pages with most images (top 10)")
    print(f"{'='*80}")
    
    sorted_pages = sorted(page_images.items(), key=lambda x: len(x[1]["images"]), reverse=True)
    for post_name, data in sorted_pages[:10]:
        print(f"\nPage: {post_name}")
        print(f"  Title: {data['title']}")
        print(f"  Images: {len(data['images'])}")
        if len(data['images']) > 0:
            print(f"  First image: {data['images'][0][:80]}...")
    
    print(f"\n{'='*80}")
    print(f"SAMPLE: Images used on multiple pages (top 10)")
    print(f"{'='*80}")
    
    sorted_images = sorted(image_to_pages.items(), key=lambda x: len(x[1]), reverse=True)
    for img_url, pages in sorted_images[:10]:
        if len(pages) > 1:
            print(f"\nImage: {img_url[:80]}...")
            print(f"  Used on {len(pages)} pages:")
            for page in pages:
                print(f"    - {page['post_name']} ({page['title']})")


if __name__ == "__main__":
    main()

