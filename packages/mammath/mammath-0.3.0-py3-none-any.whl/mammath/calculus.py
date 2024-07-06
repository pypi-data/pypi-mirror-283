from .constants import pi, e
from .operations import factorial

"""
CALCULUS
"""
def interpolate_polynomial(x_values, y_values, degree):
    '''
    Interpolates a polynomial of the given degree through the provided x and y values.
    
    Parameters:
    x_values (array-like): The x coordinates of the data points.
    y_values (array-like): The y coordinates of the data points.
    degree (int): The degree of the polynomial to fit.
    
    Returns:
    poly_func (np.poly1d): The polynomial function.
    '''
    coefficients = np.polyfit(x_values, y_values, degree)
    poly_func = np.poly1d(coefficients)
    return poly_func

def rsum(f, a, b, n = 1000):
    """
    Riemann sum of f(x) (a to b). Larger n is more accurate to the integral.
    """
    dx = (b - a)/n
    s = 0
    for i in range(n):
        s += dx * f(dx * i)
    return s

riemann_sum = rsum

def trapezoidal_rule(f, a, b, n = 100):
    """
    Trapezoidal approximation of f(x) (a to b). Larger n is more accurate to the integral.
    """
    x = f(a) + f(b)
    d = (b - a)/n
    for i in range(1, n):
        x += 2 * f(i * d + a)
    return x/2 * d

def disk_volume(f, a, b, n = 100, int_approx = trapezoidal_rule):
    """
    The volume of the figure formed by rotating f(x) around the x-axis (or f(y) around the y-axis). Larger n is more accurate.
    """
    return pi * int_approx(lambda x: f(x) ** 2, a, b, n = n)

def washer_volume(f, g, a, b, n = 100):
    """
    Calculates the volume between two functions. You may wish to verify points of intersection. Larger n is more accurate.
    """
    return disk_volume(f, a, b, n = n) - disk_volume(g, a, b, n = n)

def shell_volume(f, a, b, n = 100, g = lambda x: 0, R = lambda x: x, int_approx = trapezoidal_rule):
    """
    Calculates the volume between f(x) and g(x) from a to b given R(x). Larger n is more accurate.
    """
    return 2 * pi * int_approx(lambda x: (f(x) - g(x)) * R(x), a, b, n = n)

def point_derivative(f_of, x, h = 0.00001):
    """
    Returns the derivative of any function at a point x. Smaller h is more accurate.
    """
    return round(1 / (12 * h) * (f_of(x - 2 * h) - 8 * f_of(x - h) + 8 * f_of(x + h) - f_of(x + 2 * h)), 7)

def derivative(f_of, x, h = 0.00001):
    """
    Returns the derivative of any function at a point x. Smaller h is more accurate.
    """
    return 1 / (12 * h) * (f_of(x - 2 * h) - 8 * f_of(x - h) + 8 * f_of(x + h) - f_of(x + 2 * h))

def limit_derivative(f, x, h = 0.00001):
    """
    Returns the derivative of any function at a point x. Smaller h is more accurate.
    """
    return (f(x + h) - f(x))/h

def newton_approx(f, initial, n = 100, h = 0.00001, dydx = point_derivative):
    """
    Approximates the 0 of f(x) closest to the inital approximation. Smaller h, accurate.
    """
    for i in range(n):
        initial = initial - f(initial)/limit_derivative(f, initial, h = h)
    return initial

def limit(f, x, h=0.00001):
    """
    [BETA]
    Calculates the limit of a function f(x) as x approaches a given value. Smaller h is cen be more accurate.
    Not always accurate. Only for simple limits.
    """
    return (f(x + h) - f(x - h)) / (2 * h)

def convergence_test(f, h = 0.00001):
    """
    [BETA]
    Tests the convergence of the sum of all terms of f(n). 
    Smaller h is can be more accurate.
    Not always accurate.
    """
    return limit(lambda x: f(x)/f(x + 1), x = float('inf'), h = h) < 1

def gamma(x, a = 0.001, b = 100, int_approx = trapezoidal_rule):
    """
    Computes the gamma function (factorial but offset) of x. a closer to 0 and larger b are more accurate.
    """
    gammaF = lambda t: t**(x - 1) * e ** -t
    return int_approx(gammaF, a, b)

def pi_function(x, a = 0.001, b = 100, int_approx = trapezoidal_rule):
    """
    Computes the pi (factorial, offset gamma) function of x. a closer to 0 and larger b are more accurate.
    """
    return gamma(x + 1, a = a, b = b, int_approx = int_approx)

def local_minima(f, a, b, h = 0.00001):
    """
    Finds the local minimum of a function f(x) from a to b. Smaller h is more accurate.
    """
    l = []
    x = a
    while x <= b:
        if f(x - h) > f(x) and f(x + h) > f(x):
            l.append(x)
        x += h
    return l

def local_maxima(f, a, b, h = 0.00001):
    """
    Finds the local maximum of a function f(x) from a to b. Smaller h is more accurate.
    """
    l = []
    x = a
    while x <= b:
        if f(x - h) < f(x) and f(x + h) < f(x):
            l.append(x)
        x += h
    return l

def partial_derivative(function, inputs, var_idx, h = 0.0001):
    """
    Partial derivative with respect to the variable whose index is specified.
    """
    fi = function(*inputs)
    inputs[var_idx] += h
    return (function(*inputs) - fi) / h

def del_operator(function, inputs, h = 0.0001):
    """
    The vector at the location of the inputs.
    """
    vec = []
    for i in range(len(inputs)):
        vec.append(partial_derivative(function, inputs, i, h = h))
    return vec

def directional_derivative(vec, inputs, function, h = 0.0001):
    """
    Dot product of the del operator with the corresponding unit vector.
    """
    mag = (vec[0] ** 2 + vec[1] ** 2) ** (1/2)
    vec = [i / mag for i in vec]
    delop = del_operator(function, inputs, h = h)
    new = list(zip(vec, delop))
    for i in range(len(new)):
        new[i] = new[i][0] * new[i][1]
    return new

def tangent_line(function, x, h = 0.001, derivative = point_derivative):
    """
    Tangent line to a function at point x
    """
    return lambda X: derivative(function, x, h = h) * (X - x) + function(x)

def tangent_plane(function, x, y, h = 0.001, partial = partial_derivative):
    """
    Tangent plane to a function at point x, y
    """
    return lambda X, Y: partial(function, [x, y], 0, h = h) * (X - x) + partial(function, [x, y], 1, h = h) * (Y - y) + function(x, y)

def nth_derivative(n, function, x, h = 0.0001, derivative = point_derivative):
    """
    Finds the nth derivative at a point for a given function
    """
    if n < 1:
        raise ValueError
    if n == 1:
        return derivative(function, x, h = h)
    return nth_derivative(n - 1, lambda X: derivative(function, X, h = h))

def taylor_approx(function, x, terms, h = 0.001):
    """
    Numerical Taylor series approximation accurate at x.
    """
    return lambda X: sum([(1 / factorial(i)) * nth_derivative(i, function, x, h = h) * (X - x) ** i for i in range(1, terms + 1)]) + function(x)
   
def taylor_coefficients(function, x, terms, h = 0.001, with_factorial = True):
    """
    Numerical Taylor series coefficients. Choose to ignore factorial for speed.
    """
    if with_factorial:
        return [(1 / factorial(i)) * nth_derivative(i, function, x, h = h) for i in range(1, terms + 1)]
    return [nth_derivative(i, function, x, h = h) for i in range(1, terms + 1)]

def maclaurin_approx(function, terms, h = 0.001, taylor_alg = taylor_approx):
    """
    Numerical Maclaurin series approximation for accuracy analysis.
    """
    return taylor_alg(function, 0, terms, h = h)

def maclaurin_coefficients(function, terms, h = 0.001, with_factorial = True, taylor_alg = taylor_coefficients):
    """
    Numerical Taylor series coefficients. Choose to ignore factorial for speed.
    """
    return taylor_alg(function, 0, terms, h = h, with_factorial = with_factorial)

def divergence(functions, inputs, h = 0.001, partial = partial_derivative):
    """
    The divergence of the vector field composed of many functions and a set of coordinates
    """
    s = 0
    for i in range(len(inputs)):
        s += partial(i, inputs, functions[i], h = h)
    return s

def curl(functions, inputs, h = 0.001, partial = partial_derivative):
    """
    The curl of the vector field composed of many functions and a set of coordinates
    """
    curl_matrix = [[0] * inputs for _ in range(inputs)]
    for i in range(inputs):
        for j in range(i + 1, inputs):
            partial_i = lambda *args: partial(i, args, functions[j])
            partial_j = lambda *args: partial(j, args, functions[i])
            curl_matrix[i][j] = partial_i(*[0]*inputs) - partial_j(*[0]*inputs)
            curl_matrix[j][i] = -curl_matrix[i][j]
    return curl_matrix

def f_derivative(f_of, h = 0.00001):
    """
    The function for the derivative of f(x)
    """
    return lambda x: derivative(f_of, x, h = h)

def f_partial_derivative(function, var_idx, h = 0.0001):
    """
    The function for the partial derivative of any function
    """
    return lambda *args: partial_derivative(function, args, var_idx, h = h)

def f_del_operator(function, h = 0.0001):
    """
    The function for the del operator of any function
    """
    return lambda *args: del_operator(function, args, h = h)

def f_directional_derivative(vec, inputs, function, h = 0.0001):
    """
    The function for the directional derivative of any function
    """
    return lambda *args: directional_derivative(vec, args, function, h = h)

def f_nth_derivative(n, function, h = 0.0001, derivative = point_derivative):
    """
    The function for the nth derivative of f(x)
    """
    return lambda x: nth_derivative(n, function, x, h = h, derivative = derivative)

def f_divergence(functions, h = 0.001, partial = partial_derivative):
    """
    The function for the divergence of any function
    """
    return lambda *args: divergence(functions, args, h = h, partial = partial)

def f_curl(functions, h = 0.0001):
    """
    The function for the curl of any function
    """
    return lambda *args: curl(functions, args, h = h)

def nth_partial_derivative(n, f_of, inputs, var_idx, h = 0.0001):
    """
    nth Partial derivative with respect to the variable whose index is specified.
    """
    if n < 1:
        raise ValueError
    if n == 1:
        return partial_derivative(f_of, inputs, var_idx, h = h)
    return nth_partial_derivative(n, f_partial_derivative(f_of, var_idx), inputs, var_idx, h = h)

def double_partial_xy(f_of, x, y, h = 0.0001):
    """
    Computes partial squared f / (partial x partial y)
    """
    return partial_derivative(f_partial_derivative(function, 0, h = h), [x, y], 1, h = h)

def f_double_partial_xy(f_of, h = 0.0001):
    """
    Computes the function partial squared f / (partial x partial y)
    """
    return lambda x, y: double_partial_xy(f_of, x, y, h = h)

def max_min_saddle(f_of, x, y, h = 0.0001):
    """
    Calculates (second partial x)(second partial y) - (second partial x, y) ** 2
    """
    return nth_partial_derivative(2, f_of, [x, y], 0, h = h) * nth_partial_derivative(2, f_of, [x, y], 1, h = h) - double_partial_xy(f_of, x, y, h = h) ** 2

def jacobian_matrix(functions, point, h = 0.0001):
    """
    Computes the Jacobian matrix of a vector function at a given point.
    """
    n = len(functions)
    m = len(point)
    jacobian = [[0] * m for _ in range(n)]
    
    for i in range(n):
        for j in range(m):
            jacobian[i][j] = partial_derivative(functions[i], point, j, h)
    
    return jacobian

def jacobian_determinant(functions, point, h = 0.0001):
    """
    Computes the determinant of the Jacobian matrix of a vector function at a given point.
    """
    jacobian = jacobian_matrix(functions, point, h)
    return jacobian[0][0] * jacobian[1][1] - jacobian[0][1] * jacobian[1][0]

def f_jacobian_matrix(functions, h = 0.0001):
    """
    Jacobian matrix as a function
    """
    return lambda point: jacobian_matrix(functions, point, h = h)

def f_jacobian_determinant(functions, h = 0.0001):
    """
    Jacobian determinant as a function
    """
    return lambda point: jacobian_determinant(functions, point, h = h)

def double_integral(f, a, b, c, d, nx=100, ny=100):
    """
    Approximate the volume under the surface f(x, y) over the rectangular region [a, b] x [c, d]
    using the double trapezoidal rule.
    """
    hx = (b - a) / nx
    hy = (d - c) / ny
    volume = 0

    for i in range(nx + 1):
        for j in range(ny + 1):
            x = a + i * hx
            y = c + j * hy
            weight = 1
            if i == 0 or i == nx:
                weight *= 0.5
            if j == 0 or j == ny:
                weight *= 0.5
            volume += weight * f(x, y)

    volume *= hx * hy
    return round(volume, 7)

def line_integral(f, x, y, a, b):
    '''
    The line integral under f(x, y) using parametric functions x and y of t
    a <= t <= b
    '''
    return trapezoidal_rule(lambda t: f(x(t), y(t)) * (derivative(x, t) ** 2 + derivative(y, t) ** 2) ** (1/2), a, b)

"""
END OF CALCULUS
"""
