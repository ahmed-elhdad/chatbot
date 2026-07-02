from bson import ObjectId
from datetime import datetime
from src.models.BaseDataModel import BaseDataModel


class UserDataModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.db = self.db_client["cluster0"]
        self.collection = self.db["users"]

    def _serialize(self, user: dict) -> dict:
        if user is None:
            return None
        if "_id" in user:
            user["_id"] = str(user["_id"])
        return user

    def create_user(self, user_payload: dict) -> dict:
        insert_payload = user_payload.copy()
        if "created_at" not in insert_payload or insert_payload["created_at"] is None:
            insert_payload["created_at"] = datetime.utcnow()
        result = self.collection.insert_one(insert_payload)
        insert_payload["_id"] = str(result.inserted_id)
        return insert_payload

    def get_user_by_email(self, email: str) -> dict:
        user = self.collection.find_one({"email": email})
        return self._serialize(user)

    def get_user_by_username(self, username: str) -> dict:
        user = self.collection.find_one({"username": username})
        return self._serialize(user)

    def get_user_by_id(self, user_id: str) -> dict:
        try:
            user = self.collection.find_one({"_id": ObjectId(user_id)})
            return self._serialize(user)
        except Exception:
            return None

    def update_user(self, user_id: str, update_payload: dict) -> dict:
        if not update_payload:
            return None
        update_payload["updated_at"] = update_payload.get("updated_at") or None
        self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_payload},
        )
        return self.get_user_by_id(user_id)

    def delete_user(self, user_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count == 1
