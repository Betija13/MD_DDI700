import numpy as np
import math
import sympy as sp
from tqdm import tqdm


def get_matrix(theta_d, alfa_d, a, s):
    if isinstance(theta_d, (int, float)):
        theta = math.radians(theta_d)
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
    else:
        cos_theta = sp.cos(theta_d)
        sin_theta = sp.sin(theta_d)
    if isinstance(alfa_d, (int, float)):
        alfa = math.radians(alfa_d)
        cos_alfa = np.cos(alfa)
        sin_alfa = np.sin(alfa)
    else:
        cos_alfa = sp.cos(alfa_d)
        sin_alfa = sp.sin(alfa_d)
    B_matrix = [
        [cos_theta, -sin_theta*cos_alfa, sin_theta*sin_alfa, a*cos_theta],
        [sin_theta, cos_theta*cos_alfa, -cos_theta*sin_alfa, a*sin_theta],
        [0, sin_alfa, cos_alfa, s],
        [0, 0, 0, 1]
    ]

    return B_matrix


alfa_1 = sp.symbols('alfa_1')
alfa_2 = sp.symbols('alfa_2')
theta_1 = sp.symbols('theta_1')

alfa_4 = 60

alfa_1_prim = -90
s_1_prim = 486.5
s_1 = 150
s_2 = 700
s_3 = 600
s_4 = 265

x_value = 900
y_value = 300
z_value = 800

print(f"Nemainīgie lielumi:\n\talfa_1_prim: {alfa_1_prim}\n\ts_1_prim: {s_1_prim}\n\ts_1: {s_1}\n\ts_2: {s_2}"
      f"\n\ts_3: {s_3}\n\ts_4: {s_4}")
print(f"Mana varianta leņķi:\n\talfa_4: {alfa_4}")
print(f"Dotās koordinātas:\n\tx: {x_value}\n\ty: {y_value}\n\tz: {z_value}")
print(f"Jāaprēķina:\n\talfa_1: ?\n\talfa_2: ?\n\ttheta_1: ?")


x, y, z = sp.symbols('x y z')

def get_coordinates(theta_1, alfa_1_p, s_1_p, alfa_1, s_1, alfa_2, s2, alfa_4, s3, s4):
    B_1 = get_matrix(theta_1, alfa_1_p, 0, s_1_p)
    B_2 = get_matrix(0, alfa_1, 0, s_1)
    B_3 = get_matrix(0, alfa_2, 0, s2)
    B_4 = get_matrix(0, -alfa_4, 0, s3)
    B_5 = get_matrix(0, 0, 0, s4)

    result = np.dot(np.dot(np.dot(np.dot(B_1, B_2), B_3), B_4), B_5)

    x_prim = result[0][-1]
    y_prim = result[1][-1]
    z_prim = result[2][-1]

    return x_prim, y_prim, z_prim

def angle_post_processing(solutions, range_alfa_1, range_alfa_2, range_theta_1):
    list_deg = [[math.degrees(sol[0]), math.degrees(sol[1]), math.degrees(sol[2])] for sol in solutions]
    list_deg = [[-(each_list[0] - 90), -90 - each_list[1], each_list[2] + 90] for each_list in list_deg]
    list_deg = [
        [(angle + 360) % 360 - 360 if angle <= -360 else (angle - 360) % 360 if angle >= 360 else angle for angle in
         values]
        for values in list_deg
    ]
    list_deg_rounded = [[round(float(val), 2) for val in inner] for inner in list_deg]
    unique_deg = list(map(list, set(map(tuple, list_deg_rounded))))
    only_valid_values = [lst for lst in unique_deg if range_alfa_1[0] <= lst[0] <= range_alfa_1[1] and
                         range_alfa_2[0] <= lst[1] <= range_alfa_2[1] and range_theta_1[0] <= lst[2] <= range_theta_1[
                             1]]
    return only_valid_values


x_prim, y_prim, z_prim = get_coordinates(theta_1, alfa_1_prim, s_1_prim, alfa_1, s_1, alfa_2, s_2, alfa_4, s_3, s_4)

x_p_simplified = sp.simplify(x_prim)
y_p_simplified = sp.simplify(y_prim)
z_p_simplified = sp.simplify(z_prim)
print(f"\nVienādojumi:\n\tx_prim = {x_p_simplified}\n\ty_prim = {y_p_simplified}\n\tz_prim = {z_p_simplified}")


eq1 = sp.Eq(x_p_simplified, x)
eq2 = sp.Eq(y_p_simplified, y)
eq3 = sp.Eq(z_p_simplified, z)

eq1_sub = eq1.subs({x: x_value})
eq2_sub = eq2.subs({y: y_value})
eq3_sub = eq3.subs({z: z_value})


target_values = [eq1_sub, eq2_sub, eq3_sub]
range_alfa_1 = (-90, 150)
range_alfa_2 = (-245, 65)
range_theta_1 = (-180, 180)

step = 15

# Vispārīgais atrisinājums
# solutions = sp.solve((eq1_sub, eq2_sub, eq3_sub), (alfa_1, alfa_2, theta_1))

solutions = []
for a1 in tqdm(np.arange(range_alfa_1[0], range_alfa_1[1], step)):
    for a2 in np.arange(range_alfa_2[0], range_alfa_2[1], step):
        for t1 in np.arange(range_theta_1[0], range_theta_1[1], step):
            try:
                solution = sp.nsolve(target_values, (alfa_1, alfa_2, theta_1), (math.radians(90-a1),
                                                                                math.radians(-90-a2),
                                                                                math.radians(t1-90)))
                solutions.append(solution)
            except Exception as e:
                pass

solutions_degrees = angle_post_processing(solutions, range_alfa_1, range_alfa_2, range_theta_1)
print(f"Kopā pieejamas {len(solutions_degrees)} leņķu opcijas")
i = 1
for angles in solutions_degrees:
    alph_1_answer = angles[0]
    alph_2_answer = angles[1]
    theta_1_answer = angles[2]
    print(f"\nLeņķi {i}. opcija: \n\talfa_1 = {alph_1_answer}\n\talfa_2 = {alph_2_answer}\n\ttheta_1 = {theta_1_answer}")
    i += 1
