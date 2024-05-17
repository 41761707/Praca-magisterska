def update_home_team(h_att_i, h_def_i, a_att_i, a_def_j, a_att_j, s_h, s_a, l, phi_1):
    h_att_i = max((h_att_i + l * phi_1 * (s_h - ((h_att_i + a_def_j) / 2))), 0)
    a_att_i = max((a_att_i + l * (1 - phi_1) * (s_h - ((h_att_i + a_def_j) / 2))), 0)
    h_def_i = max((h_def_i + l * phi_1 * (s_a - ((a_att_j + h_def_i) / 2))), 0)
    a_def_i = max((a_def_i + l * (1 - phi_1) * (s_a - ((a_att_j + h_def_i) / 2))), 0)

    return h_att_i, a_att_i, h_def_i, a_def_i 
def update_away_team(a_att_j, h_att_j, a_def_j, h_def_j, h_def_i, h_att_i, s_h, s_a, l,phi_2):
    a_att_j = max((a_att_j + l * phi_2 * (s_a - ((a_att_j + h_def_i) / 2))), 0)
    h_att_j = max((h_att_j + l * (1 - phi_2) * (s_a - ((a_att_j + h_def_i) / 2))), 0)
    a_def_j = max((a_def_j + l * phi_2 * (s_h - ((h_att_i + a_def_j) / 2))), 0)
    h_def_j = max((h_def_j + l * (1 - phi_2) * (s_h - ((h_att_i + a_def_j) / 2))), 0)
    
    return a_att_j, h_att_j, a_def_j, h_def_j

def main():
    l = 0.4
    phi_1 = 0.5
    phi_2 = 0.5
    h_att_i = 0
    h_def_i = 0
    a_att_i = 0
    a_def_i = 0
    s_h = 0
    s_a = 0