from enum import Enum


class ConversationEnum(Enum):
    COLLECTION_PROJECT_NAME = "conversations"
    CREATE_CONVERSATION_FAILED="failed_create_conversation"
    FAILED_GET_CONVERSATION_OR_CREATE_ONE="failed_get_conversation_or_create_one"
    FAILED_GET_ALL_CONVERSATIONS="failed_get_all_conversations"