import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
import os
import sys
import subprocess
import time
import math

# import local code
beso_path = os.getcwd() + '/beso'
sys.path.append(beso_path)
import beso_lib
import vis_tools
import beso_filters
import beso_separate
import beso_tools
sys.path.remove(beso_path)

# global variables
domain_optimized = {}
domain_density = {}
domain_thickness = {}
domain_offset = {}  # TODO read offset from .inp file
domain_FI = {}
domain_material = {}
domain_boundary = [] # boundaries nodes readed from .inp file
domain_shells = {}
domain_volumes = {}

path = '.'         # working directory
path_calculix = None
path_temp = None
file_name = None

mass_goal_ratio = None
continue_from = None
filter_list = None
r_min = None
filter_on_sensitivity = None
cpu_cores = None
FI_violated_tolerance = None
decay_coefficient = None
shells_as_composite = None
reference_points = None
reference_value = None
mass_addition_ratio = None
mass_removal_ratio = None
ratio_type = None
sensitivity_averaging = None
iterations_limit = None
tolerance = None
save_iteration_results = None
save_iteration_format = None
domains_from_config = None
criteria = []
elm_states = {}
number_of_states = 0  # find number of states possible in elm_states

# Data structure
nodes = None
Elements = None
domains = None
opt_domains = None
en_all = None
plane_strain = None
plane_stress = None
axisymmetry = None
cg = None
cg_min = None
cg_max = None
volume_elm = None
area_elm = None
mass = [0.0]
mass_full = 0  # sum from 0th list position TODO make it independent on starting elm_states?
weight_factor2 = {}
near_elm = {}
domains_to_filter = []
weight_factor_node = None
M = None
weight_factor_distance = None
near_nodes = None
weight_factor3 = None
near_elm3 = None
near_points = None
load_node_list = None
constraint_node_list = None
FI_step = None

# ITERATION CYCLE
sensitivity_number = {}
sensitivity_number_old = {}
FI_step_max = {}  # maximal FI over all steps for each element in this iteration
FI_max = []   # list of max stress for each element 
FI_mean = []  # list of mean stress in every iteration
FI_mean_without_state0 = []  # mean stress without elements in state 0
FI_violated = [] # num of elements with stress(strain? > 1) in each step i
i = 0
i_violated = 0
continue_iterations = True
check_tolerance = False
elm_states_before_last = {}
elm_states_last = elm_states

# Figure
fig, (ax1,ax2) = plt.subplots(2, figsize=(8,6))
cur_figs = [fig, (ax1, ax2)]



conf_path = './beso/beso_conf.py'

class suBeso(object):   
    
    def __init__(self):  
        print('Init beso---')
        
    def read_config(self):
        global number_of_states
        global domains_from_config
        global criteria
        domains_from_config = domain_optimized.keys()
        for dn in domain_FI:  # extracting each type of criteria
            for state in range(len(domain_FI[dn])):
                for dn_crit in domain_FI[dn][state]:
                    if dn_crit not in criteria:
                        criteria.append(dn_crit)
        
        for dn in domains_from_config:
            number_of_states = max(number_of_states, len(domain_density[dn]))        
    
    def setup_convergen_conditions(self):
        global iterations_limit
        if iterations_limit == 0:  # automatic setting
            if ratio_type == "absolute":
                iterations_limit = int((1 - mass_goal_ratio) / abs(mass_removal_ratio - mass_addition_ratio) + 25)
            elif ratio_type == "relative":
                m = 1
                it = 0
                while m > mass_goal_ratio:
                    m -= m * abs(mass_removal_ratio - mass_addition_ratio)
                    it += 1
                iterations_limit = it + 25
            print("iterations_limit set to %s" % iterations_limit)
    def setup_FEA_environment(self):
        # set an environmental variable driving number of cpu cores to be used by CalculiX
        global cpu_cores
        if cpu_cores == 0:  # use all processor cores
            cpu_cores = multiprocessing.cpu_count()
        os.putenv('OMP_NUM_THREADS', str(cpu_cores))
        
    def write_log(self):
        # writing log file with settings
        msg = "\n"
        msg += "---------------------------------------------------\n"
        msg += ("file_name = %s\n" % file_name)
        msg += ("Start at    " + time.ctime() + "\n\n")
        for dn in domain_optimized:
            msg += ("elset_name              = %s\n" % dn)
            msg += ("domain_optimized        = %s\n" % domain_optimized[dn])
            msg += ("domain_density          = %s\n" % domain_density[dn])
            msg += ("domain_thickness        = %s\n" % domain_thickness[dn])
            msg += ("domain_FI               = %s\n" % domain_FI[dn])
            msg += ("domain_material         = %s\n" % domain_material[dn])
            msg += "\n"
        msg += ("mass_goal_ratio         = %s\n" % mass_goal_ratio)
        msg += ("filter_list             = %s\n" % filter_list)
        msg += ("r_min                   = %s\n" % r_min)
        msg += ("filter_on_sensitivity   = %s\n" % filter_on_sensitivity)
        msg += ("cpu_cores               = %s\n" % cpu_cores)
        msg += ("FI_violated_tolerance   = %s\n" % FI_violated_tolerance)
        msg += ("decay_coefficient       = %s\n" % decay_coefficient)
        msg += ("shells_as_composite     = %s\n" % shells_as_composite)
        msg += ("reference_points        = %s\n" % reference_points)
        msg += ("reference_value         = %s\n" % reference_value)
        msg += ("mass_addition_ratio     = %s\n" % mass_addition_ratio)
        msg += ("mass_removal_ratio      = %s\n" % mass_removal_ratio)
        msg += ("ratio_type              = %s\n" % ratio_type)
        msg += ("sensitivity_averaging   = %s\n" % sensitivity_averaging)
        msg += ("iterations_limit        = %s\n" % iterations_limit)
        msg += ("tolerance               = %s\n" % tolerance)
        msg += ("save_iteration_results  = %s\n" % save_iteration_results)
        msg += ("save_iteration_format   = %s\n" % save_iteration_format)
        msg += "\n"
        beso_lib.write_to_log(file_name, msg)
        
        # writing log table header
        msg = "\n"
        msg += "domain order: \n"
        dorder = 0
        for dn in domains_from_config:
            msg += str(dorder) + ") " + dn + "\n"
            dorder += 1
        msg += "\niteration              mass FI_violated_0)"
        for dno in range(len(domains_from_config) - 1):
            msg += (" " + str(dno + 1)).rjust(4, " ") + ")"
        if len(domains_from_config) > 1:
            msg += " all)"
        msg += "          FI_mean    _without_state0         FI_max 0)"
        for dno in range(len(domains_from_config) - 1):
            msg += str(dno + 1).rjust(17, " ") + ")"
        if len(domains_from_config) > 1:
            msg += "all".rjust(17, " ") + ")"
        msg += "\n"
        beso_lib.write_to_log(file_name, msg)        
            
    def load_model(self, model_path=None):
        global nodes, Elements, domains, opt_domains, en_all, plane_strain, plane_stress, axisymmetry, file_name, domain_shells, domain_volumes, elm_states
        
        model_path = model_path if (model_path is not None) else file_name
        
        [nodes, Elements, domains, opt_domains, en_all, plane_strain, plane_stress, axisymmetry] = beso_lib.import_inp(
            model_path, domains_from_config, domain_optimized, shells_as_composite)
        domain_shells = {}
        domain_volumes = {}
        for dn in domains_from_config:  # distinguishing shell elements and volume elements
            domain_shells[dn] = set(domains[dn]).intersection(list(Elements.tria3.keys()) + list(Elements.tria6.keys()) +
                                                              list(Elements.quad4.keys()) + list(Elements.quad8.keys()))
            domain_volumes[dn] = set(domains[dn]).intersection(list(Elements.tetra4.keys()) + list(Elements.tetra10.keys()) +
                                                               list(Elements.hexa8.keys()) + list(Elements.hexa20.keys()) +
                                                               list(Elements.penta6.keys()) + list(Elements.penta15.keys()))
        
        # initial element state
        elm_states = {} 
        if continue_from[-4:] == ".frd":
            elm_states = beso_lib.import_frd_state(continue_from, elm_states, number_of_states, file_name)
        elif continue_from[-4:] == ".inp":
            elm_states = beso_lib.import_inp_state(continue_from, elm_states, number_of_states, file_name)
        else:
            for dn in domains_from_config:
                for en in domains[dn]:
                    elm_states[en] = len(domain_density[dn]) - 1  # set to highest state
        
    def compute_element_center(self):
        '''
        Computing volume or area, and centre of gravity of each element
        '''
        global cg, cg_min, cg_max, volume_elm, area_elm, mass, mass_full
        [cg, cg_min, cg_max, volume_elm, area_elm] = beso_lib.elm_volume_cg(file_name, nodes, Elements)        
        
        for dn in domains_from_config:
            if domain_optimized[dn] is True:
                for en in domain_shells[dn]:
                    mass[0] += domain_density[dn][elm_states[en]] * area_elm[en] * domain_thickness[dn][elm_states[en]]
                    mass_full += domain_density[dn][len(domain_density[dn]) - 1] * area_elm[en] * domain_thickness[dn][
                                                                                                    len(domain_density[dn]) - 1]
                for en in domain_volumes[dn]:
                    mass[0] += domain_density[dn][elm_states[en]] * volume_elm[en]
                    mass_full += domain_density[dn][len(domain_density[dn]) - 1] * volume_elm[en]
        print("initial optimization domains mass {}" .format(mass[0]))
        
    def prepare_filter(self):
        '''
        Todo: add explaination
        '''
        global weight_factor2, near_elm, domains_to_filter, weight_factor_node, M, weight_factor_distance, near_nodes, weight_factor3, near_elm3, near_points
        
        for ft in filter_list:
            if ft[0] and ft[1]:
                f_range = ft[1]
                if len(ft) == 2:
                    domains_to_filter = list(opt_domains)
                else:
                    domains_to_filter = []
                    for dn in ft[2:]:
                        domains_to_filter += domains[dn]
                if ft[0] == "simple":
                    [weight_factor2, near_elm] = beso_filters.prepare2s(cg, cg_min, cg_max, f_range, domains_to_filter,
                                                                        weight_factor2, near_elm)
                elif ft[0].split()[0] in ["erode", "dilate", "open", "close", "open-close", "close-open", "combine"]:
                    near_elm = beso_filters.prepare_morphology(cg, cg_min, cg_max, f_range, domains_to_filter, near_elm)
        
        if filter_on_sensitivity == "over nodes":
            [weight_factor_node, M, weight_factor_distance, near_nodes] = beso_filters.prepare1s(nodes, Elements, cg, r_min,
                                                                                                 opt_domains)
        elif filter_on_sensitivity == "over points":
            [weight_factor3, near_elm3, near_points] = beso_filters.prepare3(file_name, cg, cg_min, r_min, opt_domains)        
            
    def separating_nodes_by_element(self):
        # separating elements for reading nodal input        
        if reference_points == "nodes":
            beso_separate.separating(file_name, nodes)
    def init_visulization(self):
        global load_nodes, boundary_node_indexes, load_node_list, constraint_node_list
        ax2.set_xticks((0, iterations_limit))
        ax2.set_yticks((1000, 3000))    
        ax2.set_xlabel("Iteration")
        ax2.set_ylabel("Mass")
        # find load nodes and boundary node 
        load_nodes = beso_lib.import_inp_load(file_name)
        boundary_node_indexes = beso_lib.import_inp_boundary(file_name) 
        
        load_node_list = np.array([])
        for _idx in load_nodes.keys():
            _load_node = nodes[_idx][:2]
            load_node_list = np.append(load_node_list, _load_node[0:2])
            
        load_node_list = np.reshape(load_node_list, (len(load_node_list)//2,2))
        
        constraint_node_list = np.array([])
        for iter_key in boundary_node_indexes:    
            constraint_node_list = np.append(constraint_node_list, nodes[iter_key][0:2])
        
        constraint_node_list = constraint_node_list.reshape( (len(constraint_node_list) // 2, 2) )         
        
    def run_optimization(self):
        global i
        print('running optimzation...')
        while(True):
            self.FEA()
            self.Sensitivity_Analysis()
            self.Update()
            if(self.Is_Convergence() ): break
            self.Swith_Element_State()
            self.Check_oscillation()
            self.Filter_State() 
            self.Show()
        
    def FEA(self):
        global i, FI_step, sensitivity_number, FI_violated, FI_step_max
        
        print("FEA")
        # creating a new .inp file for CalculiX
        file_nameW = path_export + '/' + str(i).zfill(3)
        beso_lib.write_inp(file_name, file_nameW, elm_states, number_of_states, domains, domains_from_config,
                           domain_optimized, domain_thickness, domain_offset, domain_material, domain_volumes,
                           domain_shells, plane_strain, plane_stress, axisymmetry, save_iteration_results, i,
                           reference_points, shells_as_composite)
        # running CalculiX analysis
        subprocess.call(os.path.normpath(path_calculix) + " " + os.path.join(path, file_nameW), shell=True)
    
        # reading results and computing failure indeces
        if reference_points == "integration points":  # from .dat file
            FI_step = beso_lib.import_FI_int_pt(reference_value, file_nameW, domains, criteria, domain_FI, file_name,
                                                elm_states, domains_from_config)
        elif reference_points == "nodes":  # from .frd file
            FI_step = beso_lib.import_FI_node(reference_value, file_nameW, domains, criteria, domain_FI, file_name,
                                              elm_states)
        os.remove(file_nameW + ".inp")
        if not save_iteration_results or np.mod(float(i - 1), save_iteration_results) != 0:
            os.remove(file_nameW + ".dat")
            os.remove(file_nameW + ".frd")
        os.remove(file_nameW + ".sta")
        os.remove(file_nameW + ".cvg")
        FI_max.append({})
        for dn in domains_from_config:
            FI_max[i][dn] = 0
            for en in domains[dn]:
                for sn in range(len(FI_step)):
                    try:
                        FI_step_en = list(filter(lambda a: a is not None, FI_step[sn][en]))  # drop None FI
                        FI_max[i][dn] = max(FI_max[i][dn], max(FI_step_en))
                    except ValueError:
                        msg = "FI_max computing failed. Check if each domain contains at least one failure criterion."
                        beso_lib.write_to_log(file_name, "ERROR: " + msg + "\n")
                        raise Exception(msg)
                    except KeyError:
                        msg = "Some result values are missing. Check available disk space."
                        beso_lib.write_to_log(file_name, "ERROR: " + msg + "\n")
                        raise Exception(msg)
        print("domain ordered \nFI_max and number of violated elements")
    
        # handling with more steps
        FI_step_max = {}  # maximal FI over all steps for each element in this iteration
        FI_violated.append([])
        dno = 0
        for dn in domains_from_config:
            FI_violated[i].append(0)
            for en in domains[dn]:
                FI_step_max[en] = 0
                for sn in range(len(FI_step)):
                    FI_step_en = list(filter(lambda a: a is not None, FI_step[sn][en]))  # drop None FI
                    FI_step_max[en] = max(FI_step_max[en], max(FI_step_en))
                sensitivity_number[en] = FI_step_max[en] / domain_density[dn][elm_states[en]]
                if FI_step_max[en] >= 1:
                    FI_violated[i][dno] += 1
            print(str(FI_max[i][dn]).rjust(15) + " " + str(FI_violated[i][dno]).rjust(4))
            dno += 1        
        
    def Sensitivity_Analysis(self):
        '''
        1. Simple filter: d
        '''
        global i, domains_to_filter, sensitivity_number, sensitivity_number_old
        print("Sensitivity_Analysis")
        
        for ft in filter_list:
            if ft[0] and ft[1]:
                if len(ft) == 2:
                    domains_to_filter = list(opt_domains)
                else:
                    domains_to_filter = []
                    for dn in ft[2:]:
                        domains_to_filter += domains[dn]
                if ft[0] == "simple":
                    sensitivity_number = beso_filters.run2(file_name, sensitivity_number, weight_factor2, near_elm,
                                                           domains_to_filter)
                elif ft[0].split()[0] in ["erode", "dilate", "open", "close", "open-close", "close-open", "combine"]:
                    if ft[0].split()[1] == "sensitivity":
                        domains_en_in_state = [[]] * number_of_states
                        for en in domains_to_filter:
                            sn = elm_states[en]
                            domains_en_in_state[sn].append(en)
                        for sn in range(number_of_states):
                            if domains_en_in_state[sn]:
                                sensitivity_number = beso_filters.run_morphology(sensitivity_number, near_elm,
                                                                                 domains_en_in_state[sn], ft[0].split()[0])
        if filter_on_sensitivity == "over nodes":
            sensitivity_number = beso_filters.run1(file_name, sensitivity_number, weight_factor_node, M,
                                                   weight_factor_distance, near_nodes, nodes, opt_domains)
        elif filter_on_sensitivity == "over points":
            sensitivity_number = beso_filters.run3(sensitivity_number, weight_factor3, near_elm3, near_points)
    
        if sensitivity_averaging:
            for en in opt_domains:
                # averaging with the last iteration should stabilize iterations
                if i > 0:
                    sensitivity_number[en] = (sensitivity_number[en] + sensitivity_number_old[en]) / 2.0
                sensitivity_number_old[en] = sensitivity_number[en]  # for averaging in the next step
                
    def Update(self):
        '''
        # computing mean stress from maximums of each element in all steps in the optimization domain
        '''
        global i, FI_max, FI_mean, FI_mean_without_state0, FI_violated
        print("Update")
        
        FI_mean_sum = 0
        FI_mean_sum_without_state0 = 0
        mass_without_state0 = 0
        for dn in domain_optimized:
            if domain_optimized[dn] is True:
                for en in domain_shells[dn]:
                    mass_elm = domain_density[dn][elm_states[en]] * area_elm[en] * domain_thickness[dn][elm_states[en]]
                    FI_mean_sum += FI_step_max[en] * mass_elm
                    if elm_states[en] != 0:
                        FI_mean_sum_without_state0 += FI_step_max[en] * mass_elm
                        mass_without_state0 += mass_elm
                for en in domain_volumes[dn]:
                    mass_elm = domain_density[dn][elm_states[en]] * volume_elm[en]
                    FI_mean_sum += FI_step_max[en] * mass_elm
                    if elm_states[en] != 0:
                        FI_mean_sum_without_state0 += FI_step_max[en] * mass_elm
                        mass_without_state0 += mass_elm
        FI_mean.append(FI_mean_sum / mass[i])
        FI_mean_without_state0.append(FI_mean_sum_without_state0 / mass_without_state0)
        print("FI_mean                = {}" .format(FI_mean[i]))
        print("FI_mean_without_state0 = {}".format(FI_mean_without_state0[i]))
    
        # writing log table row
        msg = str().rjust(9, " ") + " " + str(mass[i]).rjust(17, " ") + " " + str(FI_violated[i][0]).rjust(13, " ")
        for dno in range(len(domains_from_config) - 1):
            msg += " " + str(FI_violated[i][dno + 1]).rjust(4, " ")
        if len(domains_from_config) > 1:
            msg += " " + str(sum(FI_violated[i])).rjust(4, " ")
        msg += " " + str(FI_mean[i]).rjust(17, " ") + " " + str(FI_mean_without_state0[i]).rjust(18, " ")
        FI_max_all = 0
        for dn in domains_from_config:
            msg += " " + str(FI_max[i][dn]).rjust(17, " ")
            FI_max_all = max(FI_max_all, FI_max[i][dn])
        if len(domains_from_config) > 1:
            msg += " " + str(FI_max_all).rjust(17, " ")
        msg += "\n"
        beso_lib.write_to_log(file_name, msg)
        
    def Is_Convergence(self):
        '''
        # relative difference in a mean stress for the last 5 iterations must be < tolerance
        # i >= iterations_limit 
        '''
        global i, i_violated, difference_last, continue_iterations, check_tolerance, mass_goal_i
        if len(FI_mean) > 5:
            difference_last = []
            for last in range(1, 6):
                difference_last.append(abs(FI_mean[i] - FI_mean[i-last]) / FI_mean[i])
            difference = max(difference_last)
            if check_tolerance is True:
                print("maximum relative difference in FI_mean for the last 5 iterations = {}" .format(difference))
            if difference < tolerance:
                continue_iterations = False
            elif FI_mean[i] == FI_mean[i-1] == FI_mean[i-2]:
                continue_iterations = False
                print("FI_mean[i] == FI_mean[i-1] == FI_mean[i-2]")
    
        # start of the new iteration or finish of the iteration process
        if continue_iterations is False or i >= iterations_limit:
            # break
            return True
        else:
            # export the present mesh
            if save_iteration_results and np.mod(float(i - 1), save_iteration_results) == 0:
                if "frd" in save_iteration_format:
                    beso_lib.export_frd(path_export + "/file" + str(), nodes, Elements, elm_states, number_of_states)
                if "inp" in save_iteration_format:
                    beso_lib.export_inp(path_export + "/file" + str(), nodes, Elements, elm_states, number_of_states)
        i += 1  # iteration number
        print("\n----------- new iteration number %d ----------" % i)
    
        # check for number of violated elements
        if sum(FI_violated[i - 1]) > sum(FI_violated[0]) + FI_violated_tolerance:
            mass_goal_i = mass[i - 1]  # use mass_new from previous iteration
            if i_violated == 0:
                i_violated = i
                check_tolerance = True
        elif mass[i - 1] <= mass_goal_ratio * mass_full:  # goal volume achieved
            if not i_violated:
                i_violated = i  # to start decaying
                check_tolerance = True
            try:
                mass_goal_i
            except NameError:
                msg = "ERROR: mass goal is lower than initial mass. Check mass_goal_ratio"
                beso_lib.write_to_log(file_name, msg + "\n")
        else:
            mass_goal_i = mass_goal_ratio * mass_full
        
        return False
    
    
    def Swith_Element_State(self):
        '''
        # switch element states
        '''
        global i, mass_referential, elm_states, mass, elm_states_before_last, elm_states_last, continue_iterations
        
        if ratio_type == "absolute":
            mass_referential = mass_full
        elif ratio_type == "relative":
            mass_referential = mass[i - 1]
        [elm_states, mass] = beso_lib.switching(elm_states, domains_from_config, domain_optimized, domains, FI_step_max,
                                                domain_density, domain_thickness, domain_shells, area_elm, volume_elm,
                                                sensitivity_number, mass, mass_referential, mass_addition_ratio,
                                                mass_removal_ratio, decay_coefficient, FI_violated, i_violated, i,
                                                mass_goal_i)
    
        # check for oscillation state
        if elm_states_before_last == elm_states:  # oscillating state
            msg = "OSCILLATION: model turns back to " + str(i - 2) + "th iteration\n"
            beso_lib.write_to_log(file_name, msg)
            print(msg)
            continue_iterations = False
        elm_states_before_last = elm_states_last.copy()
        elm_states_last = elm_states.copy()
    
        # filtering state
        for ft in filter_list:
            if ft[0] and ft[1]:
                if len(ft) == 2:
                    domains_to_filter = list(opt_domains)
                else:
                    domains_to_filter = []
                    for dn in ft[2:]:
                        domains_to_filter += domains[dn]
    
                if ft[0].split()[0] in ["erode", "dilate", "open", "close", "open-close", "close-open", "combine"]:
                    if ft[0].split()[1] == "state":
                        # the same filter as for sensitivity numbers
                        elm_states_filtered = beso_filters.run_morphology(elm_states, near_elm, opt_domains, ft[0].split()[0])
                        # compute mass difference
                        for dn in domains_from_config:
                            if domain_optimized[dn] is True:
                                for en in domain_shells[dn]:
                                    if elm_states[en] != elm_states_filtered[en]:
                                        mass[i] += area_elm[en] * (
                                            domain_density[dn][elm_states_filtered[en]] * domain_thickness[dn][
                                                                                                    elm_states_filtered[en]]
                                            - domain_density[dn][elm_states[en]] * domain_thickness[dn][elm_states[en]])
                                        elm_states[en] = elm_states_filtered[en]
                                for en in domain_volumes[dn]:
                                    if elm_states[en] != elm_states_filtered[en]:
                                        mass[i] += volume_elm[en] * (
                                            domain_density[dn][elm_states_filtered[en]] - domain_density[dn][elm_states[en]])
                                        elm_states[en] = elm_states_filtered[en]
        print("mass = {}" .format(mass[i]))        
        print("Swith_Element_State")
    def Check_oscillation(self):
        global i
        print("Check_oscillation")
    def Filter_State(self):
        global i
        print("Filter_State")
        
    def Show(self):
        vis_tools.disp_2D_evolution_with_strain_energy(cur_figs, cg, FI_step, constraint_node_list, load_node_list, elm_states, str(i) + "th Iteration", iterations_limit, i, mass)
        FF = plt.gcf()
        DPI = FF.get_dpi()
        #DefaultSize = FF.get_size_inches()
        plt.savefig(path_image + '/' +str(i) + "th Iteration")        
        
    def debug(self):
        print(domains[elset_name])
        
if __name__ == '__main__':
    # read config
    exec(open(conf_path).read() )
    if os.path.isdir(path_export) == False:
        os.mkdir(path_export)
    if os.path.isdir(path_image) == False:
        os.mkdir(path_image)
    
    # Create BESO object
    beso = suBeso()
    beso.read_config()
    beso.setup_convergen_conditions()
    beso.setup_FEA_environment()
    
    beso.load_model()
    beso.compute_element_center()
    beso.prepare_filter()
    beso.separating_nodes_by_element()
    beso.init_visulization()
    beso.write_log()
    #beso.FEA()
    beso.run_optimization()
    #beso.debug()
