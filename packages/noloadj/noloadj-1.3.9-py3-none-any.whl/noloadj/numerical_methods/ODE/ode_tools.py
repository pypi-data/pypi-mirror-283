import jax.numpy as np
from jax.lax import switch,cond
from jax import custom_jvp,jvp,Array
from functools import partial
from typing import Callable
from noloadj.numerical_methods.ODE.ode45_extract import final_time
import matplotlib.pyplot as plt

def vect_temporel(debut,fin,pas):
    '''
    Creates a time vector.

    :param debut: float: starting time
    :param fin: float: ending time
    :param pas: float : step size
    :return: JaxArray: time vector
    '''
    return np.linspace(debut,fin,int((fin-debut)/pas))

def indice_t(t,pas,debut=0.):
    return ((t-debut)/pas).astype(int)

def Switch(etat,funcs):
    return switch(etat,[func for func in funcs])

def Condition(conditions,functions,state):
    for i in range(len(conditions)):
        state=cond(conditions[i],functions[i],lambda state:state,state)
    return state


###################################################### integrale
@partial(custom_jvp,nondiff_argnums=(0,1,2,3))
def integrale(t0,tf,pas,f,*inputs):
    '''
    Computes the integral of a function on a domain.

    :param t0: float: initial bound of the integral
    :param tf: float: final bounds of the integral
    :param pas: float: step size of the time vector
    :param f: the function on which the integral has to be computed
    :param inputs: input variables across a time vector
    :return: the integral value
    '''
    longueur=(tf-t0)/int(tf/pas)
    res=f(*inputs)
    S=2*np.sum(res)-res[0]-res[-1]
    S*=longueur*0.5
    return S

@integrale.defjvp
def integrale_jvp(t0,tf,pas,f,primals,tangents):
    '''
    Computes the derivatives of the integral of a function on a domain w.r.t inputs.

    :param t0: float: initial bound of the integral
    :param tf: float: final bounds of the integral
    :param pas: float: step size of the time vector
    :param f: the function on which the integral has to be computed
    :param primals: tuple of input values
    :param tangents: tuple of input differentials
    :return: JaxArray: Derivatives of integral w.r.t inputs
    '''
    longueur=(tf-t0)/int(tf/pas)
    primal_dot,tangent_dot=jvp(f,primals,tangents)
    S=2*np.sum(primal_dot)-primal_dot[0]-primal_dot[-1]
    S*=longueur*0.5
    dS = 2*np.sum(tangent_dot)-tangent_dot[0]-tangent_dot[-1]
    dS *= longueur * 0.5
    return S,dS
############################################################################

def vect_freq(t0,tf,Te):
    '''
    Computes the frequency vector for FFT computation.

    :param t0: initial time
    :param tf: final time
    :param Te: sampling period
    :return: the frequency vector
    '''
    M=int((tf-t0)/Te)
    freq=np.where(M//2==0,np.linspace(0.,(M/2-1)/(M*Te),M//2),
                          np.linspace(0.,(M-1)/(2*M*Te),M//2))
    return freq

class Creneau:
    '''
    Class to implement a MLI command of the system (optional)
    
    Attributes:
    - a : float for Duty cycle of the system
    - T : float for Operating period of the system
    '''
    def __init__(self,a,T):
        self.aT=a*T
        self.T=T
        if hasattr(self.aT,'primal'):
            self.aT=self.aT.primal
        if hasattr(self.T,'primal'):
            self.T=self.T.primal
    
    def next_command(self,t):
        '''
        Returns command value for next iteration.
        :param t: float :time at present iteration
        :return: command value for next iteration : c
        '''
        moduloT=(t//self.T)*self.T
        c=np.where(t-moduloT<self.aT,1,0)
        return c
        
    def next_pdi(self,t):
        '''
        Returns next important date. tpdi.
        :param t: float :time at present iteration
        :return: next important date tpdi.
        '''
        moduloT=(t//self.T)*self.T
        tpdi=np.where(t-moduloT<self.aT,self.aT+moduloT,self.T+moduloT)
        return tpdi+1e-12
        

from abc import abstractmethod

class ODESystem:
    '''
    Interface class to call when you create a dynamic system class.

    Attributes:
        - xnames : list for state variables names
        - ynames : list for output variables names
        - stop : Callable for stopping criteria
        - constraints : dict for features to extract from dynamic simulation
        - state: int/Array: configuration of the system (optional)
        - commande : Callable to call a MLI command of the system (optional)
    '''
    def __init__(self):
        self.xnames:list=[]
        self.ynames:list=[]
        self.stop:Callable=final_time(1.0) # initialization with a stopping criteria
        self.constraints : dict={}
        self.state:[int,Array]=None
        self.commande:Callable=None # Class to implement a MLI command of the system (optional)

    @abstractmethod
    def timederivatives(self,X:Array,t:float,*P):
        '''
        Method to compute time derivatives of state vector.

        :param X: Array : state vector at present iteration
        :param t: float :time at present iteration
        :param P: tuple : simulation parameters to optimize
        :return: Array : time derivatives of state vector.
        '''
        pass

    @abstractmethod
    def output(self,X:Array,t:float,*P):
        '''
        Method to compute output vector.

        :param X: Array : state vector at present iteration
        :param t: float :time at present iteration
        :param P: tuple : simulation parameters to optimize
        :return: Array : output vector
        '''
        pass

    @abstractmethod
    def update(self,X:Array,Y:Array,t:float):
        '''
        Method to do configuration changes of the system (optional).

        :param X: Array : state vector at present iteration
        :param Y: Array : output vector
        :param t: float :time at present iteration
        :return: Several outputs :
        - int : configuration at next iteration 'i_now' (optional)
        - Array : modified state vector Xm
        - Array : output vector Ym
        '''
        pass

    @abstractmethod
    def initialize(self,*P):
        '''
        Method to compute state matrices that changed during simulation process (optional).

        :param P: tuple : simulation parameters to optimize
        :return: state matrices
        '''
        pass

    def get_indice(self,xy,desired_var):
        '''
        Returns the value(s) of an array corresponding to the variable name(s)
        given in desired_names.

        :param xy: Array: the state/output vector
        :param desired_var: list: the name of the variable(s) to get
        :return: Array: the value(s) of the desired names of variables in an array.
        '''
        if desired_var[0] in self.xnames:
            names_vars=self.xnames
        else:
            names_vars=self.ynames
        if len(desired_var)==1:
            return xy[names_vars.index(desired_var[0])]
        else:
            return (xy[names_vars.index(i)] for i in desired_var)

    def plotvar(self,xy,time,desired_var=None):
        '''
        Plots evolution of state/output variables given in desired_names.

        :param xy: Array: the state/output vector
        :param time: Array : time vector
        :param desired_var: list: the name of the variable(s) to get
        :return: /
        '''
        plt.figure()
        if len(xy)==len(self.xnames):
            if desired_var==None:
                desired_var=self.xnames
            title='State variables vs time'
        elif len(xy)==len(self.ynames):
            if desired_var==None:
                desired_var=self.ynames
            title='Outputs vs time'
        else:
            title=''
        for element in desired_var:
            var=self.get_indice(xy,[element])
            plt.plot(time,var)
        plt.xlabel('t(s)')
        plt.legend(desired_var)
        plt.title(title)
        plt.show()