from datetime import datetime

from zimmerman.main import db
from zimmerman.notification.service import send_notification
from zimmerman.main.model.main import (
    Post,
    PostLike,
    Comment,
    CommentLike,
    Reply,
    ReplyLike,
)


def check_like(likes, user_id):
    for like in likes:
        if like.owner_id == user_id:
            return True


def notify(object_type, object_public_id, target_owner_public_id):
    notif_data = dict(
        action="liked", object_type=object_type, object_public_id=object_public_id
    )
    send_notification(notif_data, target_owner_public_id)


class Like:
    def post(post_public_id, current_user):
        # Query for the post using its public id
        post = Post.query.filter_by(public_id=post_public_id).first()

        # Check if the post exists
        if not post:
            response_object = {"success": False, "message": "Post not found!"}
            return response_object, 404

        # Check if the user already liked
        likes = PostLike.query.filter_by(on_post=post.id).all()
        if check_like(likes, current_user.id):
            response_object = {
                "success": False,
                "message": "User has already liked the post.",
            }
            return response_object, 403
        
        if current_user.id in likes:
            response_object = {
                "success": False,
                "message": "User has already liked the post.",
            }
            return response_object, 403

        # Create a new like obj.
        like_post = PostLike(
            on_post=post.id, owner_id=current_user.id, liked_on=datetime.utcnow()
        )

        # Commit the changes
        try:
            if current_user.public_id != post.creator_public_id:
                notify("post", post.public_id, post.creator_public_id)

            db.session.add(like_post)
            db.session.commit()
            response_object = {"success": True, "message": "User has liked the post."}
            return response_object, 201

        except Exception as error:
            print(error)
            response_object = {
                "success": False,
                "message": "Something failed during the process!",
            }
            return response_object, 500

    def comment(comment_id, current_user):
        # Query for the comment
        comment = Comment.query.filter_by(id=comment_id).first()

        # Check if the comment exists
        if not comment:
            response_object = {"success": False, "message": "Comment not found!"}
            return response_object, 404

        # Check if the user already liked
        likes = CommentLike.query.filter_by(on_comment=comment_id).all()
        if check_like(likes, current_user.id):
            response_object = {
                "success": False,
                "message": "User has already liked the comment.",
            }
            return response_object, 403

        # Create a new like obj.
        like_comment = CommentLike(
            on_comment=comment_id, owner_id=current_user.id, liked_on=datetime.utcnow()
        )

        # Commit the changes
        try:
            if current_user.public_id != comment.creator_public_id:
                notify("comment", comment.public_id, comment.creator_public_id)

            db.session.add(like_comment)
            db.session.commit()
            response_object = {
                "success": True,
                "message": "User has liked the comment.",
            }
            return response_object, 201

        except Exception as error:
            print(error)
            response_object = {
                "success": False,
                "message": "Something went wrong during the process!",
            }
            return response_object, 500

    def reply(reply_id, current_user):
        # Query for the reply
        reply = Reply.query.filter_by(id=reply_id).first()

        # Check if the reply exists
        if not reply:
            response_object = {"success": False, "message": "Reply not found!"}
            return response_object, 404

        # Check if the user already liked
        likes = ReplyLike.query.filter_by(on_reply=reply_id).all()
        if check_like(likes, current_user.id):
            response_object = {
                "success": False,
                "message": "User has already liked the reply.",
            }
            return response_object, 403

        # Create a new like obj.
        like_reply = ReplyLike(
            on_reply=reply_id, owner_id=current_user.id, liked_on=datetime.utcnow()
        )

        try:
            if current_user.public_id != reply.creator_public_id:
                notify("reply", reply.public_id, reply.creator_public_id)

            db.session.add(like_reply)
            db.session.commit()
            response_object = {"success": False, "message": "User has liked the reply."}
            return response_object, 201

        except Exception as error:
            print(error)
            response_object = {
                "success": False,
                "message": "Something went wrong during the process!",
            }
            return response_object, 500


class Unlike:
    def post(post_public_id, current_user):
        # Query for the post
        post = Post.query.filter_by(public_id=post_public_id).first()

        for like in post.likes:
            if like.owner_id == current_user.id:
                try:
                    db.session.delete(like)
                    db.session.commit()
                    response_object = {
                        "success": True,
                        "message": "User has unliked the post.",
                    }
                    return response_object, 200

                except Exception as error:
                    print(error)
                    response_object = {
                        "success": False,
                        "message": "Something went wrong during the process!",
                    }
                    return response_object, 500

            response_object = {"success": False, "message": "Post like not found!"}
            return response_object, 404

    def comment(comment_id, current_user):
        # Query for the comment
        comment = Comment.query.filter_by(id=comment_id).first()

        for like in comment.likes:
            if like.owner_id == current_user.id:
                try:
                    db.session.delete(like)
                    db.session.commit()
                    response_object = {
                        "success": True,
                        "message": "User has unliked the comment.",
                    }
                    return response_object, 200

                except Exception as error:
                    print(error)
                    response_object = {
                        "success": False,
                        "message": "Something went wrong during the process!",
                    }
                    return response_object, 500

            response_object = {"success": False, "message": "Comment like not found!"}
            return response_object, 404

    def reply(reply_id, current_user):
        # Query for the reply
        reply = Reply.query.filter_by(id=reply_id).first()
        for like in reply.likes:
            if like.owner_id == current_user.id:
                try:
                    db.session.delete(like)
                    db.session.commit()
                    response_object = {
                        "success": True,
                        "message": "User has unliked the reply.",
                    }
                    return response_object, 200

                except Exception as error:
                    print(error)
                    response_object = {
                        "success": False,
                        "message": "Something went wrong during the process!",
                    }
                    return response_object, 500
