from sqlalchemy import select, update, delete, func
from pydantic import BaseModel, ConfigDict
from typing import List

from db.session import session as db_session
from db.models import Post, Recipe


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
        page: str = post['page']
        title: str = post['title']
        description: str = post['desc']
        category: str = post['category']
        banner_photo_path: str = post['img-path']
        markdown_file_path: str = post['md-path']

        if markdown_file_path == '':
            return 400, {'message': 'Empty post'}
        
        with cls.session() as session:
            if page.lower() == 'блог':
                new_post = Post(markdown_file_path=markdown_file_path, title=title, description=description, category=category, banner_photo_path=banner_photo_path)
                session.add(new_post)
            elif page.lower() == 'рецепты':
                new_recipe = Recipe(markdown_file_path=markdown_file_path, title=title, description=description, category=category, banner_photo_path=banner_photo_path)
                session.add(new_recipe)
            elif page.lower() == 'проекты':
                #new_project = ''
                #session.add(new_project)
                pass
            elif page.lower() == 'рекомендации':
                #new_rec = ''
                #session.add(new_rec)
                pass
            else:
                return 400, {'message': 'we do not have this table, wtf'}
            
            session.commit()

            return 201, {'message': 'Post created'}
    
    @classmethod
    def get_post(cls, post_id: int):
        with cls.session() as session:
            post = session.scalar(select(Post).where(Post.id == post_id))
            if not post:
                return 400, {'message': 'Post with this ID does not exist'}
            
            return 200, {'message': 'Post fetched', 'post': PostRepository.serialize_post(post=post)}

    @classmethod
    def get_recipe(cls, post_id: int):
        with cls.session() as session:
            post = session.scalar(select(Recipe).where(Recipe.id == post_id))
            if not post:
                return 400, {'message': 'Post with this ID does not exist'}
            
            return 200, {'message': 'Post fetched', 'post': PostRepository.serialize_post(post=post)}
    
    
    @classmethod
    def all_blog_posts(cls):
        with cls.session() as session:
            posts = session.scalars(select(Post))
            if not posts:
                return 400, {'message': 'No posts'}
            
            return 200, {'message': 'Posts fetched', 'posts': [PostRepository.serialize_post(post=post) for post in posts]}
    
    @classmethod
    def all_recipes(cls):
        with cls.session() as session:
            posts = session.scalars(select(Recipe))
            if not posts:
                return 400, {'message': 'No posts'}
            
            return 200, {'message': 'Posts fetched', 'posts': [PostRepository.serialize_post(post=post) for post in posts]}
    
    
