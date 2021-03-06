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
//add all variables to ocean

/**
 *
 * @author ericxuhao
 */
public class RegionATMOS implements NclScript{
    private Logger log = Logger.getLogger(getClass());
    @Override
    public void run_submition(List<NclScriptContext> contextList) {
        //get the ori,cdo data
        List<String> listModelName = new ArrayList();
		List<String> listVarName   = new ArrayList();
        for (NclScriptContext context_a : contextList) {
            log.info("zhoujian: handle all context data :[ var:"+context_a.getVarName()+"];model:"+context_a.getModelName()+"]");
            if(!listModelName.contains(context_a.getModelName())){
                listModelName.add(context_a.getModelName());
            }
			if(!listVarName.contains(context_a.getVarName())){
                listVarName.add(context_a.getVarName());
            }
        }
        
        for (String modelname0 : listModelName){
            log.info("zhoujian: all model names:"+modelname0+"]");
        }
/*                
        List<NclScriptContext> contextList_npp   = new ArrayList<NclScriptContext>();
        List<NclScriptContext> contextList_cVeg  = new ArrayList<NclScriptContext>();
        List<NclScriptContext> contextList_cSoil = new ArrayList<NclScriptContext>();
*/        
        NclScriptContext[][] contextArray = new NclScriptContext[listVarName.size()][listModelName.size()]; 
        String[] varname =listVarName.toArray(new String[listVarName.size()]);
        
        for (NclScriptContext context_fileOriCdo : contextList) {
            try{
                log.info("zhoujian: handle all context data :[ var:"+context_fileOriCdo.getVarName()+"];model:"+context_fileOriCdo.getModelName()+"]");
                int varname_a=0;
                int modelname_b=0;					
                for (int var_i=0;var_i<listVarName.size(); var_i++){
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
        File[][] file_ori_cdo =new File[listVarName.size()][listModelName.size()];//the same to contextArray
        for (int i =0; i<listModelName.size();i++){
            for (int j=0; j<listVarName.size(); j++){
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
        
        NclScriptContext context = contextArray[0][0];
        String lat_min=String.valueOf(context.getLatMin());
        String lat_max=String.valueOf(context.getLatMax());
        String lon_min=String.valueOf(context.getLonMin());
        String lon_max=String.valueOf(context.getLonMax());
        OutputFile[] outputFiles=new OutputFile[2];
        String Alia="Long_Term_Mean_"+lat_min+"-"+lat_max+"_"+lon_min+"-"+lon_max;
        outputFiles[0]=new OutputFile(NclScriptContext.RESULT_TYPE_FIG,new String[]{Alia},new String[]{"fig_name"},listVarName.size());
        outputFiles[1]=new OutputFile(NclScriptContext.RESULT_TYPE_NC,new String[]{Alia},new String[]{"nc_name"},(listVarName.size())*(listModelName.size()));
        
        log.info("zhoujian: output"+outputFiles.length+"]["+outputFiles);
       
        CmdExecutor cExecutor=new CmdExecutor(contextArray[0][0]);
        cExecutor.runNcl_files(contextArray, file_ori_cdo, outputFiles, CmdExecutor.FIGURE_TYPE_ADDBOTH,"RegionATMOS.ncl", null);

                
/*
        NclScriptContext context = contextArray[1][1];

        String lat_min=String.valueOf(context.getLatMin());
        String lat_max=String.valueOf(context.getLatMax());
        String lon_min=String.valueOf(context.getLonMin());
        String lon_max=String.valueOf(context.getLonMax());
       // log.info("zhoujian: after lon_max:["+lon_max+"]");
        //zhoujian: create more cmdExecutors
        CmdExecutor cExecutor=new CmdExecutor(context);//npp
        CmdExecutor cExecutor_cVeg=new CmdExecutor(context_cVeg);//cVeg
        CmdExecutor cExecutor_cSoil=new CmdExecutor(context_cSoil);//cSoil
        
        log.info("zhoujian: after cExecutor");
     //get the temporal and spatial files:
        //npp
        File file_ori=cExecutor.getOriData(context,30);
        File file_cdo=cExecutor.getCdoData(context, file_ori,45);
        File file_mean=cExecutor.getMeanData(context, file_cdo,60);
        //cVeg
        File file_ori_cVeg=cExecutor_cVeg.getOriData(context_cVeg,30);
        File file_cdo_cVeg=cExecutor_cVeg.getCdoData(context_cVeg, file_ori_cVeg,45);
        File file_mean_cVeg=cExecutor_cVeg.getMeanData(context_cVeg, file_cdo_cVeg,60);
        //cVeg
        File file_ori_cSoil=cExecutor_cSoil.getOriData(context_cSoil,30);
        File file_cdo_cSoil=cExecutor_cSoil.getCdoData(context_cSoil, file_ori_cSoil,45);
        File file_mean_cSoil=cExecutor_cSoil.getMeanData(context_cSoil, file_cdo_cSoil,60);
        
        log.info("zhoujian: after file_mean");
       
        context.addResult(NclScriptContext.RESULT_TYPE_NC, file_mean.getAbsolutePath());
        context_cVeg.addResult(NclScriptContext.RESULT_TYPE_NC, file_mean_cVeg.getAbsolutePath());
        context_cSoil.addResult(NclScriptContext.RESULT_TYPE_NC, file_mean_cSoil.getAbsolutePath());
        
        OutputFile[] outputFiles=new OutputFile[1];
        String Alia="Tracability_"+lat_min+"-"+lat_max+"_"+lon_min+"-"+lon_max;
        outputFiles[0]=new OutputFile(NclScriptContext.RESULT_TYPE_FIG,new String[]{Alia},new String[]{"fig_name"},1);
        
        System.out.println("test by zhoujian: before ncl");
        //create the list of context
        //List<NclScriptContext> context_input =new ArrayList<NclScriptContext>(); 
        //context_input(0)=context;
        //context_input(1)=context_cVeg;
        //context_input(2)=context_cSoil;
        List<File>file_mean_all = new ArrayList<File>(); 
        file_mean_all.add(file_mean);
        file_mean_all.add(file_mean_cVeg);
        file_mean_all.add(file_mean_cSoil);
        
        cExecutor.runNcl_files(contextList.get(0), file_mean_all, outputFiles, CmdExecutor.FIGURE_TYPE_ADDBOTH,"RegionTAT.ncl", null);
        //cExecutor.rmData(context,file_ori);
        //cExecutor.rmData(context,file_cdo);
*/
    }
    @Override
    public void run(NclScriptContext context) {
    }
    
}
