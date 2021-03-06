import sys
from sys import argv
import numpy as np
import netCDF4 as nc
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import random
import mpl_toolkits.mplot3d
from mpl_toolkits.mplot3d import axes3d

#==== get the baseline NPP =======
def costFunc(x,v_tem,max_tem,v_pre,max_pre,num,v_resTime):
   Q10        = x[0]
   v_basedNPP = x[1]
   s_tem      = np.power(Q10,((v_tem-max_tem)/10))
   s_pre      = v_pre/max_pre
   total_s    = np.array(s_tem)*np.array(s_pre)
   r2         = 1-(sum(np.power((v_resTime - v_basedNPP/total_s),2))/(sum(np.power(v_resTime-v_basedNPP,2)))) # 约束函数
   v_rmse     = np.linalg.norm(sum(np.power(v_resTime-v_basedNPP/total_s,2))/num)
   fun        = abs(v_rmse/r2)
   return fun

def randomcolor():
   colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
   color = ""
   for i in range(6):
      color += colorArr[random.randint(0,14)]
   return "#"+color

if __name__ == '__main__':
   list_str = [] # get data from java script: inputdata,outputdata
   for i in range(1,len(sys.argv)):
       list_str.append(sys.argv[i].replace(",", "").replace('[','').replace(']',''))
   ## l_varname,xxx,l_modelname,xxx,inputfiles,varname_tmp+"-"+modelName_tmp,xxx,out-nc-modelname
   ## out-fig-"+j:1.CarbonDynamic;2.NPP_ResTime;3.GPP_CUE;4.Envs_baseResTime;5.Tem_Pre
   ##=============start=======================
   # pre-work:read model names
   ls_modelName=list_str[list_str.index("l_modelname")+1:list_str.index("inputfiles")]
   ls_varname  = ["npp","cVeg","cSoil","cCwd","cLitter","gpp","nep","pr","tas"]
   latmin       = int(list_str[list_str.index("latmin")+1])
   latmax       = int(list_str[list_str.index("latmax")+1])
   lonmin       = int(list_str[list_str.index("lonmin")+1])
   lonmax       = int(list_str[list_str.index("lonmax")+1])
   start_year   = int(list_str[list_str.index("start_year")+1])
   end_year     = int(list_str[list_str.index("end_year")+1])
   fi_area      = list_str[list_str.index("area_nc")+1]
   nc_obj_area  = Dataset(fi_area)
   dat_area     = (nc_obj_area.variables['area'][:])
   # define the arraylist for
   dat_plot_x            = np.zeros((len(ls_modelName),end_year-start_year)) # get the start year to end year
   dat_plot_capacity     = np.zeros((len(ls_modelName),end_year-start_year))
   dat_plot_npp          = np.zeros((len(ls_modelName),end_year-start_year))
   dat_plot_resTime      = np.zeros((len(ls_modelName),end_year-start_year))
   dat_plot_cue          = np.zeros((len(ls_modelName),end_year-start_year))
   dat_plot_gpp          = np.zeros((len(ls_modelName),end_year-start_year))
   dat_plot_evns         = np.zeros((len(ls_modelName),end_year-start_year))
   dat_plot_basedResTime = np.zeros((len(ls_modelName),end_year-start_year))
   dat_plot_tem          = np.zeros((len(ls_modelName),end_year-start_year))
   dat_plot_pre          = np.zeros((len(ls_modelName),end_year-start_year))
   n_model               = 0
   for modelName in ls_modelName:
       #1.inputdata "npp","cVeg","cSoil","cCwd","cLitter"
       nc_obj_npp   = Dataset(list_str[list_str.index("npp-"+modelName)+1])
       nc_obj_cVeg  = Dataset(list_str[list_str.index("cVeg-"+modelName)+1])
       nc_obj_cSoil = Dataset(list_str[list_str.index("cSoil-"+modelName)+1])
       nc_obj_gpp   = Dataset(list_str[list_str.index("gpp-"+modelName)+1])
       nc_obj_nep   = Dataset(list_str[list_str.index("nep-"+modelName)+1])
       nc_obj_pr    = Dataset(list_str[list_str.index("pr-"+modelName)+1])
       nc_obj_tas   = Dataset(list_str[list_str.index("tas-"+modelName)+1])
       dat_npp      = (nc_obj_npp.variables['npp'][:])  #(10, 180, 360)
       dat_cVeg     = (nc_obj_cVeg.variables['cVeg'][:])
       dat_cSoil    = (nc_obj_cSoil.variables['cSoil'][:])
       dat_gpp      = (nc_obj_gpp.variables['gpp'][:])  #(10, 180, 360)
       dat_nep      = (nc_obj_nep.variables['nep'][:])
       dat_pr       = (nc_obj_pr.variables['pr'][:])
       dat_tas      = (nc_obj_tas.variables['tas'][:])
       #==========================================
       dat_x    = dat_cVeg+dat_cSoil
       if list_str[list_str.index("cCwd-"+modelName)+1] != "null":
          nc_obj_cCwd=Dataset(list_str[list_str.index("cCwd-"+modelName)+1])
          dat_x      = dat_x+(nc_obj_cCwd.variables['cCwd'][:])
       if list_str[list_str.index("cLitter-"+modelName)+1] != "null":
          nc_obj_cLitter=Dataset(list_str[list_str.index("cLitter-"+modelName)+1])
          dat_x      = dat_x+(nc_obj_cLitter.variables['cLitter'][:])
       # get the time of nc
       time = (nc_obj_npp.variables['time'][:])
       print("dat_npp.shape:",dat_npp.shape)
       print("dat_x.shape:",dat_x.shape)
       dat_npp_global    = dat_npp*(dat_area*(1e6))/(1e12)   #dat_area km2 to m2; kg to Pg C
       dat_x_global      = dat_x*(dat_area*(1e6))/(1e12)
       dat_npp_region    = dat_npp_global[:,latmin+90:latmax+90,lonmin:lonmax]
       dat_x_region      = dat_x_global[:,latmin+90:latmax+90,lonmin:lonmax]
       #dat_npp_region    = dat_npp_global
       #dat_x_region      = dat_x_global
       dat_npp_total_lat = np.sum(dat_npp_region,axis=1)
       dat_npp_total     = np.sum(dat_npp_total_lat,axis=1) #regional sum npp
       dat_x_total_lat   = np.sum(dat_x_region,axis=1)
       dat_x_total       = np.sum(dat_x_total_lat,axis=1)   #regional sum x
       dat_rate_x        = []
       for n_x in range(len(dat_x_total[:-1])):
           dat_rate_x.append(dat_x_total[n_x+1]-dat_x_total[n_x])
       dat_rate_x        = np.array(dat_rate_x)
       dat_resTime       = dat_x_total[1:]/(dat_npp_total[1:]-dat_rate_x)
       dat_resTime       = np.around(dat_resTime,decimals=2)
       dat_x_p           = dat_resTime*dat_npp_total[1:]-dat_x_total[1:]
       dat_x_c           = dat_resTime*dat_npp_total[1:]
       print("fig1:carbon(dat_x_c):",dat_x_c)
       #print("fig2:npp-rest:",)
       print("dat_resTime:",dat_resTime)
       #end of calculating residence time===start calculating GPP-CUE
       dat_gpp_global    = dat_gpp*(dat_area*(1e6))/(1e12)
       dat_gpp_region    = dat_gpp_global[:,latmin+90:latmax+90,lonmin:lonmax]
       dat_gpp_total_lat = np.sum(dat_gpp_region,axis=1)
       dat_gpp_total     = np.sum(dat_gpp_total_lat,axis=1)
       dat_cue           = dat_npp_total/dat_gpp_total   ##===calculate CUE
       #====environmental scalars and baseline NPP==========
       cons = ({'type': 'ineq', 'fun': lambda x: x[0] },
               {'type': 'ineq', 'fun': lambda x: 10  - x[0]},
               {'type': 'ineq', 'fun': lambda x: x[1]},
               {'type': 'ineq', 'fun': lambda x: np.max(dat_resTime)-x[1]})
       dat_pr_region     = dat_pr[:,latmin+90:latmax+90,lonmin:lonmax]
       dat_tas_region    = dat_tas[:,latmin+90:latmax+90,lonmin:lonmax]
       dat_area_region   = dat_area[latmin+90:latmax+90,lonmin:lonmax]
       #dat_pr_total_lat  = np.sum(dat_pr_region,axis=1)
       #dat_pr_total      = np.sum(dat_pr_total_lat,axis=1)
       dat_tas_avg       = np.zeros(dat_tas.shape[0])
       dat_pr_avg        = np.zeros(dat_pr.shape[0])
       print("range(dat_tas.shape[0]-1):",range(dat_tas.shape[0]-1))
       print("dat_tas.shape:",dat_tas.shape)
       for n_pr in range(dat_tas.shape[0]):
           dat_tas_avg[n_pr] = np.average(dat_tas_region[n_pr,:,:],weights=(dat_area_region*(1e6)))
           dat_pr_avg[n_pr]  = np.average(dat_pr_region[n_pr,:,:],weights=(dat_area_region*(1e6)))
       print("dat_tas_avg:",dat_tas_avg.shape)
       num               = len(dat_resTime)
       dat_tas_max       = np.max(dat_tas_avg)
       dat_pr_max        = np.max(dat_pr_avg)
       x0                = np.array((1.0, np.min(dat_resTime))) # 设置初始值
       res               = minimize(lambda x:costFunc(x,dat_tas_avg[1:],dat_tas_max,dat_pr_avg[1:],dat_pr_max,num,dat_resTime), x0,  constraints=cons)
       print('最小值：',res.fun)
       print('最优解：',res.x)
       print('迭代终止是否成功：', res.success)
       print('迭代终止原因：', res.message)
       print('r2:',1-sum(np.power((dat_resTime - res.x[1]/(np.array(np.power(res.x[0],((dat_tas_avg[1:]-dat_tas_max)/10)))*np.array(dat_pr_avg[1:]/dat_pr_max))),2))/(sum(np.power(dat_resTime-res.x[1],2))))
       print('rmse:')
       dat_Q10                          = res.x[0]
       dat_basedResTime                 = res.x[1]
       scalars_tem                      = np.power(dat_Q10,((dat_tas_avg[1:]-dat_tas_max)/10))
       scalars_pre                      = dat_pr_avg[1:]/dat_pr_max
       total_scalars                    = np.array(scalars_tem)*np.array(scalars_pre)
       dat_plot_x[n_model,:]            = dat_x_total[1:]
       dat_plot_capacity[n_model,:]     = dat_x_c
       dat_plot_npp[n_model,:]          = dat_npp_total[1:]
       dat_plot_resTime[n_model,:]      = dat_resTime
       print("dat_cue:",dat_cue.shape)
       print("dat_gpp:",dat_gpp_total.shape)
       dat_plot_cue[n_model,:]          = dat_cue[1:]
       dat_plot_gpp[n_model,:]          = dat_gpp_total[1:]
       dat_plot_evns[n_model,:]         = total_scalars
       dat_plot_basedResTime[n_model,:] = dat_plot_basedResTime[n_model,:]+dat_basedResTime
       dat_plot_tem[n_model,:]          = dat_tas_avg[1:]
       dat_plot_pre[n_model,:]          = dat_pr_avg[1:]
       n_model=n_model+1
# end for handling data and start to plot and nc ncfiles
#figues
#fig1.carbon dynamic
models_color=[]
for n_model in range(len(ls_modelName)):
    color                 = randomcolor()
    print("color:",color)
    models_color.append(randomcolor())
x=range(start_year,end_year)
fig, ax = plt.subplots()
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width* 0.8 , box.height])
n_model=0
for modelName in ls_modelName:
    plt.plot(x, dat_plot_x[n_model,:], models_color[n_model], linewidth=2, label=modelName)
    #plt.plot(x, dat_plot_capacity[n_model,:], randomcolor(), linewidth=0)
    #plt.ylim(ymin=0)
    plt.fill_between(x,dat_plot_capacity[n_model,:],dat_plot_x[n_model,:],facecolor=models_color[n_model],alpha=0.3)
    n_model=n_model+1
plt.xlabel('Year')
plt.ylabel('Carbon storage and capacity (Pg C)')
plt.legend(loc='center left', bbox_to_anchor=(1.02,0.5),ncol=1, borderaxespad = 0.)
plt.savefig(list_str[list_str.index("out-fig-0")+1])
#fig2.residence time <---> NPP
fig, ax = plt.subplots()
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width* 0.8 , box.height])
n_model=0
for modelName in ls_modelName:
    plt.scatter(dat_plot_npp[n_model,:], dat_plot_resTime[n_model,:], c=models_color[n_model],marker='o',label=modelName)
    n_model=n_model+1
plt.xlabel('NPP (Pg C/year)')
plt.ylabel('Residence time(year)')
plt.legend(loc='center left', bbox_to_anchor=(1.02,0.5),ncol=1, borderaxespad = 0.)
plt.savefig(list_str[list_str.index("out-fig-1")+1])
    #fig3.GPP <---> CUE
fig, ax = plt.subplots()
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width* 0.8 , box.height])
n_model=0
for modelName in ls_modelName:
    plt.scatter(dat_plot_gpp[n_model,:], dat_plot_cue[n_model,:], c=models_color[n_model],marker='o',label=modelName)
    n_model=n_model+1
plt.xlabel('GPP (Pg C/year)')
plt.ylabel('Carbon use efficiency (CUE)')
plt.legend(loc='center left', bbox_to_anchor=(1.02,0.5),ncol=1, borderaxespad = 0.)
plt.savefig(list_str[list_str.index("out-fig-2")+1])
#fig4. Envs_baseResTime <----> residenceTime
ax = plt.subplot(111,projection='3d')
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width* 0.8 , box.height])
n_model=0
for modelName in ls_modelName:
    ax.scatter(dat_plot_basedResTime[n_model,:], dat_plot_evns[n_model,:],dat_plot_resTime[n_model,:],c=models_color[n_model],label=modelName)
    n_model=n_model+1
ax.set_xlabel('Baseline residence time (year)')
ax.set_ylabel('Environmental scalars')
ax.set_zlabel('Residence time (year)')
ax.legend(loc='center left', bbox_to_anchor=(1.02,0.5),ncol=1, borderaxespad = 0.)
plt.savefig(list_str[list_str.index("out-fig-3")+1])
    #fig5.temperature <---> precipitation
fig, ax = plt.subplots()
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width* 0.8 , box.height])
n_model=0
for modelName in ls_modelName:
    plt.scatter(dat_plot_tem[n_model,:], dat_plot_pre[n_model,:], c=models_color[n_model],marker='o',label=modelName)
    n_model=n_model+1
plt.xlabel('Air temperature (degree)')
plt.ylabel('Precipitation (mm/year)')
plt.legend(loc='center left', bbox_to_anchor=(1.02,0.5),ncol=1, borderaxespad = 0.)
plt.savefig(list_str[list_str.index("out-fig-4")+1])
#save nc
#===create files and save
n_model = 0
for modelName in ls_modelName:
    da=nc.Dataset(list_str[list_str.index("out-nc-"+modelName)+1],"w",format="NETCDF4")
    da.createDimension("latsize",end_year-start_year)
    #da.createDimension("lonsize",usize[1])
    da.createVariable("npp","f8",("latsize"))
    da.createVariable("residenceTime","f8",("latsize"))
    #da.createVariable("z","f8",("latsize","lonsize"))
    #da.createVariable("lon","f8",("latsize","lonsize"))
    da.createVariable("lat","f8",("latsize"))
    #da.createVariable("num","f8",("latsize","lonsize"))
    #da.variables["u"][:]=output_u
    #da.variables["v"][:]=output_v
    #da.variables["z"][:]=output_z
    da.variables["lat"][:]=range(end_year-start_year)
    print("dat_plot_npp:",dat_plot_npp.shape)
    da.variables["npp"][:]=dat_plot_npp[n_model,:]
    da.variables["residenceTime"][:]=dat_plot_resTime[n_model,:]
    da.description="test nc"
    da.author="zhoujian"
    da.createdate="2019-08-07"
    da.close()
    n_model += 1
