import unittest
from uuid import uuid4
from datetime import datetime

from zimmerman.main import db
from zimmerman.main.model.user import Posts, User
from zimmerman.test.base import BaseTestCase

class TestPostModel(BaseTestCase):

      def test_create_post(self):
          """ Test for post model """

          # Create test user
          user = User(
            public_id = str(uuid4().int)[:15],
            email = 'email@test.com',
            username = 'testUser',
            first_name = 'Test',
            last_name = 'User',
            password = 'test1234',
            joined_date = datetime.utcnow()
          )

          db.session.add(user)
          db.session.commit()

          # Create post
          post = Posts(
              owner_id = user.id,
              creator_public_id = user.public_id,
              content = "Test content",
              image_file = "",
              status = "normal",
          )

          db.session.add(post)
          db.session.commit()

          self.assertTrue(isinstance(post, Posts))

if __name__ == '__main__':
    unittest.main()