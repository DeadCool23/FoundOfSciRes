# Описание

Нужно решить задачу двумя способами - численным и Монте-Карло.


## Первая задача (Самый простой вариант)

$\frac{\partial^2u}{\partial x^2} + \frac{\partial^2u}{\partial z^2} = f(x, z)$

### Численное решение
Метод установления.

$\frac{\partial u}{\partial t} = \frac{\partial^2u}{\partial x^2} + \frac{\partial^2u}{\partial z^2} - f(x, z)$

Краевое условие $I\text{-го}$ рода, т.е. на границах заданы $u$.

Вводим сетку x,z. (k, n) - точка на сетке.

$\frac{\hat{y}_{nk} - y_{nk}}{\tau} = \frac{\hat{y}_{k-1, n} - 2\hat{y}_{nk} + \hat{y}_{k+1, n}}{hx^2} + \frac{\hat{y}_{k, n-1} - 2\hat{y}_{nk} + \hat{y}_{k, n+1}}{hz^2} + f(x_k, z_n)$

Можем решать продольно-поперечной схемой или локально-одномерным методом.

### Метод Монте-Карло
$u_{nk} = \frac{\sum_{\alpha} T_{\alpha,\beta}}{N}$

$N$ - количество частиц (например $N = 100$).

$\alpha$ - номер частицы, (например $\alpha = 100$).

$\beta$ - номер точки на границе

$N$ варьируем.


## Остальные задачи (более сложные варианты)
2) $c\frac{\partial u}{\partial t} = \frac{\partial}{\partial x}(k(x, z)\frac{\partial u}{\partial x}) + \frac{\partial}{\partial z}(k(x, z)\frac{\partial u}{\partial z}) - f(x, z)$

3) $c(u)\frac{\partial u}{\partial t} = \frac{\partial}{\partial x}(k(u)\frac{\partial u}{\partial x}) + \frac{\partial}{\partial z}(k(u)\frac{\partial u}{\partial z}) - f(u)$

4) $\frac{\partial^2u}{\partial x^2} + \frac{\partial^2u}{\partial z^2} + \frac{\partial^2u}{\partial v^2} = f(x, z, v)$

Идеально: Придумать, какими способами максимально ускорить процесс блуждания, чтобы время рассчета двумя разными способами было сопоставимо.