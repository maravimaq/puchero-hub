from app.modules.profile.repositories import UserProfileRepository
from core.services.BaseService import BaseService


class UserProfileService(BaseService):
    def __init__(self):
        super().__init__(UserProfileRepository())

    def update_profile(self, user_profile_id, form):
        profile = self.repository.get_by_id(user_profile_id)
        if not profile:
            return None, {"error": f"UserProfile with id {user_profile_id} does not exist."}
        
        if form.validate():
            updated_instance = self.update(user_profile_id, **form.data)
            return updated_instance, None

        return None, form.errors
