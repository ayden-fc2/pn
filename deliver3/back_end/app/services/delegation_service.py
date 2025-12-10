from app.repositories.delegation_repository import DelegationRepository

class DelegationService:
    @staticmethod
    def get_delegations(user_id):
        dependents = DelegationRepository.get_dependents(user_id)
        guardians = DelegationRepository.get_guardians(user_id)
        return {
            'dependents': [dict(d) for d in dependents],
            'guardians': [dict(g) for g in guardians]
        }

    @staticmethod
    def add_dependent(guardian_id, dependent_id):
        if guardian_id == dependent_id:
            raise ValueError("Cannot be your own guardian")
        DelegationRepository.create_delegation(guardian_id, dependent_id)

    @staticmethod
    def remove_delegation(guardian_id, dependent_id):
        DelegationRepository.remove_delegation(guardian_id, dependent_id)
