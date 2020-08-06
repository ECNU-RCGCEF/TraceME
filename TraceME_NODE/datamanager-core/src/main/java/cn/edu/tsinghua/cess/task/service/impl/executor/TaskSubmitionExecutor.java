package cn.edu.tsinghua.cess.task.service.impl.executor;

import java.util.concurrent.Callable;

import cn.edu.tsinghua.cess.task.entity.SubTask;
import cn.edu.tsinghua.cess.util.RequestIdBinder;
import org.apache.log4j.Logger;

import cn.edu.tsinghua.cess.datamanager.nclscript.NclScript;
import cn.edu.tsinghua.cess.datamanager.nclscript.NclScriptContext;
import cn.edu.tsinghua.cess.task.dao.TaskExecutionDao;
import cn.edu.tsinghua.cess.task.entity.SubTaskStatus;

//test by zhoujian:
import java.util.*;

public class TaskSubmitionExecutor implements Runnable {

	private static Logger log = Logger.getLogger(TaskSubmitionExecutor.class);
	
	private List<SubTask> subTask;
	private TaskExecutionDao taskExecutionDao;
	private Callable<List<NclScriptContext>> contextBuilder;
	private Callable<NclScript> scriptBuilder;

	private TaskSubmitionExecutor() {}

	@Override
	public void run() {
        try {
            RequestIdBinder.bind();

            long begin = System.currentTimeMillis();
            StringBuilder builder = new StringBuilder();
			builder.append("begin to execute task, ");
			for (SubTask task_builder : subTask){
             builder.append("[id=").append(task_builder.getId()).append("]")
                    .append("[model=").append(task_builder.getModel()).append("]")
                    .append("[script=").append(task_builder.getScript()).append("]");
			}
            log.info(builder.toString());

        	List<NclScriptContext> contextList = contextBuilder.call();
        	NclScript script = scriptBuilder.call();
            
			log.info("zhoujian:test the context run before");
			//NclScriptContext context = contextList.get(0);
            //script.run(context);
			script.run_submition(contextList);
			for (SubTask task_builder : subTask){
            taskExecutionDao.setStatus(task_builder.getId(), SubTaskStatus.finished, null);
			}

            builder = new StringBuilder();
            builder.append("task execution succeeded, ");
				for (SubTask task_builder : subTask){
                    builder.append("[id=").append(task_builder.getId()).append("]")
                           .append("[elapsed=").append(System.currentTimeMillis() - begin).append("]");
				}
            log.info(builder.toString());
        } catch (Exception ex) {
			for (SubTask task_builder : subTask){
            taskExecutionDao.setFailed(task_builder.getId(), ex.getMessage());
			}
            StringBuilder builder = new StringBuilder();
            builder.append("task execution failed, ");
				for (SubTask task_builder : subTask){
                    builder.append("[id=").append(task_builder.getId()).append("]")
                           .append("[exception=").append(ex.getMessage()).append("]");
				}

            log.error(builder.toString(), ex);
        } finally {
            RequestIdBinder.unbind();
        }
    }
	
	public static TaskSubmitionExecutor newInstance(
			    List<SubTask> subTask,
			    TaskExecutionDao taskExecutionDao,
			    Callable<List<NclScriptContext>> contextBuilder,
			    Callable<NclScript> scriptBuilder) {
		TaskSubmitionExecutor executor = new TaskSubmitionExecutor();
		
        executor.subTask = subTask;
        executor.taskExecutionDao = taskExecutionDao;
        executor.contextBuilder = contextBuilder;
        executor.scriptBuilder = scriptBuilder;
		
        return executor;
	}
	
}