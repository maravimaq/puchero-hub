from app.modules.community.models import Community
from core.repositories.BaseRepository import BaseRepository


class CommunityRepository(BaseRepository):
    def __init__(self):
        super().__init__(Community)

    def get_all_by_user(self, user_id):
        return self.model.query.filter_by(owner_id=user_id).all()

    def get_all_joined_by_user(self, user_id):
        return self.model.query.filter(self.model.members.any(id=user_id)).all()
