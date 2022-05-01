
class Test:

    a: 10

    def __init__(self) -> None:
        self.a = 20


if __name__ == '__main__':
    test = Test()
    print(test.a)