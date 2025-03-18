class A:
    def show(self):
        print("A's show method")


class B(A):
    def show(self):
        super().show()
        print("B's show method")


class C(A):
    def show(self):
        super().show()
        print("C's show method")


class D(B, C):
    def show(self):
        super().show()
        print("D's show method")


obj = D()
obj.show()
print(D.mro())