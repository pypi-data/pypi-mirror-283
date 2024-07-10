# Checkout package

Este proyecto es con el fin de adaptar la [Kata 09: Back to the Checkout](http://codekata.com/kata/kata09-back-to-the-checkout/) a un paquete de python con DDD y TDD.

Token for pkg: pypi-AgEIcHlwaS5vcmcCJDg0ZTg2MTU3LTVkMWYtNGQ3OS1hY2ZlLTI1MzNhNjQzYTRhMgACKlszLCIzYjg1NjYwNC1kN2IzLTQ2YTQtYmIzYi02MGZlNzQ5ODNmZDUiXQAABiAE-5w6Bwup0wTMZKxYXdW4v8l2AHFMCaNCZSpUsDpjGQ

# Instalación del paquete

1. Asegurarse de tener python instalado en su sistema, si no lo tiene haga clic [aqui](https://www.python.org/downloads/) para una guía de como hacerlo.
2. Descarge el paquete kataCheckout con el comando:

``` 
pip install kataCheckout
``` 

# Uso del paquete

1. Importar las clases necesarias:

``` 
from kataCheckout import Product, Rules, Checkout
```

2. Para definir productos:

```
product_a = Product("A", 50)
product_b = Product("B", 30)
product_c = Product("C", 20)
product_d = Product("D", 15)
```

3. Para definir reglas:

```
rules = {
    "A": Rules("A", quantity=3, discount=130),
    "B": Rules("B", quantity=2, discount=45),
    "C": Rules("C"),
    "D": Rules("D")
}
``` 

4. Crear una instancia:

```
co = Checkout(rules)
``` 

5. Escanear productos:

```
co.scan(product_a)
co.scan(product_b)
co.scan(product_a)
co.scan(product_c)
co.scan(product_d)
co.scan(product_b)
co.scan(product_a)
``` 

6. Calcular el total:

```
total = co.total()
print(f"Total: {total}")
```

Recuerda que el método "total()" devolverá "Item not in list" si intentas escanear un producto que no está definido en las reglas.Last edited 10 minutes ago
