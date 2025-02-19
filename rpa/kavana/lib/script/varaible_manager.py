class VariableManager:
    def __init__(self):
        self.global_vars = {}  # 전역 변수 저장소
        self.local_vars_stack = []  # 지역 변수 스택 (함수 호출 시 사용)

    def set_variable(self, name, value, local=False):
        """ 변수 설정 (지역/전역 변수 구분) """
        if local and self.local_vars_stack:
            self.local_vars_stack[-1][name] = value  # 현재 실행 중인 함수의 지역 변수로 저장
        else:
            self.global_vars[name] = value  # 전역 변수로 저장

    def get_variable(self, name):
        """ 변수 조회 (지역 변수를 먼저 찾고, 없으면 전역 변수에서 찾기) """
        for scope in reversed(self.local_vars_stack):
            if name in scope:
                return scope[name]
        return self.global_vars.get(name, None)

    def push_local_scope(self):
        """ 새로운 지역 변수 스코프 추가 (함수 호출 시) """
        self.local_vars_stack.append({})

    def pop_local_scope(self):
        """ 지역 변수 스코프 제거 (함수 종료 시) """
        if self.local_vars_stack:
            self.local_vars_stack.pop()
