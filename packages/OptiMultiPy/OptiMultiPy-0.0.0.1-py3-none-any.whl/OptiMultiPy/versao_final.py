import matplotlib.pyplot as plt
import numpy as np
import control
from functools import lru_cache

class ob:
    @staticmethod
    def imprime(Kp, Ki, Kd):
        s = control.tf('s')
        Gc = Kp + Ki / (s) + Kd * s
        G = 30 / (s**3 + 6 * s**2 + 5 * s)
        MFscompP = control.feedback(G)
        MFcompP = control.feedback(G * Kp)
        MFcompPID = control.feedback(G * Gc)
        
        plt.figure(1)
        t, y = control.step_response(MFcompPID, 10)
        tref, yref = control.step_response(s / s, 10)
        t1, y1 = control.step_response(MFscompP, 10)
        plt.plot(t1, y1, t, y, tref, yref)
        plt.title('Resposta ao degrau')
        plt.xlabel('tempo [s]')
        plt.ylabel('Amplitude')
        plt.legend(["Sem compensador", "Com compensador", "Referência"])
        plt.grid(True)
        plt.show()

    @staticmethod
    @lru_cache(maxsize=None)
    def funcao_transferencia(Kp, Ki, Kd, G):
        s = control.tf('s')
        Gc = Kp + Ki / (s) + Kd * s
        MFscompP = control.feedback(G)
        MFcompP = control.feedback(G * Kp)
        MFcompPID = control.feedback(G * Gc)
        polos = control.pole(MFcompPID)
        parte_real_polos = np.real(polos)
        for valor in parte_real_polos:
            if valor > 0:
                return "não"
        t, y = control.step_response(MFcompPID, 10)
        s = control.step_info(MFcompPID)
        rise_time = s['RiseTime']
        settling_time = s['SettlingTime']
        overshoot = s['Overshoot']
        Overshoot = (y.max() / y[-1] - 1) * 100
        SettlingMin = s['SettlingMin']
        SettlingMax = s['SettlingMax']
        Peak = s['Peak']
        PeakTime = s['PeakTime']
        steady_state_error = 1 - y[-1]
        funcao_custo = (Overshoot * 10 + rise_time * 2 + settling_time * 3 + steady_state_error * 4 +
                        abs(steady_state_error) * 15 + abs(SettlingMin) + abs(SettlingMax) * 3 + abs(Peak) + abs(PeakTime))

        return funcao_custo

    @staticmethod
    def main(G):
        n_p = 10
        dim = 3
        Fmax = 5
        Fmin = 0
        alfa0 = 1
        alfa1 = 2
        beta0 = 0.1
        beta1 = 2
        T = 100

        xi = np.random.rand(n_p, dim) * (Fmax - Fmin) + Fmin
        m = np.random.rand(n_p, dim) * (Fmax - Fmin) + Fmin

        aux2 = 0
        for per in range(0, n_p):
            aux2 = ob.funcao_transferencia(m[per, 0], m[per, 1], m[per, 2], G)
            while aux2 == "não":
                m[per, :] = np.random.rand(1, dim) * (Fmax - Fmin) + Fmin
                aux2 = ob.funcao_transferencia(m[per, 0], m[per, 1], m[per, 2], G)

        apditao = []
        aux = 0
        for per in range(0, n_p):
            aux = ob.funcao_transferencia(xi[per, 0], xi[per, 1], xi[per, 2], G)
            while aux == "não":
                xi[per, :] = np.random.rand(1, dim) * (Fmax - Fmin) + Fmin
                aux = ob.funcao_transferencia(xi[per, 0], xi[per, 1], xi[per, 2], G)

            apditao.append(aux)

        apditao, poss = np.sort(apditao), np.argsort(apditao)

        ind_best = poss[0]
        ind_gbest = poss[0]
        best, gbest = xi[ind_best, :], xi[ind_best, :]

        custo = []

        for t in range(1, T + 1):
            Td = alfa0 * np.exp(-1 * alfa1 * (t / T) ** alfa1)
            Pp = beta0 * np.log(beta1 * (t / T) ** beta0)
            y = np.random.rand(1, dim) * (Fmax - Fmin) + Fmin

            xi1 = np.empty_like(xi)
            for i in range(n_p):
                r1, r2, r3, r4 = np.random.rand(), np.random.rand(), np.random.rand(), np.random.rand()
                if r3 >= 0.5:
                    if r4 >= Pp:
                        xi1[i, :] = gbest + (Td * (best - y) * r1 + Td * (y - m[i, :]) * r2) * np.sign(np.random.rand() - 0.5)
                    else:
                        xi1[i, :] = Td * np.random.rand(1, dim) * (Fmax - Fmin) + Fmin
                else:
                    xi1[i, :] = gbest - (Td * (best - y) * r1 + Td * (y - m[i, :]) * r2) * np.sign(np.random.rand() - 0.5)

            apditao1 = []
            aux1 = 0
            for per in range(0, n_p):
                aux1 = ob.funcao_transferencia(xi1[per, 0], xi1[per, 1], xi1[per, 2], G)
                while aux1 == "não":
                    xi1[per, :] = xi[per, :]
                    aux1 = ob.funcao_transferencia(xi1[per, 0], xi1[per, 1], xi1[per, 2], G)
                apditao1.append(aux1)

            poss1 = np.argsort(apditao1)
            ind_best1 = poss1[0]

            best = xi1[ind_best1, :]
            if ob.funcao_transferencia(best[0], best[1], best[2], G) <= ob.funcao_transferencia(gbest[0], gbest[1], gbest[2], G):
                gbest = best

            for i in range(n_p):
                apditao_Marjaneh = ob.funcao_transferencia(m[i, 0], m[i, 1], m[i, 2], G)
                if apditao_Marjaneh <= apditao1[i]:
                    m[i, :] = xi1[i, :]

            custo.append(ob.funcao_transferencia(gbest[0], gbest[1], gbest[2], G))

        return gbest, custo, T

#s = control.tf('s')
#G = 30 / (s**3 + 6 * s**2 + 5 * s)

#gb, ct, T = ob.main(G)

#plt.figure(3)
#t = np.arange(1, T + 1)
#plt.plot(t, ct)
#plt.xlabel('Iteração')
#plt.ylabel('Custo')
#plt.show()

