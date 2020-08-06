package cn.edu.tsinghua.cess.task.service.impl.executor;

import cn.edu.tsinghua.cess.datamanager.nclscript.NclScript;
import cn.edu.tsinghua.cess.datamanager.nclscript.NclScriptContext;
import cn.edu.tsinghua.cess.modelfile.service.ModelFileQueryService;
import cn.edu.tsinghua.cess.task.dao.TaskExecutionDao;
import cn.edu.tsinghua.cess.task.entity.SubTask;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.concurrent.Callable;

//test by zhoujian:
import org.apache.log4j.Logger;
//test by zhoujian:
import cn.edu.tsinghua.cess.task.entity.dto.TaskSubmition;
import java.util.*;
import cn.edu.tsinghua.cess.modelfile.entity.Model;
import cn.edu.tsinghua.cess.modelfile.dao.ModelFileDao;


@Component
public class TaskExecutorFactory {

    @Autowired TaskExecutionDao taskExecutionDao;
    @Autowired NclScriptFactory nclScriptFactory;
    @Autowired ModelFileQueryService modelFileQueryService;
    @Autowired ModelFileDao modelFileDao;
//test by zhoujian:
    private Logger log = Logger.getLogger(getClass());
    
    public TaskExecutor getTaskExecutor(final SubTask subTask) {
    	Callable<NclScriptContext> contextBuilder = new Callable<NclScriptContext>() {
			@Override
			public NclScriptContext call() throws Exception {
		        return NclScriptContextImpl.newInstance(subTask, taskExecutionDao, modelFileQueryService);
			}
		};
		Callable<NclScript> scriptBuilder = new Callable<NclScript>() {
			@Override
			public NclScript call() throws Exception {
		        return nclScriptFactory.getNclScript(subTask.getScriptEntity().getName());
			}
		};

        return TaskExecutor.newInstance(subTask, taskExecutionDao, contextBuilder, scriptBuilder);
	}

    //test by zhoujian:for handling the data together
        public TaskSubmitionExecutor getTaskExecutor_submition(final TaskSubmition submition, final List<SubTask> subTask) { //get the context of subtask
    	Callable<List<NclScriptContext>> contextBuilder_List = new Callable<List<NclScriptContext>>() { //NclScriptContext to list???
			@Override
			public List<NclScriptContext> call() throws Exception {
                log.info("zhoujian:into the NclScriptContext");
                // divide the submition to subtask for the context_list
                List<NclScriptContext> contextList = new ArrayList<NclScriptContext>();
                List<Model> modelList = modelFileDao.queryModelOfLocal(submition.getModels());
                for (SubTask subTask_n : subTask) {
        	         try {
                         subTask_n.setId(subTask.get(0).getId());
	                      //SubTask task = SubTask.newInstance(model, submition.getNclScript());
	                      contextList.add(NclScriptContextImpl.newInstance(subTask_n, taskExecutionDao, modelFileQueryService));

	                      log.info("subtask created, [subTaskId=" + subTask_n.getId() + "]");
        	             } catch (Exception e) {
        		           String message = "error occurred while submiting task, msg=" + e.getMessage();
        		           log.error(message, e);
			               }
                }//end for
		        return contextList;
			}
		};
		Callable<NclScript> scriptBuilder = new Callable<NclScript>() {//get the ncl name for runing
			@Override
			public NclScript call() throws Exception {
                log.info("zhoujian:into the scriptBuilder");
		        return nclScriptFactory.getNclScript(submition.getNclScript().getName());
			}
		};

        return TaskSubmitionExecutor.newInstance(subTask, taskExecutionDao, contextBuilder_List, scriptBuilder);
	}
    
}
