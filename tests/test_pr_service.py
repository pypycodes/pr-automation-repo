"""
Tests for the PR service.
"""

import unittest
from services.pr_service import PRService
from models.user import User

class TestPRService(unittest.TestCase):
    """Test cases for PR service."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pr_service = PRService()
        self.author = User(id=1, username="author", email="author@example.com")
        self.reviewer = User(id=2, username="reviewer", email="reviewer@example.com")
    
    def test_create_pr(self):
        """Test creating a pull request."""
        pr = self.pr_service.create_pr(
            title="Test PR",
            description="Test description",
            author=self.author,
            source_branch="feature-branch"
        )
        
        self.assertEqual(pr['title'], "Test PR")
        self.assertEqual(pr['description'], "Test description")
        self.assertEqual(pr['author']['username'], "author")
        self.assertEqual(pr['source_branch'], "feature-branch")
        self.assertEqual(pr['target_branch'], "main")
        self.assertEqual(pr['status'], "open")
        self.assertEqual(len(pr['reviewers']), 0)
        self.assertEqual(len(pr['comments']), 0)
    
    def test_add_reviewer(self):
        """Test adding reviewer to PR."""
        pr = self.pr_service.create_pr(
            title="Test PR",
            description="Test description",
            author=self.author,
            source_branch="feature-branch"
        )
        
        success = self.pr_service.add_reviewer(pr['id'], self.reviewer)
        self.assertTrue(success)
        
        updated_pr = self.pr_service.get_pr(pr['id'])
        self.assertEqual(len(updated_pr['reviewers']), 1)
        self.assertEqual(updated_pr['reviewers'][0]['username'], "reviewer")
    
    def test_add_duplicate_reviewer(self):
        """Test adding duplicate reviewer."""
        pr = self.pr_service.create_pr(
            title="Test PR",
            description="Test description",
            author=self.author,
            source_branch="feature-branch"
        )
        
        self.pr_service.add_reviewer(pr['id'], self.reviewer)
        success = self.pr_service.add_reviewer(pr['id'], self.reviewer)
        self.assertFalse(success)
        
        updated_pr = self.pr_service.get_pr(pr['id'])
        self.assertEqual(len(updated_pr['reviewers']), 1)
    
    def test_add_comment(self):
        """Test adding comment to PR."""
        pr = self.pr_service.create_pr(
            title="Test PR",
            description="Test description",
            author=self.author,
            source_branch="feature-branch"
        )
        
        success = self.pr_service.add_comment(pr['id'], self.author, "Great work!")
        self.assertTrue(success)
        
        updated_pr = self.pr_service.get_pr(pr['id'])
        self.assertEqual(len(updated_pr['comments']), 1)
        self.assertEqual(updated_pr['comments'][0]['comment'], "Great work!")
        self.assertEqual(updated_pr['comments'][0]['author']['username'], "author")
    
    def test_list_prs(self):
        """Test listing PRs."""
        pr1 = self.pr_service.create_pr("PR 1", "Desc 1", self.author, "branch1")
        pr2 = self.pr_service.create_pr("PR 2", "Desc 2", self.author, "branch2")
        
        open_prs = self.pr_service.list_prs("open")
        self.assertEqual(len(open_prs), 2)
        
        self.pr_service.close_pr(pr1['id'])
        open_prs = self.pr_service.list_prs("open")
        self.assertEqual(len(open_prs), 1)
        
        closed_prs = self.pr_service.list_prs("closed")
        self.assertEqual(len(closed_prs), 1)
    
    def test_close_pr(self):
        """Test closing a PR."""
        pr = self.pr_service.create_pr("Test PR", "Desc", self.author, "branch")
        self.assertEqual(pr['status'], "open")
        
        success = self.pr_service.close_pr(pr['id'])
        self.assertTrue(success)
        
        updated_pr = self.pr_service.get_pr(pr['id'])
        self.assertEqual(updated_pr['status'], "closed")
    
    def test_get_pr_stats(self):
        """Test getting PR statistics."""
        self.pr_service.create_pr("PR 1", "Desc 1", self.author, "branch1")
        self.pr_service.create_pr("PR 2", "Desc 2", self.author, "branch2")
        
        stats = self.pr_service.get_pr_stats()
        self.assertEqual(stats['total_prs'], 2)
        self.assertEqual(stats['open_prs'], 2)
        self.assertEqual(stats['closed_prs'], 0)
        self.assertEqual(stats['total_reviewers'], 0)
        
        self.pr_service.add_reviewer(1, self.reviewer)
        stats = self.pr_service.get_pr_stats()
        self.assertEqual(stats['total_reviewers'], 1)

if __name__ == '__main__':
    unittest.main()
