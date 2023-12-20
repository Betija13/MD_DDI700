import numpy as np
import math
import plotly.graph_objs as go


def get_matrix(theta_d, alfa_d, a, s):
    theta = math.radians(theta_d)
    alfa = math.radians(alfa_d)
    B_matrix = [
        [np.cos(theta), -np.sin(theta)*np.cos(alfa), np.sin(theta)*np.sin(alfa), a*np.cos(theta)],
        [np.sin(theta), np.cos(theta)*np.cos(alfa), -np.cos(theta)*np.sin(alfa), a*np.sin(theta)],
        [0, np.sin(alfa), np.cos(alfa), s],
        [0, 0, 0, 1]
    ]
    return B_matrix


def get_coordinates_for_plot(B_1, B_2, B_3, B_4, B_5):
    x_c = [0]
    y_c = [0]
    z_c = [0]
    x_c.append(B_1[0][-1])
    y_c.append(B_1[1][-1])
    z_c.append(B_1[2][-1])
    first_point = np.dot(B_1, B_2)
    x_c.append(first_point[0][-1])
    y_c.append(first_point[1][-1])
    z_c.append(first_point[2][-1])

    second_point = np.dot(first_point, B_3)
    x_c.append(second_point[0][-1])
    y_c.append(second_point[1][-1])
    z_c.append(second_point[2][-1])

    third_point = np.dot(second_point, B_4)
    x_c.append(third_point[0][-1])
    y_c.append(third_point[1][-1])
    z_c.append(third_point[2][-1])

    fourth_point = np.dot(third_point, B_5)
    x_c.append(fourth_point[0][-1])
    y_c.append(fourth_point[1][-1])
    z_c.append(fourth_point[2][-1])
    return x_c, y_c, z_c


def draw_plot(x_c, y_c, z_c):

    fig = go.Figure()

    # Scatter plot with lines connecting points
    fig.add_trace(go.Scatter3d(x=x_c, y=y_c, z=z_c, mode='lines+markers', marker=dict(color='blue', size=6)))

    fig.update_layout(scene=dict(xaxis=dict(title='X Axis'),
                                 yaxis=dict(title='Y Axis'),
                                 zaxis=dict(title='Z Axis')),
                      margin=dict(l=0, r=0, b=0, t=0))

    fig.show()

alfa_1 = 60
alfa_2 = -30
alfa_4 = -60

theta_1 = -30

alfa_1_prim = -90
s_1_prim = 486.5
s_1 = 150
s_2 = 700
s_3 = 600
s_4 = 265

print(f"Nemainīgie lielumi:\n\talfa_1_prim: {alfa_1_prim}\n\ts_1_prim: {s_1_prim}\n\ts_1: {s_1}\n\ts_2: {s_2}"
      f"\n\ts_3: {s_3}\n\ts_4: {s_4}")
print(f"Mana varianta leņķi:\n\talfa_1: {alfa_1}\n\talfa_2: {alfa_2}\n\talfa_4: {alfa_4}\n\ttheta_1: {theta_1}")
print(f"Jāaprēķina:\n\tx: ?\n\ty: ?\n\tz: ?")

B_1 = get_matrix(theta_1-90, alfa_1_prim, 0, s_1_prim)
B_2 = get_matrix(0, 90-alfa_1, 0, s_1)
B_3 = get_matrix(0, -90-alfa_2, 0, s_2)
B_4 = get_matrix(0, -alfa_4, 0, s_3)
B_5 = get_matrix(0, 0, 0, s_4)

result = np.dot(np.dot(np.dot(np.dot(B_1, B_2), B_3), B_4), B_5)
x_coord = result[0][-1]
y_coord = result[1][-1]
z_coord = result[2][-1]
print(f"\nManipulatora gala pozicionēšanas koordinātas: \n\tx: {round(x_coord, 2)}\n\ty: {round(y_coord, 2)}"
      f"\n\tz: {round(z_coord, 2)}")

x_c, y_c, z_c = get_coordinates_for_plot(B_1, B_2, B_3, B_4, B_5)
draw_plot(x_c, y_c, z_c)


