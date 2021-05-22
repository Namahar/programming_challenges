import math
import sympy

def main():
   sympy.init_printing(use_unicode=False, wrap_line=False)

   # sympy integrate for indefinite integrals
   x = sympy.Symbol('x')
   integral = sympy.integrate(x**2 + x + 1, x)
   print(integral)

   return

if __name__ == '__main__':
   main()
