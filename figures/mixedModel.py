import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import os
name = os.path.basename(__file__).split(".py")[0]#name="prueba"
pdf = matplotlib.backends.backend_pdf.PdfPages(name+".pdf")
###############

"""
if __package__ is None or __package__ == '':
    # uses current directory visibility
    import sys
    sys.path.append('..')
    print("__package__ None!")
"""
import sys
sys.path.append('..')
from ablr.mixed.mixedModel import *
from ablr.linear.basisFunctions import polynomial_basis_function
import numpy as np
import math
from scipy.stats import multivariate_normal as normal
# Training dataset sizes

M, L = 2, 10
n = [3]*L
N = sum(n)

w_true = np.array([1,-1]).reshape((M,1))
v_true = np.arange(L).reshape((L,1))

def dijoint_sample(n, M, L, w_true, v_true, alpha = (1e-5)**2, beta = (10.0)**2, R=1):
    X = np.zeros((N,1))
    for i in range(L):
        X[(n[i]*i):n[i]*(i+1),:] = (np.random.rand(n[i],1)+i)*2/L -1
    
    '''
    X = np.random.rand(N,1)*2 -1
    '''
    
    Phi = polynomial_basis_function(X,range(M))
    
    C = np.zeros((N,R*L))
    for i in range(L):#i=1
        # Intercept
        pos = np.arange((n[i]*i),n[i]*(i+1))
        for r in range(R):
            C[pos,(r*L)+i] = Phi[pos,r]
        
    epsilon = np.random.normal(0,np.sqrt(1/beta), N).reshape((N,1))
    t = Phi.dot(w_true) + C.dot(v_true) + epsilon 
    return t, X, Phi, C, alpha, beta
    
t, X, Phi, C, alpha, beta = dijoint_sample(n, M, L, w_true, v_true,alpha=0.0001)

m, S = moments_posterior(t,Phi,C,alpha,beta)
mw_N, Sw_N = p_de_w_dado_t(t,Phi,C,alpha,beta)
mv_N, Sv_N = p_de_v_dado_t(t,Phi,C,alpha,beta)

Phi.shape

m[1][0] == mv_N
m[1][1] == mw_N
S[1][0][0] == Sv_N
S[1][1][1] == Sw_N


for i in range(L):#i=0
    plt.plot([-1,1],[mw_N[0]+mv_N[i]-mw_N[1],mw_N[0]+mv_N[i]+mw_N[1]],color="gray" )
    plt.plot(X[(n[i]*i):n[i]*(i+1),0],t[(n[i]*i):n[i]*(i+1),0], '.')
plt.xticks(fontsize=12) # rotation=90
plt.yticks(fontsize=12) # rotation=90
plt.title("Same slope")
plt.savefig("pdf/mixedModel_linearSameSlope.pdf")
plt.close()    

"""
fig = plt.figure()   
rep = 20
MAPw = np.zeros((rep,M))
MAPv = np.zeros((rep,L))
for r in range(rep):
    
    t, X, Phi, C, alpha, beta = dijoint_sample(n, M, L, w_true, v_true,alpha=0.01)
    mw_N, Sw_N = p_de_w_dado_t(t,Phi,C,alpha,beta)
    mv_N, Sv_N = p_de_v_dado_t(t,Phi,C,alpha,beta)
    
    MAPw[r,] = mw_N.T
    MAPv[r,] = mv_N.T
    
    for i in range(L):#i=0
        plt.plot([-1,1],[mw_N[0]+mv_N[i]-mw_N[1],mw_N[0]+mv_N[i]+mw_N[1]],color="gray" )
        #plt.plot(X[(n[i]*i):n[i]*(i+1),0],t[(n[i]*i):n[i]*(i+1),0], '.')
for i in range(L):#i=0
    plt.plot([-1,1],[w_true[0]+v_true[i]-w_true[1],w_true[0]+v_true[i]+w_true[1]],'--',color="red" )
plt.close()

plt.plot(MAPw[:,0],MAPw[:,1],'.')
plt.plot(5,-1,'.',color="red")


M, L = 2, 10
n = [3]*L
N = sum(n)

t, Phi, C, alpha, beta = dijoint_sample(n, M, L, w_true, v_true,alpha=1e-4,beta=1e5)
mw_N, Sw_N = p_de_w_dado_t(t,Phi,C,alpha,beta)
    

def _posterior(x, y):
    return normal.pdf(np.array([x,y]).ravel(),mw_N.ravel(),Sw_N)
_posterior_v = np.vectorize(_posterior)

w0_grilla =  np.linspace(-10, 20, 50).reshape(-1, 1)
w1_grilla =  np.linspace(-2, 0, 50).reshape(-1, 1)

X_, Y_ = np.meshgrid(w0_grilla , w1_grilla )

belief = _posterior_v(X_,Y_)
plt.imshow(belief,extent=[0,10,-2,0],)
plt.plot(w_true[0]+sum(v_true)/L,w_true[1],'+',color="red")
plt.tight_layout()
"""

# intercept
M, L = 2, 10
n = [6]*L
N = sum(n)
R = 2
w_true = np.array([1,-1]).reshape((M,1))
v0_true = np.arange(L).reshape((L,1))
v1_true = np.linspace(-1, -6, L).reshape((L,1))
v_true = np.concatenate((v0_true,v1_true ))

t, X, Phi, C, alpha, beta = dijoint_sample(n, M, L, w_true, v_true,alpha=(1/1e3),beta=(1/1e-3),R=R)

(m_N, (mv_N, mw_N)), (S_N, [[Sv_N, Svw_N],[Swv_N, Sw_N]]) = moments_posterior(t,Phi,C,alpha,beta)

for i in range(L):#i=0
    plt.plot([-1,1], [mw_N[0]+mv_N[:L][i]-(mv_N[L:][i]+mw_N[1]), mw_N[0]+mv_N[:L][i]+(mv_N[L:][i]+mw_N[1])],color="gray" )
    plt.plot(X[(n[i]*i):n[i]*(i+1),0],t[(n[i]*i):n[i]*(i+1),0], '.')

plt.xticks(fontsize=12) # rotation=90
plt.yticks(fontsize=12) # rotation=90
plt.title("Different Intercept and slope")

plt.savefig("pdf/mixedModel_linearAllDifferent.pdf")
plt.close()    

#### End
pdf.close()

'''
# Datos reales
ftot_perf <- read.csv("../Datos/dosClases/glmm/10.csv", header =T)
for (i in seq(11,500)){ #i<-100
  file <- paste0(paste0("../Datos/dosClases/glmm/",toString(i)),".csv")
  ftot_perf <- rbind(ftot_perf,read.csv(file, header =T))
}

activity <- ftot_perf[,"team_times1"]>=1
loyalty <- ftot_perf[,"max_times12"][activity]/ftot_perf[,"team_times1"][activity]
teamOriented <- ftot_perf[,"team_times1"][activity]/ftot_perf[,"times1"][activity]
experience <- log(ftot_perf$times1,10)
skill <- log(ftot_perf[,"mean"][activity],10)
players <- ftot_perf$p

pm.prueba <-lmer(skill~loyalty*teamOriented*experience*(1|players))
names(pm.prueba)
summary(pm.prueba)
'''
