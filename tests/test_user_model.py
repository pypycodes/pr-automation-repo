"""
Tests for the User model.
"""

import unittest
from datetime import datetime
from models.user import User

class TestUserModel(unittest.TestCase):
    """Test cases for User model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.user = User(
            id=1,
            username="testuser",
            email="test@example.com"
        )
    
    def test_user_creation(self):
        """Test user creation with valid data."""
        self.assertEqual(self.user.id, 1)
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.is_active)
        self.assertEqual(self.user.roles, [])
    
    def test_invalid_email(self):
        """Test user creation with invalid email."""
        with self.assertRaises(ValueError):
            User(id=2, username="user2", email="invalid-email")
    
    def test_short_username(self):
        """Test user creation with short username."""
        with self.assertRaises(ValueError):
            User(id=3, username="ab", email="valid@example.com")
    
    def test_user_hash(self):
        """Test user hash generation."""
        hash1 = self.user.user_hash
        hash2 = self.user.user_hash
        self.assertEqual(hash1, hash2)
        self.assertIsInstance(hash1, str)
        self.assertEqual(len(hash1), 64)  # SHA256 hash length
    
    def test_add_role(self):
        """Test adding roles to user."""
        self.user.add_role("admin")
        self.assertIn("admin", self.user.roles)
        self.assertEqual(len(self.user.roles), 1)
    
    def test_add_duplicate_role(self):
        """Test adding duplicate role."""
        self.user.add_role("admin")
        self.user.add_role("admin")
        self.assertEqual(self.user.roles.count("admin"), 1)
    
    def test_remove_role(self):
        """Test removing roles from user."""
        self.user.add_role("admin")
        self.user.add_role("user")
        self.user.remove_role("admin")
        self.assertNotIn("admin", self.user.roles)
        self.assertIn("user", self.user.roles)
    
    def test_to_dict(self):
        """Test converting user to dictionary."""
        user_dict = self.user.to_dict()
        self.assertIsInstance(user_dict, dict)
        self.assertEqual(user_dict['id'], 1)
        self.assertEqual(user_dict['username'], "testuser")
        self.assertEqual(user_dict['email'], "test@example.com")
        self.assertIn('user_hash', user_dict)
        self.assertIn('created_at', user_dict)
        self.assertIn('updated_at', user_dict)

if __name__ == '__main__':
    unittest.main()
