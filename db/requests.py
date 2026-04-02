from sqlalchemy import select, update, delete, func
from pydantic import BaseModel, ConfigDict
from typing import List

from db.session import session
from db.models import Post


class PostRepository:
    @staticmethod
    def serialize_post(post: Post):
        return {
            'post': {
                'md_file_path': post.markdown_file_path,
                'content': '',
                'create_time': post.create_time
            }
        }
    
    @classmethod
    async def add_post(cls, markdown_file_path: str):
        if markdown_file_path == '':
            return 400, {'message': 'Empty post'}
        
        async with session() as session:
            new_post = Post(markdown_file_path=markdown_file_path)
            session.add(new_post)
            await session.commit()
            
            return 201, {'message': 'Post created'}
    
    @classmethod
    async def get_post(cls, post_id: int):
        async with session() as session:
            post = await session.scalar(select(Post).where(Post.id == post_id))
            if not post:
                return 400, {'message': 'Post with this ID does not exist'}
            
            return 200, PostRepository.serialize_post(post=post)
