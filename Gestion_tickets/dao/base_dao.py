from abc import ABC, abstractmethod


class BaseDAO(ABC):
    """Classe abstraite contenant les opérations génériques des DAO."""

    @abstractmethod
    def get_all(self):
        """Retourne tous les enregistrements."""
        pass

    @abstractmethod
    def get_by_id(self, id_element):
        """Retourne un enregistrement à partir de son identifiant."""
        pass

    @abstractmethod
    def delete_by_id(self, id_element):
        """Supprime un enregistrement à partir de son identifiant."""
        pass