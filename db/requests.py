from sqlalchemy import select, update, delete, func
from pydantic import BaseModel, ConfigDict
from typing import List

from db.session import session as db_session
from db.models import Post


class PostRepository:
    session = db_session

    @staticmethod
    def serialize_post(post: Post):
        return {
            'id': post.id,
            'md_file_path': post.markdown_file_path,
            'banner_photo_path': post.banner_photo_path,
            'title': post.title,
            'description': post.description,
            'content': '',
            'create_time': post.create_time
        }
    
    @classmethod
    def add_post(cls, post: dict):
        title: str = post['title']
        description: str = post['desc']
        banner_photo_path: str = post['img-path']
        markdown_file_path: str = post['md-path']

        if markdown_file_path == '':
            return 400, {'message': 'Empty post'}
        
        with cls.session() as session:
            new_post = Post(markdown_file_path=markdown_file_path, title=title, description=description, banner_photo_path=banner_photo_path)
            session.add(new_post)
            session.commit()
            
            return 201, {'message': 'Post created'}
    
    @classmethod
    def get_post(cls, post_id: int):
        with cls.session() as session:
            post = session.scalar(select(Post).where(Post.id == post_id))
            if not post:
                return 400, {'message': 'Post with this ID does not exist'}
            
            return 200, PostRepository.serialize_post(post=post)
    
    @classmethod
    def all_posts(cls):
        with cls.session() as session:
            posts = session.scalars(select(Post))
            if not posts:
                return 400, {'message': 'No posts'}
            
            return 200, [PostRepository.serialize_post(post=post) for post in posts]
