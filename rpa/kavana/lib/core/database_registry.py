# database_registry.py
from typing import Dict
from lib.core.commands.database.db_commander import DbCommander


class DatabaseRegistry:
    """✅ 글로벌 DB Commander들을 관리하는 싱글톤 레지스트리"""
    _commanders: Dict[str, DbCommander] = {}

    @classmethod
    def set_commander(cls, name: str, commander: DbCommander):
        """✅ DB Commander 등록"""
        name = name.lower()
        cls._commanders[name] = commander

    @classmethod
    def get_commander(cls, name: str = "default") -> DbCommander:
        """✅ DB Commander 가져오기"""
        name = name.lower()
        return cls._commanders.get(name)

    @classmethod
    def has_commander(cls, name: str) -> bool:
        """✅ 해당 이름의 Commander 존재 여부"""
        return name.lower() in cls._commanders

    @classmethod
    def clear(cls):
        """✅ 모든 등록된 Commander 초기화 (테스트용)"""
        cls._commanders.clear()
