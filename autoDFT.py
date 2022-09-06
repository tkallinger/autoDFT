import pandas as pd 
import numpy as np 
import matplotlib.gridspec as gridspec
from ultranest import ReactiveNestedSampler
from ultranest.plot import cornerplot
import matplotlib.pyplot as plt
import shutil
import os

### UltraNest functions ######
### define parameter names
parameters_sin = ['amp','freq','phase']

def prior_transform(cube):
    params = cube.copy()
    for i in range(len(params)) : 
    	params[i] = cube[i] * (par_hi[i] - par_lo[i]) + par_lo[i]
    return params
def log_likelihood_sin(params):
    amp, freq, phase = params
    y_model = sin_model(x, amp, freq, phase)
    #loglike = -0.5 * (((y_model - y) / yerr)**2 - np.sqrt(2*np.pi)*yerr).sum()
    loglike = -0.5 * (((y_model - y) / yerr)**2).sum()
    return loglike
def sin_model(x, amp, freq, phase):
	return amp * np.sin(2 * np.pi * (x * freq + phase))

### UltraNest functions END ######
def sinfit(plots=False):
    if os.path.exists('sampler') : shutil.rmtree('sampler')
    sampler = ReactiveNestedSampler(parameters_sin, log_likelihood_sin, prior_transform,log_dir="sampler", resume=True, wrapped_params=[False,False,True])
    result = sampler.run(min_num_live_points=400, dKL=np.inf, min_ess=100)
    if plots:
        sampler.plot()

    #quit()
    return sampler, result



def read_ts(filename):
    p = pd.read_csv(filename, delimiter=' ', skiprows = 0 , skipinitialspace = True, header = None, names = [
        'x', 'y', 'ye']) 
    #p = pd.read_csv(filename, delimiter='\t' , skiprows = 0, skipinitialspace = True, header = None, 
    #    names = ['x','y','ye'],engine='python' )
    return p

def dft(x,y,frange,os=5):
    df= 1 /((np.max(x) - np.min(x)) * os)
    N = len(x)
    f = np.arange(frange[0], frange[1], df)
    loops = len(f)
    a = np.zeros(loops)
    for i in range(loops):
        arg = f[i] * x * 2 * np.pi
        re = np.sum(y * np.sin(arg))
        im = np.sum(y * np.cos(arg))
        a[i] = 2 / N * np.sqrt(re**2 + im**2)
    return f, a



######################################################################################
######################################################################################
######################################################################################
def autoDFT(filename, frange, iter_max=10, df_factor=3, snr_box=2, write_res=False, plots=False, path='',os=5, write_spec=False):

    if path != '':
        path += '/'

    plt.rcParams.update({'font.size':7, 'ytick.right':True, 'xtick.top':True, 'axes.linewidth':0.5,'xtick.major.width':0.5, 'ytick.major.width':0.5,'xtick.direction':'in','ytick.direction':'in', 'font.sans-serif':'Arial'})
    grid = gridspec.GridSpec(4,1, hspace=0.2)


    ts = read_ts(path+filename)
    print(ts.head())
    #quit()


    global x, y, yerr, par_lo, par_hi
    x_min = ts['x'].mean()
    x = ts['x'].values - x_min
    y = ts['y'].values - ts['y'].mean()
    yerr = ts['ye'].values #/ 2

    #fit = np.poly1d(np.polyfit(x, y, 1))
    #y -= fit(x)

    f = open(path+filename+'.flist','a+')
    f.write('file: {}\n'.format(filename))
    f.write('frange: {} - {}\n'.format(frange[0],frange[1]))
    f.write('phase 0 at: {}\n'.format(x_min))
    f.write('local SNR: +/-{}c/d\n'.format(snr_box/2))
    f.write('\n')
    f.write('     f                 f_err             a               a_err            p               p_err           ev              globalSNR       localSNR\n')
    f.write('--------------------------------------------------------------------------------------------------------------------------------------------------\n')
    f.close()




    for iteration in range(iter_max):
        f = plt.figure()
        ax = plt.subplot(grid[0,0], facecolor='gainsboro')
        plt.plot(x,y,'.')
        plt.title('iteration '+str(iteration))
        plt.draw()
        plt.pause(0.5)


        freq, amp = dft(x, y, frange,os=os)
        pos = np.argmax(amp)
        f_g = freq[pos]

        if write_spec:
            spec = pd.DataFrame({'f': freq, 'a':amp})
            spec.to_csv(filename+'.'+str(iteration)+'.fou' ,sep=',',index=False,header=True)

        noise_glo = np.mean(amp)
        noise_loc = np.mean(amp[(freq > f_g-snr_box/2) & (freq < f_g+snr_box/2)])

        #f = plt.figure()
        ax = plt.subplot(grid[1,0], facecolor='gainsboro')
        plt.plot(freq,amp,linewidth=0.5)
        plt.axvline(x=f_g, color='red', linestyle='dashed')
        plt.draw()
        plt.pause(0.5)

        df = df_factor / (np.max(x) - np.min(x))

        ax = plt.subplot(grid[2,0], facecolor='gainsboro')
        plt.plot(freq,amp,linewidth=0.5)
        plt.axvline(x=f_g, color='red', linestyle='dashed')
        plt.xlim(f_g-df,f_g+df)
        plt.draw()
        plt.pause(0.5)



        par_lo = [0,freq[pos]-df,0.0]
        par_hi = [2*amp[pos],freq[pos]+df,1.0]

        ### fit a single sin
        sampler, result = sinfit(plots=plots)
        sampler.print_results()
        logZ = result['logz']
        logZ_nosig = -0.5 * (((y) / yerr)**2).sum()
        par = np.array(result['posterior']['median'])

        if (par[2] > 0.8) or (par[2] < 0.2):
            if par[2] > 0.8:
                par_lo = [0,freq[pos]-df,0.2]
                par_hi = [2*amp[pos],freq[pos]+df,1.2]
            else:
                par_lo = [0,freq[pos]-df,-0.2]
                par_hi = [2*amp[pos],freq[pos]+df,0.8]

            ### fit a single sin
            sampler, result = sinfit(plots=plots)
            sampler.print_results()
            logZ = result['logz']

        par = np.array(result['posterior']['median'])
        par_up = np.abs(np.array(result['posterior']['errup']) - par)
        par_lo = np.abs(par - np.array(result['posterior']['errlo']))
        par_e = (par_up + par_lo) / 2
        if par_up[2] > 3*par_lo[2]:
            par_e[2] = par_lo[2]
        if par_lo[2] > 3*par_up[2]:
            par_e[2] = par_up[2]






        print(result)

        if plots:
            shutil.move('sampler/plots', path+'plots.f'+str(iteration+1))
        ### if phase is close to parameter borders refit with new borders
        #if np.abs(par[2]-0.5) < par_e[2]:
        #    par_lo = [0,freq[pos]-df,-0.25]
        #    par_hi = [2*amp[pos],freq[pos]+df,0.75]

            ### fit a single sin
        #    sampler, result = sinfit()
        #    sampler.print_results()
        #    logZ = result['logz']
        #    logZ_nosig = -0.5 * (((y) / yerr)**2).sum()
        
        #    par = result['posterior']['mean']
        #    par_e = result['posterior']['stdev']


        
        fit = sin_model(x, par[0], par[1], par[2])
        snr_glo = par[0] / noise_glo
        snr_loc = par[0] / noise_loc
        z = [logZ,logZ_nosig]
        z = z - np.min(z)
        p = np.exp(z[0]) / (np.exp(z[0]) + np.exp(z[1])) if np.max(z) < 100 else 1
        print('prob:',p)

        print('snr:',snr_glo,snr_loc)



        ax = plt.subplot(grid[3,0], facecolor='gainsboro')
        plt.plot(x,y,'.')
        plt.plot(x,fit,linewidth=0.5)
        plt.draw()
        plt.pause(0.5)
        plt.clf()

        plt.close()


        y -= fit


        f = open(path+filename+'.flist','a+')
        f.write('{:15.6f} {:15.6f} {:15.4f} {:15.4f} {:15.3f} {:15.3f} {:15.3f} {:15.2f} {:15.2f}\n'.format(par[1],par_e[1],par[0],par_e[0],par[2],par_e[2],p,snr_glo,snr_loc))
        f.close()

    if write_res:
        d = pd.DataFrame({'x':x, 'y':y})
        d.to_csv(path+filename+'.residuals', sep=' ', header=False, index=False)

    pass
