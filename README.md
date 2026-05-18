<div align="center">

# 🇰🇷 한코 · Hanco

> 한국어로 코딩하는 프로그래밍 언어

[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](https://github.com/nslookup255-pixel/Hanco-lang/blob/main/LICENSE)
[![Version](https://img.shields.io/badge/version-v0.8-blue?style=flat-square)](https://github.com/nslookup255-pixel/Hanco-lang/releases/tag/v0.8)
[![Language](https://img.shields.io/badge/language-Korean-purple?style=flat-square)](https://github.com/nslookup255-pixel/Hanco-lang)
[![Python](https://img.shields.io/badge/python-3.x-yellow?style=flat-square)](https://www.python.org)

</div>

---

## 소개

**한코(Hanco)** 는 한국어로 작성하는 프로그래밍 언어입니다.
복잡한 영어 키워드 대신, 한국어로 직관적인 코드를 작성할 수 있습니다.

- 한국어 기반 문법
- `< ~>` 블록, `()` 함수 호출 문법
- 교육 및 실험용 언어

---

## 특징

### 한국어 문법

```hanco
변수 숫자 나이 = 20
출력("나이:", 나이)
```

### 조건문

```hanco
조건 [점수 >= 80] <
    출력("합격")
~>
아니면 <
    출력("불합격")
~>
```

### 반복문

```hanco
반복 i [1~5] <
    출력(i)
~>
```

### 함수

```hanco
함수 더하기 인수 a, b <
    반환 a + b
~>

출력(더하기(3, 5))
```

### 메서드 스타일

```hanco
문장:나누기(",")
```

---

## 빠른 시작

### 설치

```bash
git clone https://github.com/nslookup255-pixel/Hanco-lang
cd Hanco-lang
pip install .
```

### 실행

```bash
hanco run <파일>.hanco   # 파일 실행
hanco repl               # 대화형 모드
hanco version            # 버전 확인
```

### Hello, World!

```hanco
출력("안녕하세요, 한코!")
```

---

## 예제

### 리스트

```hanco
변수 목록 과일 = ("사과", "바나나", "딸기")
출력(과일[0])
```

### 소수 판별

```hanco
함수 소수판별 인수 n <
    조건 [n < 2] <
        반환 거짓
    ~>
    변수 숫자 i = 2
    반복 [i * i <= n] <
        조건 [n % i == 0] <
            반환 거짓
        ~>
        i = i + 1
    ~>
    반환 참
~>

반복 i [2~20] <
    조건 [소수판별(i)] <
        출력(i, "는 소수")
    ~>
~>
```

---

## 개발 상태

- [x] Lexer
- [x] Parser
- [x] 실행 엔진 (VM)
- [x] 기본 IDE
- [ ] 표준 라이브러리
- [ ] 모듈/패키지 시스템

---

## 목표

- 한국어 기반 프로그래밍 환경 제공
- 직관적인 코드 경험
- 한국어 사용자 친화적인 언어 설계

---

아이디어, 개선 제안 환영합니다!

## 라이선스

MIT License
