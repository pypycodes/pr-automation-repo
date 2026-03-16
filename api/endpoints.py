"""
API endpoints for the PR automation application.
"""

from flask import Flask, request, jsonify
from typing import Dict, Any
from services.pr_service import PRService
from models.user import User
from config.settings import settings

app = Flask(__name__)
pr_service = PRService()

@app.route('/health', methods=['GET'])
def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        'status': 'healthy',
        'app_name': settings.app_name,
        'timestamp': pr_service.get_pr_stats()['last_updated']
    }

@app.route('/users', methods=['POST'])
def create_user() -> Dict[str, Any]:
    """Create a new user."""
    data = request.get_json()
    
    try:
        user = User(
            id=data['id'],
            username=data['username'],
            email=data['email'],
            is_active=data.get('is_active', True),
            roles=data.get('roles', [])
        )
        return jsonify({'user': user.to_dict()}), 201
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), 400

@app.route('/prs', methods=['POST'])
def create_pr() -> Dict[str, Any]:
    """Create a new pull request."""
    data = request.get_json()
    
    try:
        author = User(
            id=data['author']['id'],
            username=data['author']['username'],
            email=data['author']['email']
        )
        
        pr = pr_service.create_pr(
            title=data['title'],
            description=data['description'],
            author=author,
            source_branch=data['source_branch'],
            target_branch=data.get('target_branch', 'main')
        )
        return jsonify({'pr': pr}), 201
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), 400

@app.route('/prs', methods=['GET'])
def list_prs() -> Dict[str, Any]:
    """List pull requests."""
    status = request.args.get('status', 'open')
    prs = pr_service.list_prs(status)
    return jsonify({'prs': prs, 'count': len(prs)})

@app.route('/prs/<int:pr_id>/reviewers', methods=['POST'])
def add_reviewer(pr_id: int) -> Dict[str, Any]:
    """Add reviewer to pull request."""
    data = request.get_json()
    
    try:
        reviewer = User(
            id=data['id'],
            username=data['username'],
            email=data['email']
        )
        
        success = pr_service.add_reviewer(pr_id, reviewer)
        if success:
            return jsonify({'message': 'Reviewer added successfully'})
        else:
            return jsonify({'error': 'Failed to add reviewer'}), 400
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), 400

@app.route('/prs/<int:pr_id>/comments', methods=['POST'])
def add_comment(pr_id: int) -> Dict[str, Any]:
    """Add comment to pull request."""
    data = request.get_json()
    
    try:
        author = User(
            id=data['author']['id'],
            username=data['author']['username'],
            email=data['author']['email']
        )
        
        success = pr_service.add_comment(pr_id, author, data['comment'])
        if success:
            return jsonify({'message': 'Comment added successfully'})
        else:
            return jsonify({'error': 'Failed to add comment'}), 400
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), 400

@app.route('/prs/stats', methods=['GET'])
def get_pr_stats() -> Dict[str, Any]:
    """Get PR statistics."""
    return jsonify(pr_service.get_pr_stats())

if __name__ == '__main__':
    app.run(debug=settings.debug, host='0.0.0.0', port=5000)
