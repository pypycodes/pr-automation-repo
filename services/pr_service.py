"""
PR service for handling pull request operations.
"""

from typing import List, Dict, Optional
from datetime import datetime
from models.user import User
from utils.helpers import format_timestamp, chunk_list

class PRService:
    """Service for managing pull requests."""
    
    def __init__(self):
        self.prs: List[Dict] = []
        self.reviewers: Dict[str, User] = {}
    
    def create_pr(self, title: str, description: str, author: User, 
                  source_branch: str, target_branch: str = "main") -> Dict:
        """Create a new pull request."""
        pr = {
            'id': len(self.prs) + 1,
            'title': title,
            'description': description,
            'author': author.to_dict(),
            'source_branch': source_branch,
            'target_branch': target_branch,
            'status': 'open',
            'created_at': format_timestamp(),
            'updated_at': format_timestamp(),
            'reviewers': [],
            'comments': [],
            'changes': []
        }
        self.prs.append(pr)
        return pr
    
    def add_reviewer(self, pr_id: int, reviewer: User) -> bool:
        """Add a reviewer to a pull request."""
        pr = self.get_pr(pr_id)
        if pr and reviewer.username not in [r['username'] for r in pr['reviewers']]:
            pr['reviewers'].append(reviewer.to_dict())
            pr['updated_at'] = format_timestamp()
            self.reviewers[reviewer.username] = reviewer
            return True
        return False
    
    def add_comment(self, pr_id: int, author: User, comment: str) -> bool:
        """Add a comment to a pull request."""
        pr = self.get_pr(pr_id)
        if pr:
            comment_data = {
                'id': len(pr['comments']) + 1,
                'author': author.to_dict(),
                'comment': comment,
                'created_at': format_timestamp()
            }
            pr['comments'].append(comment_data)
            pr['updated_at'] = format_timestamp()
            return True
        return False
    
    def get_pr(self, pr_id: int) -> Optional[Dict]:
        """Get pull request by ID."""
        return next((pr for pr in self.prs if pr['id'] == pr_id), None)
    
    def list_prs(self, status: str = 'open') -> List[Dict]:
        """List pull requests by status."""
        return [pr for pr in self.prs if pr['status'] == status]
    
    def close_pr(self, pr_id: int) -> bool:
        """Close a pull request."""
        pr = self.get_pr(pr_id)
        if pr:
            pr['status'] = 'closed'
            pr['updated_at'] = format_timestamp()
            return True
        return False
    
    def get_pr_stats(self) -> Dict:
        """Get PR statistics."""
        total = len(self.prs)
        open_prs = len([pr for pr in self.prs if pr['status'] == 'open'])
        closed_prs = len([pr for pr in self.prs if pr['status'] == 'closed'])
        
        return {
            'total_prs': total,
            'open_prs': open_prs,
            'closed_prs': closed_prs,
            'total_reviewers': len(self.reviewers),
            'last_updated': format_timestamp()
        }
