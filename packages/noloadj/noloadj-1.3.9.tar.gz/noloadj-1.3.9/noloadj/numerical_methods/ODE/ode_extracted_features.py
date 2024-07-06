import jax.numpy as np
from jax import jvp,lax
from abc import abstractmethod
#from noloadj.numerical_methods.ODE.ode_tools import Switch

################################################################################
# TIME FEATURES
def T_pair(T):
    return lambda t:(t//T)%2==0

def T_impair(T):
    return lambda t:(t//T)%2!=0

def T_numero(T,n,i):
    return lambda t:(t//T)%n!=i

class TimeFeature:
    '''
    Interface class to implement time-domain criteria to extract from dynamic simulation.

    Attributes:
        - name : str to explicit on which variable the criteria will be applied
        - type : str to explicit its type (time-domain criteria 'time')
    '''
    def __init__(self,name):
        self.name=name
        self.type='time'
    @abstractmethod
    def init(self,z0,t0,h0):
        '''
        Compute the initial value of the criteria.

        :param z0: float : the initial value of the variable given in "name" attribute
        :param t0: float : time for the initial iteration
        :param h0: float : step size for the initial iteration
        :return: The initial value of the criteria
        '''
        pass
    @abstractmethod
    def expression(self,t_prev,z_prev,t_now,z_now,cstr,h_prev,T):
        '''
        Compute the value of the criteria for the present iteration of the simulation.

        :param t_prev: float : time for the previous iteration
        :param z_prev: the value of the variable given in "name" attribute, for the previous iteration
        :param t_now: float : time for the  present iteration
        :param z_now: float : the value of the variable given in "name" attribute, for the present iteration
        :param cstr: float : the criteria value for the  previous iteration
        :param h_prev: float : step size for the  previous iteration
        :param T: float : operating period
        :return: The value of the criteria for the present iteration of the simulation
        '''
        pass
    @abstractmethod
    def fin(self,tf,cstr,T):
        '''
        Compute the final value of the criteria.

        :param tf: float : final time of simulation
        :param cstr: float : the criteria value before for the previous iteration of final time
        :param T: float : operating period
        :return: The final value of the criteria
        '''
        pass
    @abstractmethod
    def dinit(self,z0,dz0,t0,h0):
        '''
        Compute the initial gradients of the criteria.

        :param z0: float : the initial value of the variable given in "name" attribute
        :param dz0: float : the initial gradients of the variable given in "name" attribute
        :param t0: float : time for the initial iteration
        :param h0: float : step size for the initial iteration
        :return: The initial gradients of the criteria
        '''
        pass
    @abstractmethod
    def der_expression(self,t_prev,z_prev,dz_prev,t_now,z_now,dz_now,cstr,dcstr,
                    h_prev,T,dT):
        '''
        Compute the gradients of the criteria for the present iteration of the simulation.

        :param t_prev: float : time for the previous iteration
        :param z_prev: float : the value of the variable given in "name" attribute, for the previous iteration
        :param dz_prev: Array : the gradients of the variable given in "name" attribute, for previous iteration
        :param t_now: float : time for the present iteration
        :param z_now: float : the value of the variable given in "name" attribute, for present iteration
        :param dz_now: Array : the gradients of the variable given in "name" attribute, for present iteration
        :param cstr: float : the criteria value for the previous iteration
        :param dcstr: Array : the criteria gradients for the previous iteration
        :param h_prev: float : step size for the previous iteration
        :param T: float : operating period
        :param dT: Array : gradients of operating period
        :return: The gradients of the criteria for the present iteration of the simulation
        '''
        pass
    @abstractmethod
    def der_fin(self,tf,cstr,T,dcstr,dT,zf):
        '''
        Compute the final gradients of the criteria.

        :param tf: float : final time of simulation
        :param cstr: float : the criteria value before for the previous iteration of final time
        :param T: float : operating period
        :param dcstr: Array : the criteria gradients before for the previous iteration of final time
        :param dT: Array : gradients of operating period
        :param zf: float : final value of the variable given in "name" attribute
        :return: The final gradients of the criteria
        '''
        pass


class Min(TimeFeature):
    '''
    Minimum of a variable over a period of dynamic simulation.
    '''
    def __init__(self,name,nbT=1):
        TimeFeature.__init__(self,name)
        self.nbT=nbT
    def init(self,z0,t0,h0):
        return z0
    def expression(self,t_prev,z_prev,t_now,z_now,cstr,h_prev,T):
        ind=np.where(T==0.,0,1)
        def without_T():
            return np.minimum(z_now,cstr)
        def with_T():
            return np.where((t_prev//(self.nbT*T))==(t_now//(self.nbT*T)),
                        np.minimum(z_now,cstr),z_now)
        return lax.switch(ind,[without_T,with_T])
    def fin(self,tf,cstr,T):
        return cstr
    def dinit(self,z0,dz0,t0,h0):
        return dz0
    def der_expression(self,t_prev,z_prev,dz_prev,t_now,z_now,dz_now,cstr,dcstr,
                    h_prev,T,dT):
        return jvp(self.expression,(t_prev,z_prev,t_now,z_now,cstr,h_prev,T),
                   (0.,dz_prev,0.,dz_now,dcstr,0.,dT))[1]
    def der_fin(self,tf,cstr,T,dcstr,dT,zf):
        return dcstr

class Max(TimeFeature):
    '''
    Maximum of a variable over a period of dynamic simulation.
    '''
    def __init__(self,name,nbT=1):
        TimeFeature.__init__(self,name)
        self.nbT=nbT
    def init(self,z0,t0,h0):
        return z0
    def expression(self,t_prev,z_prev,t_now,z_now,cstr,h_prev,T):
        ind=np.where(T==0.,0,1)
        def without_T():
            return np.maximum(z_now,cstr)
        def with_T():
            return np.where((t_prev//(self.nbT*T))==(t_now//(self.nbT*T)),
                        np.maximum(z_now,cstr),z_now)
        return lax.switch(ind,[without_T,with_T])
    def fin(self,tf,cstr,T):
        return cstr
    def dinit(self,z0,dz0,t0,h0):
        return dz0
    def der_expression(self,t_prev,z_prev,dz_prev,t_now,z_now,dz_now,cstr,dcstr,
                    h_prev,T,dT):
        return jvp(self.expression,(t_prev,z_prev,t_now,z_now,cstr,h_prev,T),
                   (0.,dz_prev,0.,dz_now,dcstr,0.,dT))[1]
    def der_fin(self,tf,cstr,T,dcstr,dT,zf):
        return dcstr

class moy(TimeFeature):
    '''
    Average value of a variable over a period of dynamic simulation.
    '''
    def __init__(self,name):
        TimeFeature.__init__(self, name)
    def init(self,z0,t0,h0):
        return 0.
    def expression(self,t_prev,z_prev,t_now,z_now,cstr,h_prev,T):
        ind=np.where(T==0.,0,1)
        def without_T():
            return cstr+0.5*h_prev*(z_prev+z_now)
        def with_T():
            return np.where((t_prev//T)==(t_now//T),cstr+0.5*h_prev*(z_prev+
                                                                z_now),0.)
        return lax.switch(ind,[without_T,with_T])
    def fin(self,tf,cstr,T):
        ind=np.where(T==0.,0,1)
        def without_T():
            return cstr/tf
        def with_T():
            return cstr/T
        return lax.switch(ind,[without_T,with_T])
    def dinit(self,z0,dz0,t0,h0):
        return 0.
    def der_expression(self,t_prev,z_prev,dz_prev,t_now,z_now,dz_now,cstr,dcstr,
                    h_prev,T,dT):
        ind=np.where(T==0.,0,1)
        def without_T():
            return dcstr+0.5*h_prev*(dz_prev+ dz_now)
        def with_T():
            return np.where((t_prev//T)==(t_now//T),dcstr+0.5*h_prev*(dz_prev+
                                                                  dz_now),0.)
        return lax.switch(ind,[without_T,with_T])
    def der_fin(self,tf,cstr,T,dcstr,dT,zf):
        ind=np.where(T==0.,0,1)
        def without_T():
            return dcstr/tf
        def with_T():
            return dcstr/T+((zf-cstr)/T)*dT
        return lax.switch(ind,[without_T,with_T])

class eff(TimeFeature):
    '''
    RMS value of a variable over a period of dynamic simulation.
    '''
    def __init__(self,name):
        TimeFeature.__init__(self,name)
    def init(self,z0,t0,h0):
        return 0.
    def expression(self,t_prev,z_prev,t_now,z_now,cstr,h_prev,T):
        ind=np.where(T==0.,0,1)
        def without_T():
            return cstr+0.5*h_prev*(z_prev**2+ z_now**2)
        def with_T():
            return np.where((t_prev//T)==(t_now//T),cstr+0.5*h_prev*(z_prev**2+
                                                                 z_now**2),0.)
        return lax.switch(ind,[without_T,with_T])
    def fin(self,tf,cstr,T):
        ind=np.where(T==0.,0,1)
        def without_T():
            return np.sqrt(cstr/tf)
        def with_T():
            return np.sqrt(cstr/T)
        return lax.switch(ind,[without_T,with_T])
    def dinit(self,z0,dz0,t0,h0):
        return 0.
    def der_expression(self,t_prev,z_prev,dz_prev,t_now,z_now,dz_now,cstr,dcstr,
                    h_prev,T,dT):
        ind=np.where(T==0.,0,1)
        def without_T():
            return dcstr+0.5*h_prev*(2*z_prev*dz_prev+2*z_now*dz_now)
        def with_T():
            return np.where((t_prev//T)==(t_now//T),dcstr+0.5*h_prev*(2*z_prev*
                                    dz_prev+2*z_now*dz_now),0.)
        return lax.switch(ind,[without_T,with_T])
    def der_fin(self,tf,cstr,T,dcstr,dT,zf):
        ind=np.where(T==0.,0,1)
        def without_T():
            return dcstr/(2*tf*cstr)
        def with_T():
            return dcstr/(2*T*cstr)+(zf**2-cstr**2)/(2*cstr*T)*dT
        return lax.switch(ind,[without_T,with_T])

################################################################################
# FREQUENCY FEATURES

class FreqFeature:
    '''
    Interface class to implement frequency-domain criteria to extract from dynamic simulation.

    Attributes:
        - name : str to explicit on which variable the criteria will be applied.
        - type : str to explicit its type (frequency-domain criteria 'freq')
    '''
    def __init__(self,name):
        self.name=name
        self.type='freq'
    @abstractmethod
    def expression(self,module,phase,vect_freq,f):
        """
        Compute the value of the criteria.

        :param module: Array : the module of the FFT of the variable given in "name" attribute
        :param phase: Array : the phase of the FFT of the variable given in "name" attribute
        :param vect_freq: Array : frequency vector
        :param f: float : fundamental frequency
        :return: Value of the criteria
        """
        pass
    @abstractmethod
    def der_expression(self,module,phase,dmodule,dphase,vect_freq,f):
        """
        Compute the gradients of the criteria with respect to optimization inputs.

        :param module: Array : the module of the FFT of the variable given in "name" attribute
        :param phase:  Array : the phase of the FFT of the variable given in "name" attribute
        :param dmodule: Array : the gradients of the module of the FFT of the variable given in "name" attribute
        :param dphase: Array : the gradients of the phase of the FFT of the variable given in "name" attribute
        :param vect_freq: Array : frequency vector
        :param f: float : fundamental frequency
        :return: Gradients of the criteria
        """
        pass



class Module_FFT(FreqFeature):
    '''
    Module of the FFT of a variable for a given frequency.
    '''
    def __init__(self,name,number):
        FreqFeature.__init__(self,name)
        self.number=number
    def expression(self,module,phase,vect_freq,f):
        if isinstance(self.number,int):
            if self.number==0:
                return module[0]
            elif self.number==1:
                indf=np.argmin(np.abs(vect_freq-f))
                return module[indf]
            else:
                res=np.zeros(self.number)
                for j in range(len(res)):
                    indf=np.argmin(np.abs(vect_freq-j*f))
                    res=res.at[j].set(module[indf])
        else:
            res=np.zeros(len(self.number))
            for j in range(len(res)):
                indf=np.argmin(np.abs(vect_freq-self.number[j]))
                res=res.at[j].set(module[indf])
        return res
    def der_expression(self,module,phase,dmodule,dphase,vect_freq,f):
        if isinstance(self.number,int):
            if self.number==0:
                return module[0],dmodule[0]
            elif self.number==1:
                indf=np.argmin(np.abs(vect_freq-f))
                return module[indf],dmodule[1]
            else:
                res = np.zeros(self.number)
                dres=np.zeros(self.number)
                for j in range(len(res)):
                    indf=np.argmin(np.abs(vect_freq-j*f))
                    res=res.at[j].set(module[indf])
                    dres=dres.at[j].set(dmodule[indf])
        else:
            res = np.zeros(len(self.number))
            dres=np.zeros(len(self.number))
            for j in range(len(res)):
                indf=np.argmin(np.abs(vect_freq-self.number[j]))
                res=res.at[j].set(module[indf])
                dres=dres.at[j].set(dmodule[indf])
        return res,dres

class THD(FreqFeature):
    '''
    Total Harmonic Distorsion (THD) of a variable.
    '''
    def __init__(self,name):
        FreqFeature.__init__(self, name)
    def expression(self,module,phase,vect_freq,f):
        ref=np.maximum(module[0],module[1])
        harm=module[2::]
        THD=np.sqrt(np.sum(harm**2))/ref
        return THD
    def der_expression(self,module,phase,dmodule,dphase,vect_freq,f):
        ref=np.maximum(module[0],module[1])
        dref=np.where(ref==module[0],dmodule[0],dmodule[1])
        harm,dharm=module[2::],dmodule[2::]
        THD=np.sqrt(np.sum(harm**2))/ref
        dTHD=-dref*THD/ref+np.sum(np.dot(harm,dharm))/(ref*ref*THD)
        return THD,dTHD

