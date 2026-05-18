from hanco.core.lexer import Lexer
from hanco.core.parser import Parser
from hanco.core.vm import VM

code = """
사용(랜덤)
사용(시간)

:: 비교 연산자 테스트
변수 숫자 x = 5
변수 숫자 y = 10

출력("x:", x, "y:", y)
조건 [x < y] <
  출력("x가 y보다 작습니다")
~>
아니면 [x > y] <
  출력("x가 y보다 큽니다")
~>
아니면 <
  출력("x와 y가 같습니다")
~>

:: >= 테스트
변수 숫자 나이 = 20
조건 [나이 >= 18] <
  출력("성인")
~>

:: 반복문 테스트
반복 i[1~3] <
  출력(i)
~>

:: 함수 테스트
함수 최대 인수 a, b <
  조건 [a >= b] <
    반환 a
  ~>
  반환 b
~>

출력(최대(7, 3))

:: 랜덤 + 메서드 호출
출력(랜덤:무작위(1, 10))
출력(시간:현재())
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

print("\n=== 실행 결과 ===")
vm = VM()
vm.run(ast)
