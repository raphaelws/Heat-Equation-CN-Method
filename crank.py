import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rc('font', size=18)
matplotlib.rc('font', family='Arial')

N = 31 #numero de pontos na malha
sigma = 1 #coeficiente de difusao 
dt = 0.002 #delta tempo
L = float(1) #tamanho da malha
nsteps = 200 #numero de passos
dx = L/(N-1) #espacamento calculado com base no numero de pontos
nplot = 5 #fazer uma imagem a cada nplots passos
pi=np.pi

r = sigma*dt/dx**2 
print(r)

#Matrizes A e B, vetor b
A = np.zeros((N-2,N-2))
B = np.zeros((N-2,N-2))
b = np.zeros((N-2))


#Colocamosas as entradas
for i in range(N-2):
    if i==0:
        A[i,:] = [2+2*r if j==0 else (-r) if j==1 else 0 for j in range(N-2)]
        B[i,:] = [2-2*r if j==0 else r if j==1 else 0 for j in range(N-2)]
        b[i] = 0. #condicoes de contorno em i=1
    elif i==N-3:
        A[i,:] = [-r if j==N-4 else 2+2*r if j==N-3 else 0 for j in range(N-2)]
        B[i,:] = [r if j==N-4 else 2-2*r if j==N-3 else 0 for j in range(N-2)]
        b[i] = 0. #condicoes de contorno em i=N
    else:
        A[i,:] = [-r if j==i-1 or j==i+1 else 2+2*r if j==i else 0 for j in range(N-2)]
        B[i,:] = [r if j==i-1 or j==i+1 else 2-2*r if j==i else 0 for j in range(N-2)]

#malha
x = np.linspace(0,1,N)
#consicoes iniciais 
u = np.asarray([np.sin(np.pi*xx) for xx in x])
#faz o calculo para t=0
bb = B.dot(u[1:-1]) + b
ureal = np.linspace(0,1,N)

k = 0
for j in range(nsteps):
    #prina o numero de passos
    print(j)
    #encontra a solucao para esse passo
    #Ax=bb
    u[1:-1] = np.linalg.solve(A,bb)
    #encontra o u analitico
    ureal = np.exp(-pi**2*j*dt)*np.sin(pi*x)
    #atualiza o bb
    bb = B.dot(u[1:-1]) + b
    #faz o plot a cada nplot passos
    if(j%nplot==0): 
        plt.plot(x,u,linewidth=2,label="CN")
        plt.plot(x,ureal,linewidth=2,label="Analitico")
        plt.ylim([0,1])
        filename = 'heat' + str(k+1).zfill(3) + '.jpg';
        plt.xlabel("x")
        plt.ylabel("u")
        plt.legend(loc=1, prop={'size': 10})
        plt.title("t = %2.2f"%(dt*(j+1)))
        plt.savefig("./heat-evolution/"+filename,format="jpg")
        plt.clf()
        k += 1
