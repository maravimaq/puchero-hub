from app.modules.community.repositories import CommunityRepository
from core.services.BaseService import BaseService


class CommunityService(BaseService):
    def __init__(self):
        super().__init__(CommunityRepository())

    def get_all_by_user(self, user_id):
        return self.repository.get_all_by_user(user_id)

    def get_all_joined_by_user(self, user_id):
        return self.repository.get_all_joined_by_user(user_id)

    def get_members_by_id(self, community_id):
        return self.repository.get_with_members_by_id(community_id)
