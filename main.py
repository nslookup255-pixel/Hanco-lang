from hanco.core.lexer import Lexer
from hanco.core.parser import Parser
from hanco.core.vm import VM

code = """
사용<랜덤>
사용<시간>
사용<파일>
변수 목록 후보 = ("사과", "바나나", "포도")
변수 목록 후보2 = ("강아지", "고양이", "토끼")
출력<랜덤:무작위<1, 10>>
출력<랜덤:실수<>>
출력<랜덤:선택<후보>>
출력<랜덤:섞기<후보2>>
출력<랜덤:선택<후보2>>
출력<시간:현재<>>
출력<시간:시간<>, 시간:분<>, 시간:초<>>
출력<시간:타임스탬프<>>
시간:대기<2>
출력<"2초 대기 후 출력">
파일:쓰기<"test.txt", "안녕하세요!">
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

print("\n=== 실행 결과 ===")
vm = VM()
vm.run(ast)
