from app.modules.community.repositories import CommunityRepository
from core.services.BaseService import BaseService
from app import db


class CommunityService(BaseService):
    def __init__(self):
        super().__init__(CommunityRepository())

    def get_all_by_user(self, user_id):
        return self.repository.get_all_by_user(user_id)

    def get_all_joined_by_user(self, user_id):
        return self.repository.get_all_joined_by_user(user_id)

    def get_members_by_id(self, community_id):
        return self.repository.get_with_members_by_id(community_id)

    def get_communities_not_joined_by_user(self, user_id):
        return self.repository.get_communities_not_joined_by_user(user_id)

    def join_community(self, community_id, user):
        community = self.repository.get_by_id(community_id)
        if community and user not in community.members:
            community.members.append(user)
            db.session.commit()
            return True
        return False

    def get_with_datasets_by_id(self, community_id):
        return self.repository.get_with_datasets_by_id(community_id)
