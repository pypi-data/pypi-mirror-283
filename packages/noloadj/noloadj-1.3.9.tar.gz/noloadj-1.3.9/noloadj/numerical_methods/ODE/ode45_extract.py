import jax.numpy as np
from jax import config
config.update("jax_enable_x64", True)
from jax.lax import *
from jax import custom_jvp,jvp
from functools import partial
from noloadj.numerical_methods.ODE.ode45 import next_der_step_simulation,\
    next_step_simulation,compute_new_point,odeint45,odeint45_etendu

def odeint45_extract(f,x0,*P,M=None,T=0.,h0=1e-5,tol=1.48e-8):
    '''
    Solves an ODE system described by f with Runge-Kutta 5 (7M) algorithm, without
    storing values across time and with features extraction.

    :param f: a class inherited from ODESystem abstract class that describes the ODE system
    :param x0: Array: initial state vector
    :param P: tuple : simulation parameters to optimize
    :param M: int: number of points to compute the FFT
    :param T: float: operating period of the system (optional)
    :param h0: float: initial step size
    :param tol: float: tolerance for optimal step size computation
    :return: Several outputs :
    - float : final time 'tf'
    - Array : final state vector 'xf'
    - Array : final output vector 'yf'
    - dict : extracted features dictionary 'cstr'
    - int/Array : final configuration 'state' if the system is periodic.
    '''
    return _odeint45_extract(f,h0,tol,M,x0,T,*P)

def compute_init_time_cstr(f,cstr,x0,y0,h0,dcstr=None,dx0=None,dy0=None):
    test_dcstr=not isinstance(dcstr,type(None))
    for i in f.constraints.keys():
        if isinstance(f.constraints[i], tuple):
            test_exp,feature = f.constraints[i]
        else:
            feature = f.constraints[i]
            test_exp = lambda t: True
        if feature.type=='time':
            if feature.name in f.xnames:
                ind=f.xnames.index(feature.name)
                z0=x0
                if test_dcstr:
                    dz0=dx0
            else:
                ind=f.ynames.index(feature.name)
                z0=y0
                if test_dcstr:
                    dz0=dy0
            cstr[i]=np.where(test_exp(0.),feature.init(z0[ind],0.,h0),cstr[i])
            if test_dcstr:
                dcstr[i]=np.where(test_exp(0.),feature.dinit(z0[ind],dz0[ind],
                                    0.,h0),dcstr[i])
    if test_dcstr:
        return cstr,dcstr
    else:
        return cstr

def compute_expres_time_cstr(f,cstr,t_prev,x_prev,y_prev,h_prev,t_now,x_now,
        y_now,T,dcstr=None,dx_prev=None,dy_prev=None,dx_now=None,dy_now=None,
        dT=None):
    test_dcstr=not isinstance(dcstr,type(None))
    for i in f.constraints.keys():
        if isinstance(f.constraints[i], tuple):
            test_exp,feature= f.constraints[i]
        else:
            feature=f.constraints[i]
            test_exp = lambda t: True
        if feature.type=='time':
            if feature.name in f.xnames:
                ind=f.xnames.index(feature.name)
                z_prev,z_now=x_prev,x_now
                if test_dcstr:
                    dz_prev,dz_now=dx_prev,dx_now
            else:
                ind = f.ynames.index(feature.name)
                z_prev,z_now=y_prev,y_now
                if test_dcstr:
                    dz_prev,dz_now=dy_prev,dy_now
            cstr[i] =np.where(test_exp(t_now),feature.expression(t_prev,
                        z_prev[ind],t_now,z_now[ind], cstr[i],h_prev,T),cstr[i])
            if test_dcstr:
                dcstr[i]= np.where(test_exp(t_now),feature.der_expression(
                        t_prev,z_prev[ind],dz_prev[ind],t_now,z_now[ind],dz_now
                        [ind],cstr[i],dcstr[i],h_prev,T,dT),dcstr[i])
    if test_dcstr:
        return cstr, dcstr
    else:
        return cstr

def compute_fin_time_cstr(f,cstr,tf,xf,yf,T,dcstr=None,dT=None):
    test_dcstr=not isinstance(dcstr,type(None))
    for i in f.constraints.keys():
        if isinstance(f.constraints[i],tuple):
            _,feature=f.constraints[i]
        else:
            feature=f.constraints[i]
        if feature.type == 'time':
            if feature.name in f.xnames:
                ind = f.xnames.index(feature.name)
                zf=xf
            else:
                ind = f.ynames.index(feature.name)
                zf=yf
            cstr[i]=feature.fin(tf,cstr[i],T)
            if test_dcstr:
                dcstr[i]=feature.der_fin(tf,cstr[i],T,dcstr[i],dT,zf[ind])
    if test_dcstr:
        return cstr, dcstr
    else:
        return cstr

def compute_freq_cstr(f,cstr,modX,modY,phX,phY,vect_freq,T,dcstr=None,
                      dmodX=None,dmodY=None,dphX=None,dphY=None):
    test_dcstr=not isinstance(dcstr,type(None))
    for i in f.constraints.keys():
        if isinstance(f.constraints[i], tuple):
            _, feature = f.constraints[i]
        else:
            feature = f.constraints[i]
        if feature.type == 'freq':
            if feature.name in f.xnames:
                ind = f.xnames.index(feature.name)
                modZ,phZ=modX,phX
                if test_dcstr:
                    dmodZ, dphZ = dmodX, dphX
            else:
                ind = f.ynames.index(feature.name)
                modZ,phZ=modY,phY
                if test_dcstr:
                    dmodZ, dphZ = dmodY, dphY
            if test_dcstr:
                cstr[i],dcstr[i]=feature.der_expression(modZ[ind],
                        phZ[ind],dmodZ[ind], dphZ[ind],vect_freq,1/T)
            else:
                cstr[i]=feature.expression(modZ[ind],phZ[ind],vect_freq,1/T)
    if test_dcstr:
        return cstr, dcstr
    else:
        return cstr


@partial(custom_jvp,nondiff_argnums=(0,1,2,3))
def _odeint45_extract(f,h0,tol,M,x0,T,*P):

    def cond_fn(state):
        x_prev2,x_prev,t_prev,_,h_prev,cstr,_,_=state
        return (h_prev > 0) & f.stop.cond_stop(t_prev,t_prev+h_prev,cstr,
                                               x_prev2,x_prev,T)

    def body_fn(state):
        _,x_prev,t_prev,y_prev,h_prev,cstr,i_prev,c_prev=state

        x_now,t_now,y_now,h_now,i_now,c_now=next_step_simulation(x_prev,t_prev,
                                    y_prev,i_prev,c_prev,h_prev,f,tol,T,*P)

        if f.stop.type=='threshold':
            output,seuil=x_now[f.stop.ind],f.stop.threshold
            outputprev=x_prev[f.stop.ind]
            condition=np.bitwise_not(f.stop.cond_stop(t_prev,t_now,cstr,x_prev,
                                                      x_now,T))
            x_now,h_prev,t_now,y_now=cond(condition,lambda state:
                compute_new_point(x_now,x_prev,t_prev,t_now,y_prev,y_now,
                output-seuil,outputprev-seuil),lambda state:state,(x_now,h_prev,
                                                                   t_now,y_now))
            x_now,t_now,y_now,h_now,i_now,c_now=cond(condition,lambda state:
                next_step_simulation(x_prev,t_prev,y_prev,i_prev,c_prev,h_prev,
                f,tol,T,*P),lambda state:state,(x_now,t_now,y_now,h_now,i_now,
                                                c_now))

        elif f.stop.type=='final_time':
            h_tf=f.stop.tf-t_now
            h_now=np.minimum(h_now,h_tf)

        cstr=compute_expres_time_cstr(f,cstr,t_prev,x_prev,y_prev,h_prev,t_now,
                                      x_now,y_now,T)

        return x_prev,x_now,t_now,y_now,h_now,cstr,i_now,c_now

    if f.stop.type=='steady_state':
        f.constraints=f.stop.init_dico(f.constraints,T)
    elif f.stop.type=='threshold':
        f.stop.init_ind(f.xnames)
    cstr=dict(zip(list(f.constraints.keys()),[0.]*len(f.constraints)))# INITIALISATION
    if not isinstance(f.state,type(None)):
        i0=f.state
    else:
        i0=0
    if not isinstance(f.commande,type(None)):
        c0=f.commande.next_command(0.)
    else:
        c0=0
    tempP=None
    if 'initialize' in f.__class__.__dict__:
        tempP=P
        P=f.initialize(*P)
    y0=f.output(x0,0.,*P)
    if isinstance(y0,tuple):
        x0,y0=y0
    if 'initialize' in f.__class__.__dict__:
        P=tempP

    cstr=compute_init_time_cstr(f,cstr,x0,y0,h0)

    _,xf,tf,yf,hf,cstr,ifinal,_=while_loop(cond_fn,body_fn,
                                         (x0,x0,0.,y0,h0,cstr,i0,c0))
    if not isinstance(f.state,type(None)):
        f.state=ifinal

    cstr=compute_fin_time_cstr(f,cstr,tf,xf,yf,T)
    
    if f.stop.type=='steady_state':
        f.constraints=f.stop.delete_dico(f.constraints)
        cstr=f.stop.delete_dico(cstr)

    if M!=None:
        _,modX,phX,_,modY,phY,_=odeint45(f,xf,np.linspace(tf,tf+T,M),*P,
                                        M=M,T=T,h0=h0)
        vect_freq=np.where(M//2==0,np.linspace(0.,(M/2-1)/T,M//2),
                              np.linspace(0.,(M-1)/(2*T),M//2))

        cstr=compute_freq_cstr(f,cstr,modX,modY,phX,phY,vect_freq,T)

    if not isinstance(f.state,type(None)):
        return (tf,xf,yf,cstr,ifinal)
    else:
        return (tf,xf,yf,cstr)


@_odeint45_extract.defjvp
def _odeint45_extract_jvp(f,h0,tol,M, primals, tangents):
    '''
    Solves an ODE system described by df/dP with Runge-Kutta 5 (7M) algorithm, and
    computes derivatives of extracted features w.r.t optimization inputs.

    :param f: a class that describes the ODE system
    :param h0: initial step size
    :param tol: tolerance for optimal step size computation
    :param M: number of points to compute the FFT
    :param primals: tuple including initial state vector,operating period and
        optimization inputs.
    :param tangents: tuple including differentials of initial state vector,
        operating period and optimization inputs.
    :return: the final time tf, final state vector xf, final output vector yf,extracted features dictionary cstr, their derivatives w.r.t P, and the final
    configuration state if the system is periodic.
    '''
    x0,T, *P = primals
    dx0,dT, *dP = tangents
    nPdP = len(P)

    res=odeint45_extract_etendu(f,nPdP,h0, tol,M, x0,dx0,T,dT, *P, *dP)

    if not isinstance(f.state,type(None)):
        xf,yf,cstr,tf,dtf,dxf,dyf,dcstr,states=res
        return (tf,xf,yf,cstr,states),(dtf,dxf,dyf,dcstr,states)
    else:
        xf,yf,cstr,tf,dtf,dxf,dyf,dcstr=res
        return (tf,xf,yf,cstr),(dtf,dxf,dyf,dcstr)


def odeint45_extract_etendu(f,nPdP,h0,tol,M,x0,dx0,T,dT,*P_and_dP):
    P,dP = P_and_dP[:nPdP],P_and_dP[nPdP:]

    def cond_fn(state):
        x_prev2,x_prev,_,_,_,t_prev, h_prev,cstr,_,_,_,_,_,_ = state
        return (h_prev > 0) & f.stop.cond_stop(t_prev,t_prev+h_prev,cstr,
                                               x_prev2,x_prev,T)

    def body_fn(state):
        _,x_prev,dx_prev,y_prev,dy_prev,t_prev, h_prev,cstr,\
                dcstr,i_prev,c_prev,Mat,dMat,chgt_state= state

        x_now,t_now,y_now,h_now,i_now,c_now=next_step_simulation(x_prev,t_prev,
                                        y_prev,i_prev,c_prev,h_prev,f,tol,T,*P)
        dx_now,dy_now,Mat,dMat=next_der_step_simulation(x_prev,t_prev,dx_prev,
                    x_now,t_now,h_prev,f, nPdP,chgt_state,Mat,dMat,*P_and_dP)
        chgt_state = np.bitwise_not(np.array_equal(i_now, i_prev))

        if f.stop.type=='threshold':
            output,seuil=x_now[f.stop.ind],f.stop.threshold
            outputprev=x_prev[f.stop.ind]
            condition=np.bitwise_not(f.stop.cond_stop(t_prev,t_now,cstr,x_prev,
                                                      x_now,T))
            x_now,h_prev,t_now,y_now=cond(condition,lambda state:
                compute_new_point(x_now,x_prev,t_prev,t_now,y_prev,y_now,
                output-seuil,outputprev-seuil),lambda state:state,(x_now,h_prev,
                                                                t_now,y_now))
            x_now,t_now,y_now,h_now,i_now,c_now=cond(condition,lambda state:
                next_step_simulation(x_prev,t_prev,y_prev,i_prev,c_prev,h_prev,
                f,tol,T,*P),lambda state:state,(x_now,t_now,y_now,h_now,i_now,
                                                c_now))
            dx_now,dy_now,_,_=cond(condition,lambda state:next_der_step_simulation
                (x_prev,t_prev,dx_prev,x_now,t_now,h_prev,f, nPdP,i_now,Mat,
                 dMat,*P_and_dP),lambda state:state,(dx_now,dy_now,Mat,dMat))

        elif f.stop.type=='final_time':
            h_tf=f.stop.tf-t_now
            h_now=np.minimum(h_now,h_tf)

        cstr,dcstr=compute_expres_time_cstr(f,cstr,t_prev,x_prev,y_prev,h_prev,
            t_now,x_now,y_now,T,dcstr,dx_prev,dy_prev,dx_now,dy_now,dT)

        return x_prev,x_now,dx_now,y_now,dy_now,t_now,h_now,cstr,dcstr,i_now,\
               c_now,Mat,dMat,chgt_state

    if f.stop.type=='steady_state':
        f.constraints=f.stop.init_dico(f.constraints,T)
    elif f.stop.type=='threshold':
        f.stop.init_ind(f.xnames)
    cstr=dict(zip(list(f.constraints.keys()),[0.]*len(f.constraints)))#INITIALISATION
    dcstr=dict(zip(list(f.constraints.keys()),[0.]*len(f.constraints)))

    for element in f.__dict__.keys(): # pour eviter erreurs de code
        if hasattr(f.__dict__[element],'primal'):
            f.__dict__[element]=f.__dict__[element].primal
    if not isinstance(f.state,type(None)):
        i0=f.state
    else:
        i0=0
    if not isinstance(f.commande,type(None)):
        c0=f.commande.next_command(0.)
    else:
        c0=0
    tempP,tempdP,Mat,dMat=None,None,0,0
    if 'initialize' in f.__class__.__dict__:
        tempP,tempdP=P,dP
        P,dP=jvp(f.initialize,(*P,),(*dP,))
        Mat,dMat=P,dP
    y0,dy0=jvp(f.output,(x0,0.,*P),(dx0,0.,*dP))
    if isinstance(y0,tuple):
        x0,y0=y0
        dx0,dy0=dy0
    if 'initialize' in f.__class__.__dict__:
        P,dP=tempP,tempdP

    cstr,dcstr=compute_init_time_cstr(f,cstr,x0,y0,h0,dcstr,dx0,dy0)

    chgt_state=False
    xfm1,xf,dxf,yf,dyf,tf,hf,cstr,dcstr,ifinal,_,_,_,_=while_loop(cond_fn,
        body_fn,(x0,x0,dx0,y0,dy0,0.,h0,cstr,dcstr,i0,c0,Mat,dMat,chgt_state))
    if not isinstance(f.state,type(None)):
        f.state=ifinal
    if 'initialize' in f.__class__.__dict__:
        P=f.initialize(*P)

    cstr,dcstr=compute_fin_time_cstr(f,cstr,tf,xf,yf,T,dcstr,dT)

    if f.stop.type=='threshold': # partial derivatives of ts
        dout=dxf[f.stop.ind]
        xseuil=f.timederivatives(xf,tf,*P)[f.stop.ind]
        dtf=-(1/xseuil)*dout
    elif f.stop.type=='steady_state':
        ind_rp=0
        xseuil=f.timederivatives(xf,tf,*P)[ind_rp]
        dtf=-(1/xseuil)*dxf[ind_rp]
    else:
        dtf=0.
        
    if f.stop.type=='steady_state':
        f.constraints=f.stop.delete_dico(f.constraints)
        cstr=f.stop.delete_dico(cstr)
        dcstr=f.stop.delete_dico(dcstr)

    if M!=None:
        _,_,modX,phX,dmodX,dphX,_,_,modY,phY,dmodY,dphY,_=odeint45_etendu(f,
            nPdP,h0,tol,M,xf,dxf,np.linspace(tf,tf+T,M),T,*P_and_dP)

        vect_freq=np.where(M//2==0,np.linspace(0.,(M/2-1)/T,M//2),
                              np.linspace(0.,(M-1)/(2*T),M//2))
        cstr,dcstr=compute_freq_cstr(f,cstr,modX,modY,phX,phY,vect_freq,T,dcstr,
                      dmodX,dmodY,dphX,dphY)

    if not isinstance(f.state,type(None)):
        return xf,yf,cstr,tf,dtf,dxf,dyf,dcstr,ifinal
    else:
        return xf,yf,cstr,tf,dtf,dxf,dyf,dcstr


from noloadj.numerical_methods.ODE.ode_extracted_features import T_pair,\
    T_impair,Min,Max
from abc import abstractmethod

class StoppingCriteria:
    def __init__(self):
        self.type=''
    @abstractmethod
    def cond_stop(self,t_prev,t,cstr,x_prev,x,T):
        pass

class threshold(StoppingCriteria):
    def __init__(self,var,threshold_=0.):
        StoppingCriteria.__init__(self)
        self.type='threshold'
        self.var=var
        self.threshold=threshold_
    def init_ind(self,names_var):
        self.ind=names_var.index(self.var)
    def cond_stop(self,t_prev,t,cstr,x_prev,x,T):
        return np.sign(x[self.ind]-self.threshold)==np.sign(x_prev[self.ind]-
                                                            self.threshold)

class final_time(StoppingCriteria):
    def __init__(self,tf):
        StoppingCriteria.__init__(self)
        self.type='final_time'
        self.tf=tf
    def cond_stop(self,t_prev,t,cstr,x_prev,x,T):
        return t_prev<self.tf

class steady_state(StoppingCriteria):

    def __init__(self,nbT,names_var,a=1e-5):
        StoppingCriteria.__init__(self)
        self.type='steady_state'
        self.nbT=nbT
        self.names_var=names_var
        self.a=a
    def init_dico(self,constr,T):
        for i in range(len(self.names_var)):
            constr[self.names_var[i]+'_minp']=(T_pair(self.nbT * T),
                                                Min(self.names_var[i],self.nbT))
            constr[self.names_var[i]+'_minimp']=(T_impair(self.nbT * T),
                                                Min(self.names_var[i],self.nbT))
            constr[self.names_var[i]+'_maxp']=(T_pair(self.nbT * T),
                                                Max(self.names_var[i],self.nbT))
            constr[self.names_var[i]+'_maximp']=(T_impair(self.nbT * T),
                                                Max(self.names_var[i],self.nbT))
        return constr
    def cond_stop(self,t_prev,t,cstr,x_prev,x,T):
        vectp,vectimp=np.zeros(2*len(self.names_var)),np.zeros(2*len(
            self.names_var))
        for i in range(len(self.names_var)):
            vectp=vectp.at[i].set(cstr[self.names_var[i]+'_minp'])
            vectp=vectp.at[2*i+1].set(cstr[self.names_var[i]+'_maxp'])
            vectimp=vectimp.at[i].set(cstr[self.names_var[i]+'_minimp'])
            vectimp=vectimp.at[2*i+1].set(cstr[self.names_var[i]+'_maximp'])
        return np.bitwise_not(np.bitwise_and(np.allclose(vectp,vectimp,
                                atol=self.a),np.not_equal(t_prev//T,t//T)))
    def delete_dico(self,constr):
        for i in range(len(self.names_var)):
            del constr[self.names_var[i]+'_minp']
            del constr[self.names_var[i]+'_minimp']
            del constr[self.names_var[i]+'_maxp']
            del constr[self.names_var[i]+'_maximp']
        return constr