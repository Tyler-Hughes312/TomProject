"""
Category Helper for Lead Generator
Based on existing category helper patterns
"""

import json
from typing import List, Dict, Optional
from pathlib import Path


class CategoryHelper:
    """
    Helper class to manage Yelp categories and provide category search functionality.
    """
    
    def __init__(self, categories_file: str = "yelp_categories.json"):
        """
        Initialize the CategoryHelper with Yelp categories.
        
        Args:
            categories_file: Path to the JSON file containing Yelp categories
        """
        self.categories_file = categories_file
        self.categories = self._load_categories()
        self._build_search_index()
    
    def _load_categories(self) -> List[Dict]:
        """Load categories from JSON file."""
        try:
            with open(self.categories_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {self.categories_file} not found. Using empty categories list.")
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing {self.categories_file}: {e}")
            return []
    
    def _build_search_index(self):
        """Build search index for faster category lookups."""
        self.title_to_alias = {cat["title"].lower(): cat["alias"] for cat in self.categories}
        self.alias_to_title = {cat["alias"]: cat["title"] for cat in self.categories}
        self.parent_categories = {}
        
        for cat in self.categories:
            for parent in cat.get("parent_aliases", []):
                if parent not in self.parent_categories:
                    self.parent_categories[parent] = []
                self.parent_categories[parent].append(cat["alias"])
    
    def search_categories(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for categories by title or alias.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
            
        Returns:
            List of matching categories
        """
        query_lower = query.lower()
        matches = []
        
        for cat in self.categories:
            title_lower = cat["title"].lower()
            alias_lower = cat["alias"].lower()
            
            # Check if query matches title or alias
            if (query_lower in title_lower or 
                query_lower in alias_lower or
                title_lower.startswith(query_lower) or
                alias_lower.startswith(query_lower)):
                matches.append(cat)
                
                if len(matches) >= limit:
                    break
        
        return matches
    
    def get_category_by_alias(self, alias: str) -> Optional[Dict]:
        """
        Get category by its alias.
        
        Args:
            alias: Category alias
            
        Returns:
            Category dictionary or None if not found
        """
        for cat in self.categories:
            if cat["alias"] == alias:
                return cat
        return None
    
    def get_category_by_title(self, title: str) -> Optional[Dict]:
        """
        Get category by its title.
        
        Args:
            title: Category title
            
        Returns:
            Category dictionary or None if not found
        """
        for cat in self.categories:
            if cat["title"].lower() == title.lower():
                return cat
        return None
    
    def get_subcategories(self, parent_alias: str) -> List[Dict]:
        """
        Get all subcategories of a parent category.
        
        Args:
            parent_alias: Parent category alias
            
        Returns:
            List of subcategory dictionaries
        """
        subcategories = []
        for cat in self.categories:
            if parent_alias in cat.get("parent_aliases", []):
                subcategories.append(cat)
        return subcategories
    
    def get_parent_categories(self) -> List[Dict]:
        """
        Get all top-level categories (those with no parent_aliases).
        
        Returns:
            List of parent category dictionaries
        """
        return [cat for cat in self.categories if not cat.get("parent_aliases")]
    
    def get_popular_categories(self) -> List[Dict]:
        """
        Get a list of popular business categories.
        
        Returns:
            List of popular category dictionaries
        """
        popular_aliases = [
            "restaurants", "food", "shopping", "health", "auto", 
            "beautysvc", "homeservices", "professional", "active",
            "arts", "education", "financialservices", "hotelstravel"
        ]
        
        popular_categories = []
        for alias in popular_aliases:
            cat = self.get_category_by_alias(alias)
            if cat:
                popular_categories.append(cat)
        
        return popular_categories
    
    def validate_category(self, category: str) -> bool:
        """
        Validate if a category exists (by title or alias).
        
        Args:
            category: Category title or alias
            
        Returns:
            True if category exists, False otherwise
        """
        return (self.get_category_by_title(category) is not None or 
                self.get_category_by_alias(category) is not None)
    
    def get_category_alias(self, category: str) -> Optional[str]:
        """
        Get the alias for a category (by title or alias).
        
        Args:
            category: Category title or alias
            
        Returns:
            Category alias or None if not found
        """
        # First try to find by alias
        cat = self.get_category_by_alias(category)
        if cat:
            return cat["alias"]
        
        # Then try to find by title
        cat = self.get_category_by_title(category)
        if cat:
            return cat["alias"]
        
        return None
    
    def print_category_tree(self, parent_alias: Optional[str] = None, indent: int = 0):
        """
        Print a tree view of categories.
        
        Args:
            parent_alias: Parent category alias (None for root categories)
            indent: Indentation level
        """
        if parent_alias is None:
            # Print root categories
            root_categories = self.get_parent_categories()
            for cat in root_categories:
                print(" " * indent + f"• {cat['title']} ({cat['alias']})")
                self.print_category_tree(cat['alias'], indent + 2)
        else:
            # Print subcategories
            subcategories = self.get_subcategories(parent_alias)
            for cat in subcategories:
                print(" " * indent + f"• {cat['title']} ({cat['alias']})")
                self.print_category_tree(cat['alias'], indent + 2)
