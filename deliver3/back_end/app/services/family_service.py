from app.repositories.family_repository import FamilyRepository

class FamilyService:
    @staticmethod
    def get_family_info(user_id):
        group = FamilyRepository.get_user_family_group(user_id)
        if not group:
            return None
        
        group_dict = dict(group)
        members = FamilyRepository.get_family_members(group_dict['group_id'])
        group_dict['members'] = [dict(m) for m in members]
        return group_dict

    @staticmethod
    def create_family(user_id, name):
        # Check if user is already in a family
        if FamilyRepository.get_user_family_group(user_id):
            raise ValueError("User is already in a family group")
            
        group_id = FamilyRepository.create_family_group(name)
        FamilyRepository.add_member(group_id, user_id, role='Admin')
        return group_id

    @staticmethod
    def leave_family(user_id):
        group = FamilyRepository.get_user_family_group(user_id)
        if group:
            FamilyRepository.remove_member(group['group_id'], user_id)
