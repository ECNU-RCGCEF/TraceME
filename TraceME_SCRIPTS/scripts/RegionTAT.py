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
from multiprocessing import Pool
import math
from mpl_toolkits.basemap import Basemap,cm

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

def map_func(i_latlon):
   cons = ({'type': 'ineq', 'fun': lambda x: x[0] },
           {'type': 'ineq', 'fun': lambda x: 10  - x[0]},
           {'type': 'ineq', 'fun': lambda x: x[1]},
           {'type': 'ineq', 'fun': lambda x: np.max(dat_resTime)-x[1]})
   #transfer the item to i_lat and i_lon
   v_divmod    = divmod(i_latlon,(lonmax-lonmin))
   i_lat       = v_divmod[0]
   i_lon       = v_divmod[1]
   v_tas_max   = np.max(dat_tas_region[:,i_lat,i_lon])
   v_pr_max    = np.max(dat_pr_region[:,i_lat,i_lon])
   #print('i_lat',i_lat)
   #print('i_lon',i_lon)
   #print("dat_resTime_mean",dat_resTime_mean[i_lat,i_lon])
  # if(dat_resTime_mean[i_lat,i_lon] > 0):
   x0                    = np.array((1.0, np.min(dat_resTime[:,i_lat,i_lon])))
   res                   = minimize(lambda x:costFunc(x,dat_tas_region[1:,i_lat,i_lon],v_tas_max,dat_pr_region[1:,i_lat,i_lon],v_pr_max,num,dat_resTime[:,i_lat,i_lon]), x0,  constraints=cons)
   v_q10          = res.x[0]
   v_basedResTime = res.x[1]
   if(res.success == "True"):
      v_results      = 1
   else:
      v_results      = 0
   #else:
   #      v_q10          = 0
   #      v_basedResTime = 0
   #      v_results      = 0
   return v_tas_max,v_pr_max,v_q10,v_basedResTime,v_results

def randomcolor():
   colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
   color = ""
   for i in range(6):
      color += colorArr[random.randint(0,14)]
   return "#"+color

def fuc_draw(str_modelName,drawData,outputFig):
   fig       = plt.figure()
   num_model = drawData.shape[0] # the number of models
   m         = Basemap(projection='cyl',resolution='l',area_thresh=10000,llcrnrlon=lonmin,urcrnrlon=lonmax,llcrnrlat=latmin,urcrnrlat=latmax)
   r_lat     = np.arange(latmin,latmax)
   r_lon     = np.arange(lonmin,lonmax)
   x,y       = m(r_lon,r_lat)
   x,y       = np.meshgrid(x,y)
   for i_model in range(num_model):
       ax    = fig.add_subplot(n_row,n_col,i_model+1)
       ax.set_title(ls_modelName[i_model],size=8)
       if(str_modelName == "Residence Time (year)"):
          m.contourf(x,y,drawData[i_model,:].squeeze(),500,cmap='bwr',vmin=0,vmax=1000)
       else:
          m.contourf(x,y,drawData[i_model,:].squeeze(),500,cmap='bwr')
       m.drawcoastlines(linewidth=0.2)
       m.drawlsmask(land_color = (0,0,0,0),ocean_color="skyblue",lakes=True)
       m.drawparallels(np.arange(latmin,latmax,(latmax-latmin)/5),labels=[1,0,0,0],fontsize=8)
       m.drawmeridians(np.arange(lonmin,lonmax,(lonmax-lonmin)/5),labels=[0,0,0,1],fontsize=8)
       m.colorbar()
   #draw variation of all models
   if(num_model>1):
      ax    = fig.add_subplot(n_row,n_col,num_model+1)
      ax.set_title("variation",size=8)
      m.contourf(x,y,np.var(drawData,axis=0).squeeze(),500,cmap='bwr')
      m.drawcoastlines(linewidth=0.2)
      m.drawlsmask(land_color = (0,0,0,0),ocean_color="skyblue",lakes=True)
      m.drawparallels(np.arange(latmin,latmax,(latmax-latmin)/5),labels=[1,0,0,0],fontsize=8)
      m.drawmeridians(np.arange(lonmin,lonmax,(lonmax-lonmin)/5),labels=[0,0,0,1],fontsize=8)
      m.colorbar()
   plt.title(str_modelName)
   plt.savefig(outputFig)

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
   dat_plot_x            = np.zeros((len(ls_modelName),latmax-latmin,lonmax-lonmin)) # get the start year to end year
   dat_plot_capacity     = np.zeros((len(ls_modelName),latmax-latmin,lonmax-lonmin))
   dat_plot_potential    = np.zeros((len(ls_modelName),latmax-latmin,lonmax-lonmin))
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
   dat_plot_x            = np.zeros((len(ls_modelName),latmax-latmin,lonmax-lonmin)) # get the start year to end year
   dat_plot_capacity     = np.zeros((len(ls_modelName),latmax-latmin,lonmax-lonmin))
   dat_plot_potential    = np.zeros((len(ls_modelName),latmax-latmin,lonmax-lonmin))
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
   dat_plot_x            = np.zeros((len(ls_modelName),latmax-latmin,lonmax-lonmin)) # get the start year to end year
   dat_plot_capacity     = np.zeros((len(ls_modelName),latmax-latmin,lonmax-lonmin))
   dat_plot_potential    = np.zeros((len(ls_modelName),latmax-latmin,lonmax-lonmin))
   dat_plot_npp          = np.zeros((len(ls_modelName),latmax-latmin,lonmax-lonmin))
   dat_plot_resTime      = np.zeros((len(ls_modelName),latmax-latmin,lonmax-lonmin))
   dat_plot_cue          = np.zeros((len(ls_modelName),latmax-latmin,lonmax-lonmin))
   dat_plot_gpp          = np.zeros((len(ls_modelName),latmax-latmin,lonmax-lonmin))
   dat_plot_evns         = np.zeros((len(ls_modelName),latmax-latmin,lonmax-lonmin))
   dat_plot_basedResTime = np.zeros((len(ls_modelName),latmax-latmin,lonmax-lonmin))
   dat_plot_tem          = np.zeros((len(ls_modelName),latmax-latmin,lonmax-lonmin))
   dat_plot_pre          = np.zeros((len(ls_modelName),latmax-latmin,lonmax-lonmin))
   # define the attributer for figues
   n_subplot    = len(ls_modelName)+1
   sqrt_subplot = int(n_subplot ** 0.5)+1
   if(len(ls_modelName)==1):
      n_col     = 1
      n_row     = 1
   else:
      n_col        = sqrt_subplot
      n_row        = math.ceil(n_subplot/sqrt_subplot)
   n_model=0
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
       dat_npp_global    = dat_npp  
       dat_x_global      = dat_x
       dat_npp_region    = dat_npp_global[:,latmin+90:latmax+90,lonmin:lonmax]
       dat_x_region      = dat_x_global[:,latmin+90:latmax+90,lonmin:lonmax]
       #dat_npp_total     = np.sum(dat_npp_region,axis=0) #regional sum npp
       #dat_npp_mean      = np.mean(dat_npp_region,axis=0)
       # dat_x_total       = np.sum(dat_x_total_lat,axis=0)   #regional sum x
       # calculate the change rate of carbon storage
       dat_rate_x        = np.zeros((end_year-start_year,latmax-latmin,lonmax-lonmin))
       for n_x in range(end_year-start_year):
           dat_rate_x[n_x,:,:]    = dat_x_region[n_x+1,:,:]-dat_x_region[n_x,:,:]
       #dat_rate_x        = np.array(dat_rate_x)
       dat_resTime       = dat_x_region[1:,:,:]/(dat_npp_region[1:,:,:]-dat_rate_x)
       dat_resTime       = np.around(dat_resTime,decimals=2)
       dat_resTime_mean  = np.mean(dat_resTime,axis=0)
       print("dat_resTime_mean:",dat_resTime_mean.shape)
       dat_x_p           = dat_resTime*dat_npp_region[1:,:,:]-dat_x_region[1:,:,:]
       dat_x_c           = dat_resTime*dat_npp_region[1:,:,:]
       print("fig1:carbon(dat_x_c):",dat_x_c.shape)
       #print("fig2:npp-rest:",)
       print("dat_resTime:",dat_resTime.shape)
       #end of calculating residence time===start calculating GPP-CUE
       dat_gpp_global    = dat_gpp
       dat_gpp_region    = dat_gpp_global[:,latmin+90:latmax+90,lonmin:lonmax]
       #dat_gpp_total     = np.sum(dat_gpp_region,axis=0)
       dat_cue           = dat_npp_region/dat_gpp_region   ##===calculate CUE
       #====environmental scalars and baseline NPP==========
       dat_pr_region     = dat_pr[:,latmin+90:latmax+90,lonmin:lonmax]
       dat_tas_region    = dat_tas[:,latmin+90:latmax+90,lonmin:lonmax]
       #dat_area_region   = dat_area[latmin+90:latmax+90,lonmin:lonmax]
       #dat_pr_total_lat  = np.sum(dat_pr_region,axis=1)
       #dat_pr_total      = np.sum(dat_pr_total_lat,axis=1)
       dat_tas_avg       = np.mean(dat_tas_region,axis=0)
       dat_pr_avg        = np.mean(dat_pr_region,axis=0)
       num               = dat_resTime.shape[0]
       print("num",num)
       n_latlon         = np.arange((latmax-latmin)*(lonmax-lonmin))
       p                = Pool(12)
       #for i in n_latlon
       res              = list(p.map(map_func,n_latlon))
       p.close()
       p.join() 
       res              = np.array(res)
       print('res',res.shape)
       dat_tas_max      = res[:,0].reshape(latmax-latmin,lonmax-lonmin)
       dat_pr_max       = res[:,1].reshape(latmax-latmin,lonmax-lonmin)
       res_q10          = res[:,2].reshape(latmax-latmin,lonmax-lonmin)
       res_basedResTime = res[:,3].reshape(latmax-latmin,lonmax-lonmin)
       dat_results      = res[:,4].reshape(latmax-latmin,lonmax-lonmin)
       scalar_tem       = np.power(res_q10,((dat_tas_avg-dat_tas_max)/10))
       scalar_pre       = dat_pr_avg/dat_pr_max
       total_scalars    = np.array(scalar_tem)*np.array(scalar_pre)
       dat_plot_npp[n_model,:]          = np.mean(dat_npp_region,axis=0)
       dat_plot_resTime[n_model,:]      = np.mean(dat_resTime,axis=0)
       #print("dat_cue:",dat_cue.shape)
       #print("dat_gpp:",dat_gpp_total.shape)
       dat_plot_cue[n_model,:]          = np.mean(dat_cue,axis=0)
       dat_plot_gpp[n_model,:]          = np.mean(dat_gpp_region,axis=0)
       dat_plot_evns[n_model,:]         = total_scalars
       dat_plot_basedResTime[n_model,:] = res_basedResTime
       dat_plot_tem[n_model,:]          = dat_tas_avg
       dat_plot_pre[n_model,:]          = dat_pr_avg
       n_model                          = n_model +1
   
    #====start figures
   fuc_draw("carbon storage (kg/m-2)",dat_plot_x,list_str[list_str.index("out-fig-0")+1])
   fuc_draw("Carbon capacity (kg/m-2)",dat_plot_capacity,list_str[list_str.index("out-fig-1")+1])
   fuc_draw("Carbon potential (kg/m-2)",dat_plot_potential,list_str[list_str.index("out-fig-2")+1])
   fuc_draw("NPP (kg/m-2)",dat_plot_npp,list_str[list_str.index("out-fig-3")+1])
   fuc_draw("Residence Time (year)",dat_plot_resTime,list_str[list_str.index("out-fig-4")+1])     
   fuc_draw("GPP (kg/m-2)",dat_plot_gpp,list_str[list_str.index("out-fig-5")+1])
   fuc_draw("CUE",dat_plot_cue,list_str[list_str.index("out-fig-6")+1])
   fuc_draw("baseline Residence Time (year)",dat_plot_basedResTime,list_str[list_str.index("out-fig-7")+1])
   fuc_draw("Environmental scalars",dat_plot_evns,list_str[list_str.index("out-fig-8")+1])
   fuc_draw("Temperature (degree)",dat_plot_tem,list_str[list_str.index("out-fig-9")+1])
   fuc_draw("Precipitation (mm)",dat_plot_pre,list_str[list_str.index("out-fig-10")+1])

#save nc
#===create files and save
   n_model = 0
   for modelName in ls_modelName:
       da=nc.Dataset(list_str[list_str.index("out-nc-"+modelName)+1],"w",format="NETCDF4")
       da.createDimension("latsize",latmax-latmin)
       da.createDimension("lonsize",lonmax-lonmin)
       da.createVariable("carbon storage","f8",("latsize","lonsize"))
       da.createVariable("carbon capacity","f8",("latsize","lonsize"))
       da.createVariable("carbon potential","f8",("latsize","lonsize"))
       da.createVariable("cue","f8",("latsize","lonsize"))
       da.createVariable("gpp","f8",("latsize","lonsize"))
       da.createVariable("environmental scalars","f8",("latsize","lonsize"))
       da.createVariable("baseline residence time","f8",("latsize","lonsize"))
       da.createVariable("tas","f8",("latsize","lonsize"))
       da.createVariable("pr","f8",("latsize","lonsize"))
       da.createVariable("npp","f8",("latsize","lonsize"))
       da.createVariable("residence Time","f8",("latsize","lonsize"))
    ##
       da.createVariable("lat","f8",("latsize"))
       da.createVariable("lon","f8",("lonsize"))
       da.variables["lat"][:]=range(latmin,latmax)
       da.variables["lon"][:]=range(lonmin,lonmax)
       da.variables["carbon storage"][:]=dat_plot_x[n_model,:,:]
       da.variables["carbon capacity"][:]=dat_plot_capacity[n_model,:,:]
       da.variables["carbon potential"][:]=dat_plot_potential[n_model,:,:]
       da.variables["cue"][:]=dat_plot_cue[n_model,:,:]
       da.variables["gpp"][:]=dat_plot_gpp[n_model,:,:]
       da.variables["environmental scalars"][:]=dat_plot_evns[n_model,:,:]
       da.variables["baseline residence time"][:]=dat_plot_basedResTime[n_model,:,:]
       da.variables["tas"][:]=dat_plot_tem[n_model,:,:]
       da.variables["pr"][:]=dat_plot_pre[n_model,:,:]
       da.variables["npp"][:]=dat_plot_npp[n_model,:,:]
       da.variables["residence Time"][:]=dat_plot_resTime[n_model,:,:]
       da.description="test nc"
       da.author="zhoujian"
       da.createdate="2019-08-07"
       da.close()
       n_model += 1
