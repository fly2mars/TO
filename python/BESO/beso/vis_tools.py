import numpy as np
import matplotlib.pyplot as plt

#############################
# Show model and mass curve #
#############################

def disp_2D_evolution(cur_figs, element_centers, constraint_node, load_node_list, ele_state, strTitle, iterations_limit, iter_times, mass):
    '''
    Showing 2D structure and mass cure during optimization.
    cur_figs = fig, (ax1, ax2)
    '''
    _N = len(element_centers)
    X = np.zeros([_N,2])   # elements
    Xr = np.array([])      # removed element
    S = np.zeros(_N)       # element state
    
    ## coordinate of elements(X) and removed elements(Xr)
    _idx = 0
    for ii in element_centers.keys():
        X[_idx] = element_centers[ii][0:2]
        S[_idx] = ele_state[ii]
        if S[_idx] < 0.1: 
            Xr = np.append (Xr , X[_idx])   
            
        _idx += 1
    Xr = Xr.reshape( (len(Xr) // 2, 2) )     
    
    #plt.figure(0)
    F = plt.gcf() # get current figure
    F.set_size_inches(8, 6)    
    fig, (ax1, ax2) = cur_figs    
    #ax1.set_xlabel('x')
    #ax1.set_ylabel('y')
    ax1.set_title(strTitle)    
    #plt.axis('tight')
    #plt.subplot(1, 2, 1)
    ax1.scatter(X[:,0], X[:, 1], c='b', marker ='s')
    ax1.scatter(Xr[:,0], Xr[:, 1], c='w', marker ='s')
    
    ## draw load position
    ax1.scatter(load_node_list[:,0],load_node_list[:,1],c='r', marker='x')
    
    ## draw Boundaries
    ax1.scatter(constraint_node[:,0], constraint_node[:,1], c='y', marker='x')
    
    #plt.draw()    
    #plt.axis('equal')
    
    #plt.subplot(1, 2, 2)
    #plt.axis([0,iterations_limit,0,3000])    
    #ax2.set_title("Mass of optimization domains")
    #ax2.set_xticks((0, iterations_limit))
    #ax2.set_yticks((1000, 3000))    
    #ax2.set_xlabel("Iteration")
    #ax2.set_ylabel("Mass")
    ax2.scatter([iterations_limit], [0], c='w', marker='.')
       
    ax2.plot(range(iter_times+1), mass, 'r-', label="mass")    
    
    #plt.grid()
    plt.draw()    
    
    plt.pause(0.001) 
   
    

        
################################################
# Show model and mass curve with strain energy #
################################################
def disp_2D_evolution_with_strain_energy(cur_figs, element_centers, FI_step,
                                         constraint_node, load_node_list, ele_state, 
                                         strTitle, iterations_limit, iter_times, mass):
    '''
    Showing 2D structure and mass cure during optimization.
    cur_figs = fig, (ax1, ax2)
    '''
    _N = len(element_centers)
    X = np.zeros([_N,2])   # elements
    Xr = np.array([])      # removed element
    S = np.zeros(_N)       # element state
    
    ## coordinate of elements(X) and removed elements(Xr)
    _idx = 0
    
    X_list = list(element_centers.values())
    X = np.reshape(X_list, (_N, 3))
    
    ele_state_list = list(ele_state.values())
    indices = [i for i, x in enumerate(ele_state_list) if x < 0.1]
    Xr = list(X_list[i] for i in indices)
    Xr = np.reshape(Xr, (len(indices), 3))
    
    #color map
    C = list(FI_step[0].values())
    C = np.reshape(C, (len(C),2))
    C = C[:, 1]
    #plt.figure(0)
    F = plt.gcf() # get current figure
    F.set_size_inches(8, 6)    
    fig, (ax1, ax2) = cur_figs    
    #ax1.set_xlabel('x')
    #ax1.set_ylabel('y')
    ax1.set_title(strTitle)    

    z1_plot = ax1.scatter(X[:,0], X[:, 1], c = C, marker ='s', cmap='viridis')
    
    if iter_times == 1:
        plt.colorbar(z1_plot, ax = ax1)
    
    ax1.scatter(Xr[:,0], Xr[:, 1], c='w', marker ='s')
    
    ## draw load position
    ax1.scatter(load_node_list[:,0],load_node_list[:,1],c='r', marker='x')
    
    ## draw Boundaries
    ax1.scatter(constraint_node[:,0], constraint_node[:,1], c='y', marker='x')
    
 
    ax2.scatter([iterations_limit], [0], c='w', marker='.')
       
    ax2.plot(range(iter_times+1), mass, 'r-', label="mass")    
    
    #plt.grid()
    plt.draw()    
    
    plt.pause(0.001) 
