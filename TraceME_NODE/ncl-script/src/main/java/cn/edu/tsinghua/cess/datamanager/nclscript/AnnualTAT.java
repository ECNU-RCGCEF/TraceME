/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package cn.edu.tsinghua.cess.datamanager.nclscript;

import org.apache.log4j.Logger;
import java.io.File;
import java.io.IOException;
import java.util.*;

/**
 *
 * @author ericxuhao
 */
public class AnnualTAT implements NclScript{
    private Logger log = Logger.getLogger(getClass());
    @Override
    public void run_submition(List<NclScriptContext> contextList) {
        //get the ori,cdo data
        List<String> listModelName = new ArrayList(); 
	List<String> listVarName   = new ArrayList();
        for (NclScriptContext context_a : contextList) { //order the files according to model and variable name
            log.info("zhoujian: handle all context data :[ var:"+context_a.getVarName()+"];model:"+context_a.getModelName()+"]");
            if(!listModelName.contains(context_a.getModelName())){
                listModelName.add(context_a.getModelName());
            }
	    if(!listVarName.contains(context_a.getVarName())){
                listVarName.add(context_a.getVarName());
            }
        }
        
        for (String modelname0 : listModelName){ //zhoujian:just for test
            log.info("zhoujian: all model names:"+modelname0+"]");
        }
        
        String[] varname ={"npp","cVeg","cSoil","cCwd","cLitter","gpp","nep","pr","tas"};
        int n_varname=varname.length;
        NclScriptContext[][] contextArray = new NclScriptContext[n_varname][listModelName.size()]; 
		//for(int i_intial=0;i_intial<contextArray.length;++i_intial){
		//	for(int j_intial=0;j_intial<contextArray[i_intial].length;++j_intial){
		//		contextArray[i_intial][j_intial] = null;
		//	}
		//}
        
        
        for (NclScriptContext context_fileOriCdo : contextList) {
            try{
                log.info("zhoujian: handle all context data :[ var:"+context_fileOriCdo.getVarName()+"];model:"+context_fileOriCdo.getModelName()+"]");
                int varname_a=0;
                int modelname_b=0;				
                for (int var_i=0;var_i<n_varname; var_i++){
                    if (context_fileOriCdo.getVarName().equals(varname[var_i])){
                        varname_a=var_i;                   
                    }
                }
                for (int model_i=0;model_i<listModelName.size(); model_i++){
                    if (context_fileOriCdo.getModelName().equals(listModelName.get(model_i))){
                        modelname_b=model_i;                   
                    }
                }
				
                contextArray[varname_a][modelname_b]=context_fileOriCdo;

                }catch (Exception e) {
        		  String message = "error occurred while submiting task, msg=" + e.getMessage();
        		  log.error(message, e);
			      }
        }
// the varname and modelname array has been created:
        //get the ori and cdo nc data: spatial and temporal
//        List<File>file_ori_cdo = new ArrayList<File>(); //recording the place of files
        File[][] file_ori_cdo =new File[n_varname][listModelName.size()];//the same to contextArray
        for (int i =0; i<listModelName.size();i++){
            for (int j=0; j<n_varname; j++){
                // NclScriptContext context =new NclScriptContext;
                log.info("zhoujian: contextArray [i="+i+";j="+j+":"+contextArray[j][i]+"]");
		if(contextArray[j][i]==null){
		    log.info("zhoujian: inif contextArray [i="+i+";j="+j+":"+contextArray[j][i]+"]");
		    file_ori_cdo[j][i]=null;
		    continue;
		}else{
                    CmdExecutor cExecutor=new CmdExecutor(contextArray[j][i]);
                    File file_ori=cExecutor.getOriData(contextArray[j][i],30);
                    File file_cdo=cExecutor.getCdoData(contextArray[j][i], file_ori,45);
                    contextArray[j][i].addResult(NclScriptContext.RESULT_TYPE_NC, file_cdo.getAbsolutePath());
                    file_ori_cdo[j][i]=file_cdo;
		}
            }
        }
         //log.info("zhoujian: after file_cdo");
// calling cdo to add all cdo.* files to create carbon storage nc.
        //CmdExecutor cExecutor_c=new CmdExecutor(contextArray[j][i]);
       //File file_cdo_add = c        

        NclScriptContext context = contextArray[0][0];
        String lat_min=String.valueOf(context.getLatMin());
        String lat_max=String.valueOf(context.getLatMax());
        String lon_min=String.valueOf(context.getLonMin());
        String lon_max=String.valueOf(context.getLonMax());
        OutputFile[] outputFiles=new OutputFile[2];
        String[] Alia  = new String[5];
        Alia[0]        = "CarbonDynamic"+lat_min+"-"+lat_max+"_"+lon_min+"-"+lon_max;
        Alia[1]        = "NPP_ResidenceTime-"+lat_min+"-"+lat_max+"_"+lon_min+"-"+lon_max;
        Alia[2]        = "GPP_CUE-"+lat_min+"-"+lat_max+"_"+lon_min+"-"+lon_max;
        Alia[3]        = "Envs_baselineResidenceTime-"+lat_min+"-"+lat_max+"_"+lon_min+"-"+lon_max;
        Alia[4]        = "Temperature_Precipitation-"+lat_min+"-"+lat_max+"_"+lon_min+"-"+lon_max;
        outputFiles[0]=new OutputFile(NclScriptContext.RESULT_TYPE_FIG,Alia,new String[]{"fig_name"},5);
        outputFiles[1]=new OutputFile(NclScriptContext.RESULT_TYPE_NC,Alia,new String[]{"nc_name"},listModelName.size());
       
        
        log.info("zhoujian: output"+outputFiles.length+"]["+outputFiles);
       
        CmdExecutor cExecutor=new CmdExecutor(contextArray[0][0]);
       // cExecutor.runNcl_files(contextArray, file_ori_cdo, outputFiles, CmdExecutor.FIGURE_TYPE_ADDBOTH,"AnnualTAT.ncl", null);//get the results of npp, residence time, carbon potential and carbon storage.
        
        // transfer the 
        // call the python code to run the traceability method
        cExecutor.runPython_files(contextArray, file_ori_cdo, outputFiles, CmdExecutor.FIGURE_TYPE_ADDBOTH,"AnnualTAT.py", null);       

    }
    @Override
    public void run(NclScriptContext context) {
    }
    
}
