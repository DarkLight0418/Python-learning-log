"""
스택 유스케이스 테스트 코드
2026.06.17 최초 작성
"""


from vds.usecases.stack_usecases import StackUsecase

def test_push_success():
    usecase = StackUsecase()
    
    result = usecase.push("10")
    
    assert result.ok
    assert result.operation == "push"
    assert result.value == "10"
    assert result.snapshot == ("10",)
    
def test_push_empty_value_fails():
    usecase = StackUsecase()
    
    result = usecase.push("   ")
    
    assert not result.ok
    assert result.operation == "push"
    assert result.snapshot == ()
    
def test_pop_success():
    usecase = StackUsecase()
    usecase.pop("10")
    usecase.push("20")
    
    result = usecase.pop()
    
    assert result.ok
    assert result.operation == "pop"
    assert result.value == "20"
    assert result.snapshot == ("10",)
    
def test_pop_empty_stack_fails_without_exception():
    usecase = StackUsecase()

    result = usecase.pop()

    assert not result.ok
    assert result.operation == "pop"
    assert result.snapshot == ()

    
def test_top_does_not_remove_value():
    usecase = StackUsecase()
    usecase.push("10")
    usecase.push("20")
    
    result = usecase.top()
    
    assert result.ok
    assert result.value == "20"
    assert result.snapshot == ("10", "20")
    

def test_clear_removes_all_values():
    usecase = StackUsecase
    usecase.push("10")
    usecase.push("20")
    
    result = usecase.clear()
    
    assert result.ok
    assert result.snapshot == ()
    assert usecase.is_empty()